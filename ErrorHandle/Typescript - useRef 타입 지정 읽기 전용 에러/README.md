# Typescript - useRef 타입 지정 읽기 전용 에러

# 1. useRef는 읽기 전용?

- useRef는 DOM에 연결하여 해당 Element를 읽어오거나, .current 프로퍼티에 값을 저장해놓고 해당 값이 변동되어도 렌더링하고 싶지 않을 때 사용한다.
- 만약 DOM에 연결하거나 동적인 데이터 값을 .current 값에 할당하여 사용할 때 초기엔 의미적으로 값이 없음을 나타내기 위해 `초기 값을 null로 작성`해야하지 않을까? 생각했었다.
- 다만, useRef를 사용할 때 타입 지정을 해놓고 사용하려고 하니 .current 프로퍼티에 값을 할당하는데 **읽기 전용**이라고 **에러**가 뜨는 것이다.

<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159434512-0e121ec4-7f2f-4b66-a18e-f9bc355f6fcb.png">
</div>

<br />

# 2. MutableRefObject | RefObject

- useRef에 마우스 커서를 올려 놓으면 MutableRefObject 이라는 타입을 반환하고 있다.
- MutableRefObject 타입이 무엇인지 들어가보자 (ctrl + 우클릭)
    
<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159434531-769684f6-3cf1-40b0-861c-e9903c08c6ed.png">
</div>
    

```tsx
interface MutableRefObject<T> {
    current: T;
}
```

- useRef에서의 .current 프로퍼티는 <T> 제네릭으로 표현되어 있다. 그런데 왜 읽기 전용일까?

<br />

- useRef에서 최초에는 null 값을 주고 컴포넌트가 마운트되면 ref를 연결하거나 ref.current에 값을 할당하는 방식으로 사용하므로 useRef에 Type을 지정해야 한다.
    - 그런데, 타입을 지정하니 useRef의 타입이 아래와 같이 바뀌었다.
    
<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159434529-f84b2bcc-cfd5-4681-80b1-ebb2d1871cb8.png">
</div>
    
<br />

- 그럼 RefObject는 뭘까? 들어가보자

```tsx
interface RefObject<T> {
    readonly current: T | null;
}
```

- RefObject는 null 이거나 T 타입의 제네릭인데 readonly 처리 되어있다.
- 왜 다르게 동작하는 것일까?

<br />

# 3. 파라미터의 Type이 설정한 Type과 같은지 확인?

- 그럼 useRef의 interface는 어떻게 구성되어 있을까?

```tsx
function useRef<T>(initialValue: T): MutableRefObject<T>;

function useRef<T>(initialValue: T|null): RefObject<T>;
```

- useRef에 대해 위에서 확인한 두 가지 interface가 작성되어 있다.
- 즉, 초기 값인 initialValue에 null 값을 할당하니 RefObject의 interface를 가진 useRef를 사용하게 되고, .current 프로퍼티는 읽기 전용이 되는 것이다.

<br />

# 4. 어떻게 사용해야 할까?

- 그럼 어떻게 사용해야 할까?
- useRef의 interface를 더 살펴보니 아래와 같은 interface도 존재했다.

```tsx
function useRef<T = undefined>(): MutableRefObject<T | undefined>;
```

- 해당 interface는 초기 값이 undefined일 경우 MutableRefObject interface가 지정되어 있다.
- 즉, 초기 값을 null이 아닌 undefined라고 작성하면 읽기 전용이 아닌 값을 할당하여 사용할 수 있게 된다.

<br />

- **수정 전**

```tsx
const ref = useRef<number>(null);
ref.current = 10; // Error. .current는 읽기 전용
```

- **수정 후**

```tsx
const ref = useRef<number>();
ref.current = 10; // 정상 동작
```