# 코드베이스 문서 생성기

파이썬으로 작성된 이 스크립트는 프로젝트의 디렉토리 구조와 각 파일의 내용을 Markdown 형식으로 문서화합니다.

## 주요 기능

- 디렉토리 구조를 트리 형태로 출력
- 각 파일의 내용을 Markdown 파일에 포함
- 제외할 파일이나 폴더 패턴 지정 가능
- 탐색할 디렉토리 깊이 제한 기능
- 실행된 디렉토리 내 `codebases/` 폴더에 결과물 저장

## 사용 방법

### 요구 사항

- Python 3.6 이상

### 설치

필요한 패키지는 표준 라이브러리에 포함되어 있어 별도의 설치가 필요 없습니다.

### 실행 방법

```bash
python3 ./script.py [옵션] <경로>
```

#### 옵션

- `-I`, `--ignore`: 무시할 패턴 지정 (예: `*.pyc __pycache__`)
- `-L`, `--level`: 탐색할 최대 디렉토리 깊이
- `<경로>`: 탐색할 대상 디렉토리 (기본값: 현재 디렉토리)

#### 예시

- 기본 사용:

  ```bash
  ./script.py
  ```

- 특정 패턴 무시 및 깊이 제한:
  ```bash
  ./script.py -I "*.log" "temp*" -L 3 ./src
  ```

## 결과

스크립트 실행 시 현재 디렉토리에 `codebases/` 폴더가 생성되고, `{타임스탬프}_codebase.md` 파일이 저장됩니다. 이 파일에는 프로젝트의 디렉토리 구조와 파일 내용이 포함되어 있습니다.

## 예제 출력

# 파일구조

```

src
├── app
│ ├── api
│ │ ├── auth
│ │ │ └── route.ts
│ │ └── ...

```

# **/src/app/page.tsx**

```javascript
import React from "react";
import Login from "./Login";

function App() {
  return (
    <div>
      <h1>My App</h1>
      <Login />
    </div>
  );
}

export default App;
```
