# React - children 사이에 split element 넣기

# 1. Space 컴포넌트 만들기

```tsx
interface Props {
  align?: Align;
  direction?: Direction;
  size?: Size | Size[];
  split?: React.ReactNode;
  wrap?: boolean;
}

const Space = ({
  align = "center",
  children,
  direction = "horizontal",
  size = "middle",
  split,
  wrap,
}: React.PropsWithChildren<Props>) => {
  return <div className={className}>{children}</div>;
};

export default Space;
```

Ant Design에 있는 Space 컴포넌트를 보고 구조를 잡아봤다. 대부분 CSS와 관련된 컴포넌트라 어렵지 않게 구현이 가능했지만, children 사이사이에 `split` child를 껴(?) 넣어주는 부분은 조금 생소했다. 이 부분에 대해 알아보자.

<br />

# 2. Split props

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/221103460-e8bbd0c6-f75c-4e50-8a28-9f3703b6e8d2.png">
</div>

**split props**로 `<Divider />` 를 넘겨준 모습이다.

split에 ReactNode에 해당하는 Element를 props로 넘겨주면 Children 사이사이에 split에 들어온 ReactNode를 넣어준다.

<br />

# 3. React.Children

React.Children에는 `count`, `forEach`, `map`, `toArray`, `only` 5가지 메서드가 있는데, 각 메서드의 동작은 [여기](https://ko.reactjs.org/docs/react-api.html#cloneelement)에서 확인할 수 있다.

첫 번째로 Children을 배열로 만드는 toArray 메서드를 사용해서 children 배열을 만들고, 이를 순회하면서 각각의 children 사이에 split element를 껴주면 될 것 같다는 생각을 했다.

<br />

## 3-1) React.Children.toArray() 시도

```tsx
React.Children.toArray(children).reduce<React.ReactNode[]>((acc, cur, i) => {
  if (i === 0) {
    return acc.concat(cur);
  } else {
    return acc.concat([split, cur]);
  }
}, []);
```

- children을 배열로 만들고, 배열 사이사이에 split element를 끼워 넣어준다.

**결과**

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/221103468-212b2661-9fcb-4512-beae-4e1aa6866722.png">
</div>

동작은 잘 되나 유니크한 key props이 필요하다는 warning이 뜬다. 이를 해결하기 위해 `toArray()` 대신 `map()` 사용하는 것으로 수정.

<br />

## 3-2) React.Children.map(children, func)

```tsx
React.Children.map(children, (child, i) =>
  i === 0 ? (
    child
  ) : (
    <React.Fragment key={child?.toString()}>
      <>{split}</>
      <>{child}</>
    </React.Fragment>
  )
);
```

- 첫 번째 index일 때만 그대로 렌더링, 그 이후부터 child 앞에 split element를 추가해준다.
- Fragment 태그를 이용해 key 값을 넘겨준다.

**결과**

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/221103465-43e0e920-73c2-44cd-adaf-14a10a171440.png">
</div>

key props warning 없이 잘 렌더링 되었다.

<br />

# 정리

Ant Design에 있는 컴포넌트들을 하나씩 만들어 보기로 했다. 간단한 것 부터 하나씩 만들어가는데 Space에서 split props로 내려주는 것이 생소하기도 하고, `React.Children` 을 존재만 알고 제대로 알지는 못했는데 정리하면 좋을 것 같아서 내용도 같이 정리했다.
