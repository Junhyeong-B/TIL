# React-Redux

# Redux

- Redux는 상태 관리 라이브러리이다.
- Vanilla Javascript, Angular, React, Vue 등 Javascript Application에서 작동 가능하도록 설계되었고, **React만의 라이브러리는 아니다**.(React 외 프레임워크, 라이브러리, Vanilla Javascript에서도 사용 가능하다.)

<br />

# 1. 기본 사용 방법

1. Redux를 사용할 프로젝트에 redux 라이브러리를 설치한다.

```
$yarn add redux
	or
$npm install redux
```

2. redux로부터 `createStore` 함수를 import하여 store를 생성한다.
    - 첫 번째 인자로 `Reducer`를 생성하여 작성한다.

```jsx
import { createStore } from "redux";

// Counter 역할을 하는 구성 요소 만들기
const countModifier = (count = 0) => {  // reducer 역할, 매개변수 State initializing
	return count;
};
const countStore = createStore(countModifier);

console.log(countStore);
// {dispatch: ƒ, subscribe: ƒ, getState: ƒ, replaceReducer: ƒ, Symbol(observable): ƒ}
// countStore.getState()를 호출하면 return문에서 반환한 state(여기선 count)가 반환됨
```

- `createStore` 함수를 통해 store를 생성하면 해당 상태(state)에 접근할 수 있다.
- 여기서 count를 늘리거나 줄이는 메소드를 수행하려면 `Action`을 이용하면 된다.

<br />

3. 작성한 Reducer의 두 번째 매개변수로 Action을 사용하여 메소드를 작성한다.
    - 메소드는 `store.dispatch()` 함수를 사용하여 매개변수로 `Object`를 넘겨준다.

```jsx
const countModifier = (count = 0, action) => {
  if (action.type === "ADD") {
    return count + 1;
  }
  return count;
};

countStore.dispatch({ type: "ADD" });
```

<br />

4. 위 내용을 바탕으로 State를 관리, 사용하면 된다.

```jsx
const add = document.getElementById("add");
const minus = document.getElementById("minus");
const number = document.querySelector("span");

const countModifier = (count = 0, action) => {
  if (action.type === "ADD") {
    return count + 1;
  } else if (action.type === "MINUS") {
    return count - 1;
  }
  return count;
};

const countStore = createStore(countModifier);

const handleAdd = () => {
  countStore.dispatch({ type: "ADD" });
};
const handleMinus = () => {
  countStore.dispatch({ type: "MINUS" });
};

add.addEventListener("click", handleAdd);
minus.addEventListener("click", handleMinus);
```

<br />

## ※ Redux 알아두면 좋은 팁

### 1. `store.subscribe()`

- store를 생성했을 때 나타나는 4가지 함수(`dispatch`, `subscribe`, `getState`, `replaceReducer`) 중 subscribe는 우리에게 store 안에 있는 변화들을 알 수 있게 해준다.
- subscribe 함수는 store에 변화가 있을 때마다 호출된다.

```jsx
const number = document.querySelector("span");

const onChange = () => {
  number.innerText = countStore.getState();
};

countStore.subscribe(onChange);
// 위 경우 store가 변화할 때 마다 number document에 변화된 state를 rendering 해준다.
```

<br />

### 2. Action 작성 시 if ~ else 대신 switch

- if문 보다 더 간결하게 코드를 작성할 수 있다.
- redux 공식 문서에도 switch 문을 사용하고 있다.
    - 필수는 아니다.

```jsx
const countModifier = (count = 0, action) => {
  switch (action.type) {
    case "ADD":
      return count + 1;
    case "MINUS":
      return count - 1;
    default:
      return count;
  }
};
```

<br />

### 3. action.type은 string 대신 const

- type에 string으로 작성하면 redux가 정상적으로 작동하지 않을 때 어느 부분이 잘못된건지 알기 어려워진다.
- type을 상수로 선언하고 관리하면 해당 이슈를 피할 수 있다.

