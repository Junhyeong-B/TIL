# 9장 컴포넌트 스타일링

- 리액트에서 컴포넌트 스타일링 하는 방식은 여러가지가 있다.
    - 일반 CSS
    - CSS 전처리기(Sass, SCSS)
    - CSS Module
    - styled-components

<br />

## 9.1 일반 CSS

- `import './app.css'` 형태로 사용한다.
- CSS 클래스를 중복되지 않게 만드는 것이 중요하다.
    1. **컴포넌트 이름을 포함**시켜 중복을 방지할 수 있다.
    2. **BEM 네이밍**(.card__title-primary 등)으로 일종의 규칙을 지켜 중복을 방지할 수 있다.
    3. **CSS Selector**를 사용하면 특정 클래스 내부에 있는 경우에만 스타일을 적용할 수 있다.
        
        ```css
        .App .logo { ... }
        ```
        

<br />

## 9.2 Sass

- CSS 전처리기로 복잡한 작업을 쉽게 할 수 있도록 해주고, 스타일 코드의 재활용성을 높여 유지 보수를 쉽게 해준다.
- `$variable`, `@mixin` 등을 활용하여 특정 속성을 변수처럼 사용할 수 있고, 스타일 블록을 함수처럼 사용할 수 있다.
    - `$variable`은 속성의 값으로 그대로 사용하고, `@mixin`은 `@include` 구문으로 사용한다.
        
        ```sass
        $red: #fa5252;
        
        @mixin square($size) {
        	$calculated: 32px * $size;
        	width: $calculated;
        	hieght: $calculated;
        }
        
        .app {
        	background-color: $red;
        	@include square(2);
        }
        ```
        
- 변수, 믹스인은 다른 파일로 따로 분리하여 작성한 뒤 필요한 곳에서 `@import './style.sass'` 형태로 불러와 사용할 수 있다.
    - `@import` 구문을 사용하면 불러온 전처리기 파일을 모두 적용하고, 해당 파일의 변수, 믹스인 등을 사용할 수 있다.

<br />

### 9.2.2 sass-loader 설정 커스터마이징

- `@import './styles/utils'` 의 형태로 import하여 여러 개의 Sass, SCSS 파일을 분리하여 작성할 수 있는데, 프로젝트의 규모가 커져 파일 구조도 복잡해진다면 상위, 하위 폴더로 한참을 거슬러 올라가야하는 단점이 있다.
    - 이를 sass-loader 설정 커스터마이징을 통해 해결할 수 있다.
    - create-react-app으로 생성한 프로젝트라면 eject키워드를 통해 webpack을 직접 설정해야 한다.
    - yarn eject 명령어 후 config 폴더 내의 webpack.config.js를 수정하여 커스터마이징할 수 있다.

```jsx
{
  test: sassRegex,
  exclude: sassModuleRegex,
  use: getStyleLoaders(
    {
      importLoaders: 3,
      sourceMap: isEnvProduction
        ? shouldUseSourceMap
        : isEnvDevelopment,
      modules: {
        mode: 'icss',
      },
    },
    'sass-loader'
  ),
	sideEffects: true,
}
```

<br />

- 최초 eject 시 위와 같은 구문(ctrl + f로 ‘sassRegex’ 찾기)이 있는데 'sass-loader' 부분을 아래와 같이 수정한다.

<br />

```jsx
{
  test: sassRegex,
  exclude: sassModuleRegex,
  use: getStyleLoaders({
    importLoaders: 3,
    sourceMap: isEnvProduction
      ? shouldUseSourceMap
      : isEnvDevelopment,
    modules: {
      mode: 'icss',
    },
  }).concat({
		loader: require.resolve('sass-loader'),
		options: {
			sassOptions: {
				includePaths: [paths.appSrc + "/styles"],
			},
		},
	}),
	sideEffects: true,
}
```

- 위와 같이 수정하면 `./styles` 폴더가 절대 경로로 설정되어 import 구문이 짧아진다.
    - `@import './styles/utils'` → `@import 'utils.sass'`
    - 만약 모든 파일에 `@import 'utils.sass'` 구문을 작성해줘야 한다면 webpack 설정 중 additionalData 필드를 설정하여 해당 구문을 불러오도록 설정할 수 있다.

<br />

```jsx
{
  test: sassRegex,
  exclude: sassModuleRegex,
  use: getStyleLoaders({
    importLoaders: 3,
    sourceMap: isEnvProduction
      ? shouldUseSourceMap
      : isEnvDevelopment,
    modules: {
      mode: 'icss',
    },
  }).concat({
		loader: require.resolve('sass-loader'),
		options: {
			sassOptions: {
				includePaths: [paths.appSrc + "/styles"],
			},
			**addtionalData: "@import 'utils';",**
		},
	}),
	sideEffects: true,
}
```

<br />

## 9.3 CSS Module

- 클래스 이름을 고유한 값으로 만들어 중첩되는 현상을 방지해주는 CSS 방식이다.
- `filename.module.css` 형태로 파일을 작성한다.
- 해당 파일을 불러오면 key, value 형태로 클래스 이름이 들어 있어 아래와 같이 사용한다.
    
    ```jsx
    import styles from './CSS.module.css';
    
    const MyApp = () => <div className={styles.wrapper}></div>
    ```
    
- CSS Module 내부에서 전역으로 클래스를 작성하고 싶다면 :global 키워드를 붙여 CSS를 작성한다.
    - 일반 CSS(또는 Sass, SCSS) 파일에서 :local 키워드를 사용하여 작성하면 Module 처럼 사용할 수 있다.

<br />

## 9.4 styled-components

- 자바스크립트 파일 안에 스타일을 선언하는 방식(CSS-in-JS)
- 일반 CSS/Sass/SCSS와 비교했을 때 가장 큰 장점은 props 값으로 전달해주는 값을 쉽게 스타일에 적용할 수 있다.
- `(백틱) 기호 내부에 스타일을 작성하는데 이를 Tagged 템플릿 리터럴이라고 한다.
    - 일반 템플릿과 다르게 템플릿 안에 자바스크립트 객체나 함수를 전달할 때 온전히 추출할 수 있다.

```jsx
// 일반 템플릿은 함수, 객체 등을 온전히 전달하지 못한다.
console.log(`hello ${{foo: 'bar'}} ${() => 'world'}!`)
// hello [object Object] () => 'world'!

// tagged 템플릿 리터럴의 장점은 내부 함수, 객체를 온전히 추출할 수 있다.
function tagged(...args) {
  console.log(args);
}
tagged`hello ${{foo: 'bar'}} ${() => 'world'}!`
/*
	(3) [Array(3), {…}, ƒ]
	0: ['hello ', ' ', '!', raw: Array(3)]
	1: {foo: 'bar'}
	2: () => 'world'
	length: 3
*/
```

<br />

- styled-components를 통해 작성된 Tagged 템플릿 리터럴은 해당 스타일이 적용된 리액트 컴포넌트로 생성된다.
- props 값을 styled-components로 전달하여 사용할 때 css 등을 import하여 Tagged 템플릿 리터럴로 작성되도록 해야한다.
    - css로 감싸주지 않으면 일반 템플릿이 되어 내부에 작성된 함수나 객체를 그대로 전달해줄 수 없기 때문.
    - 만약 해당 템플릿 내부에서 props를 참조하지 않는다면 감싸주지 않아도 상관 없다.

```jsx
import styled, { **css** } from 'styled-components';

const Button = styled.button`
	/* ... */
	${props => props.inverted && 
		**css**`
			background-color: white;
		`
	}
`;
```