# Qt (C++) Coding Rules

> Auto-generated: 2026-03-13 00:00:00
> Framework Version: Qt 6.x (latest)
> Status: 🤖 Auto-Generated

---

## 1. Project Structure

```
project-root/
├── CMakeLists.txt              # Primary build configuration
├── .gitignore                  # Version control exclusions
├── README.md                   # Project documentation
├── src/                        # Source code
│   ├── main.cpp               # Application entry point
│   ├── models/                # Data models (M in MVC/MVVM)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── views/                 # UI components (V in MVC/MVVM)
│   │   ├── CMakeLists.txt
│   │   ├── *.h, *.cpp
│   │   └── *.ui               # Qt Designer forms
│   ├── controllers/           # Business logic (C in MVC)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── delegates/             # Custom item delegates
│   │   └── *.h, *.cpp
│   ├── utils/                 # Utility classes
│   │   └── *.h, *.cpp
│   └── resources/             # Qt resources
│       ├── qml/              # QML files (if using Qt Quick)
│       ├── images/           # Image assets
│       └── resources.qrc     # Qt resource file
├── include/                   # Public headers (for libraries)
│   └── projectname/
│       └── *.h
├── tests/                     # Test code
│   ├── CMakeLists.txt
│   ├── unit/                 # Unit tests
│   │   └── tst_*.cpp
│   └── integration/          # Integration tests
│       └── tst_*.cpp
├── docs/                      # Documentation
│   └── *.md
└── build/                     # Build output (git-ignored)
```

### Directory Roles

