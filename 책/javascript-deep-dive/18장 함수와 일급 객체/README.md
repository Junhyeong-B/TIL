# 18장 함수와 일급 객체

# 1. 일급 객체

- **무명의 리터럴로 생성**할 수 있다.(런타임에 생성)
- **변수나 자료구조**에 **저장**할 수 있다.
- **함수의 매개변수**에 전달할 수 있다.
- **함수의 반환값**으로 사용할 수 있다.

```jsx
// 함수는 무명의 리터럴로 생성할 수 있다.
// 함수는 변수에 저장할 수 있다.
const increase = function (num) {
	return ++num;
}

const decrease = function (num) {
	return --num;
}

// 함수는 객체에 저장할 수 있다.
const predicates = { increase, decrease };

// 함수의 반환값으로 사용할 수 있다.
function makeCounter(predicate) {
	let num = 0;
	return function () {
		num = predicate(num);
		return num;
	};
}

const increaser = makeCounter(predicates.increase);
console.log(increaser()); // 1
console.log(increaser()); // 2
```

<br />

- 함수가 일급 객체라는 것은 함수를 객체와 동일하게 사용할 수 있다는 의미다.
    - 따라서 함수는 값을 사용할 수 있는 곳이라면 어디서든지 **리터럴로 정의할 수 있고** 런타임에 **함수 객체로 평가**된다.
    

<br />

# 2. 함수 객체의 프로퍼티

- 함수는 객체이고, 프로퍼티를 가질 수 있다.

```jsx
function square(number) {
	return number * number;
}

console.dir(Object.getOwnPropertyDescriptors);
/*
	length: {value: 1, writable: false, enumerable: false, configurable: true};
	name: {value: "square", writable: false, enumerable: false, configurable: true};
	arguments: {value: null, writable: false, enumerable: false, configurable: true};
	caller: {value: null, writable: false, enumerable: false, configurable: true};
	prototype: {value: { ... }, writable: false, enumerable: false, configurable: true};

	square 함수의 모든 프로퍼티의 프로퍼티 어트리뷰트를 확인할 수 있다.
*/

console.log(Object.getOwnPropertyDescriptor(square, '__proto__'))
// __proto__는 프로퍼티가 아니다.
// undefined

console.log(Object.getOwnPropertyDescriptor(Object.prototype, '__proto__'))
// Object.prototype 객체로부터 __proto__ 접근자 프로퍼티를 상속받는다.
// {enumerable: false, configurable: true, get: ƒ, set: ƒ}
```

<br />

## 1) arguments 프로퍼티

- **arguments 객체**는 **함수 호출 시 전달된 인수들의 정보**를 담고 있는 순회 가능한 유사 배열 객체이다.
- 함수 외부에서는 참조할 수 없다.
- `arguments` 객체는 함수가 **나머지 매개변수(...), 기본 매개변수(**`function (x = 1)` **매개변수 초기화), 비구조화된 매개변수(**`[1, 2] = [a, b]`**)**에 포함되지 않는 경우에만 제공된다.

<br />

- 함수가 호출되면 함수 몸체 내에서 **암묵적으로 매개변수가 선언**되고 **undefined로 초기화**된 이후 **인수가 할당**된다.
    - 매개변수의 개수가 인수보다 적으면 undefined를 유지하고,
        
        매개변수의 개수가 인수보다 많으면 버려지는 것이 아니고 arguments 객체의 프로퍼티로 보관된다.
        

<br />

- 자바스크립트는 매개변수의 개수, 인자의 개수를 확인하지 않는 특성 때문에 매개변수 개수를 확정할 수 없는 **가변 인자 함수**를 구현할 때 arguments 객체가 유용하게 사용된다.

```jsx
function sum() {
	let res = 0;
	
	for (let i = 0; i < arguments.length; i++) {
		res += arguments[i];
	}

	return res;
}

console.log(sum());        // 0
console.log(sum(1, 2));    // 3
console.log(sum(1, 2, 3)); // 6
```

<br />

- arguments 개겣는 유사 배열 객체이므로 length 프로퍼티, for문 순회 등이 가능하지만, 배열 메서드를 사용할 경우 에러가 발생한다.
    - 배열 메서드를 사용하려면 call, apply를 사용해 간접 호출해야 한다.

<br />

## 2) caller 프로퍼티

- caller 프로퍼티는 ECMAScript 사양에 포함되지 않은 비표준 프로퍼티다.
- 함수 객체의 caller 프로퍼티는 함수 자신을 호출한 함수를 가리킨다.

<br />

## 3) length 프로퍼티

- 함수 객체의 length 프로퍼티는 **함수를 정의할 때 선언한** **매개변수의 개수**를 가리킨다.
- arguments 객체의 length는 프로퍼티 인자의 개수, 함수 객체의 length 프로퍼티는 매개 변수의 개수를 나타낸다.

```jsx
function a() {}
console.log(a.length); // 0

function b(x) { return x }
console.log(b.length); // 1

function b(x, y) { return x + y }
console.log(b.length); // 2
```

<br />

## 4) name 프로퍼티

- 함수 객체의 name 프로퍼티는 함수 이름을 나타낸다.

```jsx
// 기명 함수 표현식
const a = function b() {};
console.log(a.name); // b

// 익명 함수 표현식
const anonymousFunc = function () {};
console.log(anonymousFunc.name); // anonymousFunc

// 함수 선언문
function c() {}
console.log(c.name); // c
```

<br />

## 5) __proto__ 접근자 프로퍼티

- 모든 객체는 `[[Prototype]]` 이라는 내부 슬롯을 갖는다.
- __proto__프로퍼티는 `[[Prototype]]` 내부 슬롯이 가리키는 프로토타입 객체에 접근하기 위해 사용하는 접근자 프로퍼티다.
- 내부 슬롯에는 직접 접근할 수 없고 간접적인 접근 방법을 제공하는 경우에 한하여 접근할 수 있다.

```jsx
const obj = {a: 1};
console.log(obj.__proto__ === Object.prototype); // true
```

<br />

## 6) prototype 프로퍼티

- 생성자 함수로 호출할 수 있는 constructor를 소유하는 함수 객체에 존재하는 프로퍼티이다.
- 일반 객체, non-constructor 함수 객체에는 prototype 프로퍼티가 없다.

<br />

# 🤔 문제

1. 다음 코드의 실행 결과는?

```jsx
function A(a = 1) {
  arguments[0] = 100;
  return a;
}

function B(a) {
  arguments[0] = 100;
  return a;
}

console.log(A(10)); // (1)
console.log(B(10)); // (2)
```

<br />

- 답
    
    (1) 10
    
    (2) 100
    
    `arguments` 객체는 함수가 **나머지 매개변수, 기본 매개변수, 비구조화된 매개변수**에 포함되지 않는 경우에만 제공된다.
    

<br />

2. 다음 중 일급 객체에 대한 설명 중 아닌 것은?
    1. 배열에 저장할 수 있다.
    2. 함수의 매개변수에 전달할 수 있다.
    3. 함수가 일급 객체라면 함수 객체와 일반 객체는 차이가 없다.
    4. 함수의 반환값으로 사용할 수 있다.
    5. 일급 객체를 정의할 경우 런타임에 함수 객체로 평가된다.

<br />

- 답
    
    c.
    
    일반 객체는 호출할 수 없지만 함수 객체는 호출할 수 있다.
    
    함수 객체는 일반 객체에 없는 함수 고유의 프로퍼티를 소유한다.