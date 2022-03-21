# 10장 일정관리 웹 애플리케이션 만들기

- 해당 챕터는 웹 애플리케이션 만들기로 해당 챕터에서 나온 내용 중 정리하고 싶거나 몰랐던 내용을 정리하자.

<br />

### 1. classnames 라이브러리

- 일반 CSS, CSS module을 사용할 때 className의 작성을 더 편하게 할 수 있다.
    - boolean 값에 따라 조건부 className 추가에 용이하다.
- [https://www.npmjs.com/package/classnames](https://www.npmjs.com/package/classnames)

```
# via npm
npm install classnames

# via Bower
bower install classnames

# or Yarn
yarn add classnames
```

```jsx
classNames('foo', 'bar'); // => 'foo bar'
classNames('foo', { bar: true }); // => 'foo bar'
classNames({ 'foo-bar': true }); // => 'foo-bar'
classNames({ 'foo-bar': false }); // => ''
classNames({ foo: true }, { bar: true }); // => 'foo bar'
classNames({ foo: true, bar: true }); // => 'foo bar'

// lots of arguments of various types
classNames('foo', { bar: true, duck: false }, 'baz', { quux: true }); // => 'foo bar baz quux'

// other falsy values are just ignored
classNames(null, false, 'bar', undefined, 0, 1, { baz: null }, ''); // => 'bar 1'
```

<br />

### 2. react-icons 라이브러리

- 다양한 icon들을 svg 형태로 컴포넌트처럼 쉽게 사용할 수 있다.
- [https://react-icons.github.io/react-icons](https://react-icons.github.io/react-icons)

```jsx
npm install react-icons --save

yarn add react-icons
```

```jsx
import { FaBeer } from 'react-icons/fa';

class Question extends React.Component {
    render() {
        return <h3> Lets go for a <FaBeer />? </h3>
    }
}
```

<br />

### 3. useRef로 특정 값으로 사용하기

- useRef의 값은 변경돼도 리렌더링이 일어나지 않는다.
- 따라서 id값을 부여하고 해당 값을 증가시키면서 state를 늘려나간다면 useRef.current 값에 id 값을 저장해놓고 사용하면 해당 값이 변경돼도 리렌더링이 일어나지 않으니 조금이나마 최적화가 가능하다.