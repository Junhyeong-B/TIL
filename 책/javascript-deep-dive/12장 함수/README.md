# 12장 함수

1. **함수 정의(function definition)** 을 통해 함수를 생성할 수 있는데, 함수 정의만으로 함수가 실행되는 것은 아니다.
    - 함수 실행은 명시적으로 **함수 호출(function call/invoke)** 을 해야한다.
    - 함수 이름은 생략할 수 있다.
        - 이름이 있는 함수: 기명 함수 **(named function)**
        - 이름이 없는 함수: 무명/익명 함수 **(anonymous function)**

<br />

2. 함수는 객체 타입의 값이므로 식별자를 붙일 수 있다.
    - 함수는 객체이지만 일반 객체와 다르게 호출이 가능하다.

<br />

3. 함수를 정의하는 방법은 아래와 같다.

```jsx
// 함수 선언문
function Fn(x, y) { return x + y }

// 함수 표현식
const Fn = function (x, y) { return x + y }

// function 생성자 함수
const Fn = new Function('x', 'y', 'return x + y')

// 화살표 함수
const Fn = (x, y) => x + y;
```

- 함수 이름을 생략하여 정의할 수 있지만, 함수 선언문은 함수 이름을 생략할 수 없다.

<br />

4. 함수 선언문은 표현식이 아닌 문으로 변수에 할당할 수 없으나 변수에 할당하는 것 처럼 작성하여 사용할 수 있는데, 이는 자바스크립트 엔진이 코드 문맥에 따라 해석이 달라질 수 있기 때문이다.

<br />

5. 그룹 연산자 `()` 내에 있는 함수 선언문은 함수 선언문으로 해석되지 않고 함수 리터럴 표현식으로 해석된다.
    
    그룹 연산자 내에 피연산자는 값으로 평가될 수 있는 표현식이어야 하지만 표현식이 아닌 문으로 해석되는 함수 선언문을 작성하면 에러가 발생한다.
    

```jsx
(function A() { console.log("A~"); })
A()
// Uncaught ReferenceError: A is not defined
```

<br />

6. 함수를 정의할 때 자바스크립트 엔진은 생성된 함수를 호출하기 위해 함수 이름과 동일한 이름의 식별자를 암묵적으로 생성하고, 거기에 함수 객체를 할당한다.
    - 6)의 내용으로 인해 생성된 함수 이름은 해당 함수를 가리키는 식별자가 된다.]
    - 함수 이름으로 함수를 호출한 것이 아니고, 함수 객체를 가리키는 식별자로 호출한 것이다.

<br />

7. 함수를 호출할 때 정의한 매개 변수보다 적은 매개변수로 호출하게 되면 호출한 매개변수 외의 변수들은 `undefined`로 할당되고, 더 많은 매개변수로 호출하게 되면 정의된 매개변수 이외의 값은 `arguments` 객체의 프로퍼티로 보관되고 사용되지는 않는다.(에러를 발생하지 않는다.)

```jsx
function add(x, y) { return x + y };

console.log(add(2)) // NaN => 2 + undefined
console.log(add(2, 5, 7)) // 7 => Arguments(3) [2, 5, 10, ...]
```

<br />

8. 함수의 인자의 타입을 명확하게 하기 위해 타입스크립트를 사용하거나 `typeof`, `throw new Error` 키워드의 사용, 호출 시 매개변수가 없다면 초기값 할당 등일 이용해 에러를 방지할 수 있다.

9. 함수의 매개변수에 대한 제한은 없지만 많을 수록 전달해야 할 인수의 순서를 고려해야 하고 유지보수나 가독성 측면에서 좋지 않으며 매개변수 개수는 0개가 가장 이상적이다.
    - 매개변수로 객체를 사용할 경우 프로퍼티 키를 정확하게 사용한다면 순서를 신경쓰지 않아도 된다.
    - **함수는 한 가지 일만 해야 하며 가급적 작게 만들어야 한다.**

<br />

10. 함수 정의와 동시에 즉시 호출되는 함수를 즉시 실행 함수(Immediately invoked function expression)이라고 한다.

```jsx
(function () { return console.log(1 + 2) }());
// 3
```

<br />

11. 함수의 매개변수를 통해 다른 함수의 내부로 전달되는 함수를 **콜백 함수(callback function)**라고 하며, 매개변수를 통해 함수의 외부에서 콜백 함수를 전달받은 함수를 **고차 함수(higher-order function, HOF)**라고 한다.

<br />

# 🤔 문제

1. 다음 중 에러가 발생하지 않는 경우는?

```jsx
// 1)
(function A() {
	console.log("A~");
}())
A();

// 2)
function (x, y) {
	return x + y;
}

// 3)
const C = function CC(x, y) {
	return x + y;
}
console.log(CC(1, 2));

// 4)
(function () {
	var d = 10;
	return d;
}());
```

- 답
    
    답: 4
    
    1) A~
    
        `ReferenceError: A is not defined`
    
    2) `SyntaxError: Function statements require a function name`
    
    3) `ReferenceError: CC is not defined`
    
    4) 10
    

<br />

2. 다음 코드의 실행 결과는?

```jsx
const a = function (x, y) { x + y }
console.log(a(1, 2));
```

1) `3`

2) `NaN`

3) `undefined`

4) `SyntaxError: Function statements require a function name`

5) `ReferenceError: a is not defined`

- 답
    
    3) undefined
    
    ⇒ 리턴문이 없기 때문에 undefined를 반환한다.