# 5장 ref: DOM에 이름 달기

# 5.1 ref는 어떤 상황에서 사용해야 할까

- DOM 을 직접적으로 건드려야 할 때 사용한다.
    - 특정 input에 포커스 주기
    - 스크롤 박스 조작하기
    - Canvas 요소에 그림 그리기

<br />

# 5.2 ref 사용

### Class형 컴포넌트 내부에서의 ref 지정

- class형 컴포넌트로 작성할 때 ref를 콜백 함수로 지정할 수 있다.

```jsx
<input ref={(ref) => {this.input = ref} />
```

- 위와 같이 작성하면 클래스 컴포넌트 내부의 `this.input`은 input 요소의 DOM을 가리킨다.

<br />

### Class형 컴포넌트에서 createRef를 통한 ref 설정

- React v16.3 버전 이후에 도입된 `createRef` 메서드를 통해 ref를 설정할 수 있다.

```jsx
class RefSample extends Component {
	input = React.createRef();

	handleFocus = () => {
		this.input.current.focus();
	}

	render() {
		return (
			<div>
				<input ref={this.input} />
			</div>
		)
	}
}
```

- 사용할 때는 ref.current를 통해 접근하여 사용한다.

<br />

# 5.3 컴포넌트에 ref 달기

- 컴포넌트에도 ref를 설정할 수 있고, DOM에 ref 지정하듯 사용하면 된다.

```jsx
<MyComponent
	ref={(ref) => {this.myComponent = ref}}
/>
```

- 이렇게 설정하면 this.myComponent에 `MyComponent` DOM 요소를 ref로 설정하게 되고 내부의 ref에 접근하여 메소드를 사용할 수도 있다.

<br />

```jsx
/* ScrollBox 컴포넌트 내부 ref 지정 */
class ScrollBox extends Component {
	scrollToBottom = () => {
		const { scrollHeight, clientHeight } = this.box;
		this.box.scrollTop = scrollHeight - clientHeight;
	}

	render() {...}
}

/* ScrollBox 컴포넌트 외부에서 ref로 ScrollBox 내부의 메서드 호출 */
class App extends Component {
	render() {
		return (
			<div>
				<ScrollBox ref={(ref) => {this.scrollBox=ref}} />
				<button onClick={() => this.scrollBox.scrollToBottom()}>
					맨 밑으로
				</button>
			</div>
		)
	}
}
```

<br />

- App 컴포넌트 내부의 button에서 `onClick={this.scrollBox.scrollToBottom}` 라고 작성할 수도 있지만, ref를 사용하면 최초 렌더링될 때는 ref값이 undefined 이므로 값을 읽어 오는 과정에서 오류가 발생한다. ⇒ 그래서 `onClick={() => this.scrollBox.scrollToBottom()}` 로 작성해서 버튼을 누를 때 ref 값을 읽어오도록 작성해야 오류가 발생하지 않는다.

<br />

# 5.4 정리

- 꼭 DOM에 직접적으로 접근해야할 경우를 제외하면 ref를 사용하여 컴포넌트 끼리 데이터를 교류하는 것은 올바른 사용 방법이 아니다.
    - 프로젝트 규모가 커질수록 스파게티처럼 구조가 꼬여서 유지보수가 어렵기 때문
- 컴포넌트간 데이터를 교류할 때는 반드시 부모, 자식 흐름으로 교류하고, Context API, Redux 등의 전역 상태를 사용하여 이를 더 효율적으로 관리할 수 있다.