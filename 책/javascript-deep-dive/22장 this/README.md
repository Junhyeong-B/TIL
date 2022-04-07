# 22장 this

# 1. this 키워드

- **this**는 자신이 속한 객체 또는 자신이 생성할 인스턴스를 가리키는 **자기 참조 변수(self-referencing variable)**다.
- this는 자바스크립트 엔진에 의해 암묵적으로 생성되고, 코드 어디서든 참조할 수 있다.
- 자바스크립트에서는 함수가 호출되는 방식에 따라 this 바인딩이 동적으로 결정된다.

```jsx
// this는 어디서든지 참조 가능하다.
// 전역에서 this는 전역 객체 window를 가리킨다.
console.log(this); // window

function square(number) {
  // 일반 함수 내부에서 this는 전역 객체 window를 가리킨다.
  console.log(this); // window
  return number * number;
}
square(2);

const person = {
  name: 'Lee',
  getName() {
    // 메서드 내부에서 this는 메서드를 호출한 객체를 가리킨다.
    console.log(this); // {name: "Lee", getName: ƒ}
    return this.name;
  }
};
console.log(person.getName()); // Lee

function Person(name) {
  this.name = name;
  // 생성자 함수 내부에서 this는 생성자 함수가 생성할 인스턴스를 가리킨다.
  console.log(this); // Person {name: "Lee"}
}

const me = new Person('Lee');
```

<br />

- this는 객체의 프로퍼티나 메서드를 참조하기 위한 자기 참조 변수이므로 객체의 메서드 내부, 생성자 함수 내부에서만 의미가 있다.
    
    ⇒ 따라서 strict mode에서 일반함수에서의 this는 undefined가 바인딩된다.(사용할 필요가 없기 때문)
    

<br />

# 2. 함수 호출 방식과 this 바인딩

- this 바인딩은 함수 호출 방식에 따라 동적으로 결정된다.
    - 일반 함수 호출
    - 메서드 호출
    - 생성자 함수 호출
    - Function.prototype.apply/call/bind 메서드에 의한 간접 호출

```jsx
// this 바인딩은 함수 호출 방식에 따라 동적으로 결정된다.
const foo = function () {
  console.dir(this);
};

// 동일한 함수도 다양한 방식으로 호출할 수 있다.

// 1. 일반 함수 호출
// foo 함수를 일반적인 방식으로 호출
// foo 함수 내부의 this는 전역 객체 window를 가리킨다.
foo(); // window

// 2. 메서드 호출
// foo 함수를 프로퍼티 값으로 할당하여 호출
// foo 함수 내부의 this는 메서드를 호출한 객체 obj를 가리킨다.
const obj = { foo };
obj.foo(); // obj

// 3. 생성자 함수 호출
// foo 함수를 new 연산자와 함께 생성자 함수로 호출
// foo 함수 내부의 this는 생성자 함수가 생성한 인스턴스를 가리킨다.
new foo(); // foo {}

// 4. Function.prototype.apply/call/bind 메서드에 의한 간접 호출
// foo 함수 내부의 this는 인수에 의해 결정된다.
const bar = { name: 'bar' };

foo.call(bar);   // bar
foo.apply(bar);  // bar
foo.bind(bar)(); // bar
```

<br />

## 2-1) 일반 함수 호출

- 전역 함수는 물론 중첩 함수를 일반 함수로 호출하면 함수 내부의 this에는 전역 객체가 바인딩된다.
- 콜백 함수의 내부 this에도 전역 객체가 바인딩된다.

<br />

### ✅ 메서드 내부의 중첩 함수나 콜백 함수에 this를 바인딩 하려면?

- 메서드 내부에서 this를 변수에 할당하고, 해당 변수를 this처럼 사용한다.
- Function.prototype.apply/call/bind 메서드를 통해 this를 바인딩한다.
- 화살표 함수를 사용해 this를 바인딩한다.
    - 화살표 함수의 this는 상위 스코프의 this를 가리킨다.

<br />

## 2-2) 메서드 호출

- 메서드를 호출할 때 메서드 이름 앞의 마침표 연산자 앞에 기술한 객체가 바인딩된다.
    - 메서드를 **소유한 객체가 아닌** 메서드를 **호출한 객체에 바인딩**된다.

