# 16장 프로퍼티 어트리뷰트

## 내부 슬롯과 내부 메서드

- ECMAScript 사양에 등장하는 이중 대괄호(`[[...]]`)로 감싼 이름들이 내부 슬롯과 내부 메서드다.

<br />

- 자바스크립트 엔진의 내부 로직이므로 원칙적으로 내부 슬롯과 내부 메서드에 **직접적으로 접근하거나 호출할 수 있는 방법을 제공하지 않는다**.
    - 단, 간접적으로 접근할 수 있는 수단을 제공하기는 한다.

```jsx
const o = {};
o.[[Prototype]] // SyntaxError: Unexpected token '['
o.__proto__ // Object.prototype
```

<br />

## 프로퍼티 어트리뷰트 / 프로퍼티 디스크립터

- 자바스크립트 엔진은 프로퍼티를 생성할 때 프로퍼티의 상태를 나타내는 프로퍼티의 어트리뷰트를 기본값으로 자동 정의한다.

<br />

### 프로퍼티 어트리뷰트

- `[[Value]]` | `value`: 프로퍼티의 값

<br />

- `[[Writable]]` | `writable`: 프로퍼티 값의 갱신 가능 여부, `false`일 경우 값은 읽기 전용이 된다.

<br />

- `[[Enumerable]]` | `enumerable`: 프로퍼티의 열거 가능 여부, `false`일 경우 `for...in`, `Object.keys` 등의 메서드를 사용할 수 없다.

<br />

- `[[Configurable]]` | `configurable`: 프로퍼티의 재정의 가능 여부, `false`의 경우 프로퍼티의 삭제, 어트리뷰트 값의 변경이 금지된다. 단, writable이 `true`인 경우 value, writable을 false로 변경하는 것은 가능하다.

<br />

- 프로퍼티 어트리뷰트의 상태는 프로퍼티가 생성(또는 동적 생성)될 때 writable, enumerable, configurable 값은 true로 초기화된다.

<br />

- 프로퍼티 어트리뷰트에 직접 접근할 수 없지만 `Object.getOwnPropertyDescriptor`메서드를 사용하여 간접적으로 확인할 수는 있다.
    - 반환되는 객체는 **프로퍼티 디스크립터 객체**이다.

```jsx
const person = { name: 'Lee' };

console.log(Object.getOwnPropertyDescriptor(person, 'name'));
// {value: 'Lee', writable: true, enumerable: true, configurable: true}

// 프로퍼티 동적 생성
person.age = 20;

console.log(Object.getOwnPropertyDescriptors(person)); // 객체만 인자로 사용할 때는 메서드 뒤에 s가 붙는다.
// {
//   age: {value: 20, writable: true, enumerable: true, configurable: true}
//   name: {value: 'Lee', writable: true, enumerable: true, configurable: true}
// }
```

<br />

## 접근자 프로퍼티

- 접근자 프로퍼티의 종류
    - `get`: 프로퍼티의 값을 읽을 때 호출되는 접근자 함수, getter함수가 호출되고 그 결과가 프로퍼티 값으로 반환된다.
    - `set`: 데이터 프로퍼티의 값을 저장할 때 호출되는 접근자 함수, setter 함수가 호출되고 그 결과가 프로퍼티 값으로 저장된다.
    - `enumerable`: 데이터 프로퍼티의 enumerable과 같다.
    - `configurable`: 데이터 프로퍼티의 configurable과 같다.

```jsx
const person = {
	firstName: "A",
	lastName: "B",

	get fullName() {
		return `${this.firstName} ${this.lastName}`
	},
	set fullName(name) {
		[this.firstName, this.lastName] = name.split(" ");
	}
}

console.log(Object.getOwnPropertyDescriptor(person, 'firstName'));
// {value: 'A', writable: true, enumerable: true, configurable: true}
// **데이터 프로퍼티**로 호출한 프로퍼티 어트리뷰트

console.log(Object.getOwnPropertyDescriptor(perso, 'fullName'));
// {enumerable: true, configurable: true, get: ƒ, set: ƒ}
// **접근자 프로퍼티**로 호출한 프로퍼티 어트리뷰트
```

