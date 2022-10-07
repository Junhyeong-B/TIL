# item 30 문서에 타입 정보를 쓰지 않기

## 1. 코드와 주석의 정보가 다를 때

```tsx
/**
 * 전경색(foreground) 문자열을 반환합니다.
 * 0 개 또는 1 개의 매개변수를 받습니다.
 * 매개변수가 없을 때는 표준 전경색을 반환합니다.
 * 매개변수가 있을 때는 특정 페이지의 전경색을 반환합니다.
 */
function getForegroundColor(page?: string) {
  return page === "login" ? { r: 127, g: 127, b: 127 } : { r: 0, g: 0, b: 0 };
}
```

- 최초 문자열을 반환했지만 추후에 객체를 반환하도록 바뀌었고, 주석을 갱신하는 것을 깜빡했을 가능성이 있다.
- 함수가 `string` 형태의 색깔을 반환한다고 적혀 있지만 실제로는 `{r, g, b}` 객체를 반환한다.
- 주석에는 함수가 0개 또는 1개의 매개변수를 받는다고 설명하고 있지만, 타입 시그니처만 보아도 명확하게 알 수 있는 정보이다.
- 함수 선언과 구현체보다 주석이 더 길다.

<br />

타입스크립트를 사용하면서 함수의 입력과 출력의 타입을 코드로 표현하는 것이 주석보다 더 나은 방법이다.

또 타입 구문은 타입스크립트 컴파일러가 체크해주기 때문에 구현체와의 정합성이 어긋나지 않는다.

주석은 누군가 강제하지 않는 이상 코드와 동기화되지 않지만 타입 구문은 타입 체커가 타입 정보를 동기화하도록 강제한다.

<br />

## 2. 개선된 주석을 사용

```tsx
/** 애플리케이션 또는 특정 페이지의 전경색을 가져옵니다. */
function getForegroundColor(page?: string) {
  return page === "login" ? { r: 127, g: 127, b: 127 } : { r: 0, g: 0, b: 0 };
}
```

특정 매개변수를 설명하고 싶다면 JSDoc의 `@param` 구문을 사용하면 된다.

- JSDoc은 아이템 48 API 주석에 TSDoc 사용하기 에서 자세히 다룬다.

<br />

## 3. 불필요한 주석

### 3-1) 값을 변경하지 않는다

- 값을 변경하지 않는다는 주석, 매개변수를 변경하지 않는다는 주석도 사용하지 않는 것이 좋다. 대신 `readonly`로 타입을 선언해 규칙을 강제할 수 있게 해준다.

```tsx
function sort(nums: readonly number[]) { /* ... */ }
```

<br />

### 3-2) 변수명에 타입 정보를 넣지 않는다.

ageNum 이라는 변수 명을 사용하는 것 보다 age 변수명을 사용하고 그 타입이 number임을 명시하는 것이 좋다.

```tsx
// Bad
function func(ageNum: number) {}

// Good
function func(age: number) {}
```

<br />

단, 단위가 있는 숫자들은 예외이다.

```tsx
type time = number;
type timeMs = number;

type temperature = number;
type temperatureC = number;
```

- `time` 보다 `timeMS` 가 / `temperature` 보다 `temperatureC` 가 더 명확하다.

<br />

## 요약

- 주석과 변수명에 타입 정보를 적는 것은 피해야 한다.
- 타입이 명확하지 않은 경우는 변수명에 단위 정보를 포함하는 것을 고려하는 것이 좋다.(timeMs 또는 temperatureC)