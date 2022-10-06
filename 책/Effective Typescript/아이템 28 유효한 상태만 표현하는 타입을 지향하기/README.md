# 아이템 28 유효한 상태만 표현하는 타입을 지향하기

- 효과적으로 타입을 설계하려면 **유효한 상태**만 표현할 수 있는 타입을 만들어 내는 것이 중요하다.

<br />

## 1. 유효하지 않은 상태도 포함하는 잘못된 설계

페이지를 선택하면 페이지의 내용을 로드하고 화면에 표시하는 웹 어플리케이션을 만든다고 가정하자.

<br />

### 페이지를 그리는 renderPage 함수

```tsx
interface State {
	pageText: string;
	isLoading: boolean;
	error?: string;
}

function renderPage(state: State) {
	if (state.error) {
		return `Error! Unable to load ${currentPage}: ${state.error}`;
	} else if (state.isLoading) {
		return `Loading ${currentPage}...`
	}

	return `<h1>${currentPage}</h1>\n${state.pageText}`;
}
```

- 여기선 분기 조건이 명확하지 않다.
- `error`, `isLoading` 값이 모두 true이면 어떤 상태를 반환할지 명확히 구분할 수 없다.

<br />

### 페이지를 전환하는 changePage 함수

```tsx
async function changePage(state: State, newPage: string) {
  state.isLoading = true;
  try {
    const response = await fetch(getUrlForPage(newPage));
    if (!response.ok) {
      throw new Error(`Unable to load ${newPage}: ${response.statusText}`);
    }
    const text = await response.text();
    state.isLoading = false;
    state.pageText =text;
  } catch(e) {
    state.error = "" + e;
  }
}
```

- 오류가 발생했을 때 `state.isLoading` 값을 `false` 로 설정하는 로직이 빠져있다.
- `state.error`를 초기화해주지 않아서 페이지 전환 중에 로딩 메시지 대신 과거이 오류 메시지를 보여주게 된다.
- 페이지 로딩 중에 사용자가 페이지를 전환하면 어떤 일이 벌어질지 예상하기 어렵다.
- `isLoading`, `error` 값이 동시에 정보가 부족하거나 충돌할 수 있다.
    - 요청이 실패한건지 로딩중인지 알 수 없음.
    - 오류이면서 로딩 중일 수도 있음.

<br />

위의 State 타입은 isLoading이 true 이면서 동시에 error 값이 설정되는 **무효한 상태**를 허용한다.

<br />

## 2. 유효한 상태만 표함하는 설계

```tsx
interface RequestPending {
  state: "pending";
}
interface RequestError {
  state: "error";
  error: string;
}
interface RequestSuccess {
  state: "ok";
  pageText: string;
}

type RequestState = RequestPending | RequestError | RequestSuccess;

interface State {
  currentPage: string;
  requests: { [page: string]: RequestState };
}
```

요청 과정 각각의 상태를 명시적으로 모델링된 태그된 유니온이 사용되었다.

<br />

### 개선된 renderPage

```tsx
function renderPage(state: State) {
  const { currentPage } = state;
  const requestState = state.requests[currentPage];
  switch (requestState.state) {
    case "pending":
      return `Loading ${currentPage}...`;
    case "error":
      return `Error! Unable to load ${currentPage}: ${requestState.error}`;
    case "ok":
      return `<h1>${currentPage}</h1>\n${requestState.pageText}`;
  }
}
```

- 위의 renderPage에서는 `isLoading`, `error` 가 true일 때의 상태가 모호했지만 여기선 정확히 하나의 상태만을 표현한다.

<br />

### 개선된 changePage

```tsx
async function changePage(state: State, newPage: string) {
  state.requests[newPage] = { state: "pending" };
  state.currentPage = newPage;
  try {
    const response = await fetch(getUrlForPage(newPage));
    if (!response.ok) {
      throw new Error(`Unable to load ${newPage}: ${response.statusText}`);
    }
    const text = await response.text();
    state.requests[newPage] = { state: "ok", pageText: text };
  } catch (e) {
    state.requests[newPage] = { state: "error", error: "" + e };
  }
}
```

