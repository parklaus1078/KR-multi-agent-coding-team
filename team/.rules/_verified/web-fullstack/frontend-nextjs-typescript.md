# Frontend Coding Rules (Next.js / React)

> 이 파일은 Coding Agent와 QA Agent가 web-fullstack 프로젝트의 프론트엔드를 작업할 때 반드시 준수해야 하는 코딩 룰입니다.

---

## 1. 프로젝트 구조

```
fe-project/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # 루트 레이아웃 (폰트, 전역 프로바이더)
│   │   ├── page.tsx
│   │   ├── loading.tsx             # 루트 Suspense 폴백
│   │   ├── not-found.tsx           # 404 페이지
│   │   ├── error.tsx               # 루트 에러 바운더리 (Client Component)
│   │   ├── global-error.tsx        # 크래시 수준 에러 바운더리
│   │   ├── providers.tsx           # 전역 Client Provider 모음 ('use client')
│   │   └── (routes)/               # 라우트 그룹 — 도메인별 폴더
│   │       └── {domain}/
│   │           ├── page.tsx
│   │           ├── loading.tsx
│   │           ├── error.tsx
│   │           └── _components/    # 라우트 로컬 컴포넌트 (공유 불가)
│   ├── components/
│   │   ├── ui/                     # 재사용 원자 컴포넌트 (Button, Input 등)
│   │   └── features/               # 도메인별 복합 컴포넌트
│   ├── hooks/                      # 커스텀 훅
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # 기본 fetch 래퍼
│   │   │   └── {domain}.ts         # 도메인별 API 함수
│   │   └── utils/                  # 순수 유틸 함수
│   ├── stores/                     # Zustand 스토어 (클라이언트 전역 상태 전용)
│   ├── types/
│   │   └── api/                    # API 응답 타입 (BE 스키마 미러링)
│   ├── constants/                  # 앱 전역 상수 및 Enum
│   ├── styles/                     # 전역 스타일
│   └── middleware.ts               # Edge 미들웨어 (인증, 리다이렉트 등)
├── public/
├── tests/
│   ├── components/
│   └── hooks/
├── next.config.ts
├── tsconfig.json
└── .env.example                    # 필요한 환경변수 키만 나열 (값 없음)
```

---

## 2. TanStack Query 설정

### 2-1. QueryClient Provider (필수 초기 설정)

`layout.tsx`는 Server Component이므로 `QueryClientProvider`를 직접 넣을 수 없다.
반드시 별도 `providers.tsx`를 만들어 분리한다.

```tsx
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function AppProviders({ children }: { children: React.ReactNode }) {
  // useState로 감싸야 컴포넌트당 한 번만 생성됨
  // new QueryClient()를 직접 쓰면 매 렌더마다 새 인스턴스가 생성됨
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 1000 * 60,       // 전역 기본 staleTime: 1분
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```tsx
// src/app/layout.tsx — Server Component 유지
import { AppProviders } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 2-2. 데이터 페칭 전략 선택 기준

퍼포먼스와 정확성에 가장 큰 영향을 미치는 판단이다. 데이터 특성에 따라 패턴을 선택한다.

| 데이터 유형 | 패턴 | 위치 |
|------------|------|------|
| 거의 변하지 않음, SEO 중요 | `fetch` + `cache: 'force-cache'` (SSG) | Server Component |
| 주기적으로 변함 (분~시간 단위) | `fetch` + `next: { revalidate: N }` (ISR) | Server Component |
| 매 요청마다 변함, 인증 의존 | `fetch` + `cache: 'no-store'` (SSR) | Server Component |
| 실시간, 사용자 트리거, 네비게이션 후 갱신 | TanStack Query | Client Component |

### 2-3. Server Component 데이터 페칭

```typescript
// app/(routes)/products/page.tsx
// ✅ 컴포넌트 레벨에서 직접 fetch — prop drilling 불필요
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// src/lib/api/products.ts
export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`, {
    next: { revalidate: 60 },           // ISR: 60초마다 재검증
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) throw new Error('Failed to fetch products');
  const data: ApiResponse<Product[]> = await res.json();
  return data.data ?? [];
}
```

### 2-4. Prefetch + HydrationBoundary (SSR + Client 캐시 연결)

Server Component에서 데이터를 미리 패칭하여 Client Component로 hydrate한다.
이 패턴을 쓰지 않으면 Client Component가 마운트 후 처음부터 fetch를 시작해 로딩 깜빡임이 발생한다.

```tsx
// app/(routes)/users/page.tsx — Server Component
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { UserList } from './_components/UserList';

