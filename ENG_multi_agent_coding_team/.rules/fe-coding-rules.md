# Frontend Coding Rules (Next.js / React)

> This file defines the coding rules that the FE Coding Agent and QA-FE Agent must strictly follow.

---

## 1. Project Structure

```
fe-project/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # Root layout (fonts, global providers)
│   │   ├── page.tsx
│   │   ├── loading.tsx             # Root Suspense fallback
│   │   ├── not-found.tsx           # 404 page
│   │   ├── error.tsx               # Root error boundary (Client Component)
│   │   ├── global-error.tsx        # Crash-level error boundary
│   │   ├── providers.tsx           # Global Client Provider wrapper ('use client')
│   │   └── (routes)/               # Route groups — one folder per domain
│   │       └── {domain}/
│   │           ├── page.tsx
│   │           ├── loading.tsx
│   │           ├── error.tsx
│   │           └── _components/    # Route-local components (not shared)
│   ├── components/
│   │   ├── ui/                     # Atomic reusable components (Button, Input, etc.)
│   │   └── features/               # Domain-specific composite components
│   ├── hooks/                      # Custom hooks
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # Base fetch wrapper
│   │   │   └── {domain}.ts         # Domain API functions
│   │   └── utils/                  # Pure utility functions
│   ├── stores/                     # Zustand stores (client global state only)
│   ├── types/
│   │   └── api/                    # API response types (mirroring BE schemas)
│   ├── constants/                  # App-wide constants and enums
│   ├── styles/                     # Global styles
│   └── middleware.ts               # Edge middleware (auth, redirects, etc.)
├── public/
├── tests/
│   ├── components/
│   └── hooks/
├── next.config.ts
├── tsconfig.json
└── .env.example                    # Required env var keys only — no values
```

---

## 2. TanStack Query Setup

### 2-1. QueryClient Provider (Required Initial Setup)

`layout.tsx` is a Server Component, so `QueryClientProvider` cannot be placed there directly.
Always create a separate `providers.tsx` file.

```tsx
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function AppProviders({ children }: { children: React.ReactNode }) {
  // Wrapping with useState ensures a single instance per component
  // Using new QueryClient() directly creates a new instance on every render
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 1000 * 60,       // Global default staleTime: 1 minute
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
// src/app/layout.tsx — keep as Server Component
import { AppProviders } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 2-2. Data Fetching Strategy

This is the most impactful decision for performance and correctness. Choose a pattern based on the data characteristics.

| Data type | Pattern | Location |
|-----------|---------|----------|
| Rarely changes, SEO-critical | `fetch` + `cache: 'force-cache'` (SSG) | Server Component |
| Changes periodically (minutes to hours) | `fetch` + `next: { revalidate: N }` (ISR) | Server Component |
| Changes on every request, auth-dependent | `fetch` + `cache: 'no-store'` (SSR) | Server Component |
| Real-time, user-triggered, post-navigation refresh | TanStack Query | Client Component |

### 2-3. Server Component Data Fetching

```typescript
// app/(routes)/products/page.tsx
// ✅ Fetch at the component level — no prop drilling needed
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// src/lib/api/products.ts
export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`, {
    next: { revalidate: 60 },           // ISR: revalidate every 60 seconds
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) throw new Error('Failed to fetch products');
  const data: ApiResponse<Product[]> = await res.json();
  return data.data ?? [];
}
```

### 2-4. Prefetch + HydrationBoundary (SSR + Client Cache)

Prefetch data in a Server Component and hydrate it into Client Components.
Without this pattern, the Client Component starts fetching from scratch after mount, causing a loading flash.

```tsx
// app/(routes)/users/page.tsx — Server Component
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { UserList } from './_components/UserList';

export default async function UsersPage() {
  const queryClient = new QueryClient();

  // Prefetch on the server — queryKey must be identical to the client
  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });

  return (
    // Pass dehydrated cache to the client
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserList />   {/* Cache already populated — renders immediately without loading */}
    </HydrationBoundary>
  );
}
```

```tsx
// app/(routes)/users/_components/UserList.tsx — Client Component
'use client';

export function UserList() {
  // Prefetched data is already in cache — isLoading starts as false
  const { data: users } = useQuery({
    queryKey: ['users'],              // Must match the server prefetchQuery key exactly
    queryFn: getUsers,
  });

  return (
    <ul>
      {users?.map((user) => <UserCard key={user.id} user={user} />)}
    </ul>
  );
}
```

> ⚠️ If the `queryKey` in `prefetchQuery` and `useQuery` do not match exactly, the hydration connection breaks and the server-fetched data is discarded.