```jsx
const person = {
  name: 'Lee',
  getName() {
    // 메서드 내부의 this는 메서드를 호출한 객체에 바인딩된다.
    return this.name;
  }
};

// 메서드 getName을 호출한 객체는 person이다.
console.log(person.getName()); // Lee

const anotherPerson = {
  name: 'Kim'
};
// getName 메서드를 anotherPerson 객체의 메서드로 할당
anotherPerson.getName = person.getName;

// getName 메서드를 호출한 객체는 anotherPerson이다.
console.log(anotherPerson.getName()); // Kim

// getName 메서드를 변수에 할당
const getName = person.getName;

// getName 메서드를 일반 함수로 호출
console.log(getName()); // ''
// 일반 함수로 호출된 getName 함수 내부의 this.name은 브라우저 환경에서 window.name과 같다.
// 브라우저 환경에서 window.name은 브라우저 창의 이름을 나타내는 빌트인 프로퍼티이며 기본값은 ''이다.
// Node.js 환경에서 this.name은 undefined다.
```

<br />

## 2-3) 생성자 함수 호출

- 생성자 함수 내부의 this에는 생성자 함수가 생성할 인스턴스가 바인딩된다.

```jsx
// 생성자 함수
function Circle(radius) {
  // 생성자 함수 내부의 this는 생성자 함수가 생성할 인스턴스를 가리킨다.
  this.radius = radius;
  this.getDiameter = function () {
    return 2 * this.radius;
  };
}

// 반지름이 5인 Circle 객체를 생성
const circle = new Circle(5);
console.log(circle.getDiameter()); // 10
```

 
<br />


## 2-4) Function.prototype.apply/call/bind 메서드에 의한 간접 호출

- apply, call, bind 메서드는 Function.prototype의 메서드이므로 모든 함수가 상속받아 사용할 수 있다.
- apply/call 메서드의 본질적인 기능은 함수를 호출하는 것이다.
    - 해당 메서드로 함수를 호출하면서 첫 번째 인수로 전달한 특정 객체를 호출한 함수의 this에 바인딩한다.

```jsx
function getThisBinding() {
  console.log(arguments);
  return this;
}

// this로 사용할 객체
const thisArg = { a: 1 };

// getThisBinding 함수를 호출하면서 인수로 전달한 객체를 getThisBinding 함수의 this에 바인딩한다.
// apply 메서드는 호출할 함수의 인수를 배열로 묶어 전달한다.
console.log(getThisBinding.apply(thisArg, [1, 2, 3]));
// Arguments(3) [1, 2, 3, callee: ƒ, Symbol(Symbol.iterator): ƒ]
// {a: 1}

// call 메서드는 호출할 함수의 인수를 쉼표로 구분한 리스트 형식으로 전달한다.
console.log(getThisBinding.call(thisArg, 1, 2, 3));
// Arguments(3) [1, 2, 3, callee: ƒ, Symbol(Symbol.iterator): ƒ]
// {a: 1}
```

<br />

- bind 메서드는 함수를 호출하지 않고 this로 사용할 객체만 전달한다.
    - 메서드의 this와 메서드 내부의 중첩 함수 또는 콜백 함수의 this가 불일치 하는 문제를 해결하기 위해 유용하게 사용된다.

```jsx
function getThisBinding() {
  return this;
}

// this로 사용할 객체
const thisArg = { a: 1 };

// bind 메서드는 첫 번째 인수로 전달한 thisArg로 this 바인딩이 교체된
// getThisBinding 함수를 새롭게 생성해 반환한다.
console.log(getThisBinding.bind(thisArg)); // getThisBinding
// bind 메서드는 함수를 호출하지는 않으므로 명시적으로 호출해야 한다.
console.log(getThisBinding.bind(thisArg)()); // {a: 1}
```

<br />

# 🤔 문제

1. 다음 실행 코드의 콘솔에는 무엇이 출력되나요?

```jsx
var value = 1;

const obj = {
  value: 100,
  foo() {
    console.log(this);         // 1)
    console.log(this.value);   // 2)

    function bar() {
      console.log(this);       // 3)
      console.log(this.value); // 4)
    }

    bar();
  }
};

obj.foo();
```

<br />

- 답
    
    1) `{value: 100, foo: ƒ}`
    
    2) 100
    
    3) `window`
    
    4) 1
    
    var 키워드로 선언한 전역 변수 value는 전역 객체의 프로퍼티이다.(const는 아님)
    
    전역 함수는 물론 중첩 함수를 **일반 함수로 호출**하면 함수 내부의 **this에는 전역 객체가 바인딩**된다.