```jsx
const ADD = "ADD"; // "ADD"를 상수로 선언하여 사용하기
const MINUS = "MINUS";

const countModifier = (count = 0, action) => {
  switch (action.type) {
    case ADD:
      return count + 1;
    case MINUS:
      return count - 1;
    default:
      return count;
  }
};

const handleAdd = () => countStore.dispatch({ type: ADD });
const handleMinus = () => countStore.dispatch({ type: MINUS });
```

<br />

### 4. State의 형태가 Object라면 previousState를 변형(mutate)하지 않고 새로운 Object를 만들어서 수정하자

- 만약, 배열(Array)을 사용한다면, `array.push()` 등의 형태로 State를 변형하여 반환하지 말고, 새로운 배열을 만들어서 반환해준다.
    - 예) array의 값을 삭제하고 싶을 때, `array.splice()` 메소드는 배열을 변형하므로 새로운 배열을 만드는 `array.filter()` 메소드를 사용한다.

```jsx
// Todo List 만들기
const ADD_TODO = "ADD_TODO";
const DELETE_TODO = "DELETE_TODO";

const reducer = (state = [], action) => {
  switch (action.type) {
    case ADD_TODO:
      return [...state, { text: action.text, id: action.id }];
    case DELETE_TODO:
			return state.filter((todo) => +todo.id !== +action.id);
    default:
      return state;
  }
};

const store = createStore(reducer);
```

<br />

## React에서 redux를 사용하는 방법

1. index.js에서 `<Provider store={store}>` 태그로 한번 감싸준다.(여기서 store는 createStore를 통해 생성한 redux store)

```jsx
import React from "react";
import reactDom from "react-dom";
import { Provider } from "react-redux";
import App from "./components/App";
import store from "./store";

reactDom.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
```

<br />

2. store를 사용할 컴포넌트의 export 코드에서 connect로 mapStateToProps, mapDispatchToProps함수를 정의하고  함수를 연결시켜 준다.
    - connect로 `state`와 `dispatch`를 연결시켜 주면 함수형 컴포넌트의 `Props`로 state, dispatch를 받아올 수 있다.
        - 여기서 state는 todos이다.

```jsx
const Home = ({ todos, dispatch }) => {
  return (
    <>
      <h1>Todo</h1>
      <form onSubmit={onSubmit}>
        <input type="text" value={text} onChange={onChange} />
        <button>Add</button>
      </form>
      <ul></ul>
    </>
  );
};

const mapStateToProps = (state) => {
  return { todos: state };
};

const mapDispatchToProps = (dispatch) => {
  return { dispatch };
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
```

<br />

3. dispatch를 그대로 가져올 수 있지만, 반환문에 함수형태로 작성하여 넘겨줄 수도 있다.

```jsx
// store.js
export const actionCreators = {
  addTodo,
  deleteTodo,
};
```

```jsx
import React, { useState } from "react";
import { connect } from "react-redux";
import { actionCreators } from "../store";

const Home = ({ todos, addTodo, deleteTodo }) => {
  const [text, setText] = useState("");
  const onChange = (e) => {
    setText(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    setText("");
    addTodo(text);
  };

  return (
    <>
      <h1>Todo</h1>
      <form onSubmit={onSubmit}>
        <input type="text" value={text} onChange={onChange} />
        <button>Add</button>
      </form>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id} id={todo.id}>
            {todo.text}
            &nbsp;
            <button onClick={() => deleteTodo(todo.id)}>DEL</button>
          </li>
        ))}
      </ul>
    </>
  );
};

const mapStateToProps = (state) => {
  return { todos: state };
};

const mapDispatchToProps = (dispatch) => {
  return {
    addTodo: (text) => dispatch(actionCreators.addTodo(text)),
    deleteTodo: (id) => dispatch(actionCreators.deleteTodo(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
```