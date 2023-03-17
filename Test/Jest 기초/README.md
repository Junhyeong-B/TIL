## 1. 개발환경 세팅

Jest는 페이스북에서 만든 테스트 프레임워크로, JavaScript 코드의 유닛 테스트를 위한 도구이다. Jest는 강력한 스냅샷 테스트, 병렬 테스트 실행과 코드 커버리지 보고서 작성과 같은 유용한 기능을 제공한다.

Jest 개발환경 세팅을 위해 터미널에 다음과 같이 입력한다.

```tsx
$ npm init -y

$ npm i -D typescript jest ts-jest @types/jest ts-node
```

설치가 완료되면 프로젝트 루트 폴더에 jest.config.ts 파일을 생성하여 Jest 컨피그를 설정해준다. 여기서 `@types/jest` 라이브러리에서 Config 타입을 import한 후 필요한 설정들을 작성해주면 된다.

```tsx
// jest.config.ts
import type { Config } from "@jest/types";

const config: Config.InitialOptions = {
  preset: "ts-jest",
  testEnvironment: "node",
  verbose: true,
};

export default config;
```

이후 `package.json`에서 test script를 작성해주면 된다.

```tsx
"scripts": {
  "test": "jest"
},
```

<br />

## 2. 기초 테스트 작성

**Utils.ts**

```tsx
export function toUpperCase(arg: string) {
  return arg.toUpperCase();
}
```

<br />

**Utils.test.ts** | **Utils.spec.ts**

```tsx
import { toUpperCase } from "../app/Utils";

describe("Utils test suite", () => {
  test("should return uppercase of valid string", () => {
    // arrange
    const suite = toUpperCase;
    const expected = "ABC";

    // act
    const actual = suite("abc");

    // assert
    expect(actual).toBe(expected);
  });
});
```

위와 같은 형태로 test 파일을 만들고, `describe`, `it(or test)`, `expect`, `toBe` 와 같은 메서드들을 이용하여 테스트 코드를 작성한다.

1. **`describe()`:** 관련 있는 테스트 케이스를 그룹화하는 함수.
   - 첫번째 매개변수는 해당 테스트 그룹의 이름을 나타내고, 두번째 매개변수는 테스트 그룹 안에 수행될 콜백 함수이다.
2. **`test()`:** 테스트 케이스를 정의.
   - 첫번째 매개변수는 테스트 케이스의 이름을 나타내고, 두번째 매개변수는 테스트 케이스 안에 수행될 콜백 함수이다.
3. **`expected`:** 예상 결과값을 저장하는 변수.
4. **`actual`:** 실제 결과값을 저장하는 변수.
5. **`expect()`:** 예상 결과값을 검증하는 함수.
6. **`toBe()`:** 예상 결과값과 실제 결과값이 같은지 검증하는 함수.
   - **`toBe()`** 함수는 **`expect()`** 함수의 체이닝 함수로 사용됩니다.

<br />

작성한 이후 터미널에서 `npm test` 명령어를 입력하면 아래와 같이 테스트 결과가 터미널에 나타나게 된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225927929-5f8450b1-229e-4bf7-9c15-42c2375cd9fe.png" />
</div>

<br />

테스트 결과와 테스트를 실행하면서 발생하는 Error, Warn 등이 같이 나타난다. 여기선 Warning이 발생하고 있는데, 이 Warning은 TypeScript 코드에서 ECMAScript 모듈과 관련된 문제가 발생했을 때 발생할 수 있다.

Typescript Config에서 `esModuleInterop` 플래그는 `import` 및 `export` 문을 통해 모듈을 가져오거나 내보내는 데 사용되는 간결한 구문을 사용할 수 있도록 해주는 TypeScript 설정이고, 이 설정을 사용하면 일부 모듈 로더는 ECMAScript 모듈을 CommonJS 모듈과 상호 운용 가능하도록 변환이 가능하다.

이 warning 메시지는 `esModuleInterop` 설정이 `false`로 설정되어 있어서, TypeScript에서 `import` 문을 사용할 때에는 추가적인 변환 작업이 필요하다는 것을 알려주는 Warning이고, 이를 해결하기 위해선 tsconfig.json 파일을 추가하여 설정을 추가하면 된다.

<br />

**tsconfig.json**

```json
{
  "compilerOptions": {
    "esModuleInterop": true
  }
}
```

<br />

## 3. 더 많은 항목 테스트하기

**Utils.ts**

```tsx
export type StringInfo = {
  lowerCase: string;
  upperCase: string;
  characters: string[];
  length: number;
  extraInfo?: Object;
};

export function getStringInfo(arg: string): StringInfo {
  return {
    lowerCase: arg.toLowerCase(),
    upperCase: arg.toUpperCase(),
    characters: Array.from(arg),
    length: arg.length,
    extraInfo: {},
  };
}
```

<br />

**Utils.test.ts**

```tsx
describe("Utils test suite", () => {
	test("should return info for valid string", () => {
	    const actual = getStringInfo("My-String");

	    expect(actual.lowerCase).toBe("my-string");
	    expect(actual.upperCase).toBe("MY-STRING");

	    expect(actual.length).toBe(9);
	    expect(actual.characters).toHaveLength(9);

	    // prettier-ignore
	    expect(actual.characters).toEqual(["M", "y", "-", "S", "t", "r", "i", "n", "g"]);
	    expect(actual.characters).toContain("M");
	    // prettier-ignore
	    expect(actual.characters).toEqual(
	      expect.arrayContaining(["S", "t", "r", "i", "n", "g", "M", "y", "-"])
	    );

	    expect(actual.extraInfo).toEqual({});
	    expect(actual.extraInfo).not.toBe(undefined);
	    expect(actual.extraInfo).not.toBeUndefined();
	    expect(actual.extraInfo).toBeDefined();
	    expect(actual.extraInfo).toBeTruthy();
	  });
	});
});
```

