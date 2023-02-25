# 1. Javascript의 Garbage Collection

자바스크립트는 메모리 관리를 위해 자동 메모리 관리 방법(**Garbage Collection**)을 사용한다. 가비지 컬렉션은 도달 가능성(**Reachability**)이라는 개념을 사용해 Root에서부터 참조에 의해 어떻게든 접근 또는 사용이 가능한 값은 메모리에서 해제하지 않고, 접근이 불가능한 값은 메모리에서 해제한다.

자바스크립트는 **Mark And Sweep** 방식으로 닿을 수 없는 객체(**Unreachable**)를 메모리 해제하는 방법을 사용하고 있다.

<br />

# 2. React 함수 컴포넌트에서 사용하는 일반적인 함수와 상수의 선언

### 2-1) 컴포넌트 내부에 작성된 함수와 상수

아래와 같은 React 함수 컴포넌트 코드가 있다고 가정해보자.

```tsx
const Foo = () => {
  const scrollToTop = () => {
    window.scrollTo(0, 0);
  };

  return (
    <div>
      특정 컨텐츠
      <button onClick={scrollToTop}>TOP</button>
    </div>
  );
};
```

버튼을 하나 만들고, 그 버튼을 눌렀을 때 페이지의 최상단으로 스크롤하는 함수를 바인딩했다. 그런데, `scrollToTop` 함수는 굳이 컴포넌트 내부에 있을 필요는 없어보인다. 컴포넌트 내부에서 특정 `state`, `ref` 등을 참조하고 있는 것이 아니고, 매개변수도 없기에 컴포넌트 내부에 해당 함수를 정의하면 컴포넌트가 마운트될 때마다 새로 함수를 정의하는 것이 비효율적으로 보인다.

```tsx
const Foo = () => {
	const VALUES = [1, 2, 3, '배', '준', '형']; // 변하지 않는 값
  const newValues = VALUES.filter((value) => typeof value === 'number');

  return (
    <div>
      {newValues.map(value => ...)}
    </div>
  );
};
```

위처럼 함수 정의가 아니라 컴포넌트 내부에서 변동되지 않는 상수 배열을 매번 동일하게 가공하여 사용한다고 했을 때 배열의 크기가 매우 크다면?? 배열을 가공하는 연산도 컴포넌트 마운트마다 반복되므로 이런 함수나 상수는 `React.useMemo()`, `React.useCallback`으로 정의하는 것이 유리할 것 같다.

<br />

### 2-2) useMemo, useCallback 대신 컴포넌트 밖에 선언한 함수와 상수

그런데 굳이 `useMemo`, `useCallback`를 사용하지 않고도 그냥 전역에 함수나 상수를 선언할 수도 있을 것 같다.

```tsx
// scrollToTop 함수, VALUES 상수를 컴포넌트 밖으로 뺀다.
const scrollToTop = () => {
  window.scrollTo(0, 0);
};
const VALUES = [1, 2, 3, "배", "준", "형"];
const newValues = VALUES.filter((value) => typeof value === "number");

const Foo = () => {
  return (
    <div>
      특정 컨텐츠
      <button onClick={scrollToTop}>TOP</button>
    </div>
  );
};
```

이렇게 하면 `useMemo`, `useCallback`을 사용하지 않아도 불필요한 연산 없이 사용할 수 있다.

그런데 의문이 드는 것은, **전역에 선언한 함수나 변수가 제대로 가비지 컬렉션 되는지** 궁금하다. 전역에 선언한 변수는 언제든 도달 가능(Reachable)하기 때문에 가비지 컬렉션되지 않을 것 같기도 하고, 컴포넌트가 언마운트됐을 때 더 이상 참조하는 코드가 없다면(Unreachable) 그것대로 가비지 컬렉션이 제대로 이루어질 것 같기도 하다.

