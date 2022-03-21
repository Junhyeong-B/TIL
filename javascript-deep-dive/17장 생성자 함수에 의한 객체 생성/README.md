# 17장 생성자 함수에 의한 객체 생성

# Object 생성자 함수

- **생성자 함수(constructor)** 란 new 연산자와 함께 호출하여 객체(인스턴스)를 생성하는 함수를 말한다.
- 생성자 함수에 의해 생성된 객체를 **인스턴스(instance)** 라 한다.
- 생성자 함수는 Object 외에도 String, Number, Boolean, Function, Array, Date, RegExp, Promise 등의 빌트인 함수가 있다.

<br />

# 생성자 함수

## 객체 리터럴에 의한 객체 생성의 문제점

- 생성자 함수로 객체를 생성할 수 있지만 객체를 생성하는 것은 객체 리터럴로 생성하는 것이 더 간편하다.
- 그러나 객체 리터럴로 생성하는 객체의 단점은 단 하나의 객체만을 생성한다는 것이다.
- 객체 리터럴로 생성하는 경우에는 프로퍼티 구조가 동일해도 매번 같은 프로퍼티와 메서드를 기술해서 여러 개 작성해야 하는 불편함이 있다.

<br />

## 생성자 함수에 의한 객체 생성의 장점

- 생성자 함수에 의한 객체 생성은 **인스턴스를 생성**하기 때문에 프로퍼티 구조가 동일한 객체 여러개를 간편하게 생성할 수 있다.
- **일반 함수와 동일한 방법**으로 생성자 함수를 정의하고 new 연산자와 함께 호출하면 해당 함수는 생성자 함수로 동작한다.
    - new 연산자와 함께 호출하지 않으면 생성자 함수로 동작하지 않고 일반 함수로 호출된다.

```jsx
const circle1 = {
	radius: 5,
	getDiameter() {
		return 2 * this.radius;
	}
}
// circle1 외 해당 메서드를 사용하는 다른 값을 사용하고 싶으면
// 동일한 프로퍼티 구조를 갖는 새로운 객체를 생성해야 한다.

function Circle(radius) {
	this.radius = radius;
	this.getDiameter = function () {
		return 2 * this.radius;
	};
}
const circle2 = new Circle(10);
// circle2 외 동일한 메서드를 사용하고 싶으면 new Circle(radius)로 생성해주면 된다.
```

<br />

### ※ 함수 호출 방식에 따른 this

| 함수 호출 방식 | this가 가리키는 값(this 바인딩) |
| --- | --- |
| 일반 함수로서 호출 | 전역 객체 |
| 메서드로서 호출 | 메서드를 호출한 객체(마침표 앞에 객체) |
| 생성자 함수로서 호출 | 생성자 함수가 미래에 생성할 인스턴스 |

<br />

## 생성자 함수의 인스턴스 생성 과정

- 생성자 함수의 **역할**은 **인스턴스를 생성**하고 **생성된 인스턴스를 초기화**(인스턴스 프로퍼티 추가 및 초기값 할당) 하는 것이다.
    - 인스턴스 생성 ⇒ 필수 / 인스턴스  초기화 ⇒ 옵션

<br />

- 인스턴스를 생성하고 반환하는 코드가 없어도 **자바스크립트 엔진은 암묵적인 처리를 통해 인스턴스를 생성하고 반환**한다.
    - 암묵적으로 빈 객체가 생성되고 생성된 빈 객체가 인스턴스이다.
    - 해당 빈 객체에 인스턴스를 this에 바인딩된다.
    - 다음과 같은 순서로 인스턴스를 생성, 초기화 반환한다.
        1. 인스턴스 생성과 this 바인딩
        2. 인스턴스 초기화
        3. 인스턴스 반환

<br />

- 만약 this가 아닌 다른 객체를 명시적으로 반환하면 this가 반환되지 못하고 return 문에 명시한 객체가 반환된다.
    - 단, 객체가 아닌 원시값을 명시적으로 반환하면 원시 값 반환은 무시되고 암묵적으로 this가 바인딩된다.

```jsx
function Circle1(radius) {
	this.radius = radius;
	this.getDiameter = function () {
		return 2 * radius;
	};
	// 아무것도 반환하지 않아도 암묵적으로 인스턴스를 
}

const circle1 = new Circle1(10);
console.log(circle1); // Circle1 {radius: 10, getDiameter: f}

function Cicle2(radius) {
	this.radius = radius;
	this.getDiameter = function () {
		return 2 * radius;
	};
	return {};
	// 명시적으로 객체를 반환하면 암묵적인 this 반환이 무시된다.
}

const circle2 = new Circle2(10);
console.log(circle2); // {}

function Circle3(radius) {
	this.radius = radius;
	this.getDiameter = function () {
		return 2 * radius;
	};
	return 100;
	// 명시적으로 원시 값을 반환하면 원시 값 반환이 무시되고 암묵적으로 this가 반환된다.
}

const circle3 = new Circle3(10);
console.log(circle3); // Circle3 {radius: 10, getDiameter: f}
```

