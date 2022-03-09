# 26장 ES6 함수의 추가 기능

# 1. 함수의 구분

- ES6 이전의 함수는 사용 목적에 따라 명확히 구분되지 않고, 모든 함수는 일반 함수, 생성자 함수로서 호출할 수 있다.

```jsx
var a = function() { return 1; };
var obj = { a: a };

a(); // 1 → 일반 함수로 호출
new a(); // a {} → 생성자 함수로 호출
obj.a(); // 1 → 메서드로 호출
new obj.a(); // a {} → 프로퍼티 a에 바인딩된 함수를 생성자 함수로 호출
// ES6 이전 함수에서 객체에 바인딩된 함수를 생성자 함수로 호출하는 것은 문법상 가능하다.
```

<br />

## 1-1) ES6 이전 함수의 문제점

- 모든 함수가 **callable**, **constructor** 하다.
- 사용 목적에 따라 명확한 구분이 없으므로 호출 방식에 특별한 제약이 없다.
- 생성자 함수로 호출하지 않아도 프로토타입 객체를 생성한다.
    - 이는 실수를 유발할 가능성이 있고, 성능면에서도 좋지 않다.

<br />

# 2. 메서드

- ES6 이전에는 메서드에 대한 명확한 정의가 없었고, ES6에서 명확하게 규정되었다.
    - ES6 사양에서 메서드는 축약 표현으로 정의된 함수

<br />

## 2-1) 메서드의 특징

1. ES6에서 정의한 메서드는 인스턴스를 생성할 수 없는 **non-constructor**다.
2. 인스턴스를 생성할 수 없으므로 prototype 프로퍼티가 없고 프로토타입도 생성하지 않는다.
3. 자신을 바인딩한 객체를 가리키는 내부 슬롯 `[[HomeObject]]`를 갖는다.

```jsx
const obj = {
	a() { return 1; }, // 메서드
	b: function() { return 1; } // 일반 함수
}

console.log(obj.a()); // 1
console.log(obj.b()); // 1

1. 인스턴스를 생성할 수 없는 non-constructor이므로 생성자 함수로 호출할 수 없다.
new obj.a(); // TypeError: obj.a is not a constructor
new obj.b(); // b {}

2. 프로토타입을 생성하지 않는다.
obj.a.hasOwnProperty('prototype'); // false
obj.b.hasOwnProperty('prototype'); // true
```

<br />

# 3. 화살표 함수

- `function` 키워드 대신 화살표 (`=>`)를 사용하여 간략하게 함수를 정의할 수 있다.
- 내부 동작도 기존의 함수보다 간략하다.
- 콜백 함수 내부에서 **this가 전역 객체를 가리키는 문제를 해결**하기 위한 대안으로 유용하다.

<br />

## 3-1) 화살표 함수 정의

1. 화살표 함수는 **함수 표현식으로 정의**해야 한다.
2. 매개 변수가 한 개인 경우 소괄호를 생략할 수 있고, 그 외의 경우에는 생략할 수 없다.
3. 함수 몸체가 **하나의 문이라면 중괄호를 생략**할 수 있고, 이때 함수 몸체가 값으로 평가될 수 있는 표현식인 문이라면 **암묵적으로 반환**된다.
    - 표현식이 아닌 문은 반환할 수 없으므로 에러가 발생한다.
4. 함수 몸체가 여러 개의 문이라면 중괄호를 생략할 수 없고, 반환값이 있다면 명시적으로 반환해야 한다.
5. 화살표 함수도 **즉시 실행 함수**로 사용할 수 있다.

```jsx
const a = () => {};
const b = x => { return x };
const c = () => "문자열";
const d = () => const y = 1; // SyntaxError: Unexpected token 'const'

const e = (name => ({
	sayHi() { return `안녕 난 ${name}야`; }
}))('Bae')
console.log(e.sayHi()); // 안녕 난 Bae야
```

<br />

## 3-2) 일반 함수와의 차이

1. 화살표 함수는 인스턴스를 생성할 수 없는 non-constructor다.
2. 중복된 매개변수 이름을 선언할 수 없다.
3. 화살표 함수는 함수 자체에 this, arguments, super, new.target 바인딩을 갖지 않는다.
    - 따라서 해당 바인딩을 참조하면 스코프 체인을 통해 상위 스코프의 바인딩을 참조한다.

<br />

## 3-3) this

- 일반 함수로서 호출되는 모든 함수 내부의 this는 전역 객체를 가리킨다.

```jsx
class Prefixer {
  constructor(prefix) {
    this.prefix = prefix;
  }

  add(arr) {
    // add 메서드는 인수로 전달된 배열 arr을 순회하며 배열의 모든 요소에 prefix를 추가한다.
    // ①
    return arr.map(function (item) {
      return this.prefix + item; // ②
      // -> TypeError: Cannot read property 'prefix' of undefined
    });
  }
}

const prefixer = new Prefixer('-webkit-');
console.log(prefixer.add(['transition', 'user-select']));
```

- 위 예제의 경우 prefix가 undefined여서 TypeError가 발생하는데, 이유는 다음과 같다.
    1. 클래스 내부의 모든 코드에는 strict mode가 암묵적으로 적용된다.
    2. 따라서 클래스 내부 `.map()`에도 strict mode가 적용된다.
    3. **strict mode**에서 일반 함수로 호출된 모든 함수 내부의 **this는 undefined**가 바인딩된다.

<br />

### ES6 이전 해당 문제 해결 방법

