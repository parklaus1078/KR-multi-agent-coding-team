# Qt (C++) 코딩 룰

> 자동 생성: 2026-03-13 00:00:00
> 프레임워크 버전: Qt 6.x (latest)
> 상태: 🤖 자동 생성됨

---

## 1. 프로젝트 구조

```
project-root/
├── CMakeLists.txt              # 주요 빌드 설정
├── .gitignore                  # 버전 관리 제외 파일
├── README.md                   # 프로젝트 문서
├── src/                        # 소스 코드
│   ├── main.cpp               # 애플리케이션 진입점
│   ├── models/                # 데이터 모델 (MVC/MVVM의 M)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── views/                 # UI 컴포넌트 (MVC/MVVM의 V)
│   │   ├── CMakeLists.txt
│   │   ├── *.h, *.cpp
│   │   └── *.ui               # Qt Designer 폼
│   ├── controllers/           # 비즈니스 로직 (MVC의 C)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── delegates/             # 커스텀 아이템 델리게이트
│   │   └── *.h, *.cpp
│   ├── utils/                 # 유틸리티 클래스
│   │   └── *.h, *.cpp
│   └── resources/             # Qt 리소스
│       ├── qml/              # QML 파일 (Qt Quick 사용 시)
│       ├── images/           # 이미지 자산
│       └── resources.qrc     # Qt 리소스 파일
├── include/                   # 공개 헤더 (라이브러리용)
│   └── projectname/
│       └── *.h
├── tests/                     # 테스트 코드
│   ├── CMakeLists.txt
│   ├── unit/                 # 단위 테스트
│   │   └── tst_*.cpp
│   └── integration/          # 통합 테스트
│       └── tst_*.cpp
├── docs/                      # 문서
│   └── *.md
└── build/                     # 빌드 출력 (git-ignored)
```

### 디렉토리 역할

