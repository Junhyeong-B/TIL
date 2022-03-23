# React.lazy | Suspense를 사용한 Code Splitting

# 1. 번들링(Bundling)

- 번들링이란 어플리케이션을 구성하는 여러 개로 나뉘어있는 HTML, CSS, Javascript 등의 파일들을 하나의 Javascript 파일로 압축, 난독화하여 모아주는 것을 말한다.
- 어플리케이션의 규모가 커져서 Resource가 여러개라면, 모든 Resource를 서버에 요청해야하고, 요청이 많아질수록 더 많은 시간이 소요되므로 하나의 파일로 번들링하여 요청 횟수를 줄이는 것이다.
- 그런데, 어플리케이션의 규모가 커질수록 번들도 같이 커지게 되므로 최초 요청에 대한 시간이 증가하게 된다.
- 그러면 어떻게 해야 번들 사이즈가 커져도 성능을 유지하거나 상승시킬 수 있을까?

<br />

# 2. 지연 로딩(Lazy Loading)

- 특별히 설정한 값이 없다면 웹팩은 모든 파일을 하나의 파일에 저장하여 요청을 보내게 되는데, 이 중 당장 필요하지 않은 컴포넌트, 페이지 등을 지연 로딩(Lazy Loading)시켜 다른 파일로 저장하게 하여 필요한 순간에 요청하여 사용할 수 있다.
- 이를 코드 비동기 로딩이라고 하는데, React에서는 제공되는 `React.lazy`, `Suspense` 컴포넌트를 통해 비동기 로딩을 구현할 수 있다.
- Webpack 번들러에는 Code Splitting 기능이 있고, 이를 chunk 파일로 분리하여 비동기적으로 코드 로딩이 가능하다.
- 그럼 chunk 파일로 분리하기 위해선 어떻게 해야할까?

<br />

# 3. Dynamic Import

- Dynamic Import는 표준 자바스크립트는 아니지만, TC39 Javascript 위원회의 Stage-3에 자체 제안을 갖고 있는 기능으로, 해당 기능을 사용하면 import문을 바로 실행하는 것이 아닌 그대로 두었다가 필요할 때 import해올 수 있게 된다.
- 표준 자바스크립트가 아니어도 Webpack에서 지원하고 있으므로 별도의 설정 없이 사용할 수 있다.
- `create-react-app`으로 React 프로젝트를 셋팅하고 Dynamic Import 부터 Code Splitting을 사용해보자.

<br />

## 3-1) Dynamic Import 사용하기 전

```tsx
yarn create react-app
```

- `src/add.js`

```jsx
export default function add(a, b) {
  return a + b;
}
```

- `src/App.js`

```jsx
import { useState } from "react";
import add from "./add";

function App() {
  const [state, setState] = useState(0);

  const clickHandler = () => {
    setState(add(1, 2));
  };

  return (
    <div>
      <p>1 + 2 는? {state !== 0 && state}</p>
      <button onClick={clickHandler}>계산해보기</button>
    </div>
  );
}

export default App;
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/159623177-8887c895-65ac-45e8-b7b3-fc4e8d93af9a.png">
</div>

- 위와 같이 src 폴더에 add.js 파일 내부에 add 함수를 만들고 이를 App.js에서 import하여 사용하는 코드를 작성했다.
- 개발 서버를 열어 개발자 도구를 통해 확인해보면 Webpack에 의해 bundle.js라는 파일을 요청하고 있고, 내부를 살펴보면 아직 사용하지도 않은 add 함수가 들어있다.

<br />

## 3-2) Dynamic Import 사용하고 난 후

- `src/add.js` 변경 없음
- `src/App.js`

```jsx
import { useState } from "react";

function App() {
  const [state, setState] = useState(0);

  const clickHandler = async () => {
    const add = await import("./add.js").then((res) => res.default);
    setState(add(1, 2));
  };

  return (
    <div>
      <p>1 + 2 는? {state !== 0 && state}</p>
      <button onClick={clickHandler}>계산해보기</button>
    </div>
  );
}

export default App;
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/159623184-bd9c3d73-b357-4fad-91f4-2a43ca7b93f1.gif">
</div>

- add 함수를 코드 최상단에서 바로 import하는 것이 아니라 사용하는 곳에서 import(./add.js) 형태로 작성해줬다.
- 이렇게 작성하면 bundle.js 요청에서 add 함수를 찾아볼 수 없게 되고, 사용하는 순간에 chunk 파일로 요청하는 것을 확인할 수 있다.
- Promise 형태로 동작하기에 then 메서드 체이닝으로 결과 값을 반환해주었는데, 모듈에서 default로 export한 것은 .default 파라미터에 접근해야 사용할 수 있다.

<br />

# 4. React.lazy | Suspense

- 여기까지의 내용을 React에서 제공하는 React.lazy, Suspense를 사용하여 더 간편하게 구현할 수 있다.
    - `React.lazy`: 컴포넌트를 렌더링하는 시점에 비동기적으로 로딩할 수 있게 해주는 유틸 함수
    - `Suspense`: React 내장 컴포넌트로 코드 스플리팅된 컴포넌트를 로딩하도록 발동하거나 로딩이 끝나지 않았을 때 보여줄 UI를 설정할 수 있다.
- Suspense 컴포넌트는 React.lazy로 불러올 컴포넌트를 감싸는 형태이다.
- React.lazy는 현재 default exports만 지원한다.

- `src/SplitComponent.js`

```jsx
export default function SplitComponent() {
  return <div>React.lazy로 지연 로딩된 컴포넌트</div>;
}
```

- `src/App.js`

```jsx
import React, { Suspense, useState } from "react";
const SplitComponent = React.lazy(() => import("./SplitComponent"));

function App() {
  const [visible, setVisible] = useState(false);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      {visible && <SplitComponent />}
      <button onClick={() => setVisible(true)}>나타내기</button>
    </Suspense>
  );
}

export default App;
```

- Suspense의 fallback Prop에는 비동기로 요청한 React.lazy가 로딩되는 동안 보여줄 UI를 설정할 수 있다.
- 이렇게 작성하면 최초 SplitComponent는 bundle.js에 포함되지 않게 되고, SplitComponent가 사용될 때 chunk파일로 요청되어 나타나게 된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/159623182-a61a3621-f5db-46ca-b542-c9d0ca8dc998.png">
</div>

<br />

# 5. 언제 사용하면 좋을까?

- 코드 분할(Code Splitting)로 번들링 되는 Javascript 파일의 크기를 줄여주고 필요할 때 요청하기에 유저가 아예 진입하지 않는 페이지나 사용하지 않는 컴포넌트는 요청하지 않아 성능을 최적화할 수 있다.
- 그렇다면 필요한 대부분의 곳에서 코드 분할을 사용하는 것이 좋은 것일까?

- React 공식 문서에는 사용자의 경험을 해치지 않는 선에서 적당한 코드 분할을 권장하고 있는데, 컴포넌트마다 코드 분할을 적용하는 것이 아니라 Route 기반의 코드가 코드 분할을 설정하기 좋은 장소라고 설명하고 있다.

```tsx
import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./routes/Home'));
const About = lazy(() => import('./routes/About'));

const App = () => (
  <Router>
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Suspense>
  </Router>
);
```

- 대부분 페이지를 한 번에 렌더링하고, 페이지가 전환되는 동안에는 다른 요소와 상호작용하지 않기 때문이다.