1. this를 새로운 변수로 할당하고, this 대신 해당 변수를 참조한다.
2. add 메서드를 호출한 부분의 두 번째 인수로 this를 전달한다.
3. Function.prototype.bind 메서드를 이용해서 this를 바인딩한다.

<br />

### 화살표 함수를 통한 해결 방법

```jsx
class Prefixer {
  constructor(prefix) {
    this.prefix = prefix;
  }

  add(arr) {
    return arr.map(item => this.prefix + item);
  }
}

const prefixer = new Prefixer('-webkit-');
console.log(prefixer.add(['transition', 'user-select']));
// ['-webkit-transition', '-webkit-user-select']
```

- 화살표 함수 자체는 this 바인딩을 갖지 않고, 위 경우 함수 내부에서 this를 참조하면서 상위 스코프의 this를 그대로 참조한다.
    - 이를 **lexical this**라고 한다.

<br />

### 화살표 함수의 call, apply, bind

- call, apply, bind 메서드는 첫 번째 인자로 this를 받지만, 화살표 함수는 this가 바인딩 되지 않으므로 비어있다는 의미로 null을 사용한다.

```jsx
const add = (a, b) => a + b;

console.log(add.call(null, 1, 2));    // 3
console.log(add.apply(null, [1, 2])); // 3
console.log(add.bind(null, 1, 2)());  // 3
```

<br />

## 3-4) super | arguments

- 화살표 함수는 함수 자체의 `super`, `arguments` 바인딩을 갖지 않는다.
    - super 또는 arguments를 참조하면 this와 마찬가지로 상위 스코프의 super 또는 arguments를 참조한다.

<br />

### arguments

- 매개변수의 개수를 확정할 수 없는 **가변 인자 함수**를 구현할 때 화살표 함수를 통해 함수를 정의한다면 arguments 객체를 사용할 수 없으므로 그다지 도움되지 않는다.
- 따라서 화살표 함수로 가변 인자 함수를 구현해야 할 때는 반드시 **Rest 파라미터**를 사용해야 한다.

<br />

# 4. Rest 파라미터

## 4-1) 기본 문법

- Rest 파라미터(나머지 매개변수)는 함수에 전달된 인수들의 목록을 배열로 전달받는다.

```jsx
function foo(...rest) {
  // 매개변수 rest는 인수들의 목록을 배열로 전달받는 Rest 파라미터다.
  console.log(rest); // [ 1, 2, 3, 4, 5 ]
}

foo(1, 2, 3, 4, 5);
```

- Rest 파라미터는 **일반 매개변수와 같이 사용**할 수 있지만, 매개변수에 할당된 인수를 제외한 나머지 인수들로 구성된 배열이 할당되므로 **반드시 마지막 파라미터**여야 한다.
- 단 하나만 선언할 수 있다.
- 함수 정의 시 매개변수 개수를 나타내는 함수 객체의 length 프로퍼티에 영향을 주지 않는다.

<br />

# 5. 매개변수 기본값

- 인수가 전달되지 않은 매개변수의 값은 undefined다.
- 의도치 않은 결과를 예방하기 위해 다음과 같이 기본값(ES6에서 도입)을 작성하여 방어 코드를 작성할 수 있다.
    - 단, Rest 파라미터에는 기본값을 지정할 수 없다.

```jsx
function sum(x = 0, y = 0) {
  return x + y;
}

console.log(sum(1, 2)); // 3
console.log(sum(1));    // 1
```

<br />

# 🤔 문제

1. 다음 코드의 실행 결과로 알맞은 것은?

```jsx
function A(...rest, param1, param2) {
	console.log(rest);
	console.log(param1);
	console.log(param2);
}

A(1, 2, 3, 4, 5);
```

1. **rest**: `[1, 2, 3]`  |  **param1**: `4`  |  **param2**: `5`
2. **rest**: `1, 2, 3`  |  **param1**: `4`  |  **param2**: `5`
3. **rest**: `[1, 2, 3, 4, 5]`  |  **param1**: `undefined`  |  **param2**: `undefined`
4. **rest**: `1, 2, 3, 4, 5`  |  **param1**: `undefined`  |  **param2**: `undefined`
5. `Rest parameter must be last formal parameter`

<br />

- 답
    
    **5**
    
    Rest 파라미터는 이름 그대로 먼저 선언된 매개변수에 할당된 인수를 제외한 나머지 인수들로 구성된 배열이 할당된다.
    
    따라서 Rest 파라미터는 반드시 마지막 파라미터여야 한다.
    

<br />

2. 일반 함수와 화살표 함수의 차이로 **알맞지 않은** 것은?
    
    ① 일반 함수는 constructor, 화살표 함수는 non-constructor다.
    
    ② 일반 함수는 매개변수 이름을 중복해서 선언할 수 있고, 화살표 함수는 중복된 매개변수 이름을 선언할 수 없다.
    
    ③ 일반 함수는 즉시 실행 함수로 작성될 수 있지만 화살표 함수는 즉시 실행 함수로 작성될 수 없다.
    
    ④ 화살표 함수는 함수 자체에 arguments, super, new.target 바인딩을 갖지 않는다.
    
    ⑤ 화살표 함수로 this를 참조하면 스코프 체인을 통해 상위 스코프의 바인딩을 참조하는데, 이때 해당 화살표 함수가 가장 상위이면 window 객체가 반환된다.
    
<br />

- 답
    
    ③
    
    화살표 함수도 즉시 실행 함수로 작성될 수 있다.
    
    ```jsx
    const hello = (name => ({
    	sayHi() { return `안녕 난 ${name}야`; }
    }))('Bae')
    
    console.log(hello.sayHi()); // 안녕 난 Bae야
    ```