# NestJS (TypeScript) 백엔드 코딩 룰

> 자동 생성 일시: 2026-03-23 08:00:00
> 프레임워크 버전: latest
> 상태: 🤖 Auto-Generated

---

## 1. 프로젝트 구조

### 기본 디렉토리 구조

```
backend/
├── src/
│   ├── config/              # 환경 설정 (env, database, jwt 등)
│   ├── common/              # 공통 유틸리티
│   │   ├── constants/       # 상수 정의
│   │   ├── decorators/      # 커스텀 데코레이터
│   │   ├── dto/             # 공통 DTO
│   │   ├── filters/         # Exception Filters
│   │   ├── guards/          # Auth Guards, Role Guards
│   │   ├── interceptors/    # Logging, Transform Interceptors
│   │   ├── interfaces/      # 공통 인터페이스
│   │   ├── middleware/      # 커스텀 미들웨어
│   │   └── pipes/           # Validation Pipes
│   ├── modules/             # 비즈니스 도메인 모듈
│   │   ├── auth/
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── auth.module.ts
│   │   │   ├── dto/
│   │   │   ├── guards/
│   │   │   └── strategies/
│   │   ├── users/
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   ├── users.module.ts
│   │   │   ├── dto/
│   │   │   ├── entities/
│   │   │   └── users.repository.ts
│   │   └── [feature-modules]/
│   ├── database/            # 데이터베이스 설정
│   │   ├── migrations/
│   │   ├── seeds/
│   │   └── database.module.ts
│   ├── shared/              # 재사용 가능한 모듈
│   │   ├── email/
│   │   ├── logger/
│   │   └── cache/
│   ├── app.module.ts        # 루트 모듈
│   └── main.ts              # 엔트리 포인트
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── nest-cli.json
├── package.json
├── tsconfig.json
└── tsconfig.build.json
```

### 각 디렉토리 역할