<br />

## 프로퍼티 정의

- Object.defineProperty 메서드를 사용하여 프로퍼티의 어트리뷰트를 정의할 수 있다.

```jsx
ObjectdefineProperty(person, 'firstName', {
	value: "A",
	writable: true,
	enumerable: true,
	configurable: true,
});
// 여기서 프로퍼티 어트리뷰트를 작성하지 않으면 undefined, false가 기본값이 된다.
```

<br />

## 객체 변경 금지

<img width="500px" align="center" src="https://user-images.githubusercontent.com/85148549/157393859-c0ae6f4e-c948-4480-ae16-e267971bf17b.png">

<br />

### 객체 확장 금지(Object.`preventExtensions`)

- 프로퍼티 추가 금지

<br />

### 객체 밀봉(Object.`seal`)

- 프로퍼티 추가, 삭제 금지
- 프로퍼티 어트리뷰트 재정의 금지

<br />

### 객체 동결(Object.`freeze`)

- 프로퍼티 추가, 삭제 금지
- 프로퍼티 값 갱신 금지
- 프로퍼티 어트리뷰트 재정의 금지

<br />

### 불변 객체

- Object.`freeze` 를 사용하여 객체를 읽기 전용으로 생성할 수 있지만, 중첩 객체까지는 영향을 주진 않는다.

<br />

- 따라서 객체의 중첩 객체까지 동결하여 변경이 불가능한 **불변 객체**를 구현하려면 객체를 값으로 갖는 모든 프로퍼티에 대해 재귀적으로 Object.`freeze` 를 호출해야 한다.

<br />

# 🤔 문제

1. 프로퍼티 어트리뷰트의 설명 중 옳지 않은 것은?
    1. `value`: value를 통해 프로퍼티 값을 정의하는데, 만약 프로퍼티가 없으면 프로퍼티를 동적으로 생성하고 생성된 값을 value에 값을 저장한다.
    2. `writable`: 값의 변경 여부를 의미하고, 만약 `false`일 경우 `enumerable`, `configurable` 값과는 상관 없이 value의 값을 변경할 수 없는 읽기 전용 프로퍼티가 된다.
    3. `enumerable`: 열거 가능 여부를 의미하고, 만약 `false`일 경우 `for ... in`, `Object.keys()` 등의 메서드를 사용할 수 없다.
    4. `configurable`: 재정의 가능 여부를 의미하고, 만약 `false`일 경우 value, writable의 값도 변경할 수 없다.

<br />

 - 답
     
     d.
     
     configurable 값이 false일 때, writable이 true인 경우 **value 값의 변경**과 **writable 값을 false로 변경**하는 것이 **가능**하다.
        

<br />

2. 다음 실행 결과를 예측하시오. Error가 발생한다면 위치를 예측해 주세요.

```jsx
const obj = {
	a: 10
};

Object.freeze(obj);
console.log(Object.getOwnPropertyDescriptors(obj))
// {a: {value: 10, writable: (1), enumerable: (2), configurable: (3)}}

obj.a = 20;
console.log(obj.a); // (4)

delete obj.a;
console.log(obj.a); // (5)

obj.b = 20;
console.log(obj); // (6)
```

<br />

- 답
    
    (1) false
    
    (2) true
    
    (3) false
    
    (4) 10
    
    (5) 10
    
    (6) {a: 10}
    
    - 금지된 행위에 대해 모든 변경 시도는 무시된다.
        - 단, 엄격 모드(`'use strict'`)에서는 이러한 시도에 대해 `TypeError`가 발생한다.
    - Object.`preventExtensions`, Object.`seal`도 마찬가지로  프로퍼티 추가, 삭제, 어트리뷰트 재정의가 금지되지만 에러는 발생하지 않고 무시된다.