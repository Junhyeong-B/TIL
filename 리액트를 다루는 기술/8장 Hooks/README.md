# 8장 Hooks

- Hooks는 리액트 v16.8에 새로 도입된 기능이다.

## 8.1 [state, setState] = useState(initialState)

- 함수형 컴포넌트에서 가변적인 상태를 지닐 수 있게 해주는 상태 관리 Hook이다.
- 하나의 useState 함수는 하나의 상태 값만 관리할 수 있다.

<br />

## 8.2 useEffect(callback, dependency)

- 리액트 컴포넌트가 렌더링될 때마다 특정 작업을 수행하도록 설정할 수 있는 Hook이다.
- 클래스형 컴포넌트에서 componentDidMount, componentDidUpdate의 기능을 합친 형태라고 봐도 무방하다.
- 두 번째 파라미터로 종속성 배열을 넣어주는데, 빈 배열이 들어가면 마운트 될 때(componentDidMount) 1회 실행되고,
    
    배열 내부에 값을 작성하면 해당 값이 업데이트될 때마다(componentDidUpdate) 실행된다.
    
- useEffect 내부에서 return 문을 작성하면 업데이트 되기 직전 return문이 호출(뒷정리 함수)된다.
    - 특정 값이 변경될 때마다 실행된다면 변경되기 직전 값을 사용할 수 있다.
    - 오직 언마운트될 때만 뒷정리 함수를 호출하고 싶다면, 빈 배열을 종속성으로 작성하고 return문을 작성해주면 된다.

<br />

## 8.3 [state, dispatch] = useReducer(reducer, initialState)

- 현재 상태, 업데이트를 위한 액션값을 전달받아 새로운 상태를 반환하는 함수이다.
- state는 현재 상태, dispatch는 액션을 발생시키는 함수이다.
    - `dispatch({ type: "INCREMENT" })` 형태로 사용한다.
- useReducer의 가장 큰 장점은 컴포넌트 업데이트 로직(reducer)을 컴포넌트 바깥으로 빼낼 수 있다는 점이다.

```jsx
function reducer(state, action) {
	return {
		...state,
		[action.type]: action.value,
	}
}

function MyApp() {
	const [state, dispatch] = useReducer(reducer, { a: 0 })
	/* ... */
}
```

- 위와 같이 action.type을 switch문으로 구분하지 않고 setState와 유사한 방식으로 사용할 수도 있다.
    - action에는 어떤 값도 사용 가능하다.
- `useReducer(callback, undefined, createStateFunction)` 형태로 사용할 수도 있는데, 세 번째 파라미터로 초기값을 반환하는 함수를 작성하고 두 번째 파라미터에 undefined를 작성하면 처음 렌더링될 때만 `createStateFunction`를 호출하여 반환하는 값을 초기값으로 설정할 수 있다.

<br />

## 8.4 useMemo(callback, dependency)

- 컴포넌트 내부에서 발생하는 연산을 최적화할 수 있다.
- 두 번째 파라미터로 작성한 종속성 배열 내부의 값이 변경될 때만 callback의 연산을 실행하고, 그 외의 경우엔 연산을 실행하지 않는다.
    - 따라서, 특정 연산을 실행하는 것과 상관 없이 리렌더링될 때 useMemo를 사용하여 연산을 최적화할 수 있다.

<br />

## 8.5 useCallback(callback, dependency)

- 만들어 놓은 함수를 재사용할 수 있다.
- 컴포넌트 내부에 선언된 함수는 컴포넌트가 리렌더링될 때 재정의된다.
    - 이 때 useCallback으로 해당 함수를 첫 번째 파라미터로 작성해주면 두 번째 파라미터로 작성한 종속성 배열 내부의 값이 바뀔 때만 재정의되어 최적화할 수 있다.

<br />

## 8.6 ref = useRef(initialState)

- 컴포넌트에 ref를 쉽게 사용할 수 있도록 해준다.
- 특정 element에 ref를 지정하면 ref.current 값이 해당 element 값으로 저장된다.
- 로컬 변수로 사용할 때도 useRef를 사용할 수 있다.
    - 로컬 변수: 값이 변경되어도 렌더링되지 않는 변수
    - initialState로 작성한 값은 최초 ref.current의 값이 되고, 이후 ref.current 값이 바뀌더라도 렌더링은 일어나지 않는다.

<br />

## 8.7 커스텀 Hook

- 여러 컴포넌트에서 비슷한 기능을 공유할 경우, 커스텀 Hook으로 만들어 재사용할 수 있다.

```jsx
/* useInputs 커스텀 Hook 만들기 */
import { useReducer } from "react";

const reducer = (state, action) => {
  return {
    ...state,
    [action.type]: action.value,
  };
};

const useInputs = (initialForm) => {
  const [state, dispatch] = useReducer(reducer, initialForm);

  const onChange = (e) => {
    dispatch(e.target);
  };

  return [state, onChange];
};

export default useInputs;

/* 사용하려는 컴포넌트 내부 */
const MyApp = (props) => {
	const [state, onChange] = useInputs({
	  name: "",
	  email: "",
	});
	/* ... */
}
```

<br />

## 8.8 그 외 다른 Hooks

- [https://nikgraf.github.io/react-hooks/](https://nikgraf.github.io/react-hooks/)
- https://github.com/rehooks/awesome-react-hooks