- **src/models/**: Data structures implementing QAbstractItemModel, QAbstractListModel, or QAbstractTableModel for complex data
- **src/views/**: QWidget, QMainWindow, QDialog subclasses and .ui files
- **src/controllers/**: Business logic coordinating models and views
- **src/delegates/**: QStyledItemDelegate subclasses for custom rendering/editing
- **src/utils/**: Helper classes, constants, type definitions
- **tests/**: QTest-based test cases with tst_ prefix

---

## 2. Architecture Pattern

### Model/View/Delegate (Qt's MVC Variant)

Qt uses a modified Model-View-Controller pattern that separates data management from presentation:

**Model**: Manages data through QAbstractItemModel interface. Does not store data directly but provides access to underlying sources (databases, files, memory). Use QAbstractListModel or QAbstractTableModel for simpler structures.

**View**: Displays model data using QListView, QTableView, QTreeView, or custom views. Multiple views can display the same model simultaneously.

**Delegate**: Handles item rendering and editing via QStyledItemDelegate. Customizes appearance and user interaction.

### When to Use Model/View vs. Convenience Classes

- **Model/View**: Use for complex data, multiple views, custom rendering, large datasets, or database-backed data
- **Convenience Classes** (QListWidget, QTableWidget, QTreeWidget): Use for simple, static lists where flexibility is less important

### MVVM Pattern (with Qt Quick/QML)

For QML applications, use Model-View-ViewModel where:
- **Model**: C++ data models (QAbstractItemModel)
- **View**: QML visual components
- **ViewModel**: C++ classes exposed to QML via Q_PROPERTY and signals

---

## 3. Naming Conventions

### File Names

- **C++ Source/Header**: lowercase with underscores (e.g., `main_window.cpp`, `main_window.h`)
- **UI Files**: match corresponding class (e.g., `main_window.ui`)
- **QML Files**: UpperCamelCase (e.g., `MainWindow.qml`)
- **Test Files**: prefix with `tst_` (e.g., `tst_main_window.cpp`)

### Classes

- Classes start with uppercase letter: `MainWindow`, `UserModel`
- Public Qt classes prefix with `Q`: `QRgb`, `QString` (Qt framework classes only)
- Acronyms are camel-cased: `QXmlStreamReader` (not `QXMLStreamReader`)

### Variables and Functions

- Start with lowercase letter, subsequent words capitalized: `userName`, `calculateTotal()`
- Avoid abbreviations except for widely known terms (`id`, `url`)
- Avoid single-character names except loop counters (`i`, `j`, `k`)
- Declare each variable on separate line

### Member Variables

- Private members may use prefix convention (project-specific): `m_userName` or `_userName`
- No special prefix required by Qt style, but consistency is important

### Constants and Enums

- Constants: all uppercase with underscores: `MAX_BUFFER_SIZE`
- Enum names: UpperCamelCase: `enum ConnectionState { ... }`
- Enum values: UpperCamelCase: `Connected`, `Disconnected`

---

## 4. Coding Style

### Language-Specific Style Guide

- **C++ Standard**: Modern C++ (C++17 or later recommended with Qt 6)
- **Qt Style Guide**: [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- **Qt Coding Conventions**: [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)

### Indentation and Formatting

- **Indentation**: 4 spaces (not tabs)
- **Line Length**: Maximum 100 characters; comments under 80 characters
- **Blank Lines**: Use only one blank line for separation

### Braces

- Opening brace on same line for control structures:
  ```cpp
  if (condition) {
      // code
  }
  ```
- Opening brace on new line for functions and classes:
  ```cpp
  void MyClass::myFunction()
  {
      // code
  }
  ```
- Use braces for empty bodies: `while (a) {}`
- Single-line bodies may omit braces unless part of multi-branch structure

### Spacing

- Single space after flow-control keywords: `if (`, `while (`, `for (`
- Single space before opening brace
- Pointers/references: `Type *variable` or `Type &variable` (space after type)
- Binary operators: surround with spaces: `a + b`, `x == y`
- No space after cast operators

### Headers

- Include guards: Use `#pragma once` or traditional guards
- Include order:
  1. Corresponding header (for .cpp files)
  2. Qt headers: `#include <QtCore/qstring.h>` or `#include <QString>`
  3. Other library headers
  4. Project headers
- In public headers, use full form: `#include <QtCore/qobject.h>`

### Qt-Specific Best Practices

- Every QObject subclass must have `Q_OBJECT` macro
- Prefer Qt containers over STL for Qt-compatible types
- Use Qt signal/slot mechanism, avoid direct callbacks
- Use Qt's meta-object system: `Q_PROPERTY`, `Q_ENUM`, `Q_INVOKABLE`
- Avoid RTTI (dynamic_cast); use qobject_cast instead

---

## 5. Dependency Management

### Package Manager

- **vcpkg**: Cross-platform C++ package manager (recommended)
- **Conan**: Alternative C++ package manager
- **System package managers**: apt, brew, pacman (for development)

### CMake Configuration

**CMakeLists.txt** (primary build system for Qt 6):

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt configuration
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)

# Add executable
add_executable(${PROJECT_NAME}
    src/main.cpp
    # ... other sources
)

target_link_libraries(${PROJECT_NAME}
    Qt6::Core
    Qt6::Widgets
    Qt6::Gui
)
```

### Qt Modules

Common Qt modules:
- **Core**: Foundation (QObject, QString, containers)
- **Gui**: GUI components (QImage, QFont, events)
- **Widgets**: Traditional desktop widgets
- **Quick**: QML/Qt Quick for modern UIs
- **Network**: Networking (QNetworkAccessManager)
- **Sql**: Database access
- **Test**: Testing framework

Add only required modules to minimize dependencies.

---

## 6. Environment Configuration

### Environment Variables

- **Qt Installation**: Set `Qt6_DIR` or add to `CMAKE_PREFIX_PATH`
- **Application Settings**: Use QSettings for persistent configuration
- **Development**: Use `.env` or CMake cache variables for build configuration

### Configuration Files

```cpp
// Read settings
QSettings settings("MyCompany", "MyApp");
QString dbPath = settings.value("database/path", "default.db").toString();

// Write settings
settings.setValue("database/path", "/path/to/db");
```

### Platform-Specific Settings

- **Windows**: Registry (`HKEY_CURRENT_USER\Software\MyCompany\MyApp`)
- **macOS**: plist files (`~/Library/Preferences/com.mycompany.myapp.plist`)
- **Linux**: INI files (`~/.config/MyCompany/MyApp.conf`)

---

## 7. Security Guide

### Input Validation

- **User Input**: Always validate and sanitize
  ```cpp
  QString sanitized = userInput.simplified(); // Remove extra whitespace
  if (!validateInput(sanitized)) {
      qWarning() << "Invalid input received";
      return;
  }
  ```
- **File Paths**: Use QFileInfo to canonicalize and validate paths
- **Network Data**: Validate all data from network sources

### SQL Injection Prevention

Use parameterized queries with Qt SQL:

```cpp
// CORRECT: Parameterized query
QSqlQuery query;
query.prepare("SELECT * FROM users WHERE username = :username");
query.bindValue(":username", userName);
query.exec();

// WRONG: String concatenation
// query.exec("SELECT * FROM users WHERE username = '" + userName + "'");
```

### Memory Safety

- **RAII**: Use smart pointers or Qt parent-child ownership
  ```cpp
  QWidget *widget = new QWidget(parent); // Auto-deleted when parent destroyed
  ```
- **Buffer Overflows**: Avoid raw C strings; use QString and QByteArray
- **Array Access**: Qt containers perform bounds checking in debug mode

### Secrets Management

- **Passwords**: Never store plaintext passwords
- **API Keys**: Use QSettings with encryption or platform keychain
  - macOS: Keychain Services
  - Windows: Credential Manager (DPAPI)
  - Linux: libsecret/KWallet
- **Encryption**: Use QCryptographicHash for hashing, OpenSSL for encryption

### Code Signing (Distribution)

- **macOS**: Code sign with Apple Developer ID
- **Windows**: Sign with authenticode certificate
- **Linux**: Package signing varies by distribution

### Follow Security Standards

- **OWASP Secure Coding Practices**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- **MISRA C++**: For safety-critical applications
- **SEI CERT C++ Coding Standard**: https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682

---

## 8. Error Handling

### Exception Handling

Qt generally **avoids exceptions**:
- Qt classes do not throw exceptions
- Return error codes or use signals to indicate errors
- If using exceptions in your code, ensure proper RAII cleanup

### Error Reporting

```cpp
// Check return values
QFile file("data.txt");
if (!file.open(QIODevice::ReadOnly)) {
    qWarning() << "Failed to open file:" << file.errorString();
    return false;
}

// Use QMessageBox for user-facing errors
QMessageBox::critical(this, "Error", "Failed to save file");
```

### Logging

**Qt Logging Categories**:

```cpp
// Define logging category
Q_LOGGING_CATEGORY(lcMyApp, "myapp.main")

// Use in code
qCDebug(lcMyApp) << "Debug message";
qCInfo(lcMyApp) << "Info message";
qCWarning(lcMyApp) << "Warning message";
qCCritical(lcMyApp) << "Critical error";
```

**Log Levels**:
- **qDebug()**: Debug information (stripped in release builds by default)
- **qInfo()**: Informational messages
- **qWarning()**: Warnings that don't stop execution
- **qCritical()**: Critical errors
- **qFatal()**: Fatal errors (terminates application)

**Configuration**:
Create `qtlogging.ini` to control logging:
```ini
[Rules]
myapp.*.debug=true
qt.*.debug=false
```

---

## 9. Testing Strategy

### Test Framework

**QTest**: Qt's official unit testing framework

### Test Structure

```
tests/
├── CMakeLists.txt
├── unit/
│   ├── tst_mymodel.cpp
│   └── tst_mycontroller.cpp
└── integration/
    └── tst_database.cpp
```

### Unit Test Example

```cpp
#include <QtTest/QtTest>
#include "mymodel.h"

class TestMyModel : public QObject
{
    Q_OBJECT

private slots:
    void initTestCase();    // Called before first test
    void cleanupTestCase(); // Called after last test
    void init();            // Called before each test
    void cleanup();         // Called after each test

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

### Testing Best Practices

- **Avoid hard-coded timeouts**: Use `QTRY_VERIFY()`, `QTRY_COMPARE()`, or `QSignalSpy` instead of `QTest::qWait()`
- **Use QVERIFY2**: Provides error messages: `QVERIFY2(condition, "Error message")`
- **State restoration**: Ensure tests don't affect each other; use cleanup() or RAII
- **Headless testing**: Use `-platform offscreen` for GUI tests in CI/CD
- **Stack allocation**: Instantiate test objects on stack for automatic cleanup

### GUI Testing

```cpp
void TestMainWindow::testButtonClick()
{
    MainWindow window;
    QTest::mouseClick(window.submitButton(), Qt::LeftButton);
    QCOMPARE(window.status(), MainWindow::Submitted);
}
```

### Signal/Slot Testing

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

### Coverage Goals

- **Target**: 70-80% code coverage for business logic
- **Critical paths**: 100% coverage for security-critical code
- **UI code**: Focus on logic testing; visual testing may require manual QA

### Running Tests

```bash
# Run all tests
ctest --output-on-failure

# Run specific test
./tests/unit/tst_mymodel

# With verbose output
./tests/unit/tst_mymodel -v2
```

---

## 10. Performance Optimization

### Qt-Specific Optimizations

**Implicit Sharing**: Qt containers use copy-on-write
```cpp
QString a = "Hello";
QString b = a;  // Shares data, no deep copy until modification
```

**Reserve Capacity**: Pre-allocate for known sizes
```cpp
QVector<int> vec;
vec.reserve(1000);  // Avoid reallocations
```

**Const Correctness**: Use const iterators and references
```cpp
for (const QString &str : stringList) {  // Avoids detaching
    // read-only access
}
```

**Model/View Optimization**:
- Implement `canFetchMore()` and `fetchMore()` for lazy loading
- Use `QAbstractItemModel::dataChanged()` for minimal updates
- Override `rowCount()` and `columnCount()` efficiently

**Signals/Slots**:
- Use `Qt::QueuedConnection` to avoid blocking
- Use `Qt::UniqueConnection` to prevent duplicate connections
- Disconnect slots when no longer needed

**QString Operations**:
- Use `QString::arg()` instead of multiple concatenations
- Use `QStringBuilder` (define `QT_USE_QSTRINGBUILDER`)

**Database**:
- Use prepared statements (faster + secure)
- Batch operations with transactions
- Use appropriate fetch size for queries

---

## 11. Documentation

### Code Comments

**Header Documentation**:
```cpp
/**
 * @brief Manages user data and authentication
 *
 * The UserModel provides access to user information and handles
 * authentication logic. It implements QAbstractTableModel for
 * display in table views.
 *
 * @see QAbstractTableModel
 */
