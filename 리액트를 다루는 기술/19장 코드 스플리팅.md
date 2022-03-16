# 19장 코드 스플리팅

- 리액트 프로젝트를 완성하여 사용자에게 제공할 때 빌드 작업을 거쳐서 배포해야 한다.
- 빌드를 통해 자바스크립트 파일 내부의 불필요한 주석, 경고 메세지, 공백 등을 제거하여 파일 크기를 최소화하거나 JSX 문법이나 최신 문법 등을 트랜스파일 작업이 진행한다.
- 이 작업은 웹팩(webpack)과 같은 번들링 도구가 담당한다.
- CRA의 경우 SplitChunks라는 기능이 적용되어 일정 크기 이상의 파일, 여러 파일 간에 공유된 파일을 자동으로 분리시켜서 캐싱의 효과를 준다.

<div align="center">
  <img width="200" src="https://user-images.githubusercontent.com/85148549/158531057-46d11850-0a50-4d21-8f45-ebc9a9113b21.png">
</div>

<br />

- CRA의 초기 상태에서 build하면 위 이미지와 같이 번들링이 진행된다.
- 여기서 특정 js 파일에는 `'273c5611'`와 같이 해시 값이 포함되어 있는데 이를 통해 브라우저가 새로 파일을 받아야 할지 받지 말아야 할지를 알 수 있다.
- 위 이미지의 경우 main으로 시작하는 파일, 787로 시작하는 파일로 나뉘는데 main으로 시작하는 파일은 직접 프로젝트에 작성하는 App 같은 컴포넌트에 대한 코드가 들어있고, 787로 시작하는 파일에는 React, ReactDom 등 node_modules에서 불러온 라이브러리 관련 코드들이 들어있다.
    - 따라서 컴포넌트의 내용이 바뀐 뒤 build하면 787로 시작하는 파일은 그대로 있고 main으로 시작하는 파일이 바뀌게 된다.

- 위와 같이 파일을 분리하는 작업을코드 스플리팅이라고 한다.
- 그러나 SplitChunks 기능은 단순 캐싱 효과만 있을 뿐이고, 만약 A페이지에 진입한 유저가 B, C 페이지로 이동하지 않을 때 B, C 페이지에 대한 정보는 필요하지 않지만 SplitChunks는 이를 구분하지 않고 모든 페이지를 한 파일로 저장한다.
    - 이렇게 되면 첫 페이지 진입 시 로딩이 오래 걸려 유저 경험이 안좋아지고 트래픽도 높아질 수 있다.
- 이를 해결하기 위한 방법 중 하나로 **비동기 로딩**이 있다.

<br />

# 19.1 자바스크립트 함수 비동기 로딩

- `src/notify.js`

```jsx
export default function notify() {
	alery("notify");
}
```

- `src/App.js`

```jsx
import notify from './notify';

function App() {
	const onClick = () => {
		notify();
	};

	return (
		<div className="App">
			<p onClick={onClick}>Notify</p>
		</div>
	)
}
```

- 위와 같이 작성한 후 build하면 notify 코드가 main 파일 안에 들어가게 된다.
- 이를 다음과 같이 수정해보자.
- src/App.js

```jsx
function App() {
	const onClick = () => {
		import('./notify').then(result => result.default());
	};

	return (
		<div className="App">
			<p onClick={onClick}>Notify</p>
		</div>
	)
}
```

- 이는 아직 표준 자바스크립트가 아니지만 stage-3단계에 있는 dynamic import 문법이다.
- 웹팩에서 지원하고 있어 별도의 설정 없이 바로 사용할 수 있다.
- dynamic import는 Promise를 반환하고, 모듈에서 default로 내보낸 것은 result.default를 참조해야 사용할 수 있다.
- 이렇게 작성하면 실제 **함수가 필요한 시점에 파일을 불러와**서 함수를 사용하게 되고, 실제 동작해보면 Click이벤트 발생 시 새로운 Javascript 파일을 불러오고, **build 시에도 파일이 분리되어 저장**된다.

<br />

# 19.2 React.lazy와 Suspense를 통한 컴포넌트 코드 스플리팅

- React.lazy(유틸 함수), Suspense(컴포넌트)는 리액트 v16.6 부터 도입되었다.
- import 함수를 통해 불러온 다음 컴포넌트 자체를 state에 넣는 방식으로 구현해야 한다.

<br />

## 19.2.1 state를 사용한 코드 스플리팅

- `src/SplitMe.js`

```jsx
const SplitMe = () => {
  return <div>Split Me</div>;
};

export default SplitMe;
```