- **src/models/**: 복잡한 데이터를 위한 QAbstractItemModel, QAbstractListModel, QAbstractTableModel 구현
- **src/views/**: QWidget, QMainWindow, QDialog 서브클래스 및 .ui 파일
- **src/controllers/**: 모델과 뷰를 조정하는 비즈니스 로직
- **src/delegates/**: 커스텀 렌더링/편집을 위한 QStyledItemDelegate 서브클래스
- **src/utils/**: 헬퍼 클래스, 상수, 타입 정의
- **tests/**: tst_ 접두사를 가진 QTest 기반 테스트 케이스

---

## 2. 아키텍처 패턴

### Model/View/Delegate (Qt의 MVC 변형)

Qt는 데이터 관리와 프레젠테이션을 분리하는 수정된 Model-View-Controller 패턴을 사용합니다:

**Model**: QAbstractItemModel 인터페이스를 통해 데이터를 관리합니다. 데이터를 직접 저장하지 않고 기본 소스(데이터베이스, 파일, 메모리)에 대한 액세스를 제공합니다. 단순한 구조의 경우 QAbstractListModel 또는 QAbstractTableModel을 사용하세요.

**View**: QListView, QTableView, QTreeView 또는 커스텀 뷰를 사용하여 모델 데이터를 표시합니다. 여러 뷰가 동시에 동일한 모델을 표시할 수 있습니다.

**Delegate**: QStyledItemDelegate를 통해 아이템 렌더링 및 편집을 처리합니다. 외관과 사용자 상호작용을 커스터마이즈합니다.

### Model/View vs. 편의 클래스 사용 시기

- **Model/View**: 복잡한 데이터, 다중 뷰, 커스텀 렌더링, 대용량 데이터셋, 데이터베이스 기반 데이터에 사용
- **편의 클래스** (QListWidget, QTableWidget, QTreeWidget): 유연성이 덜 중요한 간단하고 정적인 목록에 사용

### MVVM 패턴 (Qt Quick/QML 사용 시)

QML 애플리케이션의 경우 다음과 같은 Model-View-ViewModel을 사용합니다:
- **Model**: C++ 데이터 모델 (QAbstractItemModel)
- **View**: QML 시각적 컴포넌트
- **ViewModel**: Q_PROPERTY 및 시그널을 통해 QML에 노출되는 C++ 클래스

---

## 3. 네이밍 컨벤션

### 파일명

- **C++ 소스/헤더**: 소문자 + 언더스코어 (예: `main_window.cpp`, `main_window.h`)
- **UI 파일**: 해당 클래스와 일치 (예: `main_window.ui`)
- **QML 파일**: UpperCamelCase (예: `MainWindow.qml`)
- **테스트 파일**: `tst_` 접두사 (예: `tst_main_window.cpp`)

### 클래스

- 클래스는 대문자로 시작: `MainWindow`, `UserModel`
- 공개 Qt 클래스는 `Q` 접두사: `QRgb`, `QString` (Qt 프레임워크 클래스만)
- 약어는 카멜케이스: `QXmlStreamReader` (`QXMLStreamReader` 아님)

### 변수 및 함수

- 소문자로 시작, 후속 단어는 대문자: `userName`, `calculateTotal()`
- 널리 알려진 용어를 제외하고 약어 피하기 (`id`, `url`)
- 루프 카운터를 제외하고 단일 문자 이름 피하기 (`i`, `j`, `k`)
- 각 변수를 별도 줄에 선언

### 멤버 변수

- 프라이빗 멤버는 접두사 규칙 사용 가능 (프로젝트별): `m_userName` 또는 `_userName`
- Qt 스타일에서 특별한 접두사 필요 없음, 하지만 일관성이 중요

### 상수 및 열거형

- 상수: 모두 대문자 + 언더스코어: `MAX_BUFFER_SIZE`
- 열거형 이름: UpperCamelCase: `enum ConnectionState { ... }`
- 열거형 값: UpperCamelCase: `Connected`, `Disconnected`

---

## 4. 코딩 스타일

### 언어별 스타일 가이드

- **C++ 표준**: 모던 C++ (Qt 6에서 C++17 이상 권장)
- **Qt 스타일 가이드**: [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- **Qt 코딩 규칙**: [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)

### 들여쓰기 및 포맷팅

- **들여쓰기**: 4칸 공백 (탭 아님)
- **줄 길이**: 최대 100자; 주석은 80자 이하
- **빈 줄**: 구분을 위해 한 줄만 사용

### 중괄호

- 제어 구조는 같은 줄에 여는 중괄호:
  ```cpp
  if (condition) {
      // code
  }
  ```
- 함수와 클래스는 새 줄에 여는 중괄호:
  ```cpp
  void MyClass::myFunction()
  {
      // code
  }
  ```
- 빈 본문에는 중괄호 사용: `while (a) {}`
- 단일 줄 본문은 다중 분기 구조의 일부가 아니면 중괄호 생략 가능

### 공백

- 흐름 제어 키워드 뒤 한 칸: `if (`, `while (`, `for (`
- 여는 중괄호 앞 한 칸
- 포인터/참조: `Type *variable` 또는 `Type &variable` (타입 뒤 공백)
- 이진 연산자: 공백으로 둘러싸기: `a + b`, `x == y`
- 캐스트 연산자 뒤 공백 없음

### 헤더

- Include 가드: `#pragma once` 또는 전통적 가드 사용
- Include 순서:
  1. 해당 헤더 (.cpp 파일용)
  2. Qt 헤더: `#include <QtCore/qstring.h>` 또는 `#include <QString>`
  3. 기타 라이브러리 헤더
  4. 프로젝트 헤더
- 공개 헤더에서는 전체 형식 사용: `#include <QtCore/qobject.h>`

### Qt 전용 베스트 프랙티스

- 모든 QObject 서브클래스는 `Q_OBJECT` 매크로 필요
- STL보다 Qt 호환 타입용 Qt 컨테이너 선호
- 직접 콜백 대신 Qt 시그널/슬롯 메커니즘 사용
- Qt의 메타-객체 시스템 사용: `Q_PROPERTY`, `Q_ENUM`, `Q_INVOKABLE`
- RTTI (dynamic_cast) 피하기; qobject_cast 사용

---

## 5. 의존성 관리

### 패키지 매니저

- **vcpkg**: 크로스 플랫폼 C++ 패키지 매니저 (권장)
- **Conan**: 대체 C++ 패키지 매니저
- **시스템 패키지 매니저**: apt, brew, pacman (개발용)

### CMake 설정

**CMakeLists.txt** (Qt 6의 주요 빌드 시스템):

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt 설정
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)

# 실행 파일 추가
add_executable(${PROJECT_NAME}
    src/main.cpp
    # ... 기타 소스
)

target_link_libraries(${PROJECT_NAME}
    Qt6::Core
    Qt6::Widgets
    Qt6::Gui
)
```

### Qt 모듈

일반적인 Qt 모듈:
- **Core**: 기반 (QObject, QString, 컨테이너)
- **Gui**: GUI 컴포넌트 (QImage, QFont, 이벤트)
- **Widgets**: 전통적인 데스크톱 위젯
- **Quick**: 모던 UI용 QML/Qt Quick
- **Network**: 네트워킹 (QNetworkAccessManager)
- **Sql**: 데이터베이스 액세스
- **Test**: 테스팅 프레임워크

의존성을 최소화하기 위해 필요한 모듈만 추가하세요.

---

## 6. 환경 설정

### 환경 변수

- **Qt 설치**: `Qt6_DIR` 설정 또는 `CMAKE_PREFIX_PATH`에 추가
- **애플리케이션 설정**: 영구 설정용 QSettings 사용
- **개발**: 빌드 설정용 `.env` 또는 CMake 캐시 변수 사용

### 설정 파일

```cpp
// 설정 읽기
QSettings settings("MyCompany", "MyApp");
QString dbPath = settings.value("database/path", "default.db").toString();

// 설정 쓰기
settings.setValue("database/path", "/path/to/db");
```

### 플랫폼별 설정

- **Windows**: 레지스트리 (`HKEY_CURRENT_USER\Software\MyCompany\MyApp`)
- **macOS**: plist 파일 (`~/Library/Preferences/com.mycompany.myapp.plist`)
- **Linux**: INI 파일 (`~/.config/MyCompany/MyApp.conf`)

---

## 7. 보안 가이드

### 입력 검증

- **사용자 입력**: 항상 검증 및 정제
  ```cpp
  QString sanitized = userInput.simplified(); // 여분의 공백 제거
  if (!validateInput(sanitized)) {
      qWarning() << "잘못된 입력 수신됨";
      return;
  }
  ```
- **파일 경로**: QFileInfo를 사용하여 정규화 및 검증
- **네트워크 데이터**: 네트워크 소스의 모든 데이터 검증

### SQL 인젝션 방지

Qt SQL에서 파라미터화된 쿼리 사용:

```cpp
// 올바름: 파라미터화된 쿼리
QSqlQuery query;
query.prepare("SELECT * FROM users WHERE username = :username");
query.bindValue(":username", userName);
query.exec();

// 잘못됨: 문자열 연결
// query.exec("SELECT * FROM users WHERE username = '" + userName + "'");
```

### 메모리 안전성

- **RAII**: 스마트 포인터 또는 Qt 부모-자식 소유권 사용
  ```cpp
  QWidget *widget = new QWidget(parent); // 부모 소멸 시 자동 삭제
  ```
- **버퍼 오버플로**: 원시 C 문자열 피하기; QString 및 QByteArray 사용
- **배열 액세스**: Qt 컨테이너는 디버그 모드에서 경계 검사 수행

### 시크릿 관리

- **비밀번호**: 평문 비밀번호 절대 저장 금지
- **API 키**: 암호화된 QSettings 또는 플랫폼 키체인 사용
  - macOS: Keychain Services
  - Windows: Credential Manager (DPAPI)
  - Linux: libsecret/KWallet
- **암호화**: 해싱용 QCryptographicHash, 암호화용 OpenSSL 사용

### 코드 서명 (배포)

- **macOS**: Apple Developer ID로 코드 서명
- **Windows**: authenticode 인증서로 서명
- **Linux**: 패키지 서명은 배포판마다 다름

### 보안 표준 준수

- **OWASP 보안 코딩 관행**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- **MISRA C++**: 안전 중요 애플리케이션용
- **SEI CERT C++ 코딩 표준**: https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682

---

## 8. 에러 핸들링

### 예외 처리

Qt는 일반적으로 **예외를 피합니다**:
- Qt 클래스는 예외를 던지지 않음
- 에러 코드 반환 또는 시그널 사용하여 에러 표시
- 코드에서 예외를 사용하는 경우 적절한 RAII 정리 보장

### 에러 보고

```cpp
// 반환 값 확인
QFile file("data.txt");
if (!file.open(QIODevice::ReadOnly)) {
    qWarning() << "파일 열기 실패:" << file.errorString();
    return false;
}

// 사용자 대상 에러용 QMessageBox 사용
QMessageBox::critical(this, "에러", "파일 저장 실패");
```

### 로깅

**Qt 로깅 카테고리**:

```cpp
// 로깅 카테고리 정의
Q_LOGGING_CATEGORY(lcMyApp, "myapp.main")

// 코드에서 사용
qCDebug(lcMyApp) << "디버그 메시지";
qCInfo(lcMyApp) << "정보 메시지";
qCWarning(lcMyApp) << "경고 메시지";
qCCritical(lcMyApp) << "중요 에러";
```

**로그 레벨**:
- **qDebug()**: 디버그 정보 (기본적으로 릴리스 빌드에서 제거됨)
- **qInfo()**: 정보성 메시지
- **qWarning()**: 실행을 중단하지 않는 경고
- **qCritical()**: 중요 에러
- **qFatal()**: 치명적 에러 (애플리케이션 종료)

**설정**:
로깅 제어용 `qtlogging.ini` 생성:
```ini
[Rules]
myapp.*.debug=true
qt.*.debug=false
```

---

## 9. 테스팅 전략

### 테스트 프레임워크

**QTest**: Qt 공식 단위 테스팅 프레임워크

### 테스트 구조

```
tests/
├── CMakeLists.txt
├── unit/
│   ├── tst_mymodel.cpp
│   └── tst_mycontroller.cpp
└── integration/
    └── tst_database.cpp
```

### 단위 테스트 예시

```cpp
#include <QtTest/QtTest>
#include "mymodel.h"

class TestMyModel : public QObject
{
    Q_OBJECT

private slots:
    void initTestCase();    // 첫 테스트 전 호출
    void cleanupTestCase(); // 마지막 테스트 후 호출
    void init();            // 각 테스트 전 호출
    void cleanup();         // 각 테스트 후 호출

    void testAddItem();
    void testRemoveItem();
};

void TestMyModel::testAddItem()
{
    MyModel model;
    model.addItem("Test");
    QCOMPARE(model.rowCount(), 1);
    QVERIFY(model.data(model.index(0, 0)).toString() == "Test");
}

QTEST_MAIN(TestMyModel)
#include "tst_mymodel.moc"
```

### 테스팅 베스트 프랙티스

- **하드코딩된 타임아웃 피하기**: `QTest::qWait()` 대신 `QTRY_VERIFY()`, `QTRY_COMPARE()`, `QSignalSpy` 사용
- **QVERIFY2 사용**: 에러 메시지 제공: `QVERIFY2(condition, "에러 메시지")`
- **상태 복원**: 테스트 간 영향 방지; cleanup() 또는 RAII 사용
- **헤드리스 테스팅**: CI/CD에서 GUI 테스트용 `-platform offscreen` 사용
- **스택 할당**: 자동 정리를 위해 스택에 테스트 객체 인스턴스화

### GUI 테스팅

```cpp
void TestMainWindow::testButtonClick()
{
    MainWindow window;
    QTest::mouseClick(window.submitButton(), Qt::LeftButton);
    QCOMPARE(window.status(), MainWindow::Submitted);
}
```

### 시그널/슬롯 테스팅

```cpp
void TestMyClass::testSignalEmitted()
{
    MyClass obj;
    QSignalSpy spy(&obj, &MyClass::dataChanged);

    obj.updateData();

    QCOMPARE(spy.count(), 1);
    QList<QVariant> arguments = spy.takeFirst();
    QVERIFY(arguments.at(0).toInt() == 42);
}
```

### 커버리지 목표

- **목표**: 비즈니스 로직의 70-80% 코드 커버리지
- **중요 경로**: 보안 중요 코드의 100% 커버리지
- **UI 코드**: 로직 테스팅에 집중; 시각적 테스팅은 수동 QA 필요할 수 있음

### 테스트 실행

```bash
# 모든 테스트 실행
ctest --output-on-failure

# 특정 테스트 실행
./tests/unit/tst_mymodel

# 상세 출력
./tests/unit/tst_mymodel -v2
```

---

## 10. 성능 최적화

### Qt 전용 최적화

**암시적 공유**: Qt 컨테이너는 copy-on-write 사용
```cpp
QString a = "Hello";
QString b = a;  // 데이터 공유, 수정 전까지 깊은 복사 없음
```

**용량 예약**: 알려진 크기에 대해 미리 할당
```cpp
QVector<int> vec;
vec.reserve(1000);  // 재할당 방지
```

**Const 정확성**: const 반복자 및 참조 사용
```cpp
for (const QString &str : stringList) {  // 분리 방지
    // 읽기 전용 액세스
}
```

**Model/View 최적화**:
- 지연 로딩용 `canFetchMore()` 및 `fetchMore()` 구현
- 최소 업데이트용 `QAbstractItemModel::dataChanged()` 사용
- `rowCount()` 및 `columnCount()` 효율적으로 오버라이드

**시그널/슬롯**:
- 블로킹 방지용 `Qt::QueuedConnection` 사용
- 중복 연결 방지용 `Qt::UniqueConnection` 사용
- 더 이상 필요하지 않을 때 슬롯 연결 해제

**QString 연산**:
- 여러 연결 대신 `QString::arg()` 사용
- `QStringBuilder` 사용 (`QT_USE_QSTRINGBUILDER` 정의)

**데이터베이스**:
- 준비된 문 사용 (더 빠름 + 보안)
- 트랜잭션으로 작업 일괄 처리
- 쿼리에 적절한 fetch 크기 사용

---

## 11. 문서화

### 코드 주석

**헤더 문서**:
```cpp
/**
 * @brief 사용자 데이터 및 인증 관리
 *
 * UserModel은 사용자 정보 액세스를 제공하고
 * 인증 로직을 처리합니다. 테이블 뷰에 표시하기 위해
 * QAbstractTableModel을 구현합니다.
 *
 * @see QAbstractTableModel
 */
