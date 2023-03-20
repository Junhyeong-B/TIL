# Jest Mocking

## 1. jest.fn()

어떤 유틸 함수에 대해 Test 코드를 작성하려고 할 때, 해당 유틸 함수가 의존하는 부분을 직접 생성하기 어려울 때 Mocking 기법이 사용된다. jest.fn() 함수는 Jest에서 제공하는 mocking 기능으로, 테스트할 함수의 의존성을 낮춰서 테스트를 보다 쉽게 만들어주는 기능이다.

**utils.ts**

```tsx
export type StringInfo = {
  lowerCase: string;
  upperCase: string;
  characters: string[];
  length: number;
  extraInfo: Object | undefined;
};

type LoggerServiceCallback = (arg: string) => void;

export function toUpperCaseWithCb(
  arg: string,
  callback: LoggerServiceCallback
) {
  if (!arg) {
    callback("Invalid argument!");
    return;
  }

  callback(`called function with ${arg}`);
  return arg.toUpperCase();
}
```

- **`toUpperCaseWithCb`**: 문자열과 콜백 함수를 매개변수로 하는 함수로 콜백함수는 무조건 호출되는 특징을 갖고 있다.

해당 함수의 반환값과 callback 함수에 대한 테스트 코드를 작성한다고 가정해 보자.

<br />

### 1-1) Jest.mock 을 사용하지 않고 구현

**utils.test.ts**

```tsx
describe("Tracking callbacks", () => {
  let cbArgs = [];
  let timesCalled = 0;
  function callbackMock(arg: string) {
    cbArgs.push(arg);
    timesCalled++;
  }

  test("calls callback for invalid argument - track calls", () => {
    const result = toUpperCaseWithCb("hello", callbackMock);

    expect(result).toBe("HELLO");
    expect(cbArgs).toContain("called function with hello");
    expect(timesCalled).toBe(1);
  });
});
```

- **`cbArgs`**: 콜백 함수로 전달된 인자를 저장하는 배열.
- **`timesCalled`**: 콜백 함수가 몇 번 호출되었는지 체크하기 위한 변수.

테스트를 진행하면 정상적으로 Pass된다. 그러나 이러한 테스트 케이스가 여러개 있다면 let 변수로 선언한 cbArgs, timesCalled 등이 누적되면서 의도하지 않게 테스트는 실패하게 된다.

<br />

```tsx
test("calls callback for invalid argument - track calls", () => {
  const result = toUpperCaseWithCb("", callbackMock);

  expect(result).toBeUndefined();
  expect(cbArgs).toContain("Invalid argument!");
  expect(timesCalled).toBe(1);
});

test("calls callback for invalid argument - track calls", () => {
  const result = toUpperCaseWithCb("hello", callbackMock);

  expect(result).toBe("HELLO");
  expect(cbArgs).toContain("called function with hello");
  expect(timesCalled).toBe(1);
});
```

- 첫 번째 test case는 통과.
- 두 번째 test case는 cbArgs는 toContain() 함수를 호출했기에 해당 값이 있기만 하면 돼서 통과하지만, timesCalled는 2번 호출했는데 toBe(1) 로 작성되어서 실패한다.
  이런 경우 afterEach() 라이프 사이클 함수를 이용해서 각각의 let 변수들을 초기화 해주면 해결핧 수 있다.

<br />

```tsx
describe("Tracking callbacks", () => {
  let cbArgs = [];
  let timesCalled = 0;
  function callbackMock(arg: string) {
    cbArgs.push(arg);
    timesCalled++;
  }

  afterEach(() => {
    // clearing tracking fields
    cbArgs = [];
    timesCalled = 0;
  });

  test("calls callback for invalid argument - track calls", () => {
    const result = toUpperCaseWithCb("", callbackMock);

    expect(result).toBeUndefined();
    expect(cbArgs).toContain("Invalid argument!");
    expect(timesCalled).toBe(1);
  });

  test("calls callback for invalid argument - track calls", () => {
    const result = toUpperCaseWithCb("hello", callbackMock);

    expect(result).toBe("HELLO");
    expect(cbArgs).toContain("called function with hello");
    expect(timesCalled).toBe(1);
  });
});
```

- afterEach는 각 테스트 케이스가 종료될 때마다 실행되는 라이프 사이클 함수로, 여기선 cbArgs, timesCalled를 초기화하고 있다.

<br />

### 1-2) Jest.mock 함수를 이용하여 구현

위와 같은 테스트 코드 작성을 Jest Mock을 사용하여 해당 함수의 Callback 함수를 가로채고 Mock 함수를 대신 호출하여 동작을 확인할 수 있다.

**utils.test.ts**

```tsx
test("toUpperCaseWithCb should call logger function with the correct message", () => {
  const callbackMock = jest.fn();
  const result = toUpperCaseWithCb("hello", loggerMock);

  expect(result).toBe("HELLO");
  expect(callbackMock).toHaveBeenCalledWith("called function with hello");
  expect(callbackMock).toBeCalledTimes(1);
});
```

