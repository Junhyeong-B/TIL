# 1. 무엇을 써야할까

## 1) interface

- 어떤 것의 규격 사항, 어떠한 것을 구현할 목적으로 작성한 것
- object 간의 상호작용을 할 때 interface를 통해 규격 사항을 정한다.
- class를 작성할 때 `implements` 키워드를 통해 interface에서 정의한 동일한 규격사항을 따른다.
- 이 때 type을 쓰는 것은 좋지 않다.(가능은 하다.)
    - 어떤 특정한 규격을 정하는 것이라면 interface를 쓰는 것이 더 정확하다.

<br />

## 2) Type

- 데이터의 모습, 어떠한 데이터를 담고 있는지 작성한 것
- 어떤 데이터를 정의하고, 그 데이터의 타입이 무엇인지 작성할 때는 Type을 사용한다.

**다만,** 위 사항들은 필수사항은 아니고 회사나 프로젝트 등에서 정한 규칙을 따라가면 된다.

<br />

# 2. Type alias와 Interface의 사용 차이

- 타입스크립트 초창기에는 interface가 할 수 있는 것들이 더 많아서 예전부터 배워온 사람이라면 interface만 사용하는 경우도 있다.
    - `type Type2 = Type & { new: string; }` 과 같은 intersaction은 사용할 수 없었고, interface는 extends로 상속받아 확장하는 것이 가능했다.
- interface만을 사용하는 것은 좋지 않다. ⇒ Type alias와 interface가 어떻게 다른지 알고 사용하자.

<br />

## Type alias, Interface 둘 다 가능한 것

```tsx
type PositionType = {
  x: number;
  y: number;
};

interface PositionInterface {
  x: number;
  y: number;
}

// object 🌟
const obj1: PositionType = {
  x: 1,
  y: 1,
};

const obj2: PositionInterface = {
  x: 1,
  y: 1,
};

// class 🌟
class Class1 implements PositionType {
  x: 1;
  y: 1;
}

class Class2 implements PositionInterface {
  x: 1;
  y: 1;
}

// extends 🌟
interface ZPositionInterface extends PositionInterface {
  z: number;
}

type ZPositionType = PositionType & { z: number };
```

<br />

## Type alias만 가능한 것.

- computed property

```tsx
type Person = {
  name: string;
  age: number;
};

type Name = Person["name"]; // type Name = string;
```

<br />

- Union Type

```tsx
type Direction = "up" | "down";
```

<br />

## Interface만 가능한 것

- interface merge
    - 동일한 이름으로 interface를 중복되게 작성하면 merge된다.

```tsx
interface Inter {
  x: number;
  y: number;
}

interface Inter {
  z: number;
}

const obj3: Inter = {
  x: 1,
  y: 1,
  z: 1,
};
```