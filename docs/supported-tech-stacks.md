# 지원 기술 스택 목록

> 멀티 에이전트 시스템이 지원할 프로젝트 타입별 언어 및 프레임워크 목록

---

## 1. Web-Fullstack (FE + BE 분리)

### Backend

#### Python
- **FastAPI** ⭐ (현재 지원 중)
  - 비동기, 타입 힌트, 자동 문서화
  - 사용 사례: RESTful API, 마이크로서비스
- **Flask**
  - 경량, 유연성
  - 사용 사례: 소규모 API, 프로토타입
- **Django REST Framework (DRF)**
  - Django 기반 REST API
  - 사용 사례: 기업용 API, Admin 필요 시

#### Node.js
- **Express.js**
  - 미니멀, 생태계 풍부
  - 사용 사례: RESTful API, 실시간 서버
- **NestJS**
  - TypeScript, Angular 스타일 아키텍처
  - 사용 사례: 엔터프라이즈급 백엔드
- **Fastify**
  - 고성능, 플러그인 아키텍처
  - 사용 사례: 고트래픽 API

#### Go
- **Gin**
  - 고성능 HTTP 프레임워크
  - 사용 사례: 마이크로서비스, API 게이트웨이
- **Echo**
  - 미들웨어 중심, 빠름
  - 사용 사례: RESTful API
- **Fiber**
  - Express 스타일, 제로 메모리 할당
  - 사용 사례: 고성능 API

#### Rust
- **Axum**
  - Tokio 기반, 타입 안전성
  - 사용 사례: 고성능 API, 시스템 프로그래밍
- **Actix-web**
  - Actor 모델, 매우 빠름
  - 사용 사례: 실시간 서비스, 고트래픽 API

#### Java
- **Spring Boot (Webflux)**
  - 비동기 리액티브 프로그래밍
  - 사용 사례: 엔터프라이즈 마이크로서비스

### Frontend

#### React 생태계
- **Next.js** ⭐ (현재 지원 중)
  - SSR, SSG, 파일 기반 라우팅
  - 사용 사례: SEO 중요 웹앱, 대규모 프로젝트
- **Vite + React**
  - 빠른 HMR, 경량
  - 사용 사례: SPA, 대시보드
- **Remix**
  - 중첩 라우팅, 네이티브 폼
  - 사용 사례: 데이터 중심 웹앱

#### Vue 생태계
- **Nuxt.js**
  - SSR, 파일 기반 라우팅
  - 사용 사례: Vue 선호 팀, SEO 필요 시
- **Vite + Vue 3**
  - Composition API, TypeScript
  - 사용 사례: SPA, 관리자 대시보드

#### Svelte 생태계
- **SvelteKit**
  - 컴파일 타임 프레임워크, 경량
  - 사용 사례: 고성능 필요 시, 작은 번들 크기

#### 기타
- **Angular**
  - TypeScript 네이티브, 완전한 프레임워크
  - 사용 사례: 엔터프라이즈 대규모 프로젝트
- **Solid.js**
  - 세밀한 반응성, React 스타일 문법
  - 사용 사례: 고성능 인터랙티브 UI

---

## 2. Web-MVC (Monolithic)

### Python
- **Django** ⭐
  - ORM, Admin, 템플릿 엔진 내장
  - 사용 사례: 콘텐츠 관리, 전통적 웹앱
  - 템플릿: Django Template Language (DTL)

### Ruby
- **Ruby on Rails**
  - Convention over Configuration
  - 사용 사례: 스타트업 MVP, CRUD 웹앱
  - 템플릿: ERB

### Java
- **Spring Boot (MVC)**
  - Thymeleaf, JSP
  - 사용 사례: 엔터프라이즈 웹 애플리케이션
  - 템플릿: Thymeleaf, JSP

### PHP
- **Laravel**
  - Eloquent ORM, Blade 템플릿
  - 사용 사례: CMS, 전통적 웹앱
  - 템플릿: Blade