class UserModel : public QAbstractTableModel
{
    // ...
};
```

**함수 문서**:
```cpp
/**
 * @brief 사용자명과 비밀번호로 사용자 인증
 * @param username 사용자의 사용자명
 * @param password 사용자의 비밀번호 (해시됨)
 * @return 인증 성공 시 true, 실패 시 false
 */
bool authenticate(const QString &username, const QString &password);
```

**인라인 주석**:
- "무엇"이 아닌 "왜"를 설명
- 한 줄은 `//`, 여러 줄은 `/* */` 사용
- 주석을 간결하고 최신 상태로 유지

### Qt 문서 형식

Qt는 문서 생성용 **QDoc**을 사용합니다. 특수 명령 사용:
- `\brief`: 간단한 설명
- `\param`: 파라미터 설명
- `\return`: 반환 값 설명
- `\sa`: 참조 (교차 참조)
- `\note`: 중요 참고사항
- `\warning`: 경고

### README.md 필수 섹션

```markdown
# 프로젝트 이름

## 설명
애플리케이션에 대한 간단한 설명

## 기능
- 기능 1
- 기능 2

## 요구사항
- Qt 6.x
- CMake 3.16+
- C++17 컴파일러

## 빌드
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## 실행
```bash
./MyApp
```

## 테스팅
```bash
ctest --output-on-failure
```

## 라이선스
[라이선스 타입]

## 기여
기여자용 가이드라인
```

