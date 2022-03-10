# 17장 리덕스를 사용하여 리액트 애플리케이션 상태 관리하기

- 자바스크립트에서 사용한 redux는 store.dispatch, store.subscribe 내장 함수들을 사용했지만, 리액트에서 react-redux를 사용한다면 유틸함수(connect)와 컴포넌트(Provider)를 사용하여 작업을 처리한다.
- `yarn add redux react-redux`

<br />

# 17.3 리덕스 관련 코드 작성하기

- 리덕스는 액션 타입, 액션 생성 함수, 리듀서 코드를 작성하는데 이 코드들은 각각 다른 파일에 작성하는 방법도 있고, 기능별로 작성할 수도 있다. ⇒ 정답은 없다.

1. 일반적인 구조
    - 리덕스 공식 문서에서는 actions, constants, reducers 세 개의 디렉토리를 만들고 그 안에 기능별로 파일을 하나씩 만드는 방식이 사용된다.
        - 단, 이 방법은 새로운 액션을 만들 때마다 세 종류의 파일을 모두 수정해야 한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/157603525-18f725c6-e4ac-4b61-b989-d4557bb47879.png">
</div>

<br />

2. Ducks 패턴
    - 기능별로 파일 하나에 몰아서 다 작성하는 방식이다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/157603526-5b03f897-8f63-46e8-97ec-49bda51972a1.png">
</div>

<br />

## 17.3.1 counter 모듈 작성하기

- 액션 타입을 정의할 때 `모듈 이름(소문자)/액션 이름(대문자)` 형태로 작성하면 액션 타입이 중복되는 것을 방지할 수 있다.

```jsx
const INCREASE = "counter/INCREASE";
const DECREASE = "counter/DECREASE";

export const increase = () => ({ type: INCREASE });
export const decrease = () => ({ type: DECREASE });

const initialState = {
  number: 0,
};

const counter = (state = initialState, action) => {
  switch (action.type) {
    case INCREASE:
      return {
        number: state.number + 1,
      };
    case DECREASE:
      return {
        number: state.number - 1,
      };
    default:
      return state;
  }
};

export default counter;
```

<br />

## 17.3.3 루트 리듀서 만들기

- 리듀서를 여러개 만들면(여기서는 counter만 만들었지만, todos reducer도 있다고 가정한다.) 기존의 createStore에는 한 개의 reducer만 사용해야 하므로 그대로 파라미터로 전달할 수는 없다.
- 대신 combineReducers 유틸 함수를 사용하여 두 개 이상의 리듀서를 전달하여 루트 리듀서를 생성할 수 있다.

```jsx
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  counter,
  todos,
});

export default rootReducer;
```

<br />

# 17.4 리액트 어플리케이션에 리덕스 적용하기

- `src/index.js`

```jsx
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import { Provider } from 'react-redux';
import rootReducer from './modules';

const store = createStore(rootReducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>
  document.getElementById('root')
);
```

<br />

# 17.5 컨테이너 컴포넌트 만들기

- 리덕스 스토어와 연동된 컴포넌트를 컨테이너 컴포넌트라고 부른다.
- 컨테이너 컨포넌트는 react-redux에서 제공하는 connect 함수를 사용해야 한다.
    - connect의 두 가지 파라미터
        - mapStateToProps: 리덕스 스토어 안의 상태를 컴포넌트의 props를 넘겨주기 위해 설정하는 함수
        - mapDispatchToProps: 액션 함수를 컴포넌트의 props로 넘겨주기 위해 사용하는 함수

```jsx
connect(mapStateToProps, mapDispatchToProps)(연동할 컴포넌트)
```

```jsx
import { connect } from "react-redux";

const CounterContainer = ({ number, increase, decrease }) => {
  return (
    <Counter number={number} onIncrease={increase} onDecrease={decrease} />
  );
};

const mapStateToProps = (state) => {
  number: state.counter.number;
};

const mapDispatchToProps = (dispatch) => ({
  increase: () => {
    dispatch(increase());
  },
  decrease: () => {
    dispatch(decrease());
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(CounterContainer);
```

- mapStateToProps, mapDispatchToProps 객체 내부의 값들은 컴포넌트의 props로 전달된다.
- mapStateToProps, mapDispatchToProps는 보통 변수로 선언해놓고 사용하지만 익명 함수 형태로 선언해도 문제가 되지는 않는다.

<br />

### bindActionCreators 또는 객체 형태로 작성하기

- 액션 생성 함수가 많아진다면 mapDispatchProps에서 dispatch로 감싸는 것이 불편할 수도 있다.
- 이 때 redux에서 제공하는 **bindActionCreators**를 사용하거나 **객체 형태로 작성**하면 dispatch를 사용하지 않고 더 간단하게 작성할 수 있다.

 

```jsx
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

/* ... */

const mapDispatchToProps = (dispatch) =>
  bindActionCreators(
    {
      increase,
      decrease,
    },
    dispatch
  );

export default connect(mapStateToProps, mapDispatchToProps)(CounterContainer);
```

```jsx
import { connect } from "react-redux";

/* ... */

const mapDispatchToProps = {
  increase,
  decrease,
};

export default connect(mapStateToProps, mapDispatchToProps)(CounterContainer);
```