### C#
- **.NET (ASP.NET Core MVC)**
  - Razor Pages, Entity Framework
  - 사용 사례: 엔터프라이즈 웹앱, Windows 환경
  - 템플릿: Razor

---

## 3. CLI Tool

### Python
- **Click** ⭐
  - 데코레이터 기반, 간단한 구문
  - 사용 사례: 범용 CLI 도구
- **Typer**
  - 타입 힌트 기반, Click 기반
  - 사용 사례: 현대적 Python CLI
- **argparse**
  - 표준 라이브러리
  - 사용 사례: 추가 의존성 없는 CLI

### Go
- **Cobra** ⭐
  - kubectl, docker CLI에서 사용
  - 사용 사례: 복잡한 서브커맨드 구조
- **urfave/cli**
  - 간단한 API
  - 사용 사례: 중소규모 CLI

### Rust
- **clap** ⭐
  - 파생 매크로, 성능 우수
  - 사용 사례: 고성능 CLI, 시스템 도구
- **structopt** (clap v3로 통합)
  - 구조체 기반 인자 파싱
  - 사용 사례: 타입 안전 CLI

### Node.js
- **Commander.js**
  - Express 스타일 API
  - 사용 사례: Node 생태계 CLI
- **yargs**
  - 복잡한 인자 파싱
  - 사용 사례: 다양한 옵션 지원

### Java
- **picocli**
  - 어노테이션 기반
  - 사용 사례: 엔터프라이즈 CLI 도구

---

## 4. Desktop App

### Cross-Platform

#### Electron (JavaScript/TypeScript)
- **Electron + React** ⭐
  - 사용 사례: VS Code, Slack, Discord
  - 장점: 웹 기술 활용, 풍부한 생태계
  - 단점: 무거운 번들 크기
- **Electron + Vue**
  - 사용 사례: Vue 선호 팀
- **Electron + Svelte**
  - 사용 사례: 경량 데스크톱 앱

#### Tauri (Rust + Web)
- **Tauri + React/Vue/Svelte** ⭐
  - 사용 사례: 경량 데스크톱 앱 (Electron 대안)
  - 장점: 작은 번들 크기 (3-5MB), 빠름
  - 단점: Rust 컴파일 환경 필요

#### Flutter (Dart)
- **Flutter Desktop**
  - 사용 사례: 크로스 플랫폼 (모바일 + 데스크톱)
  - 장점: 네이티브 성능, 일관된 UI
  - 단점: 상대적으로 작은 데스크톱 생태계

#### Qt
- **Qt (C++/Python)** ⭐
  - PyQt, PySide6
  - 사용 사례: 전문 도구 (Autodesk, Adobe 일부 툴)
  - 장점: 진정한 네이티브 UI, 성능
  - 단점: 학습 곡선

### Platform-Specific

#### macOS
- **SwiftUI** ⭐
  - Swift 네이티브
  - 사용 사례: macOS 전용 앱
  - 장점: 최고의 macOS 통합
- **AppKit (Objective-C/Swift)**
  - 레거시 macOS 앱
  - 사용 사례: 복잡한 macOS 전용 기능

