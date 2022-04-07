# 16장  리덕스 라이브러리 이해하기

- 단순히 전역 상태 관리만 한다면 Context API를 사용하는 것만으로 충분하다.
- 프로젝트 규모가 크다면 리덕스의 미들웨어, 개발자 도구 등으로 유지 보수에 더 유리하여 리덕스를 사용하는 편이 좋다.

<br />

# 16.1 개념

## 16.1.1 액션

- 상태에 어떤 변화가 필요하면 액션(action)이 발생한다.
- 액션 객체는 반드시 type 필드를 가지고 있어야 한다.

```jsx
{
	type: 'CHANGE_INPUT',
	text: '텍스트'
}
```

<br />

## 16.1.2 액션 생성 함수

- 액션 객체를 만들어주는 함수이다.
- 매번 액션 객체를 직접 작성하여 사용하는 것이 아니라 만드는 과정에서의 실수를 최소화하기 위해 함수로 만들어 관리한다.

```jsx
const changeInput = (text) => {
	return {
		type: 'CHANGE_INPUT',
		text
	}
}
```

<br />

## 16.1.3 리듀서

- 변화를 일으키는 함수이다.
- 액션을 만들어서 발생시키면 리듀서가 현재 상태, 액션 객체를 파라미터로 받아와 두 값을 참고하여 새로운 상태를 만들어 반환한다.

```jsx
const initialState = {
	text: ''
}

const reducer = (state, action) => {
	switch (action.type) {
		case 'CHANGE_INPUT':
			return {
				text: action.payload,
			};
		default:
			return state;
	}
}
```

<br />

## 16.1.4 스토어

- 한 개의 프로젝트는단 하나의 스토어만 가질 수 있다.
- 스토어 안에는 어플리케이션 상태, 리듀서 등이 담겨있다.

<br />

## 16.1.5 디스패치

- 스토어의 내장 함수로 디스패치를 통해 액션을 발생시킨다.
- dispatch(action) 형태로 호출한다.

<br />

## 16.1.6 구독(subscribe)

- 스토어의 내장 함수로 subscribe 함수 안에 리스터 함수를 파라미터로 호출하면 액션이 디스패치되어 **상태가 업데이트될 대마다 호출**된다.

```jsx
const listener = () => {
	/* ... */
};

const unsubscribe = store.subscribe(listener); // 구독 활성화

unsubscribe(); // 추후 구독을 비활성화할 때 사용
```

<br />

# 16.2 리액트 없이 쓰는 리덕스

- 리액트는 종속되는 라이브러리가 아니고 다른 UI 라이브러리/프레임워크와 함께 사용할 수 있다.
    - angular-redux, ember redux, Vue, Vanilla JS 등
    - `yarn add redux`

<br />

## 16.2.4 액션 타입과 액션 생성 함수 정의

- 프로젝트의 상태에 변화를 일으키는 것을 액션이라고 하는데 액션 이름은 문자열, 대문자 형태로 작성한다.
- 이름이 중복되면 의도치 않은 결과가 발생하므로 상수로 정의하여 관리한다.

```jsx
const INCREASE = 'INCREASE'; // 액션 이름

const increase = () => ({ type: INCREASE }); // 액션 생성 함수
```

<br />

## 16.2.7  스토어 만들기

- `index.js`

```jsx
import { createStore } from 'redux';

const store = createStore(reducer);
```

<br />

## 16.2.8~9 render 함수와 subscribe

- `index.js`

```jsx
const reducer = (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_SWITCH:
      return {
        ...state,
        toggle: !state.toggle,
      };
    case INCREASE:
      return {
        ...state,
        counter: state.counter + 1,
      };
    case DECREASE:
      return {
        ...state,
        counter: state.counter + 1,
      };
    default:
      return state;
  }
};

const store = createStore(reducer);

const render = () => {
  const state = store.getState(); // 현재 상태를 불러온다.

  if (state.toggle) {
    $div.classList.add("active");
  } else {
    $div.classList.remove("active");
  }

  $counter.innerText = state.counter;
};

render();
store.subscribe(render);
```

- 상태가 바뀔 때마다 render 함수를 실행시킨다.

## 16.2.10 액션 발생시키기

```jsx
const toggleSwitch = () => ({ type: TOGGLE_SWITCH });
const increase = () => ({ type: INCREASE });
const decrease = () => ({ type: DECREASE });

$div.onclick = () => {
  store.dispatch(toggleSwitch());
};
$increaseBtn.onclick = () => {
  store.dispatch(increase());
};
$decreaseBtn.onclick = () => {
  store.dispatch(decrease());
};
```

<br />

# 16.3 리덕스의 세 가지 규칙

1. 단일 스토어
    - 하나의 어플리케이션 안에는 하나의 스토어가 들어있다.
    - 여러 개의 스토어가 가능하기는 하나 상태 관리가 복잡해지므로 권장되지는 않는다.
2. 읽기 전용 상태
    - 리덕스 상태는 읽기 전용이다.
    - 상태를 업데이트할 때 기존의 상태를 직접 조작하지 않고 새로운 객체를 생성해주어야 한다.
    - 리덕스에서 불변성을 유지해야하는 이유는 데이터가 변경되는 것을 감지하기 위해 얕은 비교(swallow equality) 검사를 하기 때문이다.
3. 리듀서는 순수한 함수
    - 리듀서는 순수한 함수여야 하고, 순수한 함수의 조건은 다음과 같다.
        1. 이전 상태와 액션 객체를 파라미터로 받는다.
        2. 파라미터 외의 값에는 의존하면 안된다.
        3. 이전 상태를 건드리지 않고, 새로운 객체 상태를 만들어 반환한다.
        4. 똑같은 파라미터로 호출된 리듀서 함수는 언제나 똑같은 결과 값을 반환해야 한다.
            - 리듀서 내부에서 랜덤 값을 만들거나 Date 함수를 만들어 현재 시간을 가져오거나 비동기 요청 등은 사용하면 안된다. ⇒ 리듀서 외부 또는 미들웨어에서 작성한다.