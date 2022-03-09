# 37장 Set과 Map

# 1. Set

- Set 객체는 **중복되지 않는** 유일한 값들의 집합이다.
- 배열(Array)은 중복이 허용되고, 순서가 있어 인덱스로 접근할 수 있지만 Set 객체에는 **중복이 불가능하며 순서가 없다**.
- 따라서 교집합, 합집합, 차집합, 여집합 등을 구현할 수 있다.

<br />

## 1-1) Set 객체의 생성

- Set 객체는 **Set 객체 생성자 함수**로 생성한다.
- 인수를 전달할 수도 있고, 전달하지 않을 수도 있다.
- Set 생성자 함수는 이터러블을 인수로 전달받아 Set 객체를 생성한다. 이때 **중복된 값은 Set 객체에 요소로 저장되지 않는다**.

<br />

## 1-2) 요소 개수 확인

- `Set.prototype.size`
- getter 함수만 존재하는 접근자 프로퍼티여서 해당 프로퍼티에 숫자를 할당하여 Set 객체 요소 개수를 변경할 수 없다.

<br />

## 1-3) 요소 추가

- `Set.prototype.add`
- add 메서드는 새로운 요소가 추가된 Set 객체를 반환한다. 따라서 add를 연속해서 체이닝하여 사용할 수도 있다.
- `NaN`, `-0`, `+0` 등의 값들도 비교 연산자의 결과와 상관 없이 중복을 허용하지 않는다.
- 자바스크립트의 모든 값을 요소로 저장할 수 있다.(함수 포함)

<br />

## 1-4) 요소 존재 여부 확인

- `Set.prototype.has`
- 불리언 값을 반환한다.

<br />

## 1-5) 요소 삭제

- `Set.prototype.delete`
- 없는 요소를 삭제하면 에러 없이 무시된다.
- 삭제 성공 여부를 불리언 값으로 반환한다.

<br />

## 1-6) 요소 일괄 삭제

- `Set.prototype.clear`
- 언제나 `undefined`를 반환한다.

<br />

## 1-7) 요소 순회

1. `Set.prototype.forEach`
    - **첫 번째 인수**: 현재 순회 중인 요소값
    - **두 번째 인수**: 현재 순회 중인 요소값
    - **세 번째 인수**: 현재 순회 중인 Set 객체 자체

```jsx
const set = new Set([1, 2, 3]);

set.forEach((v, v2, set) => console.log(v, v2, set));
/*
1 1 Set(3) {1, 2, 3}
2 2 Set(3) {1, 2, 3}
3 3 Set(3) {1, 2, 3}
*/
```

<br />

1. `for ... of 문`

## 1-8) 집합 연산

### 1) 교집합

```jsx
Set.prototype.intersection = function (set) {
  return new Set([...this].filter(v => set.has(v)));
};

const setA = new Set([1, 2, 3, 4]);
const setB = new Set([2, 4]);

// setA와 setB의 교집합
console.log(setA.intersection(setB)); // Set(2) {2, 4}
// setB와 setA의 교집합
console.log(setB.intersection(setA)); // Set(2) {2, 4}
```

<br />

### 2) 합집합

```jsx
Set.prototype.union = function (set) {
  return new Set([...this, ...set]);
};

const setA = new Set([1, 2, 3, 4]);
const setB = new Set([2, 4]);

// setA와 setB의 합집합
console.log(setA.union(setB)); // Set(4) {1, 2, 3, 4}
// setB와 setA의 합집합
console.log(setB.union(setA)); // Set(4) {2, 4, 1, 3}
```

<br />

### 3) 차집합

```jsx
Set.prototype.difference = function (set) {
  return new Set([...this].filter(v => !set.has(v)));
};

const setA = new Set([1, 2, 3, 4]);
const setB = new Set([2, 4]);

// setA에 대한 setB의 차집합
console.log(setA.difference(setB)); // Set(2) {1, 3}
// setB에 대한 setA의 차집합
console.log(setB.difference(setA)); // Set(0) {}
```

<br />

### 4) 부분 집합과 상위 집합

```jsx
// this가 subset의 상위 집합인지 확인한다.
Set.prototype.isSuperset = function (subset) {
  const supersetArr = [...this];
  return [...subset].every(v => supersetArr.includes(v));
};

const setA = new Set([1, 2, 3, 4]);
const setB = new Set([2, 4]);

// setA가 setB의 상위 집합인지 확인한다.
console.log(setA.isSuperset(setB)); // true
// setB가 setA의 상위 집합인지 확인한다.
console.log(setB.isSuperset(setA)); // false
```

<br />

# 2. Map

