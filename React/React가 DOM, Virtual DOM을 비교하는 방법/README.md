# React가 DOM, Virtual DOM을 비교하는 방법

# DOM, Virtual DOM을 비교하는 알고리즘

- DOM은 Tree 형태로 생성되고, DOM과 Virtual DOM을 비교하기 위해 일반적인 Tree 비교 알고리즘을 사용한다면 O(n^3)의 시간복잡도를 가진다.
- 이는 Element가 증가할수록 효율이 떨어진다.(1000개의 Element가 있다고 가정하면 최악의 경우 10억번의 비교를 해야한다)
- 따라서 React는 2가지 가정을 통해 heuristic O(n) Algorithm을 사용하여 DOM을 비교한다.
    1. **서로 다른 타입의 두 Element는 서로 다른 Tree를 만들어낸다.**
    2. **개발자가 Key prop을 통해 어떤 자식 Element가 변경되지 않아야할지를 표시해준다.**

<br />

## 1. Element의 타입이 다른 경우

- DOM, Virtual DOM 두 Tree의 Root Element의 타입이 다르면 React는 이전 Tree를 버리고 완전히 새로운 트리를 구축한다.
- 만약 아래와 같은 변화가 발생한다면,

```jsx
<div>
  <Counter />
</div>

<span>
  <Counter />
</span>
```

- 기존의 Counter 컴포넌트는 완전히 사라지고, 새로운 Counter가 새로 마운트된다.

<br />

## 2. Element의 타입이 같은 경우

- 타입이 같다면, 두 Element의 속성을 확인하여 변경된 속성들만 갱신한다.
- className, style 등의 속성들을 변경하게 되면 변경된 것을 갱신하게된다.
- 해당 변경사항을 갱신하면 이어서 해당 노드의 자식들에 대해 재귀적으로 처리한다.

<br />

## 3. Component형태의 Element가 같은 경우

- Component가 업데이트되면 인스턴스는 동일하게 유지되고 이로인해 state도 유지된다.
- React는 새로운 Element의 내용을 반영하기 위해 인스턴스의 prop을 갱신한다.

<br />

## 4. 자식에 대한 재귀적 처리

- DOM 노드의 자식을 재귀적으로 처리할 때 두 노드 자식에 대한 리스트를 동시에 순회하면서 차이점이 있다면 해당 사항을 생성한다.
- 만약 아래와 같은 변화가 발생한다면,

```jsx
<ul>
  <li>first</li>
  <li>second</li>
</ul>

<ul>
  <li>first</li>
  <li>second</li>
  <li>third</li>
</ul>
```

- first, second element 까지 순회하고 third는 두 Element가 일치하지 않으므로 \<li>third\</li> Element를 Tree에 추가한다.
- 만약, 리스트의 맨 뒤가 아닌 맨 앞에 추가한다면 다음과 같이 비효율적으로 모든 자식을 mutate하여 변경한다.

```jsx
<ul>
  <li>first</li>
  <li>second</li>
</ul>

<ul>
  <li>third</li>  // Element 내부 Child 내용 변경(first => third)
  <li>first</li>  // Element 내부 Child 내용 변경(second => first)
  <li>second</li> // Element 생성
</ul>
```

<br />

## 5. keys

- 위와 같은 비효율적인 재귀적 처리를 해결하기 위해 key prop을 이용한다.
- React는 key prop을 통해 기존 Tree와 변경 후의 Tree의 자식들이 일치하는지 확인한다.

```jsx
<ul>
  <li key="first">first</li>
  <li key="second">second</li>
</ul>

<ul>
  <li key="third">third</li>   // Element 생성
  <li key="first">first</li>   // Element 변경 없음
  <li key="second">second</li> // Element 변경 없음
</ul>
```

<br />

# 참고

- [https://reactjs.org/docs/reconciliation.html#the-diffing-algorithm](https://reactjs.org/docs/reconciliation.html#the-diffing-algorithm)
- [https://ko.reactjs.org/docs/reconciliation.html#the-diffing-algorithm](https://ko.reactjs.org/docs/reconciliation.html#the-diffing-algorithm)