export default async function UsersPage() {
  const queryClient = new QueryClient();

  // 서버에서 미리 패칭 — queryKey는 Client와 반드시 동일하게
  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });

  return (
    // dehydrate된 캐시를 클라이언트로 전달
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserList />   {/* 이미 캐시가 있으므로 로딩 없이 즉시 렌더링 */}
    </HydrationBoundary>
  );
}
```

```tsx
// app/(routes)/users/_components/UserList.tsx — Client Component
'use client';

export function UserList() {
  // prefetch된 데이터가 캐시에 있으므로 isLoading이 false로 시작
  const { data: users } = useQuery({
    queryKey: ['users'],              // 서버의 prefetchQuery와 동일한 key 필수
    queryFn: getUsers,
  });

  return (
    <ul>
      {users?.map((user) => <UserCard key={user.id} user={user} />)}
    </ul>
  );
}
```

> ⚠️ `prefetchQuery`의 `queryKey`와 Client의 `useQuery` `queryKey`가 다르면 hydration이 연결되지 않아 서버 패칭 결과가 버려진다.

### 2-5. useQuery — Client Component 데이터 페칭

```typescript
// src/hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api/users';

export function useUser(userId: number) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),   // src/lib/api/users.ts 함수
    staleTime: 1000 * 60 * 5,        // 5분 (전역 기본값 override)
  });
}
```

- `useEffect` 내 `fetch()` 또는 `apiClient` 직접 호출 금지 — 반드시 TanStack Query 사용
- 서버 상태(API 응답)를 Zustand에 저장 금지

### 2-6. useMutation — 서버 데이터 변경

데이터를 생성/수정/삭제하는 모든 작업은 `useMutation`을 사용한다.
`isPending`, `onSuccess`, `onError`를 `useState`로 직접 관리하는 것을 금지한다.

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api/users';

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserRequest) => userApi.create(data),
    onSuccess: () => {
      // 성공 시 관련 캐시 무효화 — 목록이 자동으로 최신화됨
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('유저가 생성되었습니다.');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// React Hook Form + useMutation 연결 패턴
'use client';

export function CreateUserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateUserRequest>({
    resolver: zodResolver(createUserSchema),
  });

  const { mutate: createUser, isPending } = useCreateUser();

  return (
    // handleSubmit이 validation 후 mutate를 호출
    <form onSubmit={handleSubmit((values) => createUser(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? '생성 중...' : '유저 생성'}
      </button>
    </form>
  );
}
```

- `mutationFn`은 반드시 `src/lib/api/{domain}.ts`의 함수를 사용
- `onSuccess`에서 `invalidateQueries`로 관련 캐시를 반드시 무효화
- `isPending` 상태를 별도 `useState`로 관리 금지 — `useMutation`의 `isPending` 사용

---

## 3. 컴포넌트 작성 규칙

### 3-1. 기본 형식

```tsx
// ✅ named export + Props 인터페이스 분리
// Client Hook(useUser)을 사용하므로 반드시 'use client' 선언 필요
'use client';

interface UserCardProps {
  userId: number;
  variant?: 'compact' | 'full';
}

export function UserCard({ userId, variant = 'full' }: UserCardProps) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <UserCardSkeleton />;
  if (!user) return null;

  return <div className={cn(userCardVariants({ variant }))}>{user.name}</div>;
}
```

### 3-2. Server Component vs Client Component

- 기본은 **Server Component** — 꼭 필요한 경우에만 `'use client'` 선언
- `'use client'`가 필요한 경우: 이벤트 핸들러, `useState`, `useEffect`, 브라우저 API, TanStack Query 훅
- `'use client'`는 트리의 최하단으로 밀어낼 것 — 부모는 Server Component로 유지

```
✅ 올바른 구조:                    ❌ 잘못된 구조:
ServerPage                        'use client' Page
  └─ ServerSection                  └─ ServerSection
       └─ 'use client' Button            └─ 'use client' Button
                                              (페이지 전체가 RSC 이점 상실)
```