class UserModel : public QAbstractTableModel
{
    // ...
};
```

**Function Documentation**:
```cpp
/**
 * @brief Authenticates a user with username and password
 * @param username The user's username
 * @param password The user's password (will be hashed)
 * @return true if authentication successful, false otherwise
 */
bool authenticate(const QString &username, const QString &password);
```

**Inline Comments**:
- Explain "why", not "what"
- Use `//` for single-line, `/* */` for multi-line
- Keep comments concise and up-to-date

### Qt Documentation Format

Qt uses **QDoc** for documentation generation. Use special commands:
- `\brief`: Short description
- `\param`: Parameter description
- `\return`: Return value description
- `\sa`: See also (cross-references)
- `\note`: Important notes
- `\warning`: Warnings

### README.md Required Sections

```markdown
# Project Name

## Description
Brief description of the application

## Features
- Feature 1
- Feature 2

## Requirements
- Qt 6.x
- CMake 3.16+
- C++17 compiler

## Building
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## Running
```bash
./MyApp
```

## Testing
```bash
ctest --output-on-failure
```

## License
[License Type]

## Contributing
Guidelines for contributors
```

---

## 12. Prohibited Actions

### Framework Anti-Patterns

- **Don't use raw pointers without ownership tracking**: Use Qt parent-child or smart pointers
- **Don't forget Q_OBJECT macro**: Required for signals/slots in QObject subclasses
- **Don't use dynamic_cast on QObject**: Use `qobject_cast` instead
- **Don't manually delete objects with Qt parents**: Parent handles deletion
- **Don't block the event loop**: Use `QThread` or `QtConcurrent` for heavy tasks