[https://ko.javascript.info/garbage-collection](https://ko.javascript.info/garbage-collection) 에서는 전역 변수는 태생부터 도달 가능하기 때문에 명백한 이유 없이는 삭제되지 않는다고 적혀있다. 다만, 이 전역 변수가 window 전역 객체에도 저장된 전역 변수를 의미하는 것인지, 단순히 최상단 스코프에 선언된 변수를 얘기하는 것인지 불분명하긴 하다.

컴포넌트가 마운트 만약 제대로 가비지 컬렉션이 되지 않고 메모리가 누수된다면 컴포넌트 내부에 적절하게 선언하고, 언마운트될 때 같이 가비지 컬렉션되도록 하는 것이 더 올바른 방법일 것이다.

<br />

# 3. React에서 전역 변수를 사용할 때 Garbage Collection 되는가?

그래서 이것저것 찾아보다 그냥 실제로 가비지 컬렉션 되는지 직접 확인해보기로 했다.

### 3-1) 간단한 React 컴포넌트 만들기

두 가지의 컴포넌트를 만들었다.

```tsx
// Foo.tsx
const outsideData = Array.from({ length: 100000 }, (_, i) => i);
const Foo = () => {
  return <div>{JSON.stringify(outsideData)}</div>;
};

// Bar.tsx
const Bar = () => {
  const insideData = Array.from({ length: 100000 }, (_, i) => i);
  return <div>{JSON.stringify(insideData)}</div>;
};

// App.tsx
const App = () => {
  const [showFoo, setShowFoo] = useState(false);
  const [showBar, setShowBar] = useState(false);
  return (
    <div>
      {showFoo && <Foo />}
      <button onClick={() => setShowFoo((prev) => !prev)}>
        컴포넌트 밖에 선언한 데이터 확인
      </button>
      {showBar && <Bar />}
      <button onClick={() => setShowBar((prev) => !prev)}>
        컴포넌트 내부에 선언한 데이터 확인
      </button>
    </div>
  );
};
```

`Foo` 컴포넌트는 파일 최상단(**컴포넌트 밖**)에 변수를 선언했고, `Bar` 컴포넌트는 **컴포넌트 내부**에 변수를 선언했다.

이를 `App.tsx`에서 각각 조건부 렌더링 시켜주고, 컴포넌트가 마운트 됐을 때, 언마운트됐을 때 제대로 가비지 컬렉션 되는지 확인한다.

<br />

### 3-2) Chrome 개발자 도구로 가비지 컬렉션 확인하기.

React에서 직접적으로 가비지 컬렉션을 확인하고 조작하는 방법은 없으나, Chrome 개발자 도구를 이용해서 메모리를 분석하면 가비지 컬렉션이 됐는지 안됐는지 확인할 수 있다.

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/221346507-325a7519-e522-4624-9d47-4e5adc37f68a.png">
</div>

개발자 도구 - `Allocation instrumentation on timeline` / `Record stack traces of allocations` 옵션을 체크 - 왼쪽 상단에 녹화 버튼처럼 보이는 원을 클릭하면 Memory Allocation 시작, 1회 더 클릭하면 종료되어 결과를 확인할 수 있다.

<br />

### 3-3) 컴포넌트 내부에 선언한 데이터 가비지 컬렉션

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/221346513-09fbdfa0-9fc2-4d2a-8023-db1a80ba69f4.gif">
</div>

- 위와 같이 memory allocation을 실행한 후에 결과값 중 `Object`에 선언한 변수 값이 있는지 확인하면 가비지 컬렉션이 됐는지 안됐는지 확인할 수 있다.

**컴포넌트가 마운트됐을 때**

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/221346512-70f140cf-786b-4ec5-b488-e9cc1ff39a48.png">
</div>

Object 탭에 **588,952** 단위 크기를 갖는 Object가 메모리에 쓰이고 있다.

**컴포넌트가 언마운트됐을 때**

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/221346511-c43d828b-cfef-4382-bd2e-6d74a4a0807e.png">
</div>

**588,952** 단위 크기를 갖는 Object는 존재하지 않는다. Allocation Snapshot3 크기도 **8.1 MB에서 7.3 MB로** 줄어들었다.

결과: 컴포넌트 내부에 선언한 변수는 언마운트될 때 **가비지 컬렉션된다**.

<br />

### 3-4) 컴포넌트 밖에 선언한 데이터 가비지 컬렉션

**컴포넌트가 마운트됐을 때**

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/221346510-be9c7874-3615-429a-a593-9f30db767978.png">
</div>

이전 결과와 마찬가지로 **588,952** 단위 크기를 갖는 Object가 메모리가 쓰이고 있다.

**컴포넌트가 언마운트됐을 때**

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/221346509-d1c58e51-048a-4500-a17d-35ce90167df3.png">
</div>

이전 결과와 동일하게 **588,952** 단위 크기를 갖는 Object는 보이지 않고, Snapshot의 크기도 **8.0 MB에서 7.4 MB로** 줄어들었다.

결과: 컴포넌트 밖에 선언한 전역 변수는 컴포넌트가 언마운트될 때 **가비지 컬렉션 된다**.

<br />

# 4. 정리

Chrome 개발자 도구로 확인한 결과, React에서 특정 변수나 함수를 **컴포넌트 내부에 선언하던, 컴포넌트 외부에 선언하던** 해당 **컴포넌트가 언마운트될 때 가비지 컬렉션 된다**.

React로 개발을 하면서 컴포넌트 내부에 선언한 상수를 여러번 연산하거나 함수를 여러번 재정의 하는 비효율은 눈에 잘 보여서 useMemo, useCallback을 사용하거나 아예 컴포넌트 밖에 선언했다. 전역에 선언됐을 때 제대로 가비지 컬렉션되어 메모리 누수를 일으키지 않는지에 대해선 제대로 생각해보진 않았다.

처음엔 당연히 가비지 컬렉션이 되겠지 생각하고 넘어갔는데, 곰곰히 생각해보니 전역에 선언한 변수도 참조하지 않고 있더라도 도달 가능한 값인데 가비지 컬렉션이 안될 수도 있지 않을까?? 하는 생각도 들었고 만약 가비지 컬렉션되지 않는다면 컴포넌트 밖에 선언하는 것보다 컴포넌트 내부에 적절하게 선언하는 것이 더 효율적이기에 제대로 확인해보기로 했다.

결과적으로 React로 컴포넌트 코드를 작성할 때 변수나 함수를 어디에 선언하던 가비지 컬렉션 되므로 불필요한 연산이 반복되지 않는 선에서 작성자의 편의에 따라 선언하면 될 것 같다.

<br />

---

# 참조

- [https://ko.javascript.info/garbage-collection](https://ko.javascript.info/garbage-collection)
- [https://velog.io/@apparatus1/Garbage-Collection](https://velog.io/@apparatus1/Garbage-Collection)