- 여기서 state.requests[newPage]에는 `pending`, `ok`, `error` 각각의 상태가 정의되어 있어서 모든 요청은 정확히 하나의 상태로 맞아 떨어진다.
- 요청 중 다른 페이지로 전환 하더라도 무효가 된 요청이 실행되긴 하겠지만 UI에는 영향을 미치지 않는다.

<br />

## 3. 유효한 상태만 포함하는 설계가 중요한 이유

<div align="center">
  <img width="1200" src="https://user-images.githubusercontent.com/85148549/194308062-0beedbaf-5bdb-4986-ac69-7643ceb1f9e9.gif">
</div>

- 에어프랑스 447 에어버스 330 비행기 추락 사례
- 추락을 일으킨 많은 원인 중 주요 원인은 **잘못된 상태 설계** 였다.

에어버스 330의 조종석에는 기장과 부기장을 위한 분리된 제어 세트가 있었고, 각 스틱이 독립적으로 움직이는 이중 입력 모드 시스템을 사용했다.
이를 타입스크립트로 나타내면 다음과 같다.

```tsx
interface CockpitControls {
  /** 왼쪽 사이드 스틱의 각도, 0 = 중립, + = 앞으로 */
  leftSideStick: number;
  /** 오른쪽 사이드 스틱의 각도, 0 = 중립, + = 앞으로 */
  rightSideStick: number;
}
```

<br />

위 데이터 구조가 주어진 상태에서 현재 스틱의 설정을 계산하는 함수를 작성한다고 가정하면 다음과 같다.

### 기장이 조종할 때

```tsx
function getStickSetting(controls: CockpitControls) {
  return controls.leftSideStick;
}
```

<br />

### 기장과 부기장이 독립적으로 조종할 때

```tsx
function getStickSetting(controls: CockpitControls) {
  const { leftSideStick, rightSideStick } = controls;
  if (leftSideStick === 0) {
    return rightSideStick;
  }

  return leftSideStick;
}
```

- 이 경우 왼쪽이 중립상태가 아니면 항상 왼쪽 스틱만 반환하므로 왼쪽 스틱도 오른쪽 스틱과 동일하게 체크를 해야한다.

<br />

```tsx
function getStickSetting(controls: CockpitControls) {
  const { leftSideStick, rightSideStick } = controls;
  if (leftSideStick === 0) {
    return rightSideStick;
  } else if (rightSideStick === 0) {
    return leftSideStick;
  }

  // ???
}
```

- 둘 다 중립이 아닐 경우 스틱의 각도를 평균해서 계산할 수 있다.

<br />

```tsx
function getStickSetting(controls: CockpitControls) {
  const { leftSideStick, rightSideStick } = controls;
  if (leftSideStick === 0) {
    return rightSideStick;
  } else if (rightSideStick === 0) {
    return leftSideStick;
  }

  if (Math.abs(leftSideStick - rightSideStick) < 5) {
    return (leftSideStick + rightSideStick) / 2;
  }

	// ???
}
```

- 스틱의 각도가 비슷하다면 위처럼 평균해 계산할 수 있지만, 각도가 매우 다른 경우 해결하기가 어렵다.

<br />

### 위 상태에서 사고가 발생했다면,

비행기가 폭풍에 휘말렸을 때 부기장은 조용히 사이드 스틱을 뒤로 당겼고, 기장은 훈련받은 대로 스틱을 앞으로 밀었다.

이 때, 에어버스의 계산 함수는 다음과 같은 모습이다.

```tsx
function getStickSetting(controls: CockpitControls) {
  return (leftSideStick + rightSideStick) / 2;
}
```

함수 반환값에서 유추가 가능하듯 기장과 부기장이 서로 반대되는 방향으로 스틱을 밀었기 때문에 비행기는 아무 반응이 없었고, 결국 바다로 추락하고 말았다.

<br />

### 이야기의 요점

getStickSetting 함수는 실패할 수 밖에 없었다. 대부분의 비행기는 스틱이 기계적으로 연결되어 있고, 이를 표현하면 

```tsx
interface CockpitControls {
	/** 스틱의 각도, 0 = 중립, + = 앞으로 */
	stickAngle: number;
}
```

처럼 간단하게 표현할 수 있다.

<br />

## 요약

- 유효한 상태와 무효한 상태를 둘 다 표현하는 타입은 혼란을 초래하기 쉽고 오류를 유발한다.
- 유효한 상태만 표현하는 타입을 지향해야 한다.