<br />

## 내부 메서드 [[call]] / [[construct]]

- 함수 선언문 또는 표현식으로 정의한 함수는 일반적인 함수로 호출할 수도, 생성자 함수로 호출할 수도 있다.
    - 함수는 객체이고, 함수 객체는 일반 객체가 가지고 있는 내부 슬롯과 내부 메서드를 모두 가지고 있기 때문이다.

<br />

- 함수는 객체이지만 일반 객체와 다르게 호출할 수 있다.(일반 객체는 호출할 수 없다.)
- 함수가 일반 함수로서 호출되면 [[call]] 내부 메서드가 호출되고, new 연산자와 함께 생성자 함수로 호출하면 [[construct]] 내부 메서드가 호출된다.

```jsx
function a() {};

a(); // [[call]] 호출
new a(); // [[construct]] 호출
```

<br />

### callable | constructor | non-constructor

- [[call]]을 갖는 함수를 callable이라고 하고, [[construct]]를 갖는 함수 객체를 constructor | 갖지 않는 함수 객체를 non-constructor라고 한다.
- 호출할 수 없는 객체는 함수 객체가 아니므로 **함수 객체는 반드시 callable**이어야 한다.
- 모든 함수 객체가 [[construct]]를 갖는 것은 아니다.
- 따라서, 함수 객체는 callable이면서 constructor 또는 callable 이면서 non-constructor 이다.
    - `constructor` : 함수 선언문, 함수 표현식, 클래스(클래스도 함수)
    - `non-constructor` : 메서드(ES6 메서드 축약 표현), 화살표 함수
    - 일반 함수로 정의된 함수만이 constructor 이다.

<br />

## new 연산자

- new 연산자로 함수를 호출하면 해당 함수는 생성자 함수로 동작하고, [[construct]]가 호출된다.
- new 연산자 없이 생성자 함수를 호출하면 일반 함수로서 호출되고, 해당 함수의 this는 전역 객체를 가리키게 된다.

<br />

## new.target

- new 연산자 없이 호출되는 것을 방지하기 위해 new.target을 사용한다.(IE는 지원 X)
- new 연산자와 함께 생성자 함수로서 호출되면 함수 내부의 new.target은 함수 자신을 가리키고 new 연산자 없이 생성자 함수로 호출되면 함수 내부의 new.target은 undefined가 된다.

```jsx
function Circle(radius) {
	if (!new.target) {
		return new Circle(radius);
		// new 연산자와 함께 호출되지 않았다면 재귀 호출하여 인스턴스를 반환한다.
	}

	this.radius = radius;
	this.getDiameter = function () {
		return 2 * radius;
	};
}

const circle = Circle(5);
console.log(circle.getDiameter()); // 10
```

<br />

# 🤔 문제

```jsx
function a() {};

a(); // [[call]] 호출
new a(); // [[construct]] 호출
```

1. 다음 중 옳지 않은 것은?
    
    1) [[call]]을 갖는 함수를 callable | [[construct]]를 갖는 함수 객체를 constructor 라고 한다.
    
    2) 함수 객체는 (callable 이면서 constructor) 이거나 (non-constructor) 이다.
    
    3) 모든 함수 객체가 [[construct]]를 갖는 것은 아니다.
    
    4) 화살표 함수는 [[construct]]를 갖지 않는다.

<br />

- 답
    
    2)
    
    호출할 수 없는 객체는 함수 객체가 아니므로 **함수 객체는 반드시 callable**이어야 한다.
    
    따라서, 함수 객체는 **callable이면서 constructor** 또는 **callable 이면서 non-constructor** 이다.
    

<br />

2. 다음 실행 결과를 예측하시오.

```jsx
function A(value) {
	this.value = value;
	this.X = function () {};
}

function B(value) {
	this.value = value;
	this.X = function () {};
	return {};
}

function C(value) {
	this.value = value;
	this.X = function () {};
	return value;
}

const a = new A(10);
const b = new B(10);
const c = new C(10);
console.log(a); // (1)
console.log(b); // (2)
console.log(c); // (3)
```

<br />

- 답
    
    (1) `A {value: 10, X: f}`
    
    (2) `{}`
    
    (3) `C {value: 10, X: f}`
    
    생성자 함수로 호출한 함수 객체에서 반환하는 코드가 없어도 **자바스크립트 엔진은 암묵적인 처리를 통해 인스턴스를 생성하고 반환**하는데,
    
    명시적으로 객체를 반환하면 암묵적인 this 반환이 무시되고
    
    명시적으로 원시 값을 반환하면 원시 값 반환이 무시되고 암묵적으로 this가 반환된다.