- **`toHaveBeenCalledWith`**: mock 함수가 콜백 함수로 실행될 때 각 전달 인자가 일치하는지 확인.
- **`toBeCalledTimes`**: mock 함수가 몇 번 호출되었는지 확인.

위 코드는 이전 예제에서 cbArgs, timesCalled 대신 jest.fn() 함수를 사용하여 동일한 테스트 코드를 구현했다. jest.fn() 함수는 원래의 Callback 기능을 대체하는 것은 아니고 다른 자체기능을 가진 mock 함수로 항상 undefined를 반환하지만 특정 함수를 통해서 반환 값을 지정해줄 수 있고, 원래의 함수를 통째로 재 구현하여 할당할 수도 있다.

<br />

mock 함수도 사용된 모든 기록을 유지하기 때문에 각각의 테스트를 독립적으로 수행하려고 한다면 라이프 사이클 함수를 통해 초기화해 주어야 한다.

```tsx
describe("Tracking callbacks with Jest Mocks", () => {
  const callbackMock = jest.fn();

  afterEach(() => {
    // clearing tracking fields
    jest.clearAllMocks();
  });

  test("calls callback for invalid argument - track calls", () => {
    const actual = toUpperCaseWithCb("", callbackMock);
    expect(actual).toBeUndefined();
    expect(callbackMock).toHaveBeenCalledWith("Invalid argument!");
    expect(callbackMock).toBeCalledTimes(1);
  });

  test("calls callback for invalid argument - track calls", () => {
    const actual = toUpperCaseWithCb("abc", callbackMock);
    expect(actual).toBe("ABC");
    expect(callbackMock).toHaveBeenCalledWith("called function with abc");
    expect(callbackMock).toBeCalledTimes(1);
  });
});
```

<br />

## 2. jest.spyOn(object, methodName)

Jest spyOn은 Jest에서 제공하는 mocking 기능 중 하나로, 함수의 호출을 추적하고, 그 함수가 어떻게 사용되었는지 확인할 수 있게 해주는 기능이다. 예를 들어, `console.log` 함수를 spyOn하면 해당 함수가 어떻게 사용되었는지 확인할 수 있다. jest.fn()과 비슷하지만, `jest.spyOn(object, methodName)` 형태로 특정 함수를 spyOn한 후 해당 함수를 호출한 다음 어떻게 사용되었는지 검증하면 된다.

**utils.test.ts**

```tsx
test("should log message to console", () => {
  const consoleSpy = jest.spyOn(console, "log");
  const message = "Hello, world!";
  console.log(message);
  expect(consoleSpy).toHaveBeenCalledWith(message);
  consoleSpy.mockRestore();
});
```

- `console.log` 함수를 spyOn한 후, 해당 함수를 호출하고 인자로 `message`를 전달
- `consoleSpy` 객체가 `toHaveBeenCalledWith` 함수를 호출하여 `message`가 함수에 전달되었는지 확인
- `mockRestore` 함수를 호출하여 `console.log` 함수가 원래의 동작을 수행하도록 복원

<br />

## 3. jest.mock(moduleName, factory)

Jest Mock은 특정 함수들을 mocking하는데 사용한다. 앞서 jest.fn() 함수는 어떤 특정 콜백 함수 등을 mocking하여 그 함수에 전달된 전달 인자, 호출된 횟수 등을 확인할 수 있지만, jest.mock() 에서는 특정 모듈에서 정의된 함수, 메서드 등을 직접 컨트롤할 수 있다.

**utils.ts**

```tsx
import { v4 } from "uuid";

export function toLowerCaseWithId(arg: string) {
  return arg.toLowerCase() + v4();
}
```

- 문자열을 인자로 받아서 소문자로 변경하고 uuid 모듈의 v4 함수 호출 반환값을 더해서 반환한다.
- v4 함수는 호출할 때마다 매번 다른 값(만에 하나 겹칠 수도 있지만)을 반환하기에 단순히 toBe()와 같은 함수로 테스트하기 어렵다.

이럴 경우 jest.mock 함수를 사용하여 mocking하면 된다.

<br />

**utils.test.ts**

```tsx
jest.mock("uuid", () => ({
  v4: () => "123",
}));

describe("mocking tests", () => {
  test("string with id", () => {
    const result = OtherUtils.toLowerCaseWithId("ABC");
    expect(result).toBe("abc123");
  });
});
```

- jest.mock 첫 번째 전달인자(moduleName)로 uuid 값을 넘겨준다. 이후 두 번째 인자(factory)로 mocking을 적용할 함수와 로직을 작성하면 된다.
- v4 함수를 mocking하여 항상 문자열 `"123"` 을 반환하도록 설정해서 실제 테스트에서도 v4() 함수의 호출 결과는 `"123"`으로 고정된다.
