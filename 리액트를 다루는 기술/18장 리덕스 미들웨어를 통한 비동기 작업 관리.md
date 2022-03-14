# 18장 리덕스 미들웨어를 통한 비동기 작업 관리

- 리액트 웹 어플리케이션은 API 서버를 연동할 때 API 요청에 대한 상태도 잘 관리행 ㅑ한다.
    - 요청시작 시 로딩 중 / 성공하거나 실패했을 때 로딩 끝
    - 성공 시 응답으로 데이터를 관히라고 실패했을 때 에러를 관리해야 함
- 이러한 비동기 작업을 관리해야 한다면 리덕스 미들웨어(middleware)를 사용하여 효율적이고 편하게 상태 관리를 할 수 있다.

<br />

# 18.2 미들웨어란?

- 리덕스 미들웨어는 액션을 디스패치했을 때 리듀서에서 이를 처리하기에 앞서 사전에 지정된 작업들을 실행하는 역할을 한다.
    - 액션 ⇒ 미들웨어 ⇒ 리듀서 ⇒ 스토어
- 미들웨어를 통해 전달받은 액션에 따라 콘솔에 기록하거나 액션을 취소할 수 있고, 다른 종류의 액션을 추가로 디스패치할 수도 있다.

<br />

## 18.2.1 미들웨어 만들기

- 실제 프로젝트에서는 미들웨어를 직접 만들지는 않고 만들어 놓은 미들웨어를 사용한다.
- 만약 원하는 미들웨어가 없다면 상황에 따라 직접 만들거나 기존 미들웨어들을 커스터마이징하여 사용할 수 있다.
- 액션이 디스패치될 때마다 액션의 정보와 전후 상태를 콘솔에 보여주는 로깅 미들웨어를 만들어보자

```jsx
const loggerMiddleware = (store) => (next) => (action) => {
  // 미들웨어 기본 구조
};

export default loggerMiddleware;
```

```jsx
const loggerMiddleware = function (store) {
  return function (next) {
    return function (action) {
      // 미들웨어 기본 구조
    };
  };
};

export default loggerMiddleware;
```

- store: 리덕스 스토어 인스턴스
- next: 함수 형태, store.dispatch와 비슷한 역할을 한다.
    - next(action)을 호출하면 그다음 처리해야 할 미들웨어에게 액션을 넘겨주고, 만약 그다음 미들웨어가 없다면 리듀서에게 액션을 넘겨준다.
    - 만약 미들웨어 내부에서 store.dispatch를 사용하면 첫 번째 미들웨어부터 다시 처리한다.
        
        ⇒ next를 사용하지 않으면 액션이 리듀서에 전달되지 않는다.
        
- action: 디스패치된 액션

```jsx
/* src/lib/loggerMiddleware.js */
const loggerMiddleware = (store) => (next) => (action) => {
  console.group(action && action.type);
  console.log("이전 상태", store.getState());
  console.log("액션", "action");
  next(action);
  console.log("다음 상태", store.getState());
  console.groupEnd();
};

export default loggerMiddleware;
```

```jsx
/* src/index.js */

import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { Provider } from "react-redux";
import { createStore } from "redux";
import rootReducer from "./modules";
import { applyMiddleware } from "redux";
import loggerMiddleware from "./lib/loggerMiddleware";

const store = createStore(rootReducer, applyMiddleware(loggerMiddleware));

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
```

<br />

<div align="center">
  <img width="400" src="https://user-images.githubusercontent.com/85148549/158142300-e0d8f2ec-645e-40fb-9cdd-dd0b959b21e7.png">
</div>

- 위와 같이 미들웨어를 통해 특정 조건에 따라 액션을 무시하게 할 수도 있고, 액션 정보를 가로채서 변경한 후 리듀서에게 전달해 줄 수도 있다.
- 이러한 속성을 이용하여 네트워크 요청같은 비동기 작업을 관리하면 매우 유용하다.

<br />

# 18.3 비동기 작업을 처리하는 미들웨어 사용

- **redux-thunk**: 비동기 작업을 처리할 때 가장 많이 사용하는 미들웨어
    - 객체가 아닌 함수 형태의 액션을 디스패치할 수 있게 해준다.
- **redux-saga**: redux-thunk 다음으로 가장 많이 사용되는 비동기 작업 관련 미들웨어 라이브러리
    - 특정 액션이 디스패치되었을 때 정해진 로직에 따라 다른 액션을 디스패치시키는 규칙을 작성하여 비동기 작업을 처리할 수 있게 해준다.

<br />

## 18.3.1 redux-thunk

- 리덕스 공식 매뉴얼에서도 이 미들웨어를 사용하여 비동기 작업을 다루는 예시를 보여주고 있다.

<br />

### 18.3.1.1 thunk란?

- Thunk는 특정 작업을 나중에 할 수 있도록 미루기 위해 함수 형태로 감싼 것을 의미한다.
- 만약 주어진 파라미터에 1을 더하는 함수를 만든다면 다음과 같을 것이다.

