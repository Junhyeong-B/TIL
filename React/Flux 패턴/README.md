# Flux 패턴

# 1. Flux 패턴이란?

Flux 패턴은 어플리케이션의 데이터 흐름을 관리하기 위한 패턴이다. **Flux 패턴에서의 데이터의 흐름이 한 방향으로만 이루어진다.** Flux  패턴의 데이터 흐름은 다음 4가지 Parts로 구분된다.

<br />

### 1) `Dispatcher`

Action을 받아 Store에 Action을 Dispatch하는 역할을 수행한다.

<br />

### 2) `Store`

어플리케이션의 데이터가 저장된 공간으로 Dispatcher로부터 받은 Action을 바탕으로 데이터를 관리하는 작업을 수행한다.

Store는 반드시 전달 받은 **Action에 의해서만** 데이터를 변화(Mutate)시켜야 한다.

<br />

### 3) `Action`

Action은 어플리케이션에서 사용되는 내부적인 API 정의, 어플리케이션 내부의 어떤 것이 Action에 의해 어플리케이션과 상호작용하는 방식을 의미한다. 만약 어플리케이션이 Todo-List 라면 `add-todo` | `update-todo` | `delete-todo` 등이 Action이 될 수 있다.

Action은 의미론적(Semantic)이어야 하고, 구현 사항의 세부적인 내용이 아닌 상호작용하는 방식을 설명(Descriptive)할 수 있어야 한다.

예를 들어 특정 Todo를 삭제한다고 했을 때 `delete-todo-id` | `delete-todo-data` 라고 정의하기 보다는 `delete-todo` 라고 정의하는 것이 권장된다.

<br />

### 4) `View`

Store에서 관리되고 있는 Data들은 View에 의해 표현되고, View는 Data를 사용할 때 해당 Data를 구독(Subscribe)하여 데이터의 변화를 감지해야 한다.

Data를 구독한다는 말은 Data가 변경됐다면 변경된 새로운 Data를 사용해 다시 렌더링 할 수 있어야 한다는 것을 의미한다.

<br />

# 2. Flux 패턴의 데이터 흐름

위에서 살펴본 4가지 Parts에 의해 관리되는 데이터의 흐름은 아래 그림과 같다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/161211554-94d8db42-38bf-41fa-b69d-22de1be9652f.png" />
</div>

1. View에서 Action을 Dispatcher로 보낸다(Send).
2. Dispatcher는 전달 받은 Action을 Store로 보낸다.
3. Store는 Action에 따라 Data를 변화(Mutate)시키고, View에서 Data를 받아온다.

<br />

# 3. Redux의 Flux 패턴 구현

Redux 창시자인 Dan Abramove는 Flux 패턴을 좀 더 단순화할 수 있을 것이라고 생각했고, 이는 Redux 개발로 이어졌다.

Redux도 Flux 패턴과 마찬가지로 단방향의 데이터 흐름을 가지며, Flux 패턴의 핵심 개념으로부터 파생됐지만 조금 다르다. Flux 패턴에 Dispatcher, Store, Action, View로 구분됐다면, Redux는 Reducers, Store, Actions, View로 구분된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/161211559-6602c1c8-3191-4907-a925-e7e5c900ccae.png" />
</div>

1. Actions는 어플리케이션의 Event에 의해 Reducer로 Dispatch된다.
2. Reducer는 전달 받은 Actions를 바탕으로 Store의 Data를 새로운 Data로 업데이트한다.(불변성 유지)
3. Reducer에 의해 Store는 새로운 상태(New state)를 생성하고, View는 생성된 새로운 상태를 바탕으로 렌더링한다.

<br />

# 4. Flux 패턴을 사용하는 이유

어플리케이션의 규모가 작다면 상태(State)를 관리하는 것은 그리 어렵지 않을 수 있다. 그러나 어플리케이션의 규모가 크고, 복잡한 상태를 다룬다면 이를 다루는 것은 어려워질 수 있다.

복잡한 상태를 다룰 때 단방향으로만 데이터 흐름을 관리한다면 **상태를 예측하기 더 쉬워진다.** 또한 역할이 구분된 Parts로 인해서 **Debugging 측면에서도 유리**하다.

<br />

## 참고

- [https://github.com/facebook/flux/tree/main/examples/flux-concepts](https://github.com/facebook/flux/tree/main/examples/flux-concepts)
- [https://www.clariontech.com/blog/mvc-vs-flux-vs-redux-the-real-differences](https://www.clariontech.com/blog/mvc-vs-flux-vs-redux-the-real-differences)