### 3-3. Suspense를 이용한 스트리밍

비동기 Server Component는 반드시 `<Suspense>`로 감싸서 스트리밍을 활성화한다.
최상위에서 모든 fetch를 await하지 않는다 — 이는 초기 렌더링 전체를 블로킹한다.

```tsx
// ✅ 각 섹션이 독립적으로 스트리밍 — 준비되는 대로 순차 전송
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />          {/* 비동기 Server Component */}
      </Suspense>
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />          {/* 비동기 Server Component */}
      </Suspense>
    </div>
  );
}
```

### 3-4. 메모이제이션 기준

기본적으로 메모이제이션을 적용하지 않는다 — 실측된 성능 문제가 있을 때만 사용한다.

| API | 사용 시점 |
|-----|----------|
| `React.memo` | 같은 props로 자주 리렌더링되며 렌더 비용이 높은 경우 |
| `useMemo` | 정말 비용이 높은 연산 (예: 대용량 리스트 정렬/필터링) |
| `useCallback` | 메모이제이션된 자식 컴포넌트에 함수를 prop으로 전달하는 경우 |

### 3-5. 컴포넌트 크기

- 100줄 초과 시 하위 컴포넌트로 분리
- 하나의 컴포넌트는 하나의 역할만

---

## 4. API 연동 규칙

### 4-1. API 클라이언트 (클라이언트 사이드)

```typescript
// src/lib/api/client.ts
export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<ApiResponse<T>> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new ApiError(error.error.code, error.error.message, res.status);
  }

  return res.json();
}
```

### 4-2. API 함수 위치

- 클라이언트 사이드 함수: `src/lib/api/{domain}.ts`
- 컴포넌트나 훅 내부에서 `fetch()` 직접 호출 금지

### 4-3. 응답 타입 정의

BE 스키마를 그대로 `src/types/api/{domain}.ts`에 정의한다.

```typescript
// src/types/api/user.ts
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
}

export interface User {
  id: number;
  email: string;
  name: string;
  isActive: boolean;
  createdAt: string;
}
```

---

## 5. 폼 처리

모든 폼은 **React Hook Form + Zod + useMutation** 조합을 사용한다.
`useState`로 폼 상태나 로딩 상태를 관리하는 것을 금지한다.

```tsx
// src/hooks/useLogin.ts — useMutation은 반드시 커스텀 훅으로 분리
// 훅 파일은 'use client' 불필요 — 이 훅을 사용하는 컴포넌트가 'use client'이면 됨
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

export function useLogin() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (values: LoginFormValues) => authApi.login(values),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['me'] });
      router.push('/dashboard');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// src/components/features/auth/LoginForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('올바른 이메일 형식이 아닙니다.'),
  password: z.string().min(8, '비밀번호는 8자 이상이어야 합니다.'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  // useMutation은 커스텀 훅으로 분리 후 가져옴 — queryClient/router는 훅 내부에서 선언
  const { mutate: login, isPending } = useLogin();

  return (
    <form onSubmit={handleSubmit((values) => login(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <input type="password" {...register('password')} />
      {errors.password && <p role="alert">{errors.password.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? '로그인 중...' : '로그인'}
      </button>
    </form>
  );
}
```

---

## 6. 상태 관리 규칙

| 상태 유형 | 도구 | 예시 |
|----------|------|------|
| 서버 상태 (API 응답) | TanStack Query | 유저 프로필, 상품 목록 |
| 공유 가능한 UI 상태 (필터, 탭, 페이지) | URL 상태 (`useSearchParams` / `nuqs`) | `?page=2&sort=asc` |
| 클라이언트 전역 상태 (인증, 테마) | Zustand | 로그인 세션 |
| 로컬 UI 상태 | `useState` | 모달 열림/닫힘 |

- 서버 상태를 Zustand에 저장 금지 — 그것은 TanStack Query의 역할
- 북마크나 공유가 필요한 UI 상태는 반드시 URL에 저장

### Zustand 스토어 패턴

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  setUser: (user: User | null) => void;
  clearUser: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));

