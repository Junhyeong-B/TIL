# 15장 Context API

- Context API는 전역적으로 사용할 데이터가 있을 때 유용한 기능이다.
- 리덕스, 리액트 라우터, styled-components 등의 라이브러리는 Context API를 기반으로 구현되어 있다.

<br />

# 15.2 Context 사용법 익히기

## 15.2.1 Context 만들기

- `src/contexts/color.js`

```jsx
import { createContext } from 'react';

const ColorContext = createContext({ color: 'black' });

export default ColorContext;
```

- Context를 만들 때는 createContext 함수를 사용한다.
- createContext 함수의 파라미터에는 기본값을 지정한다.

<br />

## 15.2.2 Consumer 사용하기

- `src/components/ColorBox.js`

```jsx
import ColorContext from '../contexts/color';

const ColorBox = () => {
  return (
    <ColorContext.Consumer>
      {(value) => (
        <div
          style={{
            width: '64px',
            height: '64px',
            background: value.color,
          }}
        />
      )}
    </ColorContext.Consumer>
  );
};

export default ColorBox;
```

- `src/App.js`

```jsx
import ColorBox from './components/ColorBox';

const App = () => {
	return (
		<div>
			<ColorBox />
		</div>
	);
};
```

<br />

- Consumer 사이에 중괄호를 열어서 그 안에 함수를 넣어 주었는데, 이러한 패턴을 Function as a child 또는 Render Props라고 한다.
    - 컴포넌트의 children이 있어야 할 자리에 일반 JSX 혹은 문자열이 아닌 함수를 전달하는 것을 말한다.
    - 예제
        
        ```jsx
        /* Render Props를 사용할 컴포넌트 작성 부분 */
        const RenderPropsSample = ({ children }) => {
        	return <div>결과: {children(5)}</div>;
        };
        
        export default RenderPropsSample;
        
        /* 사용하는 부분 */
        <RenderPropsSample>{value => value * 2}</RenderPropsSample>;
        ```
        
        - 위와 같이 사용하면 결과: 10 이 출력되고, 일반적인 children이 아닌 함수를 전달하여 사용한 예제이다.

<br />

## 15.2.3 Provider

- Provider를 사용하면 Context의 value를 변경할 수 있다.
- 앞서 createContext 함수를 작성할 때 기본값을 파라미터로 작성했는데, Provider를 사용하지 않았을 때만 사용된다.
    - 만약 Provider를 사용했는데 value를 명시하지 않았다면 기본값을 사용하지 않기 때문에 오류가 발생한다.
- `src/App.js`

```jsx
import ColorBox from './components/ColorBox';
import ColorContext from '../contexts/color';

const App = () => {
	return (
		<ColorContext.Provider value={{ color: 'red' }}>
			<div>
				<ColorBox />
			</div>
		</ColorContext.Provider>
	);
};

/* 에러가 발생하는 경우 */
const App = () => {
	return (
		<ColorContext.Provider>
			<div>
				<ColorBox />
			</div>
		</ColorContext.Provider>
	);
};
```

<br />

# 15.3 동적 Context 사용하기

- Context value에는 값뿐만 아니라 함수를 전달해줄 수도 있다.
- `src/contexts/color.js`

```jsx
import { createContext, useState } from 'react';

const ColorContext = createContext({
  state: { color: 'black', subcolor: 'red' },
  actions: {
    setColor: () => {},
    setSubcolor: () => {},
  },
});

const ColorProvider = ({ children }) => {
  const [color, setColor] = useState('black');
  const [subcolor, setSubcolor] = useState('red');

  const value = {
    state: { color, subcolor },
    actions: { setColor, setSubcolor },
  };
  return (
    <ColorContext.Provider value={value}>{children}</ColorContext.Provider>
  );
};

// const ColorConsumer = ColorContext.Consumer와 같은 의미
const { consumer: ColorConsumer } = ColorContext;

export { ColorConsumer, ColorProvider };

export default ColorContext;
```

- ColorProvider는 ColorContext.Provider를 렌더링하고 있고, value에는 상태값 state, 업데이트 함수를 actions로 묶어서 전달하고 있다.
- createContext에서 작성한 기본 값은 실제 value에 넣는 객체 형태로 작성해주는 것이 좋다.
    - Context 코드를 봤을 때 내부 값의 구성을 한눈에 보기 쉽다.
    - 실수로 Provider를 사용하지 않았을 때 어플리케이션이 동작하지 않는 에러를 방지할 수 있다.

- `src/App.js`

```jsx
import ColorBox from './components/ColorBox';
import { ColorProvider } from '../contexts/color';

const App = () => {
	return (
		<ColorProvider>
			<div>
				<ColorBox />
			</div>
		</ColorProvider>
	);
};
```

- `src/components/ColorBox.js`

```jsx
import **{ ColorConsumer }** from '../contexts/color';

const ColorBox = () => {
  return (
    **<ColorConsumer>**
      {(value) => (
				<>
	        <div
	          style={{
	            width: '64px',
	            height: '64px',
	            background: value**.state**.color,
	          }}
	        />
					<div
	          style={{
	            width: '32px',
	            height: '32px',
	            background: value**.state**.subcolor,
	          }}
	        />
				</>
      )}
    **</ColorConsumer>**
  );
};

export default ColorBox;
```

<br />

## 15.3.3 색상 선택 컴포넌트 만들어 state, actions 컨트롤하기

- `src/components/SelectColor.js`

```jsx
import { ColorConsumer } from './a';

const colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'];

const SelectColor = () => {
  return (
    <div>
      <ColorConsumer>
        {({ actions }) => (
          <div style={{ display: 'flex' }}>
            {colors.map((color) => (
              <div
                key={color}
                style={{ background: color, width: '24px', height: '24px' }}
                onClick={() => actions.setColor(color)}
                onContextMunu={(e) => {
                  e.preventDefault(); // 마우스 오른쪽 버튼 클릭 시 메뉴가 뜨는 것을 무시함
                  actions.setSubcolor(color);
                }}
              />
            ))}
          </div>
        )}
      </ColorConsumer>
    </div>
  );
};

export default SelectColor;
```

<br />

# 15.4 Consumer 대신 Hook 사용하기

## 15.4.1 useContext Hook

- useContext를 사용하면 Context를 매우 편하게 사용할 수 있다.
- 만약 children에 함수를 전달하는 Render Props 패턴이 불편하다면 useContext Hook을 사용하여 편하게 Context 값을 조회할 수 있다.
- `src/components/ColorBox.js`

```jsx
import { useContext } from 'react';
import ColorContext from '../contexts/color';

const ColorBox = () => {
	const { state } = useContext(ColorContext);
  return (
    **<>**
      {(value) => (
				<>
	        <div
	          style={{
	            width: '64px',
	            height: '64px',
	            background: **state**.color,
	          }}
	        />
					<div
	          style={{
	            width: '32px',
	            height: '32px',
	            background: **state**.subcolor,
	          }}
	        />
				</>
      )}
    **</>**
  );
};

export default ColorBox;
```