## 1. Jest 라이프 사이클 함수

describe 함수 내부에서 테스트 코드를 작성할 때 라이프 사이클 함수들을 사용할 수 있다.

```tsx
describe("example test suite", () => {
  beforeAll(() => {
    console.log("beforeAll");
  });

  afterAll(() => {
    console.log("afterAll");
  });

  beforeEach(() => {
    console.log("beforeEach");
  });

  afterEach(() => {
    console.log("afterEach");
  });

  test("example test case 1", () => {
    console.log("test case 1");
  });

  test("example test case 2", () => {
    console.log("test case 2");
  });
});
```

- **`beforeEach`**: 각각의 테스트 케이스(Test Case)가 실행되기 전에 실행되는 함수
- **`afterEach`**: 각각의 테스트 케이스(Test Case)가 실행된 후에 실행되는 함수
- **`beforeAll`**: 모든 테스트 케이스(Test Case)가 실행되기 전에 한 번만 실행되는 함수
- **`afterAll`**: 모든 테스트 케이스(Test Case)가 실행된 후에 한 번만 실행되는 함수

```bash
beforeAll
beforeEach
test case 1
afterEach
beforeEach
test case 2
afterEach
afterAll
```

<br />

## 2. Jest 디버깅(VSCode)

VS Code 에디터를 사용할 때 Jest 디버깅하는 방법이 있다. 구글에 `vscode recipes` 라고 검색한 후 `microsoft / vscode-recipes` GitHub 저장소에 접속한다.(https://github.com/microsoft/vscode-recipes)

jest 말고도 mocha 와 같은 라이브러리도 보이는데, 여기선 jest를 사용하니 `debugging-jest-tests` 폴더에 접근한다.

해당 폴더 README.md 파일에는 `Configure launch.json File for your test framework` 항목에 launch.json 파일에 붙여넣는 configurations를 제공하고 있는데, 아래 캡쳐본에서 빨간 박스 부분을 복사해서 VS Code launch.json 파일에 붙여넣는다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928882-eca95a1f-d02e-4d08-89c1-6b115c3fcee6.png" />
</div>

<br />

**VS Code**

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928842-dbaa08e9-acec-4062-94c7-9a152c002735.png" />
</div>

- 실행 및 디버그 ⇒ launch.json 파일 만들기 ⇒ configurations 배열에 복사한 내용 붙여넣기

```json
{
  // IntelliSense를 사용하여 가능한 특성에 대해 알아보세요.
  // 기존 특성에 대한 설명을 보려면 가리킵니다.
  // 자세한 내용을 보려면 https://go.microsoft.com/fwlink/?linkid=830387을(를) 방문하세요.
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Jest Current File",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": [
        "--runTestsByPath",
        "${relativeFile}",
        "--config",
        "jest.config.ts" // => jest.config.ts로 수정함
      ],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen",
      "disableOptimisticBPs": true,
      "windows": {
        "program": "${workspaceFolder}/node_modules/jest/bin/jest"
      }
    }
  ]
}
```

<br />

### 사용 방법

1. 디버깅을 원하는 테스트 왼쪽에 빨간색 점을 클릭하여 디버깅 포인트를 잡는다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928846-9b22a9bd-7b61-4e46-9e5c-1b9d4f8561a8.png" />
</div>

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928853-d44dd245-9512-4066-91b0-8be76d7dcfea.png" />
</div>

<br />

2. 이후 디버깅을 원하는 테스트 파일을 열어놓고, 실행 및 디버깅에서 상단의 Jest Current File 왼쪽 초록색 실행 버튼을 클릭한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928858-8bba26bc-bd7f-4273-b5e6-e7ddc135db9a.png" />
</div>

<br />

3. 디버깅 포인트들을 하나씩 잡아가면서 진행된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928863-f4644d02-44be-478f-88b9-b2d2864cd442.png" />
</div>

<br />

## 3. Test Coverage

Jest Config에 coverage 항목을 추가하여 실행된 테스트가 얼마 만큼의 코드 커버리지를 갖는지 확인할 수 있다.

```tsx
import type { Config } from "@jest/types";

const config: Config.InitialOptions = {
  // ...
  collectCoverage: true,
  collectCoverageFrom: ["<rootDir>/src/app/**/*.ts"],
};

export default config;
```

- `**collectCoverage**`: true / false 값으로, true면 코드 커버리지 정보를 수집하고 출력한다.
  - 코드 커버리지는 함수, 블록, 파일 등이 얼마나 실행되었는지를 보여준다.
  - 테스트에 영향을 미치지는 않는다.
- `**collectCoverageFrom**`: 수집할 파일의 경로를 지정하는 옵션.

collectCoverageFrom 항목은 사용되는 환경에 따라 적절히 수정하여 추가하면 된다. 해당 항목들을 추가한 후 test를 실행하면 터미널에 코드 커버리지의 퍼센트를 색상, 표로 보여준다.

<br />

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928868-e95a204c-8353-4ee6-bdbb-246424b26621.png" />
</div>

- 각각의 항목에 대해 %로 코드 커버리지를 보여준다.
- 여기선 일부러 몇몇 테스트를 skip 했다.
- 해당하는 코드 커버리지의 정보를 확인하기 위해선 test 이후 생성된 /coverage 폴더 내부의 index.html 파일을 확인해보면 된다.

<br />

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928873-7dc36e16-f763-4238-ab37-418fe1671514.png" />
</div>

해당 index.html 파일을 열면 각 파일별로 코드 커버리지는 몇 퍼센트이고, 파일을 클릭해보면 어떤 함수가 테스트 됐고, 어떤 함수가 테스트되지 않았는지 확인할 수 있다.

<br />

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928876-a9dfdb23-9b17-4cd0-b606-161405053949.png" />
</div>

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928878-b7286720-05b7-454c-a8a9-ce8e1a64a59e.png" />
</div>

<br />

여기선 StringUtils 이름으로 만든 class에 대한 테스트가 작성되지 않았음을 나타내는데, 아까 일부러 skip 했던 코드를 skip하지 않고 그대로 test 되도록 수정하면 아래와 같이 100%로 변경된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225928880-08ac4b23-8d0b-4079-93da-a5d8586b51ce.png" />
</div>

단, 100% 코드 커버리지를 나타내더라도 모든 경우에 대한 테스트가 진행되었다는 것을 의미하지는 않는다. 상황, 함수의 내용 등에 따라 모든 use-case, edge-case 등을 다루도록 노력해야 한다.