// ✅ 불필요한 리렌더링 방지를 위해 selector 사용
export const useCurrentUser = () => useAuthStore((state) => state.user);
```

---

## 7. 선언적 코딩 우선

명령형(how)이 아닌 선언적(what) 스타일로 작성하여 가독성과 유지보수성을 높인다.
조건, 리스트 처리, 렌더링 분기를 선언적으로 표현한다.

### 7-1. 조건부 렌더링

```tsx
// ❌ 명령형 — 조건이 늘어날수록 읽기 어려워짐
function UserStatus({ user }: { user: User }) {
  let badge;
  if (user.role === 'admin') {
    badge = <AdminBadge />;
  } else if (user.isActive) {
    badge = <ActiveBadge />;
  } else {
    badge = <InactiveBadge />;
  }
  return <div>{badge}</div>;
}

// ✅ 선언적 — 컴포넌트 맵으로 의도가 한눈에 읽힘
// JSX 인스턴스가 아닌 컴포넌트 자체를 맵핑 — props가 추가돼도 안전하게 확장 가능
const statusBadgeMap: Record<string, React.ComponentType> = {
  admin: AdminBadge,
  active: ActiveBadge,
  inactive: InactiveBadge,
};

function UserStatus({ user }: { user: User }) {
  const key = user.role === 'admin' ? 'admin' : user.isActive ? 'active' : 'inactive';
  const Badge = statusBadgeMap[key];
  return <div><Badge /></div>;
}
```

### 7-2. 리스트 처리

```tsx
// ❌ 명령형
function ActiveUserList({ users }: { users: User[] }) {
  const result = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(<UserCard key={user.id} user={user} />);
    }
  }
  return <ul>{result}</ul>;
}

// ✅ 선언적
function ActiveUserList({ users }: { users: User[] }) {
  const activeUsers = users.filter((user) => user.isActive);

  return (
    <ul>
      {activeUsers.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </ul>
  );
}
```

### 7-3. 로딩/에러/빈 상태 분기

```tsx
// ❌ 인라인 분기 — JSX가 복잡해짐
function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, isError } = useUser(userId);
  return (
    <div>
      {isLoading ? <Spinner /> : isError ? <ErrorMessage /> : !data ? <EmptyState /> : <ProfileCard user={data} />}
    </div>
  );
}
```

```tsx
// ✅ 선언적 얼리 리턴 — 각 상태가 명확히 분리됨
// 'use client'는 반드시 파일 최상단에 위치해야 함
'use client';

function UserProfile({ userId }: { userId: number }) {
  const { data: user, isLoading, isError } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  if (!user) return <EmptyState />;

  return <ProfileCard user={user} />;
}
```

### 7-4. 이벤트 핸들러

```tsx
// ❌ JSX 내 인라인 로직
<button onClick={() => {
  if (!isLoading) {
    setCount(count + 1);
    track('button_clicked');
  }
}}>
  클릭
</button>

// ✅ 의미 있는 이름의 핸들러로 분리
function handleClick() {
  if (isLoading) return;
  setCount((prev) => prev + 1);
  track('button_clicked');
}

<button onClick={handleClick}>클릭</button>
```

---

## 8. 타입스크립트 규칙

- `tsconfig.json`에 `strict: true` 필수
- `any` 타입 사용 금지 (불가피한 경우: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` + 이유 주석)
- `// @ts-ignore` 사용 금지 — `// @ts-expect-error` + 이유 주석 허용
- `interface`와 `type` 사용 기준:
  - 객체 형태 → `interface`
  - Union / Intersection / Primitive alias / 함수 시그니처 → `type`
- 모든 컴포넌트 Props에 타입 명시 필수
- 폼 및 API 검증 타입은 Zod 스키마를 단일 출처로 사용

```typescript
// ✅ Zod 스키마에서 TypeScript 타입 파생 — 중복 정의 금지
const userSchema = z.object({ id: z.number(), name: z.string() });
type User = z.infer<typeof userSchema>;
```

---

## 9. 퍼포먼스

### 9-1. 이미지

반드시 `next/image`를 사용한다. 일반 `<img>` 태그 사용 금지.

```tsx
import Image from 'next/image';

// ✅ 고정 크기 이미지
<Image src="/hero.png" alt="히어로 이미지" width={1200} height={600} priority />

// ✅ 크기를 알 수 없는 경우 fill 모드 사용
<div className="relative h-64 w-full">
  <Image src={user.avatar} alt={user.name} fill className="object-cover" />
</div>
```