- **config/**: 환경별 설정 파일 (database, jwt, cors 등)
- **common/**: 전체 애플리케이션에서 공유되는 유틸리티
- **modules/**: 도메인별 기능 모듈 (auth, users, products 등)
- **database/**: ORM 설정, 마이그레이션, Seed 데이터
- **shared/**: 독립적으로 재사용 가능한 모듈

---

## 2. 아키텍처 패턴

### Layered Architecture (3-Layer)

NestJS는 기본적으로 **3-Layer Architecture**를 따릅니다:

1. **Controller Layer** (프레젠테이션)
   - HTTP 요청/응답 처리
   - 라우팅, 입력 검증
   - DTOs 사용

2. **Service Layer** (비즈니스 로직)
   - 핵심 비즈니스 로직
   - 트랜잭션 관리
   - 여러 리포지토리 조율

3. **Repository/Data Access Layer** (데이터 접근)
   - 데이터베이스 쿼리
   - ORM 작업 (TypeORM, Prisma 등)

### Dependency Injection (DI)

NestJS의 핵심 패턴:

```typescript
// ✅ 좋은 예: Constructor Injection
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
    private readonly emailService: EmailService,
  ) {}

  async findOne(id: string): Promise<User> {
    return this.usersRepository.findOne({ where: { id } });
  }
}
```

```typescript
// ❌ 나쁜 예: 직접 인스턴스 생성
export class UsersService {
  private usersRepository = new UsersRepository(); // 절대 금지!
}
```

### Clean Architecture (선택적)

대규모 프로젝트에서는 Clean Architecture 적용 권장:

```
src/
├── domain/           # 엔티티, 도메인 로직
├── application/      # Use Cases
├── infrastructure/   # 외부 연동 (DB, API)
└── presentation/     # Controllers
```

---

## 3. 네이밍 컨벤션

### 파일명

**규칙**: `kebab-case.suffix.ts`

| 타입 | 파일명 예시 |
|------|-------------|
| Controller | `users.controller.ts` |
| Service | `users.service.ts` |
| Module | `users.module.ts` |
| DTO | `create-user.dto.ts` |
| Entity | `user.entity.ts` |
| Interface | `user.interface.ts` |
| Guard | `jwt-auth.guard.ts` |
| Interceptor | `logging.interceptor.ts` |
| Pipe | `validation.pipe.ts` |
| Filter | `http-exception.filter.ts` |

### 클래스/인터페이스

**규칙**: `PascalCase` + 접미사

```typescript
// Controllers
export class UsersController { }
export class AuthController { }

// Services
export class UsersService { }
export class EmailService { }

// DTOs
export class CreateUserDto { }
export class UpdateUserDto { }

// Entities
export class User { }
export class Product { }

// Interfaces (접두사 'I' 없이)
export interface UserResponse { }
export interface PaginationOptions { }
```

### 변수/메서드

**규칙**: `camelCase`

```typescript
// 변수
const userId = '123';
const isActive = true;
const userList = [];

// 메서드
async findUserById(id: string) { }
async createUser(dto: CreateUserDto) { }
async updateUserStatus(id: string, status: boolean) { }
```

### 상수

**규칙**: `UPPER_SNAKE_CASE`

```typescript
// constants/app.constants.ts
export const MAX_UPLOAD_SIZE = 5 * 1024 * 1024; // 5MB
export const JWT_EXPIRATION_TIME = '1h';
export const DEFAULT_PAGE_SIZE = 20;
```

---

## 4. 코딩 스타일

### TypeScript 스타일 가이드

**필수**: [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)

### NestJS 특화 스타일

#### 데코레이터 사용

```typescript
// ✅ 올바른 데코레이터 사용
@Controller('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  async findOne(@Param('id') id: string): Promise<User> {
    return this.usersService.findOne(id);
  }

  @Post()
  @UsePipes(new ValidationPipe())
  async create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.usersService.create(createUserDto);
  }
}
```

#### DTOs with Validation

```typescript
// create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'john@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'password123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;

  @ApiProperty({ example: 'John Doe', required: false })
  @IsOptional()
  @IsString()
  name?: string;
}
```

#### 타입 안정성

```typescript
// ✅ 명시적 타입 정의
async findAll(): Promise<User[]> {
  return this.usersRepository.find();
}

// ✅ 제네릭 활용
async paginate<T>(
  options: PaginationOptions,
): Promise<PaginationResult<T>> {
  // ...
}

// ❌ any 사용 금지
async getData(): Promise<any> { // 절대 금지!
  // ...
}
```

---

## 5. 의존성 관리

### 패키지 매니저

**권장**: `npm` 또는 `pnpm`

```bash
# 의존성 설치
npm install

# 개발 의존성 추가
npm install --save-dev @types/express

# 프로덕션 의존성 추가
npm install @nestjs/typeorm typeorm pg
```

### 필수 의존성

```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/platform-express": "^10.0.0",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.0",
    "rxjs": "^7.8.0",
    "reflect-metadata": "^0.1.13"
  },
  "devDependencies": {
    "@nestjs/cli": "^10.0.0",
    "@nestjs/schematics": "^10.0.0",
    "@nestjs/testing": "^10.0.0",
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "ts-node": "^10.0.0",
    "typescript": "^5.0.0"
  }
}
```

### 버전 관리

- **시맨틱 버저닝** 준수
- `package-lock.json` 또는 `pnpm-lock.yaml` 커밋 필수
- 정기적으로 `npm audit` 실행

---

## 6. 환경 설정

### 환경 변수 관리

**패키지**: `@nestjs/config`

```typescript
// config/configuration.ts
export default () => ({
  port: parseInt(process.env.PORT, 10) || 3000,
  database: {
    host: process.env.DATABASE_HOST || 'localhost',
    port: parseInt(process.env.DATABASE_PORT, 10) || 5432,
    username: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME,
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRATION || '1h',
  },
});
```

```typescript
// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [configuration],
      validationSchema: Joi.object({
        PORT: Joi.number().default(3000),
        DATABASE_HOST: Joi.string().required(),
        JWT_SECRET: Joi.string().min(32).required(),
      }),
    }),
  ],
})
export class AppModule {}
```

### 시크릿 관리

```env
# .env.example
PORT=3000
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=
JWT_SECRET=
```

**중요**:
- `.env` 파일은 `.gitignore`에 추가
- `.env.example`은 템플릿으로 커밋
- JWT_SECRET은 최소 32자 이상
- 프로덕션에서는 환경 변수로 주입

---

## 7. 보안 가이드

### 입력 검증

**필수**: `class-validator` + `class-transformer`

```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,        // DTO에 없는 속성 제거
    forbidNonWhitelisted: true, // 알 수 없는 속성 시 에러
    transform: true,        // 자동 타입 변환
  }),
);
```

```typescript
// DTO 예시
import { IsInt, Min, Max, IsUUID } from 'class-validator';

export class GetUsersDto {
  @IsInt()
  @Min(1)
  @Max(100)
  limit: number = 20;

  @IsUUID()
  userId: string;
}
```

### 인증/인가

**패키지**: `@nestjs/jwt`, `@nestjs/passport`

```typescript
// jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }

  handleRequest(err, user, info) {
    if (err || !user) {
      throw new UnauthorizedException('Invalid token');
    }
    return user;
  }
}
```

```typescript
// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

### SQL Injection 방지

**TypeORM 파라미터화 쿼리 사용**:

```typescript
// ✅ 안전: 파라미터화 쿼리
async findByEmail(email: string): Promise<User> {
  return this.usersRepository.findOne({ where: { email } });
}

// ✅ 안전: QueryBuilder
async searchUsers(keyword: string): Promise<User[]> {
  return this.usersRepository
    .createQueryBuilder('user')
    .where('user.name ILIKE :keyword', { keyword: `%${keyword}%` })
    .getMany();
}

// ❌ 위험: 직접 문자열 조합
async searchUsers(keyword: string): Promise<User[]> {
  return this.usersRepository.query(
    `SELECT * FROM users WHERE name LIKE '%${keyword}%'` // SQL Injection 취약!
  );
}
```

### XSS/CSRF 방지

```typescript
// main.ts
import helmet from 'helmet';
import * as csurf from 'csurf';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Helmet: 보안 헤더 설정
  app.use(helmet());

  // CORS 설정
  app.enableCors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
    credentials: true,
  });

  // CSRF 보호 (세션 기반 인증 시)
  // app.use(csurf());

  await app.listen(3000);
}
```

### Rate Limiting

**패키지**: `@nestjs/throttler`

```typescript
// app.module.ts
@Module({
  imports: [
    ThrottlerModule.forRoot([{
      ttl: 60000,  // 1분
      limit: 10,   // 10 요청
    }]),
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}
```

```typescript
// 특정 엔드포인트에 다른 제한 적용
@Controller('auth')
export class AuthController {
  @Throttle({ default: { limit: 3, ttl: 60000 } }) // 1분에 3번
  @Post('login')
  async login(@Body() loginDto: LoginDto) {
    // ...
  }
}
```

---

## 8. 에러 핸들링

### Exception Filters

```typescript
// http-exception.filter.ts
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus();

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message: exception.message || 'Internal server error',
    };

    Logger.error(
      `${request.method} ${request.url}`,
      JSON.stringify(errorResponse),
      'HttpExceptionFilter',
    );

    response.status(status).json(errorResponse);
  }
}
```

### 커스텀 예외

```typescript
// exceptions/user-not-found.exception.ts
export class UserNotFoundException extends NotFoundException {
  constructor(userId: string) {
    super(`User with ID ${userId} not found`);
  }
}

// 사용
async findOne(id: string): Promise<User> {
  const user = await this.usersRepository.findOne({ where: { id } });
  if (!user) {
    throw new UserNotFoundException(id);
  }
  return user;
}
```

### 로깅

**패키지**: 내장 `Logger` 또는 `winston`

```typescript
import { Logger } from '@nestjs/common';

@Injectable()
export class UsersService {
  private readonly logger = new Logger(UsersService.name);

  async findAll(): Promise<User[]> {
    this.logger.log('Fetching all users');
    try {
      const users = await this.usersRepository.find();
      this.logger.debug(`Found ${users.length} users`);
      return users;
    } catch (error) {
      this.logger.error('Failed to fetch users', error.stack);
      throw error;
    }
  }
}
```

---

## 9. 테스팅 전략

### 테스트 프레임워크

**기본**: Jest

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:cov": "jest --coverage",
    "test:e2e": "jest --config ./test/jest-e2e.json"
  }
}
```

### 테스트 구조

```
test/
├── unit/
│   ├── users.service.spec.ts
│   └── auth.service.spec.ts
├── integration/
│   └── users.controller.spec.ts
└── e2e/
    └── app.e2e-spec.ts
```

### Unit Test 예시

```typescript
// users.service.spec.ts
describe('UsersService', () => {
  let service: UsersService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            find: jest.fn(),
            findOne: jest.fn(),
            save: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const users = [{ id: '1', email: 'test@test.com' }];
      jest.spyOn(repository, 'find').mockResolvedValue(users as User[]);

      expect(await service.findAll()).toEqual(users);
    });
  });
});
```

### E2E Test 예시

```typescript
// app.e2e-spec.ts
describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });

  afterAll(async () => {
    await app.close();
  });
});
```

### 커버리지 목표

- **전체**: 80% 이상
- **Service Layer**: 90% 이상
- **Controller Layer**: 70% 이상

---

## 10. 성능 최적화

### 비동기 처리

```typescript
// ✅ Promise.all로 병렬 처리
async getUserWithPosts(userId: string) {
  const [user, posts] = await Promise.all([
    this.usersRepository.findOne({ where: { id: userId } }),
    this.postsRepository.find({ where: { userId } }),
  ]);
  return { user, posts };
}

// ❌ 순차 처리 (느림)
async getUserWithPosts(userId: string) {
  const user = await this.usersRepository.findOne({ where: { id: userId } });
  const posts = await this.postsRepository.find({ where: { userId } });
  return { user, posts };
}
```

### 캐싱

**패키지**: `@nestjs/cache-manager`

```typescript
@Injectable()
export class UsersService {
  constructor(
    @Inject(CACHE_MANAGER) private cacheManager: Cache,
  ) {}

  async findAll(): Promise<User[]> {
    const cacheKey = 'all_users';
    const cached = await this.cacheManager.get<User[]>(cacheKey);

    if (cached) {
      return cached;
    }

    const users = await this.usersRepository.find();
    await this.cacheManager.set(cacheKey, users, 300); // 5분 캐시
    return users;
  }
}
```

### Database 쿼리 최적화

```typescript
// ✅ Eager Loading (N+1 문제 방지)
async findAllWithPosts(): Promise<User[]> {
  return this.usersRepository.find({
    relations: ['posts'],
  });
}

// ✅ Select 필드 제한
async findAllEmails(): Promise<Pick<User, 'email'>[]> {
  return this.usersRepository.find({
    select: ['email'],
  });
}

// ✅ 페이지네이션
async paginate(page: number, limit: number): Promise<[User[], number]> {
  return this.usersRepository.findAndCount({
    skip: (page - 1) * limit,
    take: limit,
  });
}
```

---

## 11. 문서화

### API 문서 (Swagger)

**패키지**: `@nestjs/swagger`

```typescript
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('API Documentation')
    .setDescription('The API description')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  await app.listen(3000);
}
```

```typescript
// users.controller.ts
@ApiTags('users')
@Controller('users')
export class UsersController {
  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  @ApiResponse({ status: 200, description: 'User found', type: User })
  @ApiResponse({ status: 404, description: 'User not found' })
  async findOne(@Param('id') id: string): Promise<User> {
    return this.usersService.findOne(id);
  }
}
```

### 코드 주석

```typescript
/**
 * 사용자 서비스
 * 사용자 관련 비즈니스 로직을 처리합니다.
 */
