# 7장 컴포넌트의 라이프사이클 메서드

- 모든 리액트 컴포넌트에는 라이프사이클(생명 주기)가 존재한다.
- 컴포넌트의 수명은 페이지에 렌더링되기 전인 준비 과정에서 시작해 페이지가 사라질 때 끝난다.

<br />

# 7.1 라이프사이클 메서드의 이해

- 클래스형 컴포넌트에서 라이프사이클 메서드는 9가지로 **Will** 접두사가 붙은 메서드는 작동하기 **전** 실행되는 메서드이고, **Did** 접두사가 붙은 메서드는 작동한 **후**에 실행되는 메서드이다.
- 각 라이프사이클은 크게 **마운트**, **업데이트**, **언마운트** 세가지로 분류된다.
    - **마운트**: 페이지에 컴포넌트가 나타남
    - **업데이트**: 컴포넌트 정보를 업데이트
    - **언마운트**: 페이지에서 컴포넌트가 사라짐

<br />

## 7.1.1) Mount

- DOM이 생성되고 웹 브라우저 상 나타는 것을 마운트라고 한다.
- **constructor** → **getDerivedStateFromProps** → **render** → **componentDidMount**
    1. **constructor**: 컴포넌트를 만들 때마다 호출되는 클래스 생성자 메서드
    2. **getDerivedStateFromProps**: props에 있는 값을 state에 넣을 때 사용하는 메서드
    3. **render**: UI를 렌더링하는 메서드
    4. **componentDidMount**: 웹 브라우저상에 나타난 후 호출하는 메서드

<br />

## 7.1.2) Update

- 컴포넌트는 다음의 경우 업데이트한다.
    1. props가 바뀔 때
    2. state가 바뀔 때
    3. 부모 컴포넌트가 리렌더링될 때
    4. this.forceUpdate로 강제로 렌더링을 트리거할 때
- **getDerivedStateFromProps**
    
    → **shouldComponentUpdate**
    
    true 반환 시 render 호출, false 반환 시 여기서 작업 취소
    
    → **render**
    
    → **getSnapshotBeforeUpdate**
    
    브라우저 상 실제 DOM 변화
    
    → **componentDidUpdate**
    
    1. **getDerivedStateFromProps**: 마운트 과정에서도 호출되고, 업데이트 시작 전에도 호출되는 메서드로 props의 변화에 따라 state값에 변화를 주고 싶을 때 사용한다.
    2. **shouldComponentUpdate**: 컴포넌트가 리렌더링 해야할 지 말지를 정한다. true일 경우 리렌더링 false일 경우 리렌더링하지 않는다. 만약 this.forceUpdate() 함수를 호출하면 이 과정을 생략하고 바로 render 함수를 호출한다.
    3. **render**: 컴포넌트를 리렌더링한다.
    4. **getSnapshotBeforeUpdate**: 컴포넌트 변화를 DOM에 반영하기 직전에 호출하는 메서드
    5. **componentDidUpdate**: 컴포넌트의 업데이트 작업이 끝난 후 호출하는 메서드

<br />

## 7.1.3) UnMount

- 컴포넌트를 DOM에서 제거하는 것
- **componentWillUnmount**: 컴포넌트가 웹 브라우저 상 사라지기 전에 호출하는 메서드

<br />

# 7.2 라이프사이클 메서드 살펴보기

### 7.2.1 render() {...}

- 메서드 안에서 this.props, this.state에 접근할 수 있고, 리액트 요소를 반환한다.
- 만약 아무것도 반환하고 싶지 않다면 null, false 값을 반환한다.
- 이벤트 설정이 아닌 곳에서 setState하면 안되고, 브라우저 DOM에 접근해서도 안된다.
    
    ⇒ **DOM** 정보를 가져오거나 state에 변화를 줄 때는 **componentDidMount**에서 처리해야 한다.
    

<br />

## 7.2.2 constructor(props) {...}

- 컴포넌트를 만들 때 처음으로 실행된다.
- 초기 state를 정할 수 있다.

<br />

## 7.2.3 getDerivedStateFromProps(nextProps, prevState) {...}

- 리액트 v16.3 이후에 새로 등장한 메서드.
- props로 받아 온 값을 state에 동기화시키는 용도로 사용한다.
- 컴포넌트가 마운트될 때, 업데이트될 때 호출된다.

<br />

## 7.2.4 componentDidMount() {...}

- 컴포넌트를 만들고 첫 렌더링을 마친 후 실행한다.
- 여기서 라이브러리 등의 함수 호출, 이벤트 등록, setTimeout, setInterval, 네트워크 요청 같은 비동기 작업을 처리한다.

<br />

## 7.2.5 shouldComponentUpdate(nextProps, nextState) {...}

- props, state를 변경했을 때 리렌더링을 할지 말지 여부를 지정하는 메서드
- 반드시 true 또는 false값을 반환해야 하고, 따로 생성하지 않으면 언제나 true를 반환한다.
- 프로젝트 성능을 최적화할 때 false 값을 반환하게 한다.

<br />

## 7.2.6 **getSnapshotBeforeUpdate(prevProps, prevState) {...}**

- render에서 만들어진 결과물이 브라우저에 실제로 반영되기 직전에 호출된다.
- 이 메서드에서 반환하는 값은 componentDidUpdate에서 세 번째 파라미터인 snapshot 값으로 전달받을 수 있다.
- 주로 스크롤바 위치 유지 등 업데이트 직전 참고할 일이 있을 때 활용한다.

<br />

## 7.2.7 componentDidUpdate(prevProps, prevState, snapshot) {...}

- 리렌더링 완료 후 호출된다.
- 업데이트가 끝난 직후이므로 DOM 관련 처리를 해도 무방하다.

<br />

## 7.2.8 componentWillUnmount() {...}

- 컴포넌트를 DOM에서 제거할 때 실행한다.
- componentDidMount 에서 등록한 이벤트, 타이머, 직접 생성한 DOM 등은 여기서 제거한다.

<br />

## 7.2.9 compoinentDidCatch(error, info) {...}

- 리액트 v16에서 새롭게 도입
- 렌더링 도중 에러가 발생했을 때 어플리케이션이 먹통이 되지 않고 오류 UI를 보여줄 수 있게 해준다.
    - error: 파라미터에 어떤 에러가 발생했는지 알려준다.
    - info: 어디에 있는 코드에서 오류가 발생했는지에 대한 정보를 준다.