#### Windows
- **WPF (C#/.NET)** ⭐
  - XAML 기반
  - 사용 사례: Windows 엔터프라이즈 앱
- **WinUI 3 (C#/.NET)**
  - 현대적 Windows UI
  - 사용 사례: Windows 11 네이티브 앱
- **Windows Forms (C#/.NET)**
  - 레거시, 빠른 프로토타이핑
  - 사용 사례: 내부 도구

---

## 5. Mobile App

### Cross-Platform
- **React Native**
  - JavaScript/TypeScript
  - 사용 사례: iOS + Android 동시 개발
- **Flutter**
  - Dart
  - 사용 사례: 네이티브 성능 필요 시
- **Expo (React Native 기반)**
  - 사용 사례: 빠른 프로토타이핑

### Native
- **SwiftUI (iOS)**
  - Swift
  - 사용 사례: iOS 전용 앱
- **Jetpack Compose (Android)**
  - Kotlin
  - 사용 사례: Android 전용 앱

---

## 6. Library / SDK

### JavaScript/TypeScript
- **npm package**
  - 번들러: Rollup, tsup, Vite
  - 사용 사례: React 컴포넌트 라이브러리, 유틸리티

### Python
- **pip package**
  - 빌드 도구: setuptools, poetry, hatch
  - 사용 사례: 데이터 분석 라이브러리, API 클라이언트

### Rust
- **crates.io**
  - Cargo
  - 사용 사례: 시스템 라이브러리, WASM 모듈

### Go
- **Go module**
  - go mod
  - 사용 사례: CLI 라이브러리, 네트워크 유틸리티

### Java
- **Maven/Gradle package**
  - 사용 사례: 엔터프라이즈 유틸리티, Android 라이브러리

---

## 7. Data Pipeline / ETL

### Python
- **Apache Airflow** ⭐
  - DAG 기반 워크플로우
  - 사용 사례: 데이터 파이프라인 오케스트레이션
- **Prefect**
  - 현대적 워크플로우 엔진
  - 사용 사례: 데이터 엔지니어링
- **Luigi**
  - Spotify 개발
  - 사용 사례: 배치 작업 파이프라인

### Scala
- **Apache Spark**
  - 대규모 데이터 처리
  - 사용 사례: 빅데이터 분석

### SQL-based
- **dbt (Data Build Tool)**
  - SQL 기반 변환
  - 사용 사례: 데이터 웨어하우스 모델링

---

## 8. 기타

### Game Development
- **Unity (C#)**
  - 크로스 플랫폼 게임
- **Unreal Engine (C++)**
  - AAA 게임

### WebAssembly
- **Rust (wasm-pack)**
  - 브라우저 고성능 연산
- **AssemblyScript**
  - TypeScript 스타일 WASM

### Embedded / IoT
- **Rust (embedded-hal)**
  - 임베디드 시스템
- **C/C++ (Arduino, ESP32)**
  - IoT 디바이스

---

## 우선순위 (1차 지원 목표)

현실적으로 모든 스택을 지원하기는 어려우므로, 사용 빈도와 수요를 고려한 우선순위:

### Tier 1 (즉시 지원)
1. **Web-Fullstack**
   - BE: FastAPI (Python) ✅ 기존 지원
   - FE: Next.js (React) ✅ 기존 지원
   - BE: Express.js (Node.js) 🆕
   - BE: NestJS (Node.js) 🆕

2. **Web-MVC**
   - Django (Python) 🆕
   - Spring Boot MVC (Java) 🆕

3. **CLI Tool**
   - Click (Python) 🆕
   - Cobra (Go) 🆕

### Tier 2 (다음 단계)
4. **Desktop App**
   - Tauri + React 🆕
   - Electron + React 🆕

5. **Library**
   - npm package (TypeScript) 🆕
   - pip package (Python) 🆕

### Tier 3 (수요 확인 후)
6. **Mobile App**
   - React Native 🆕
   - Flutter 🆕

7. **Data Pipeline**
   - Airflow 🆕

---

## 다음 단계

각 기술 스택별로 작성해야 할 문서:

1. **코딩 룰** (`.rules/{카테고리}/{스택}.md`)
   - 디렉토리 구조
   - 아키텍처 패턴
   - 네이밍 컨벤션
   - 보안 가이드
   - 테스팅 전략

2. **PM 템플릿** (`.agents/pm/templates/{타입}.md`)
   - 산출물 형식
   - 명세서 템플릿

3. **코딩 에이전트 템플릿** (`.agents/coding/templates/{타입}.md`)
   - 작업 순서
   - 파일 생성 순서
   - 의존성 관리

4. **QA 템플릿** (`.agents/qa/templates/{타입}.md`)
   - 테스트 프레임워크
   - 테스트 구조
   - 커버리지 목표

---

**작성 일시**: 2026-03-12
**버전**: v1.0.0-draft