@Injectable()
export class UsersService {
  /**
   * ID로 사용자 조회
   * @param id - 사용자 UUID
   * @returns 사용자 엔티티
   * @throws {UserNotFoundException} 사용자를 찾을 수 없을 때
   */
  async findOne(id: string): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) {
      throw new UserNotFoundException(id);
    }
    return user;
  }
}
```

### README.md 필수 섹션

```markdown
# Project Name

## 설치
\`\`\`bash
npm install
\`\`\`

## 환경 설정
\`\`\`bash
cp .env.example .env
# .env 파일 수정
\`\`\`

## 실행
\`\`\`bash
# 개발
npm run start:dev

# 프로덕션
npm run build
npm run start:prod
\`\`\`

## 테스트
\`\`\`bash
npm test
npm run test:e2e
npm run test:cov
\`\`\`

## API 문서
http://localhost:3000/api/docs

## 라이선스
MIT
```

---

## 12. 금지 사항

### 안티패턴

- ❌ **Service에서 HTTP 응답 처리**: Service는 비즈니스 로직만, Controller가 HTTP 담당
- ❌ **any 타입 남용**: TypeScript의 이점 상실
- ❌ **Circular Dependency**: 모듈 간 순환 참조
- ❌ **직접 인스턴스 생성**: DI 컨테이너 사용 필수
- ❌ **동기 파일 I/O**: `fs.readFileSync()` 금지, async 사용