- 폴드 위(above-the-fold) 이미지에는 `priority` 추가 (LCP 요소)
- 항상 의미 있는 `alt` 텍스트 제공

### 9-2. 폰트

반드시 `next/font`를 사용한다. `<link>` 또는 `@import`로 폰트를 로드 금지.

```typescript
// src/app/layout.tsx — AppProviders와 폰트를 모두 포함한 최종 버전
import { Inter } from 'next/font/google';
import { AppProviders } from './providers';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // inter.variable을 반드시 적용해야 실제로 폰트가 사용됨
    <html lang="ko" className={inter.variable}>
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 9-3. Dynamic Import

초기 렌더링에 필요 없는 무거운 컴포넌트는 지연 로딩한다.

```typescript
// ✅ 무거운 차트 라이브러리 — 탭을 열기 전까지 불필요
const Chart = dynamic(() => import('@/components/features/analytics/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,         // 브라우저 전용 라이브러리
});
```

### 9-4. 번들 크기

- 함수 하나만 필요할 때 라이브러리 전체를 import 금지
- 새 의존성 추가 전 `@next/bundle-analyzer`로 번들 영향 확인

```typescript
// ❌
import _ from 'lodash';
const sorted = _.sortBy(items, 'name');

// ✅
import sortBy from 'lodash/sortBy';
const sorted = sortBy(items, 'name');
```

### 9-5. 스크립트 로딩

```tsx
import Script from 'next/script';

// ✅ 서드파티 스크립트가 렌더링을 블로킹하지 않도록
<Script src="https://analytics.example.com/script.js" strategy="lazyOnload" />
```

---

## 10. SEO 및 메타데이터

모든 페이지는 메타데이터를 export해야 한다. `<title>` 또는 OG 태그를 비워두면 안 된다.

```typescript
// 정적 메타데이터
export const metadata: Metadata = {
  title: '페이지 제목',
  description: '페이지 설명',
  openGraph: { title: '페이지 제목', description: '페이지 설명' },
};

// 동적 메타데이터
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    openGraph: { images: [product.imageUrl] },
  };
}
```

---

## 11. 환경변수 관리

| Prefix | 접근 가능 위치 | 용도 |
|--------|-------------|------|
| `NEXT_PUBLIC_` | 브라우저 + 서버 | 공개 API URL, 피처 플래그 |
| (prefix 없음) | 서버 전용 | 시크릿 키, 내부 API URL |

```bash
# .env.example — 키만 나열, 값 없음. 이 파일만 git에 커밋
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_GA_ID=
API_SECRET_KEY=
```

- 시크릿 환경변수에 `NEXT_PUBLIC_` prefix 사용 금지
- `.env*.local`은 `.gitignore`에 추가, `.env.example`만 커밋
- 환경변수는 타입 상수 파일을 통해 접근 — 누락된 변수를 시작 시점에 감지

```typescript
// src/constants/env.ts
export const env = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  gaId: process.env.NEXT_PUBLIC_GA_ID,
} as const;
```

---

## 12. 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 파일 | PascalCase | `UserCard.tsx` |
| 훅 파일 | camelCase, `use` 접두사 | `useUserProfile.ts` |
| 유틸 파일 | camelCase | `formatDate.ts` |
| 스토어 파일 | camelCase, `Store` 접미사 | `authStore.ts` |
| 타입/인터페이스 | PascalCase | `UserProfile` |
| 상수 | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| 라우트 로컬 컴포넌트 | `_components/` 접두사 폴더 | `_components/HeroSection.tsx` |
| 경로 alias | `@/`를 `src/`로 매핑 | `import { Button } from '@/components/ui/Button'` |

---

## 13. 스타일링

- **Tailwind CSS**만 사용 — 인라인 `style` 속성 금지 (Tailwind로 표현 불가한 동적 값 예외)
- 조건부 클래스는 `clsx` 또는 `cn()` 사용 — 문자열 연산 금지
- CSS Module은 복잡한 애니메이션에만 허용
- 색상 hex 값 하드코딩 금지 — 항상 Tailwind 토큰 사용

```tsx
// ❌
<div style={{ color: '#3b82f6' }} className={'card' + (active ? ' active' : '')} />

