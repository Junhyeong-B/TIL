# 11장 컴포넌트 성능 최적화

# 11.1 많은 데이터 렌더링하기

- useState의 초기값으로 함수를 작성할 수도 있는데 호출 형태가 아닌 함수 형태로 작성해줘야 처음 렌더링 때만 동작한다.
    - 호출 형태로 작성하면 렌더링이 일어날때마다 호출이 일어난다.

```jsx
const createLists = () => {
	const array = [];
	/* ... */
	return array;
}

// 아래 코드는 처음 렌더링 될 때만 createLists 함수가 호출 된다.
const MyApp = () => {
	const [list, setList] = useState(createLists)
}

// 아래 코드는 처음 렌더링할 때와 리렌더링이 일어날 때마다 createLists 함수가 호출 된다.
const MyApp = () => {
	const [list, setList] = useState(createLists())
}
```

<br />

# 11.2 크롬 개발자 도구를 통한 성능 모니터링

- 개발자 도구에서 React DevTools를 사용하여 성능을 측정할 수 있다.
- v17 이전엔 User Timing API를 사용했고, v17 이후에 React DevTools를 활용할 수 있게 되었다.
- 리액트 개발자 도구에서 Profiler 탭에서 녹화 버튼을 누르고 화면 변화가 감지되면 성능을 측정하여 나타내준다.

<br />

# 11.3 느려지는 원인 분석

- 컴포넌트는 다음 4가지 경우 리렌더링된다.
    1. 자신이 전달받은 props가 변경될 때
    2. 자신의 state가 바뀔 때
    3. 부모 컴포넌트가 렌더링될 때
    4. forceUpdate 함수가 실행될 때

<br />

# 11.4 React.memo를 통해 컴포넌트 성능을 최적화

- 컴포넌트를 export default할 때 React.memo로 한 번 감싸주면 해당 컴포넌트는 props가 변경되지 않았다면 리렌더링하지 않도록 설정할 수 있다.

```jsx
import React from 'react';

const MyApp = (props) => {/* ... */}

export default React.memo(MyApp);
// MyApp 컴포넌트는 props가 변경되지 않으면 리렌더링을 하지 않게된다.
```

<br />

# 11.5 함수가 바뀌지 않게 하여 최적화

- 특정 상태를 참조하고 있는 함수는 해당 상태가 업데이트되면 함수도 새로 만들어진다.
- 이럴 때 useState의 함수형 업데이트 기능, useReducer 사용으로 최적화할 수 있다.

<br />

## 11.5.1 useState의 함수형 업데이트

- useState에서 setState(값) 형태로 업데이트하는 것이 아니라 setState(() ⇒ 값) 형태로 함수를 작성하는 것을 함수형 업데이트라고 한다.
- 해당 기능을 사용하면 useCallback에서 참조하고 있는 값을 종속성 배열에서 제거할 수 있어 상태값이 바뀌더라도 함수가 다시 생성되지 않는다.

```jsx
const [count, setCount] = useState(0);
```

```jsx
/* 기존 */
const increase = useCallback(() => {
		setCount(count + 1);
	},
	[count]
);
```

```jsx
/* 함수형 업데이트로 최적화 */
const increase = useCallback(() => {
		setCount(prevState => prevState + 1);
	},
	[]
);
```

<br />

## 11.5.2 useReducer 사용하기

- useReducer에서 첫 번째 파라미터인 reducer 함수는 컴포넌트 외부에서 작성할 수 있어 리렌더링되어도 함수가 새로 생성되지 않는다.

```jsx
/* 기존 */
const MyApp = () => {
	const [list, setLists] = useState([]);

	const increase = useCallback((newItem) => {
			setCount(list.concat(newItem));
		},
		[count]
	);
}
```

```jsx
/* useReducer로 최적화 */
const reducer = (state, action) => {
	switch (action.type) {
		case 'INCREASE':
			return state.concat(action.newItem);
		default:
	}
}

const MyApp = () => {
	const [list, dispatch] = useReducer(reducer, []);

	/* ... */
	dispatch({ type: 'INCREASE', newItem: 'new' });
}
```

<br />

# 11.6 불변성의 중요성

- state를 관리할 때 기존의 값을 변경하는 것이 아니라 새로운 값을 만들어 업데이트하여 불변성을 유지하는 것이 중요하다.
- 새로운 값을 만드는 것이 아니라면 배열이나 객체를 상태로 갖고 있을 때, 해당 배열, 객체의 값이 바뀌어도 바뀌었는지 아닌지를 인지할 수가 없다.
    - 바뀐 것을 인지할 수 없다면 React.memo를 통한 최적화도 불가능하다.(props가 바뀌어도 바뀌었는지 인지할 수 없기 때문)

<br />

# 11.7 list 컴포넌트 최적화

- 내부 데이터가 100개를 넘지 않는 소규모 list 컴포넌트라면 작성하지 않아도 성능상 문제가 없을 수 있다.
- 리스트 관련 컴포넌트를 작성할 때는 리스트 아이템 | 리스트 두 가지 모두 최적화해야 한다.
    - 대표적으로 React.memo

<br />

# 11.8 react-virtualized를 사용한 렌더링 최적화

- 만약 특정 페이지가 마운트 되었을 때 상태가 많아서 스크롤될 경우 사용자에게 보여지지 않는 부분까지 렌더링하므로 비효율적이다.
    - ex) 1000개의 리스트를 렌더링하는 페이지에서 보여지는 부분이 10개 라면 990개의 리스트는 화면에 보이지도 않는데 렌더링해야 한다.
- react-virtualized를 사용하면 화면에 보여지지 않는 부분은 렌더링시키지 않고 크기만 차지하고 있다가 스크롤 했을 때 렌더링되도록 만들 수 있다.
    - https://github.com/bvaughn/react-virtualized
    - [https://bvaughn.github.io/react-virtualized/#/components/List](https://bvaughn.github.io/react-virtualized/#/components/List)

```jsx
npm install react-virtualized --save

yarn add react-virtualize
```

```jsx
import { List } from 'react-virtualized';

const ListItems = () => {
	const [lists, setLists] = useState([]);
	/* ... */
	// react-virtualized를 사용하려면 항목을 렌더링할 때 쓰는 함수를 새로 작성해야 한다.
	const rowRenderor = useCallback(({index, key, style}) =>{
		/* ... */
		const list = lists[index];
		
		return (
			<ListItem
				list={list}
				key={key}
				style={style}
			/>
		)},
		[dependency]
	);

	return (
		<List
			width={전체너비}
			height={전체높이}
			rowCount={전체 항목 개수}
			rowHeight={리스트 항목당 높이}
			rowRenderor={항목을 렌더링할 때 쓰는 함수}
			list={리스트 배열}
			style={{ outline: 'none' }} // List에 기본 적용되어 있는 outline 제거
		/>
	)
}

export default React.meomo(ListItems);
```

- rowRenderor 함수를 새로 작성하여 prop으로 넘겨줘야 하는데 작성된 함수는 index, key, style을 객체 타입으로 받아와서 사용한다.