---

## 12. 금지 사항

### 프레임워크 안티패턴

- **소유권 추적 없이 원시 포인터 사용 금지**: Qt 부모-자식 또는 스마트 포인터 사용
- **Q_OBJECT 매크로 빠뜨리지 않기**: QObject 서브클래스의 시그널/슬롯에 필요
- **QObject에 dynamic_cast 사용 금지**: `qobject_cast` 사용
- **Qt 부모가 있는 객체 수동 삭제 금지**: 부모가 삭제 처리
- **이벤트 루프 블로킹 금지**: 무거운 작업용 `QThread` 또는 `QtConcurrent` 사용

### 보안 취약점

- **SQL 인젝션**: 사용자 입력으로 SQL 쿼리 연결 금지
- **경로 순회**: 파일 경로 검증, 정규 경로 사용
- **버퍼 오버플로**: 원시 C 문자열 피하기, Qt 컨테이너 사용
- **하드코딩된 자격증명**: 비밀번호 또는 API 키 커밋 금지
- **검증되지 않은 입력**: 항상 사용자 및 네트워크 입력 정제

### 성능 이슈

- **공유 컨테이너 분리**: 루프에서 암시적으로 공유된 객체의 비const 연산 피하기
- **과도한 시그널 방출**: 업데이트 일괄 처리, blockSignals() 신중하게 사용
- **동기 네트워크 호출**: 비동기 Qt Network API 사용
- **빈번한 문자열 연결**: `QString::arg()` 또는 QStringBuilder 사용