// ✅
<div className={cn('rounded-lg bg-white', { 'ring-2 ring-blue-500': active })} />
```

---

## 14. 에러 처리

```tsx
// 페이지 레벨: error.tsx (Next.js App Router)
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert">
      <p>오류가 발생했습니다.</p>
      <button onClick={reset}>다시 시도</button>
    </div>
  );
}

// 컴포넌트 레벨: 조건부 렌더링 또는 ErrorBoundary
// API 에러: ApiError catch 후 toast 알림
try {
  await createUser(data);
} catch (error) {
  if (error instanceof ApiError) toast.error(error.message);
  else throw error;               // 예상치 못한 에러는 반드시 re-throw
}
```

---

## 15. 접근성 (a11y)

- 모든 이미지에 `alt` 필수 (장식용 이미지: `alt=""`)
- 모든 인터랙티브 요소(`button`, `a`)에 텍스트 내용 또는 `aria-label`로 접근 가능한 레이블 필수
- 색상만으로 상태를 나타내는 것 금지 — 아이콘 또는 텍스트 병행
- 폼 에러 메시지는 스크린 리더 알림을 위해 `role="alert"` 필수
- 마우스 없이 키보드 네비게이션 동작 확인 — Tab 키로 검증
- 모달 열림/닫힘 시 포커스 관리 필수 (`focus-trap`, `autoFocus`)
- 최소 터치 타겟 크기: 44×44px

---

## 16. Barrel Export (`index.ts`)

`index.ts` barrel 파일은 import를 단순화하기 위해 제한적으로 사용할 수 있으나, tree-shaking을 보존하기 위해 엄격한 규칙을 따른다.

```typescript
// ✅ 한 도메인 내 소수 항목 re-export — 허용
// src/components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';

// ❌ 금지 — 도메인 간 re-export 또는 디렉토리 전체 export
// tree-shaking을 깨고 순환 의존성 위험을 유발
export * from '../features';
export * from '../hooks';
```

---

## 17. 금지 사항 (전체 요약)

| 금지 항목 | 대안 |
|-----------|------|
| 커밋된 코드에 `console.log()` | 커밋 전 제거 또는 logger 유틸 사용 |
| `// @ts-ignore` | `// @ts-expect-error` + 이유 주석 |
| `any` 타입 | 명시적 타입; 불가피하면 `// eslint-disable` + 이유 |
| `default export` | named export (Next.js 페이지/레이아웃 파일 제외) |
| `useEffect` 내 API 호출 | TanStack Query (`useQuery` / `useMutation`) |
| 하드코딩된 API URL | `env` 상수를 통한 환경변수 |
| `<img>` 태그 | `next/image` |
| `<link>` / `@import` 폰트 로드 | `next/font` |
| `style={{ ... }}` | Tailwind 클래스 |
| 문자열 클래스 연산 | `cn()` / `clsx()` |
| Zustand에 서버 상태 저장 | TanStack Query |
| `useState`로 공유 가능한 UI 상태 관리 | URL 상태 (`useSearchParams` / `nuqs`) |
| `useState`로 폼 상태 / 로딩 상태 관리 | React Hook Form + Zod + `useMutation` |
| 뮤테이션 성공 후 캐시 무효화 누락 | `onSuccess`에서 `invalidateQueries` 호출 |
| `layout.tsx`에 `QueryClientProvider` 직접 사용 | `providers.tsx`로 분리 |
| `new QueryClient()`를 컴포넌트 최상위에서 직접 선언 | `useState(() => new QueryClient())` 패턴 |
| `prefetchQuery`와 `useQuery`의 `queryKey` 불일치 | 반드시 동일한 key 사용 |
| JSX 내 인라인 복잡 로직 | 의미 있는 이름의 핸들러/변수로 분리 |
| 렌더링 전 모든 fetch await | Suspense + 스트리밍 |
| 라이브러리 전체 import | named / path import |
| 시크릿에 `NEXT_PUBLIC_` prefix | prefix 없는 서버 전용 환경변수 |
| barrel 파일에서 `export *` (도메인 간) | 명시적 named re-export |