1. **`toHaveLength()`**: 배열의 길이를 검증
2. **`toEqual()`**: 객체 또는 배열을 포함하여 원시 타입의 값을 정확하게 비교하는 함수
   - `expect({}).toBe({})`는 toBe() 함수가 객체를 정확하게 비교하는 함수가 아니기 때문에 실패하고, 이럴 경우 객체 내부를 비교하는 `toEqeual()` 또는 `toMatchObject()` 등의 함수를 이용하는 것이 좋다.
3. **`toContain()`**: 배열이 특정 항목을 포함하는지 검사
4. **`arrayContaining()`**: 배열이 특정 항목을 포함하는지 검사
5. **`not.toBe()`**: **`toBe()`** 함수와 반대로, 원시값(primitive)과 object의 값을 정확하게 비교하지 않는 함수.
6. **`toBeDefined()`**: 값이 정의되어 있는지 검증
7. **`toBeTruthy()`**: 값이 true인지 검증

이 외에도 많은 검증 함수들이 있다.

<br />

### ※ Multiple 테스트 구조

위와 같이 it() 함수 하나에 expect 함수를 여러개 사용하여 코드를 작성한 후 test를 돌리면 터미널의 결과에는 it() 첫번째 전달 인자로 넣은 문자 값만 나타나서, 만약 테스트에 실패할 경우 어떤 부분에서 실패했는지 알아내기 어렵다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225927918-207981ef-bf9b-48dd-a17c-1ae353e350dc.png" />
</div>

이럴 경우 describe(), test() 함수를 여러번 사용해서 테스트를 분리하면 좀 더 구체적으로 결과를 확인할 수 있다.

**Utils.test.ts**

```tsx
describe("getStringInfo for arg My-String should", () => {
  test("return right length", () => {
    const actual = getStringInfo("My-String");
    expect(actual.characters).toHaveLength(9);
  });
  test("return right lower case", () => {
    const actual = getStringInfo("My-String");
    expect(actual.lowerCase).toBe("my-string");
  });
  test("return right upper case", () => {
    const actual = getStringInfo("My-String");
    expect(actual.upperCase).toBe("MY-STRING");
  });
  test("return right characters", () => {
    const actual = getStringInfo("My-String");
    // prettier-ignore
    expect(actual.characters).toEqual(["M", "y", "-", "S", "t", "r", "i", "n", "g"]);
    expect(actual.characters).toContain("M");
    // prettier-ignore
    expect(actual.characters).toEqual(
      expect.arrayContaining(["S", "t", "r", "i", "n", "g", "M", "y", "-"])
    );
  });
  test("return right extra info", () => {
    const actual = getStringInfo("My-String");
    expect(actual.extraInfo).toEqual({});
  });
});
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225927923-6580a1e9-682d-4725-a5d0-2ba959c674df.png" />
</div>

이렇게 되면 테스트 결과에 어떤 부분에서 Pass 했고, Fail 했는지 알 수 있다.

<br />

## 4. it.each() 함수로 Test 이름 동적으로 선언하기

**Utils.test.ts**

```tsx
describe("toUpperCase examples", () => {
  test.each([
    { input: "abc", expected: "ABC" },
    { input: "My-String", expected: "MY-STRING" },
    { input: "def", expected: "DEF" },
  ])("$input toUpperCase should be $expected", ({ input, expected }) => {
    const actual = toUpperCase(input);
    expect(actual).toBe(expected);
  });
});
```

1. **`test.each()`**: 여러 개의 입력값에 대해서 반복적으로 테스트 케이스를 실행할 수 있도록 해주는 함수
   - 입력값을 배열의 형태로 전달하고, 배열의 각 요소는 객체로 구성된다.
2. **`$input`** | **`$expected`**: **`test.each()`** 함수에서 전달한 객체의 속성 이름에 해당하는 값을 추출한다.
3. `**{ input, expected }**`: `**test.each()**` 함수에서 전달한 input, expected를 매개변수로 전달하고, 이를 콜백 함수 내부에서 사용할 수 있다.

여러 개의 테스트 케이스를 작성할 때 for 문, forEach() 등을 사용할 수도 있지만, 위와 같이 `it.each()` 함수를 사용해서도 여러 개의 테스트 케이스를 작성할 수 있다. 위 코드의 테스트 결과는 아래와 같다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/225927925-9a8e969b-e417-4590-a8fa-b14f565562e0.png" />
</div>

<br />

## 5. test vs it

Jest 테스트 코드를 작성할 때 describe 내부에 test 또는 it 함수로 테스트 코드를 작성할 수 있다. 각각 작성해보면 테스트 결과엔 큰 차이가 없고, test.only, test.each 같은 메서드들도 동일하게 존재한다. 이 둘의 차이는 뭘까?

결론은, 둘 다 동일한 함수로 동작의 차이는 없다. 다만 Jest 공식 사이트에서는 test 함수를 사용할 것을 권장하고 있고, 공식 사이트의 예제 코드에서 test 함수를 사용하고 있다.

Jest 외에 테스트 라이브러리에서 일부 it 함수를 사용하기도 해서 it 함수가 더 익숙한 사람도 있을 것이라는 의견도 있으니 취향이나 컨벤션 등에 따라 적절히 사용하면 될 것 같다.