### 보안 취약점

- ❌ **환경 변수를 코드에 하드코딩**
- ❌ **SQL 쿼리 문자열 직접 조합** (SQL Injection)
- ❌ **사용자 입력을 검증 없이 사용**
- ❌ **민감 정보 로깅** (비밀번호, 토큰 등)
- ❌ **CORS를 `*`로 설정** (프로덕션)

### 성능 이슈

- ❌ **N+1 쿼리 문제**: Eager Loading 사용
- ❌ **대용량 데이터를 한 번에 조회**: 페이지네이션 필수
- ❌ **캐시 없이 반복 조회**: Redis 등 캐시 활용
- ❌ **동기 blocking 작업**: 비동기 처리 필수

---

## 13. 참고 자료

### 공식 문서
- NestJS 공식 문서: https://docs.nestjs.com/
- TypeScript Handbook: https://www.typescriptlang.org/docs/

### 베스트 프랙티스
- NestJS Best Practices: https://github.com/weiwensangsang/nestjs-best-practices
- Awesome NestJS: https://github.com/nestjs/awesome-nestjs

### 보안 가이드
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Securing NestJS Apps: https://medium.com/@febriandwikimhan/securing-nestjs-apps-implementing-key-owasp-protections-8ef60df6ecf8

### 예시 프로젝트
- NestJS Project Structure: https://github.com/CatsMiaow/nestjs-project-structure
- Clean Architecture with NestJS: https://github.com/wesleey/nest-clean-architecture

---

## 🔄 이 문서에 대해

이 코딩 룰은 **Stack Initializer Agent**가 자동 생성했습니다.

- **검증 필요**: 프로젝트에 맞게 수정 후 `.rules/_verified/`로 이동 가능
- **만료**: 24시간 후 재생성 옵션 제공
- **기여**: 개선 사항을 GitHub에 PR로 제출 가능

---

**Sources**:
- [NestJS Official Documentation](https://docs.nestjs.com/)
- [NestJS Best Practices GitHub](https://github.com/weiwensangsang/nestjs-best-practices)
- [Securing NestJS Apps - Medium](https://medium.com/@febriandwikimhan/securing-nestjs-apps-implementing-key-owasp-protections-8ef60df6ecf8)
- [Best Security Implementation in NestJS](https://dev.to/drbenzene/best-security-implementation-practices-in-nestjs-a-comprehensive-guide-2p88)
- [NestJS Project Structure](https://github.com/CatsMiaow/nestjs-project-structure)