### 빌드/배포

- **빌드 아티팩트 커밋 금지**: `build/`, `*.o`, `*.exe`, `moc_*`, `ui_*`를 .gitignore에 추가
- **경로 하드코딩 금지**: 시스템 디렉토리용 QStandardPaths 사용
- **테스팅 건너뛰기 금지**: 릴리스 전 항상 테스트 실행

---

## 13. 참고 자료

### 공식 문서
- [Qt 문서](https://doc.qt.io/)
- [Qt 코딩 스타일](https://wiki.qt.io/Qt_Coding_Style)
- [Qt 코딩 규칙](https://wiki.qt.io/Coding_Conventions)
- [Qt 테스트 베스트 프랙티스](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Model/View 프로그래밍](https://doc.qt.io/qt-6/model-view-programming.html)
- [Qt 보안](https://doc.qt.io/qt-6/security.html)

### 베스트 프랙티스
- [Clean Qt 블로그](https://cleanqt.io/)
- [Qt 앱에서 높은 사이버 보안 보장 방법](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [OWASP 보안 코딩 관행](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [상위 10가지 안전한 C++ 코딩 관행](https://www.incredibuild.com/blog/top-10-secure-c-coding-practices)

### 예시 프로젝트
- [Qt 예시 및 튜토리얼](https://doc.qt.io/qt-6/qtexamplesandtutorials.html)
- [Qt Creator 소스 코드](https://code.qt.io/cgit/qt-creator/qt-creator.git/)

---

## 🔄 이 문서에 대해

이 코딩 룰은 **Stack Initializer Agent**가 자동 생성했습니다.

- **검증 필요**: 프로젝트별 수정 후 `.rules/_verified/`로 이동 가능
- **만료**: 24시간 후 재생성 옵션 제공
- **기여**: 개선 제안을 GitHub에 PR로 제출 가능

---

## 출처

이 문서의 연구는 다음에서 수집되었습니다:
- [Qt 코딩 스타일](https://wiki.qt.io/Qt_Coding_Style)
- [Qt 코딩 규칙](https://wiki.qt.io/Coding_Conventions)
- [Model/View 프로그래밍 | Qt 6.10.2](https://doc.qt.io/qt-6/model-view-programming.html)
- [Qt 테스트 베스트 프랙티스 | Qt 6.10.2](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Clean Qt 블로그](https://cleanqt.io/)
- [Qt 앱에서 높은 사이버 보안 보장 방법](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [Qt 보안 | Qt 6.10](https://doc.qt.io/qt-6/security.html)
- [OWASP 보안 코딩 관행](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