- `src/App.js` ⇒ class 형태로

```jsx
import { Component } from "react";

class App extends Component {
  state = {
    SplitMe: null,
  };

  handleClick = async () => {
    const loadedModule = await import("./SplitMe");
    this.setState({
      SplitMe: loadedModule.default,
    });
  };

  render() {
    const { SplitMe } = this.state;
    return (
      <div className="App">
        <p onClick={this.handleClick}>Hello React!</p>
        {SplitMe && <SplitMe />}
      </div>
    );
  }
}

export default App;
```

- 이 경우 그리 어렵지는 않지만 매번 state를 작성해야 한다는 점이 불편하다.

<br />

## 19.2.2 React.lazy와 Suspense 사용하기

### React.lazy

- 컴포넌트를 렌더링하는 시점에 비동기적으로 로딩할 수 있게 해주는 유틸 함수이다.

```jsx
const SplitMe = React.lazy(() => import('./SplitMe'));
```

<br />

### Suspense

- 리액트 내장 컴포넌트로 코드 스플리팅된 컴포넌트를 로딩하도록 발동시킬 수 있고, 로딩이 끝나지 않았을 때 보여줄 UI를 설정할 수 있다

```jsx
import { Suspense } from 'react';

<Suspense fallback={<div>loading...</div>}>
	<SplitMe />
</Suspense>
```

<br />

### 사용해보자

- src/App.js

```jsx
import React, { useState } from "react";
import { Suspense } from "react";

const SplitMe = React.lazy(() => import("./SplitMe"));

function App() {
  const [visible, setVisible] = useState(false);
  const handleClick = () => {
    setVisible((prevState) => !prevState);
  };
  return (
    <div className="App">
      <p onClick={handleClick}>Hello React!</p>
      <Suspense fallback={<div>Loading...</div>}>
        {visible && <SplitMe />}
      </Suspense>
    </div>
  );
}

export default App;
```

<div align="center">
  <img width="500" src="https://user-images.githubusercontent.com/85148549/158531063-3bf5ea69-e3b4-4842-955d-fcf9db6f7a33.gif">
</div>

- 로딩중일 때 지정한 Loading...이 뜨고, 클릭했을 때 Split된 파일을 받아온다.

<br />

## 19.2.3 Loadable Components를 통한 코드 스플리팅

- Loadable Components는 코드 스플리팅을 편하게 하도록 도와주는 서드파티 라이브러리이다.
- 서버 사이드 렌더링(SSR)을 지원한다.(React.lazy, Suspense는 아직 SSR을 지원하지 않는다.)
- 렌더링하기 전 필요할 때 스플리팅된 파일을 미리 불러올 수도 있다.
- [https://loadable-components.com/](https://loadable-components.com/)

<br />

### Loadable 사용하기

```jsx
yarn add @loadable/component
```

```jsx
import React, { useState } from "react";
import loadable from "@loadable/component";

const SplitMe = loadable(() => import("./SplitMe"), {
  fallback: <div>Loading...</div>,
});

function App() {
  const [visible, setVisible] = useState(false);
  const handleClick = () => {
    setVisible((prevState) => !prevState);
  };
  return (
    <div className="App">
      <p onClick={handleClick}>Hello React!</p>
      {visible && <SplitMe />}
    </div>
  );
}

export default App;
```

- React.lazy와 유사하지만 Suspense를 사용하지 않아도 동작한다.

<br />

### 미리 불러오기

```jsx
import React, { useState } from "react";
import loadable from "@loadable/component";

const SplitMe = loadable(() => import("./SplitMe"), {
  fallback: <div>Loading...</div>,
});

function App() {
  const [visible, setVisible] = useState(false);
  const handleClick = () => {
    setVisible((prevState) => !prevState);
  };
  const onMouseOver = () => {
    **SplitMe.preload();**
  };
  return (
    <div className="App">
      <p onClick={handleClick} onMouseOver={onMouseOver}>
        Hello React!
      </p>
      {visible && <SplitMe />}
    </div>
  );
}

export default App;
```

- onMouseOver 함수가 추가되었다.
- 해당 컴포넌트에 mouseover 이벤트 발생 시 스플리팅된 파일이 미리 로딩된다.
- SSR을 사용한다면 Loadable Components를, 그게 아니라면 React.lazy, Suspense를 사용하여 플리팅을 구현할 수 있다.
- 리액트 공식 문서에서도 Loadable Components 라이브러리를 사용하도록 권장하고 있다.