- 만약 객체 형태로 작성해준다면 connect 함수가 내부적으로 bindActionCreators 작업을 대신 해준다.

<br />

# 17.6 리덕스 더 편하게 사용하기

- redux-actions 라이브러리를 사용하여 내부의 createAction, handleActions 함수를 사용하면 위 내용들을 더 간단하게 작성할 수 있다.
- 생성된 액션 함수에 필요한 추가 데이터는 모두 payload라는 이름으로 사용한다.

```jsx
yarn add redux-actions
```

```jsx
const CHANGE_INPUT = 'sample/CHANGE_INPUT';

export const changeInput = createActions(CHANGE_INPUT, (input) => input);

const todos = handleActions(
	{
		[CHANGE_INPUT]: (state, action) => ({ ...state, input: action.payload })

		// 비구조화 할당으로 payload 이름 설정해주기 => 나중에 코드 내용 확인이 수월해진다.
		[CHANGE_INPUT]: (state, { payload: input }) => ({ ...state, input })
	},
	initialState,
);

export default todos;
```

<br />

# 17.7 Hooks를 사용하여 컨테이너 컴포넌트 만들기

## useSelector(상태 선택 함수);

- react-redux에서 제공하는 **useSelector**를 통해 connect를 사용하지 않고도 상태를 조회할 수 있다.

```jsx
const number = useSelector((state) => state.counter.number);
```

## useDispatch()

- useDispatch를 통해 스토어의 내장 함수 dispatch를 사용할 수 있게 해준다.

```jsx
const dispatch = useDispatch();
dispatch(increase());
```

- 단, 이 경우 컴포넌트 내부에서 dispatch를 사용하므로 컴포넌트가 렌더링될 때 마다 dispatch를 통해 사용하는 함수가 재생성되기 때문에 useCallback과 함께 사용할 것을 권장한다.

```jsx
const dispatch = useDispatch();
const onIncrease = useCallback(() => dispatch(increase()), [dispatch]);
```

## useStore()

- 리덕스 스토어 객체를 직접 접근하여 사용할 수 있다.
- 단, 특별히 직접 접근해야 하는 경우에만 사용해야 한다.

```jsx
const store = useStore();
store.getState();
```

<br />

## 17.7.5 useActions 유틸 Hook 만들어 사용하기

- useActions는 원래 react-redux에 내장된 상태로 릴리즈될 예정이었으나 꼭 필요하지 않다고 판단하여 제외된 Hook으로 공식 문서에서 그대로 복사하여 사용할 수 있도록 제공하고 있다.
    - [https://react-redux.js.org/api/hooks#recipe-useactions](https://react-redux.js.org/api/hooks#recipe-useactions)
- 해당 Hook은 액션 생성 함수를 액션을 디스패치하는 함수로 변환해 준다.
- 첫 번째 파라미터는 액션 생성 함수로 이루어진 배열을 받고
    
    두 번째 파라미터는 종속성 배열 deps을 받는다.
    

```jsx
import { bindActionCreators } from 'redux'
import { useDispatch } from 'react-redux'
import { useMemo } from 'react'

export function useActions(actions, deps) {
  const dispatch = useDispatch()
  return useMemo(
    () => {
      if (Array.isArray(actions)) {
        return actions.map(a => bindActionCreators(a, dispatch))
      }
      return bindActionCreators(actions, dispatch)
    },
    deps ? [dispatch, ...deps] : [dispatch]
  )
}
```

### 사용 전

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { changeInput, toggle } from '...'

const { input, todos } = useSelector(({ todos }) => ({
	input: todos.input,
	todos: todos.todos
}));
const dispatch = useDispatch();
const onChangeInput = useCallback(input => dispatch(changeInput(input)), [dispatch]);
const onToggle = useCallback(id => dispatch(toggle(id)), [dispatch]);
/* ... 등등의 함수 작성 */
```

### 사용 후

```jsx
import { useSelector } from 'react-redux';
import { changeInput, toggle } from '../components/Input'
import useActions from '../lib/useActions'

const { input, todos } = useSelector(({ todos }) => ({
	input: todos.input,
	todos: todos.todos
}));

const [onChangeInput, onToggle] = useActions(
	[changeInput, toggle],
	[]
)
```

<br />

## 17.7.6 connect 사용 vs Hooks 사용

- Hook이 있다고 해서 connect가 사라지는 것이 아니니 더 편한 것을 사용하면 된다.
- 단, connect를 사용하여 컨테이너 컴포넌트를 만들었을 경우 해당 컨테이너 컴포넌트의 부모 컴포넌트가 리렌더링될 때 해당 컨테이너 컴포넌트의 props가 바뀌지 않았다면 리렌더링이 자동으로 방지되어 성능이 최적화된다.
- 반면 Hook을 사용하여 redux 상태를 조회할 때는 성능 최적화를 위해 React.memo를 컨테이너 컴포넌트에 사용해 주어야 한다.
    - 물론, 부모 컴포넌트가 리렌더링될 일이 없다면 불필요한 최적화이다.