### Security Vulnerabilities

- **SQL injection**: Never concatenate SQL queries with user input
- **Path traversal**: Validate file paths, use canonical paths
- **Buffer overflows**: Avoid raw C strings, use Qt containers
- **Hardcoded credentials**: Never commit passwords or API keys
- **Unvalidated input**: Always sanitize user and network input

### Performance Issues

- **Detaching shared containers**: Avoid non-const operations on implicitly shared objects in loops
- **Excessive signal emissions**: Batch updates, use blockSignals() carefully
- **Synchronous network calls**: Use asynchronous Qt Network APIs
- **Frequent string concatenation**: Use `QString::arg()` or QStringBuilder

### Build/Deployment

- **Don't commit build artifacts**: Add `build/`, `*.o`, `*.exe`, `moc_*`, `ui_*` to .gitignore
- **Don't hardcode paths**: Use QStandardPaths for system directories
- **Don't skip testing**: Always run tests before release

---

## 13. References

### Official Documentation
- [Qt Documentation](https://doc.qt.io/)
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)
- [Qt Test Best Practices](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Model/View Programming](https://doc.qt.io/qt-6/model-view-programming.html)
- [Security in Qt](https://doc.qt.io/qt-6/security.html)

### Best Practices
- [Clean Qt Blog](https://cleanqt.io/)
- [How to Ensure High Cyber-security in Qt Apps](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Top 10 Secure C++ Coding Practices](https://www.incredibuild.com/blog/top-10-secure-c-coding-practices)

### Example Projects
- [Qt Examples and Tutorials](https://doc.qt.io/qt-6/qtexamplesandtutorials.html)
- [Qt Creator Source Code](https://code.qt.io/cgit/qt-creator/qt-creator.git/)

---

## 🔄 About This Document

This coding rule was auto-generated by **Stack Initializer Agent**.

- **Verification needed**: Can be moved to `.rules/_verified/` after project-specific modifications
- **Expiration**: Regeneration option provided after 24 hours
- **Contribution**: Improvement suggestions can be submitted as PR to GitHub

---

## Sources

Research for this document was compiled from:
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)
- [Model/View Programming | Qt 6.10.2](https://doc.qt.io/qt-6/model-view-programming.html)
- [Qt Test Best Practices | Qt 6.10.2](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Clean Qt Blog](https://cleanqt.io/)
- [How to Ensure High Cyber-security in Qt Apps](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [Security in Qt | Qt 6.10](https://doc.qt.io/qt-6/security.html)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