- Map 객체는 **키와 값의 쌍으로 이루어진 컬렉션**이다.
- 객체는 이터러블이 아니고 키 값으로 문자열이나 심벌 값만 사용할 수 있지만, **Map 객체**는 **객체를 포함한 모든 값**을 **키 값**으로 사용할 수 있고, **이터러블**이다.

<br />

## 2-1) Map 객체의 생성

- Map 생성자 함수로 생성한다.
- 인수를 전달하지 않으면 빈 Map 객체가 생성된다.
- 이터러블을 인수로 전달받아 Map 객체를 생성하는데, 인수로 전달되는 이터러블은 키와 값의 쌍으로 이루어진 요소로 구성되어야 한다.

<br />

## 2-2) 요소 개수 확인

- `Map.prototype.size`
- getter 함수만 존재하는 접근자 프로퍼티여서 해당 프로퍼티에 숫자를 할당하여 Map 객체 요소 개수를 변경할 수 없다.

<br />

## 2-3) 요소 추가

- `Map.prototype.set`
- 새로운 요소가 추가된 Map 객체를 반환한다. 따라서 set 메서드를 연속하여 호출할 수 있다.
- 중복된 키를 갖는 요소를 추가하면 에러 없이 덮어 써진다.
- `NaN`, `-0`, `+0` 의 값들도 일치하다고 평가하여 중복 추가가 되지 않는다.
- 객체를 포함한 모든 값을 키 값으로 설정할 수 있다.

<br />

## 2-4) 요소 취득

- `Map.prototype.get`
- 인수로 전달한 키를 갖는 요소가 존재하지 않으면 undefined를 반환한다.

<br />

## 2-5) 존재 여부 확인

- `Map.prototype.has`
- 존재 여부를 나타내는 불리언 값이 반환된다.

<br />

## 2-6) 요소 삭제

- `Map.prototype.delete`
- 삭제 성공 여부를 불리언 값으로 반환한다.
- 존재하지 않는 값을 삭제하면 에러 없이 무시된다.

<br />

## 2-7) 요소 일괄 삭제

- `Map.prototype.clear`
- 언제나 undefined를 반환한다.

<br />

## 2-8) 요소 순회

1. `Map.prototype.forEach`
    - **첫 번째 인수**: 현재 순회 중인 요소값
    - **두 번째 인수**: 현재 순회 중인 요소 키
    - **세 번째 인수**: 현재 순회 중인 Map 객체 자체

```jsx
const lee = { name: 'Lee' };
const kim = { name: 'Kim' };

const map = new Map([[lee, 'developer'], [kim, 'designer']]);

map.forEach((v, k, map) => console.log(v, k, map));
/*
developer {name: "Lee"} Map(2) {
  {name: "Lee"} => "developer",
  {name: "Kim"} => "designer"
}
designer {name: "Kim"} Map(2) {
  {name: "Lee"} => "developer",
  {name: "Kim"} => "designer"
}
*/
```

2. `for ... of 문`

- Map 객체는 이터러블이면서 동시에 이터레이터인 객체를 반환하는 메서드를 제공한다.
    - `Map.prototype.keys`
    - `Map.prototype.values`
    - `Map.prototype.entries`

<br />

# 🤔 문제

**37장**

1. 다음 Set 객체에 대한 메서드 실행 중 **에러가 발생하는 경우**는?

```jsx
1) new Set([1, 2, 3]).add(1).add(2);       // add 체이닝
2) new Set([1, 2, 3]).add(NaN).add(NaN);   // NaN 값 add 체이닝
3) new Set([1, 2, 3]).delete(null);        // 존재하지 않는 요소 삭제
4) new Set([1, 2, 3]).delete(1).delete(2); // delete 체이닝
5) new Set([1, 2, 3]).size = 10;           // Set 객체 요소 개수 할당
```

<br />

- 답
    
    **4)**
    
    `Set.prototype.delete` 메서드는 삭제 성공 여부에 대한 **불리언 값을 반환**한다.
    
    불리언 값에 대해 Set 객체 메서드를 실행하려 하므로 delete 메서드 체이닝은 불가능하다.
    
    ※ 1) **add 메서드**는 요소가 추가된 **Set 객체를 반환하여 체이닝이 가능**하다.
    
    ※ 2, 3) 중복되는 요소를 추가하거나 존재하지 않는 요소를 삭제할 때는 **에러 발생 없이 무시**된다.
    
    ※ 5) getter 함수만 존재하는 접근자 프로퍼티여서 해당 프로퍼티에 숫자를 할당하여 Set 객체 요소 개수를 변경할 수 없고 에러는 발생하지 않는다.