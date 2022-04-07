# 12장 immer를 사용하여 더 쉽게 불변성 유지하기

- 컴포넌트의 성능 최적화를 위해 불변성을 유지하는 것이 중요하다.
- 전개 연산자, Array 내장 함수 등을 이용해 불변성을 지키는 것이 가능하다.
    - 단, 객체의 구조가 깊어질수록 불변성을 유지하는 것이 어려워진다.
    - 객체의 구조가 깊어졌을 때 코드를 여러줄 작성할 수도 있지만, immer 라이브러리를 이용해 복잡한 코드도 간단하게 작성하여 불변성을 유지할 수 있다.

<br />

# 12.1 immer 설치와 사용방법

```jsx
yarn add immer

npm install immer
```

```jsx
import produce from "immer"

const baseState = [
  {
		id: 1,
    title: "Learn TypeScript",
    done: true
  },
  {
		id: 2,
    title: "Try Immer",
    done: false
  }
]

const nextState = produce(baseState, draftState => {
	// id가 2인 항목의 done 값 변경하기
	const first = draftState.find(state => state.id === 2);
	first.done = false;
	// index를 알고 있을 경우 그냥 draftState[1].done = false; 해도 된다.

	// 새로운 데이터 추가
  draftState.push({
		id: 3,
		title: "Tweet about it",
		done: false
	});

	// id가 1인 항목 제거
	draftState.splice(draftState.findIndex(state => state.id === 1), 1);
})
```

<br />

- produce 함수는 두 가지 파라미터를 받는다.
    - 첫 번째 인자: 수정하고 싶은 상태**(base State)**
    - 두 번째 인자: 어떻게 업데이트할 지 정하는 함수**(draft State)**
- 두 번째 인자로 전달한 함수 내부에서 base State값을 변경하면 불변성 유지를 대신하면서 새로운 상태를 생성해준다.
- 핵심은 불변성에 신경 쓰지 않는 것처럼 코드를 작성하지만 불변성 관리를 제대로 해 주는 것이다.
- immer를 사용하면 객체 내부의 값을 직접 수정하거나 push, pop, splice 같이 원본을 수정하는 메서드를 사용해도 무방하다.
    - immer의 사용이 무조건 코드가 간결해지지는 않으므로 적절하게 사용하는 것이 좋다.
    - filter를 사용하는 것이 더 간단하다 ⇒ immer 쓰지 않고 filter 쓴다.