```jsx
const addOne = x => x + 1;
addOne(1); // 2
```

- addOne 함수를 호출하면 바로 1 + 1이 연산 된다. 만약 이 연산을 나중으로 미루고 싶으면 어떻게 해야 할까?

```jsx
const addOne = (x) => x + 1;
function addOneThunk(x) {
  const thunk = () => addOne(x);
  return thunk;
}

const fn = addOneThunk(1);
setTimeout(() => {
  const value = fn(); // fn이 실행되는 시점에 연산
  console.log(value);
}, 1000);
```

- 위와 같이 구현하면 특정 작업을 나중에 하도록 미룰 수 있다.
- redux-thunk 라이브러리를 사용하면 thunk 함수를 만들어서 디스패치할 수 있다.
    
    ⇒ 그러면 리덕스 미들웨어가 그 함수를 전달받아 store의 dispatch, getState를 파라미터로 넣어서 호출해준다.
    

<br />

### 18.3.1.2 미들웨어 적용하기

```jsx
yarn add redux-thunk
```

```jsx
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { Provider } from "react-redux";
import { createStore } from "redux";
import rootReducer from "./modules";
import { applyMiddleware } from "redux";
import loggerMiddleware from "./lib/loggerMiddleware";
import ReduxThunk from "redux-thunk";

const store = createStore(
  rootReducer,
  applyMiddleware(loggerMiddleware, **ReduxThunk**)
);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
```

- 스토어를 만들 때 applyMiddleware를 통해 redux-thunk를 적용시킨다.

### 18.3.1.3 Thunk 생성 함수 만들기

```jsx
import { createAction, handleActions } from "redux-actions";

const INCREASE = "counter/INCREASE";
const DECREASE = "counter/DECREASE";

export const increase = createAction(INCREASE);
export const decrease = createAction(DECREASE);

**export const increaseAsync = () => (dispatch) => {
  setTimeout(() => {
    dispatch(increase());
  }, 1000);
};
export const decreaseAsync = () => (dispatch) => {
  setTimeout(() => {
    dispatch(decrease());
  }, 1000);
};**

const initialState = 0;

const counter = handleActions(
  {
    [INCREASE]: (state) => state + 1,
    [DECREASE]: (state) => state - 1,
  },
  initialState
);

export default counter;
```

- increaseAsync, decreaseAsync를 만들어 값의 변경이 비동기적으로 동작하도록 작성했다.

### 18.3.1.4 웹 요청 비동기 작업 처리하기

- JSON Place Holder API 사용하여 작업 처리해보자
- [https://jsonplaceholder.typicode.com/](https://jsonplaceholder.typicode.com/)

```jsx
/* src/lib/api.js */
import axios from "axios";

export const getPost = (id) =>
  axios.get(`https://jsonplaceholder.typicode.com/posts/${id}`);

export const getUsers = () =>
  axios.get(`https://jsonplaceholder.typicode.com/users`);
```

```jsx
/* src/lib/createRequestThunk.js */
export default function crateRequestThunk(type, request) {
  const SUCCESS = `${type}_SUCCESS`;
  const FAILURE = `${type}_SUCCESS`;
  return (params) => async (dispatch) => {
    dispatch({ type }); // dispatch 시작
    try {
      const response = await request(params);
      dispatch({
        type: SUCCESS,
        payload: response.data,
      }); // 성공
    } catch (e) {
      dispatch({
        type: FAILURE,
        payload: e,
        error: true,
      }); // 에러 발생
      throw e;
    }
  };
}
```

```jsx
import createRequestThunk from "../lib/createRequestTunnk";
import * as api from "../lib/api";
import { handleActions } from "redux-actions";

const GET_POST = "sample/GET_POST";
const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
const GET_POST_FAILURE = "sample/GET_POST_FAILURE";

const GET_USERS = "sample/GET_USERS";
const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
const GET_USERS_FAILURE = "sample/GET_USERS_FAILURE";

export const getPost = createRequestThunk(GET_POST, api.getPost);
export const getUsers = createRequestThunk(GET_USERS, api.getUsers);

const initialState = {
  loading: {
    GET_POST: false,
    GET_USERS: false,
  },
  post: null,
  users: null,
};

const sample = handleActions({
	 /* ... */
});

export default sample;
```

## 18.3.2 redux-saga

- 대부분의 경우 redux-thunk를 통해 충분한 기능을 구현할 수 있지만, 좀 더 까다로운 특정 상황에서 redux-saga를 사용하는 것이 유리하다.
    - 기존 요청을 취소 처리해야 할 때(불필요한 중복 요청 방지)
    - 특정 액션이 발생했을 때 다른 액션을 발생시키거나 API 요청 등 리덕스와 관계 없는 코드를 실행할 때
    - 웹소켓을 사용할 때
    - API 요청 실패 시 재요청해야 할 때