### 2-5. useQuery — Client Component Data Fetching

```typescript
// src/hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api/users';

export function useUser(userId: number) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),   // function from src/lib/api/users.ts
    staleTime: 1000 * 60 * 5,        // 5 minutes (overrides global default)
  });
}
```

- Never call `fetch()` or `apiClient` directly inside `useEffect` — always use TanStack Query
- Never store server state (API responses) in Zustand

### 2-6. useMutation — Mutating Server Data

All create / update / delete operations must use `useMutation`.
Never manage `isPending`, `onSuccess`, or `onError` with `useState`.

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api/users';

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserRequest) => userApi.create(data),
    onSuccess: () => {
      // Invalidate related cache on success — list updates automatically
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created successfully.');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// React Hook Form + useMutation connection pattern
'use client';

export function CreateUserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateUserRequest>({
    resolver: zodResolver(createUserSchema),
  });

  const { mutate: createUser, isPending } = useCreateUser();

  return (
    // handleSubmit validates then calls mutate
    <form onSubmit={handleSubmit((values) => createUser(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

- `mutationFn` must use a function from `src/lib/api/{domain}.ts`
- Always call `invalidateQueries` in `onSuccess` to keep cache in sync
- Never manage `isPending` with a separate `useState` — use `useMutation`'s `isPending`

---

## 3. Component Rules

### 3-1. Basic Form

```tsx
// ✅ Named export + separate Props interface
// Uses the useUser hook, so 'use client' is required
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

- Default to **Server Component** — only add `'use client'` when strictly necessary
- `'use client'` is required for: event handlers, `useState`, `useEffect`, browser APIs, TanStack Query hooks
- Push `'use client'` as far down the tree as possible — keep parents as Server Components

```
✅ Correct:                        ❌ Incorrect:
ServerPage                        'use client' Page
  └─ ServerSection                  └─ ServerSection
       └─ 'use client' Button            └─ 'use client' Button
                                              (entire page loses RSC benefits)
```

### 3-3. Streaming with Suspense

Wrap async Server Components in `<Suspense>` to enable streaming.
Never await all fetches at the top level — this blocks the entire initial render.

```tsx
// ✅ Each section streams independently — sent as soon as ready
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />          {/* async Server Component */}
      </Suspense>
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />          {/* async Server Component */}
      </Suspense>
    </div>
  );
}
```

### 3-4. Memoization Guidelines

Do not memoize by default — only apply when there is a measured performance problem.

| API | When to use |
|-----|-------------|
| `React.memo` | Component re-renders frequently with the same props and render is expensive |
| `useMemo` | Genuinely expensive computation (e.g. sorting/filtering a large list) |
| `useCallback` | Function is passed as a prop to a memoized child component |

### 3-5. Component Size

- Split into sub-components when a component exceeds 100 lines
- One component = one responsibility

---

## 4. API Integration

### 4-1. API Client (Client-side)

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

### 4-2. API Function Location

- Client-side functions: `src/lib/api/{domain}.ts`
- Never call `fetch()` directly inside components or hooks

### 4-3. Response Type Definitions

Mirror BE schemas exactly in `src/types/api/{domain}.ts`.

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

## 5. Form Handling

All forms must use the **React Hook Form + Zod + useMutation** combination.
Never manage form state or loading state with `useState`.

```tsx
// src/hooks/useLogin.ts — useMutation must always be extracted into a custom hook
// Hook files do not need 'use client' — the component that calls this hook handles that
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
  email: z.string().email('Please enter a valid email address.'),
  password: z.string().min(8, 'Password must be at least 8 characters.'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  // useMutation is extracted into a custom hook — queryClient/router are declared inside the hook
  const { mutate: login, isPending } = useLogin();

  return (
    <form onSubmit={handleSubmit((values) => login(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <input type="password" {...register('password')} />
      {errors.password && <p role="alert">{errors.password.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Logging in...' : 'Log In'}
      </button>
    </form>
  );
}
```

---

## 6. State Management

| State type | Tool | Example |
|-----------|------|---------|
| Server state (API responses) | TanStack Query | user profile, product list |
| Shareable UI state (filters, tabs, pagination) | URL state (`useSearchParams` / `nuqs`) | `?page=2&sort=asc` |
| Client global state (auth, theme) | Zustand | login session |
| Local UI state | `useState` | modal open/close |

- Never store server state in Zustand — that is TanStack Query's responsibility
- Any UI state that should be bookmarkable or shareable must live in the URL

### Zustand Store Pattern

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

// ✅ Use selectors to prevent unnecessary re-renders
export const useCurrentUser = () => useAuthStore((state) => state.user);
```

---

## 7. Declarative Code First

Write in a declarative (what) style rather than imperative (how) to improve readability and maintainability.
Express conditions, list processing, and render branching declaratively.

### 7-1. Conditional Rendering

```tsx
// ❌ Imperative — harder to read as conditions grow
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
```

```tsx
// ✅ Declarative — intent is immediately readable
// Map components, not JSX instances — safe to extend when props are added
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

### 7-2. List Processing

```tsx
// ❌ Imperative
function ActiveUserList({ users }: { users: User[] }) {
  const result = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(<UserCard key={user.id} user={user} />);
    }
  }
  return <ul>{result}</ul>;
}
```

```tsx
// ✅ Declarative
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

### 7-3. Loading / Error / Empty State Branching

```tsx
// ❌ Inline ternary chain — JSX becomes hard to read
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
// ✅ Declarative early returns — each state is clearly separated
// 'use client' must be at the very top of the file
'use client';

function UserProfile({ userId }: { userId: number }) {
  const { data: user, isLoading, isError } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  if (!user) return <EmptyState />;

  return <ProfileCard user={user} />;
}
```

### 7-4. Event Handlers

```tsx
// ❌ Inline logic in JSX
<button onClick={() => {
  if (!isLoading) {
    setCount(count + 1);
    track('button_clicked');
  }
}}>
  Click
</button>
```

```tsx
// ✅ Extract into a named handler
function handleClick() {
  if (isLoading) return;
  setCount((prev) => prev + 1);
  track('button_clicked');
}

<button onClick={handleClick}>Click</button>
```

---

## 8. TypeScript Rules

- `strict: true` required in `tsconfig.json`
- `any` type prohibited (if unavoidable: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` + reason comment)
- `// @ts-ignore` prohibited — use `// @ts-expect-error` + reason comment instead
- `interface` vs `type`:
  - Object shapes → `interface`
  - Union / Intersection / Primitive alias / function signatures → `type`
- All component Props must be explicitly typed
- Use Zod schemas as the single source of truth for form and API validation types

```typescript
// ✅ Derive TypeScript types from Zod schema — no duplicate definitions
const userSchema = z.object({ id: z.number(), name: z.string() });
type User = z.infer<typeof userSchema>;
```

---

## 9. Performance

### 9-1. Images

Always use `next/image`. Never use a bare `<img>` tag.

```tsx
import Image from 'next/image';

// ✅ Fixed size image
<Image src="/hero.png" alt="Hero banner" width={1200} height={600} priority />

// ✅ Unknown dimensions — use fill mode
<div className="relative h-64 w-full">
  <Image src={user.avatar} alt={user.name} fill className="object-cover" />
</div>
```

- Add `priority` to above-the-fold images (LCP element)
- Always provide meaningful `alt` text

### 9-2. Fonts

Always use `next/font`. Never load fonts via `<link>` or `@import`.

```typescript
// src/app/layout.tsx — final version including both AppProviders and font setup
import { Inter } from 'next/font/google';
import { AppProviders } from './providers';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // inter.variable must be applied here for the font to actually take effect
    <html lang="en" className={inter.variable}>
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 9-3. Dynamic Imports

Lazy-load heavy components that are not needed on initial render.

```typescript
// ✅ Heavy chart library — not needed until the user opens the tab
const Chart = dynamic(() => import('@/components/features/analytics/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,         // browser-only library
});
```

### 9-4. Bundle Size

- Never import an entire library when only one function is needed
- Check bundle impact with `@next/bundle-analyzer` before adding a new dependency

```typescript
// ❌
import _ from 'lodash';
const sorted = _.sortBy(items, 'name');

// ✅
import sortBy from 'lodash/sortBy';
const sorted = sortBy(items, 'name');
```

### 9-5. Script Loading

```tsx
import Script from 'next/script';

// ✅ Third-party scripts must never block rendering
<Script src="https://analytics.example.com/script.js" strategy="lazyOnload" />
```

---

## 10. SEO and Metadata

Every page must export metadata. Never leave `<title>` or OG tags empty.

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: { title: 'Page Title', description: 'Page description' },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    openGraph: { images: [product.imageUrl] },
  };
}
```

---

## 11. Environment Variables

| Prefix | Accessible from | Use for |
|--------|----------------|---------|
| `NEXT_PUBLIC_` | Browser + server | Public API URL, feature flags |
| (no prefix) | Server only | Secret keys, internal API URLs |

```bash
# .env.example — keys only, no values. This is the only file committed to git.
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_GA_ID=
API_SECRET_KEY=
```

- Never use `NEXT_PUBLIC_` prefix on secret env vars
- Add `.env*.local` to `.gitignore` — only commit `.env.example`
- Access env vars through a typed constants file to catch missing variables at startup

```typescript
// src/constants/env.ts
export const env = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  gaId: process.env.NEXT_PUBLIC_GA_ID,
} as const;
```

---

## 12. Naming Conventions

| Target | Rule | Example |
|--------|------|---------|
| Component files | PascalCase | `UserCard.tsx` |
| Hook files | camelCase, `use` prefix | `useUserProfile.ts` |
| Utility files | camelCase | `formatDate.ts` |
| Store files | camelCase, `Store` suffix | `authStore.ts` |
| Types / interfaces | PascalCase | `UserProfile` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Route-local components | `_components/` prefix folder | `_components/HeroSection.tsx` |
| Path alias | `@/` maps to `src/` | `import { Button } from '@/components/ui/Button'` |

---

## 13. Styling

- **Tailwind CSS only** — inline `style` attribute prohibited (exception: dynamic values unreachable by Tailwind)
- Conditional classes must use `clsx` or `cn()` — never string concatenation
- CSS Modules allowed only for complex animations
- Never hardcode color hex values — always use Tailwind tokens

```tsx
// ❌
<div style={{ color: '#3b82f6' }} className={'card' + (active ? ' active' : '')} />

// ✅
<div className={cn('rounded-lg bg-white', { 'ring-2 ring-blue-500': active })} />
```

---

## 14. Error Handling

```tsx
// Page level: error.tsx (Next.js App Router)
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert">
      <p>Something went wrong.</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// Component level: conditional rendering or ErrorBoundary
// API errors: catch ApiError → toast notification
try {
  await createUser(data);
} catch (error) {
  if (error instanceof ApiError) toast.error(error.message);
  else throw error;               // unexpected errors must be re-thrown
}
```

---

## 15. Accessibility (a11y)

- All images must have `alt` (decorative images: `alt=""`)
- All interactive elements (`button`, `a`) must have an accessible label via text content or `aria-label`
- Never communicate state through color alone — always pair with an icon or text
- Form error messages must use `role="alert"` for screen reader announcement
- Verify keyboard navigation works without a mouse — test with the Tab key
- Focus must be managed on modal open/close (`focus-trap`, `autoFocus`)
- Minimum touch target size: 44×44px

---

## 16. Barrel Exports (`index.ts`)

Barrel files (`index.ts`) may be used sparingly to simplify imports, but must follow strict rules to preserve tree-shaking.

```typescript
// ✅ Allowed — re-exporting a small number of items from one domain
// src/components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';

// ❌ Prohibited — re-exporting across domains or entire directories
// Breaks tree-shaking and risks circular dependencies
export * from '../features';
export * from '../hooks';
```

---

## 17. Prohibited Practices (Full Summary)

| Prohibited | Alternative |
|-----------|-------------|
| `console.log()` in committed code | Remove before commit or use a logger utility |
| `// @ts-ignore` | `// @ts-expect-error` + reason comment |
| `any` type | Explicit types; `// eslint-disable` + reason if unavoidable |
| `default export` | Named export (except Next.js page / layout files) |
| API calls inside `useEffect` | TanStack Query (`useQuery` / `useMutation`) |
| Hardcoded API URLs | Environment variables via `env` constants |
| `<img>` tag | `next/image` |
| `<link>` / `@import` for fonts | `next/font` |
| `style={{ ... }}` | Tailwind classes |
| String class concatenation | `cn()` / `clsx()` |
| Server state stored in Zustand | TanStack Query |
| Shareable UI state in `useState` | URL state (`useSearchParams` / `nuqs`) |
| Form state / loading state in `useState` | React Hook Form + Zod + `useMutation` |
| Missing cache invalidation after mutation | Call `invalidateQueries` in `onSuccess` |
| `QueryClientProvider` directly in `layout.tsx` | Extract to `providers.tsx` |
| `new QueryClient()` at component top level | `useState(() => new QueryClient())` pattern |
| Mismatched `queryKey` between `prefetchQuery` and `useQuery` | Always use identical keys |
| Complex inline logic in JSX | Extract into a named handler or variable |
| Awaiting all fetches before render | Suspense + streaming |
| Importing entire libraries | Named / path imports |
| `NEXT_PUBLIC_` prefix on secrets | Server-only env vars (no prefix) |
| `export *` across domains in barrel files | Explicit named re-exports |