# 25장 클래스

# 1. 클래스는 프로토타입의 문법적 설탕인가?

- 자바스크립트는 프로토타입 기반 객체 지향 언어
- 클래스는 객체지향 프로그래밍 언어와 매우 흡사한 새로운 객체 생성 매커니즘이다.
- ES6의 클래스가 기존의 프로토타입 기반 객체지향 모델을 폐기하는 것이 아니라 **클래스는 함수**이고, 기존 **프로토타입 기반 패턴을 클래스 기반 패턴처럼 사용**할 수 있도록 하는 문법적 설탕이라고 볼 수도 있다.

<br />

## 1-1) 클래스와 생성자 함수의 차이

### 클래스

1. new 연산자 없이 호출하면 에러가 발생
2. 상속을 지원하는 extends, super 키워드 제공
3. 호이스팅이 발생하지 않는 것처럼 동작
4. 암묵적으로 strict mode가 지정되며 해제할 수 없음
5. constructor, 프로토타입 메서드, 정적 메서드는 열거되지 않는다.
    
    (프로퍼티 어트리뷰트 [[Enumerable]] 값이 false)
    

<br />

### 생성자 함수

1. new 연산자 없이 호출하면 일반 함수로서 호출
2. extends, super 미지원
3. 함수 선언문으로 정의하면 함수 호이스팅, 함수 표현식으로 정의하면 변수 호이스팅이 발생
4. 암묵적 strict mode가 지정되지 않음

<br />

# 2. 클래스 정의

1. **`class` 키워드**를 사용하여 정의한다.
2. `**표현식**`으로 클래스를 정의한다.

```jsx
// 클래스 선언문
class Person {}

// 익명 클래스 표현식
const Person = class {};

// 기명 클래스 표현식
const Person = class MyClass {};
```

- 클래스를 표현식으로 정의할 수 있다는 것은 값으로 사용할 수 있는 일급 객체라는 뜻이다.
    - 무명의 리터럴로 생성할 수 있다.(런타임에 생성이 가능)
    - 변수나 자료구조에 저장할 수 있다.
    - 함수의 매개변수에 전달할 수 있다.
    - 함수의 반환값으로 사용할 수 있다.
- 클래스 몸체에서 정의할 수 있는 메서드는 **constructor(생성자)**, **프로토타입 메서드**, **정적 메서드**의 세 가지가 있다.

<br />

```jsx
// 클래스 선언문
class Person {
  // 생성자
  constructor(name) {
    // 인스턴스 생성 및 초기화
    this.name = name; // name 프로퍼티는 public하다.
  }

  // 프로토타입 메서드
  sayHi() {
    console.log(`Hi! My name is ${this.name}`);
  }

  // 정적 메서드
  static sayHello() {
    console.log('Hello!');
  }
}

// 인스턴스 생성
const me = new Person('Lee');

// 인스턴스의 프로퍼티 참조
console.log(me.name); // Lee
// 프로토타입 메서드 호출
me.sayHi(); // Hi! My name is Lee
// 정적 메서드 호출
Person.sayHello(); // Hello!
```

<br />

# 3. 클래스 호이스팅

- 클래스 선언문으로 정의한 클래스는 **런타임 이전**에 **먼저 평가**되어 함수 객체를 생성한다.
- 단, 클래스는 정의 이전에 참조할 수 없다.
    - ⇒ 호이스팅이 발생하지 않는 것처럼 동작한다.
    - var, let, const, function, class 키워드를 사용하여 선언된 모든 식별자는 호이스팅 된다. 모든 선언문은 런타임 이전에 먼저 실행되기 때문이다.

<br />

# 4. 인스턴스 생성

- 함수는 new 연산자의 사용 여부에 따라 일반 함수로 호출되거나 생성자 함수로 호출되지만 **클래스**는 인스턴스를 생성하는 것이 유일한 존재 이유이므로 **반드시 new 연산자와 함께 호출**해야 한다.
- 클래스 이름은 클래스 몸체 내부에서만 유효하고 외부 코드에서 접근할 수 없다.

<br />

# 5. 메서드

## 5-1) constructor

- 인스턴스를 생성하고 초기화하기 위한 특수한 메서드이고, 이름을 변경할 수 없다.
- constructor는 최대 한 개만 존재할 수 있고, 생략할 수도 있다.
    - 중복될 경우 SyntaxError 발생
    - 생략할 경우 빈 constructor(`constructor () {}`)가 암묵적으로 정의된다.
- 프로퍼티가 추가되어 초기화된 인스턴스를 생성하려면 constructor 내부에서 this에 인스턴스 프로퍼티를 추가한다.
- 인스턴스를 생성할 때 초기값을 전달하려면 constructor에 매개변수를 선언하여 전달한다.
- 별도의 반환문을 갖지 않아야 한다. ⇒ 암묵적으로 this 반환

```jsx
class Person {
  // 생성자
  constructor(name) {
    // 인스턴스 생성 및 초기화
    this.name = name;
  }
}
```

<br />

## 5-2) 프로토타입 메서드

- 생성자 함수에 의한 객체 생성 방식과 다르게 prototype 프로퍼티에 메서드를 추가하지 않아도 기본적으로 프로토타입 메서드가 된다.

```jsx
// 생성자 함수
function Person(name) {
  this.name = name;
}

// 프로토타입 메서드
Person.prototype.sayHi = function () {
  console.log(`Hi! My name is ${this.name}`);
};

// 클래스
class Person {
  // 생성자
  constructor(name) {
    // 인스턴스 생성 및 초기화
    this.name = name;
  }

  // 프로토타입 메서드
  sayHi() {
    console.log(`Hi! My name is ${this.name}`);
  }
}
```

<br />

## 5-3) 정적 메서드

- 인스턴스를 생성하지 않아도 호출할 수 있는 메서드
- `static` 키워드를 붙이면 정적 메서드가 된다.
- 정적 메서드는 인스턴스로 호출할 수 없다.
    
    ⇒ 정적 메서드가 바인딩된 클래스는 인스턴스의 프로토타입 체인 상에 존재하지 않기 때문
    

```jsx
class Person {
  // 생성자
  constructor(name) {
    // 인스턴스 생성 및 초기화
    this.name = name;
  }

  // 정적 메서드
  static sayHi() {
    console.log('Hi!');
  }
}
```

<br />

## 5-4) 정적 메서드와 프로토타입 메서드의 차이

1. 정적 메서드와 프로토타입 메서드는 자신이 속해 있는 **프로토타입 체인이 다르다**.
2. 정적 메서드는 **클래스로 호출**하고 프로토타입 메서드는 **인스턴스로 호출**한다.
3. 정적 메서드는 **인스턴스 프로퍼티를 참조할 수 없지만** 프로토타입 메서드는 **인스턴스 프로퍼티를 참조할 수 있다.**

<br />

## 5-5) 클래스에서 정의한 메서드의 특징

1. function 키워드를 생략한 메서드 축약 표현을 사용한다.
2. 메서드를 정의할 때 콤마가 필요 없다.
3. strict mode
4. `for ... in` 문이나 `Object.keys` 메서드 등으로 열거할 수 없다.
5. `[[construct]]`를 갖지 않는 non-constructor 이므로 new 연산자와 함께 호출할 수 없다.

<br />

# 6. 프로퍼티

## 6-1) 인스턴스 프로퍼티

- constructor 내부 코드가 실행되기 이전의 constructor 내부의 this에는 이미 암묵적으로 생성한 인스턴스인 빈 객체가 바인딩되어 있다.
- constructor 내부에 인스턴스 프로퍼티를 정의하면 생성한 빈 객체에 추가되어 인스턴스가 초기화된다.
- 인스턴스 프로퍼티는 언제나 public 하다.
    
    ⇒ private, public, protected 등의 접근 제한자를 지원하지 않는다.
    

<br />

## 6-2) 접근자 프로퍼티

- 자체적으로 값을 갖지 않고 다른 데이터 프로퍼티의 값을 읽거나 저장할 때 사용하는 접근자 함수로 구성된 프로퍼티다.
- getter 함수, setter 함수로 구성된다.
- getter는 메서드 이름 앞에 get, setter는 메서드 이름 앞에 set을 작성한다.
- getter | setter는 호출하는 것이 아니라 참조 | 할당 하는 형식으로 사용한다.

```jsx
class Person {
  constructor(firstName, lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  // fullName은 접근자 함수로 구성된 접근자 프로퍼티다.
  // getter 함수
  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  // setter 함수
  set fullName(name) {
    [this.firstName, this.lastName] = name.split(' ');
  }
}

const me = new Person('Ungmo', 'Lee');

// 접근자 프로퍼티 fullName에 값을 저장하면 setter 함수가 호출된다.
me.fullName = 'Heegun Lee';
console.log(me); // {firstName: "Heegun", lastName: "Lee"}

// 접근자 프로퍼티 fullName에 접근하면 getter 함수가 호출된다.
console.log(me.fullName); // Heegun Lee
```

## 6-3) private 필드 정의 제안

- 인스턴스 프로퍼티는 언제나 public이다.
- private 필드의 선두에는 #을 붙이고, 참조할 때도 #을 붙여야 한다.
- private 필드는 반드시 클래스 몸체에 정의해야 한다.
    
    ⇒ 직접 constructor에 정의하면 에러가 발생한다.
    

```jsx
class Person {
  // private 필드 정의
  #name = '';

  constructor(name) {
    // private 필드 참조
    this.#name = name;
  }
}

const me = new Person('Lee');

// private 필드 #name은 클래스 외부에서 참조할 수 없다.
console.log(me.#name);
// SyntaxError: Private field '#name' must be declared in an enclosing class
```

<br />

# 7. 상속에 의한 클래스 확장

## 7-1) 클래스 상속

- 상속에 의한 클래스 확장은 기존 클래스를 상속받아 새로운 클래스를 확장**(extends)**하여 정의한다.
    
    ⇒ 프로토타입 기반 상속은 프로토타입 체인을 통해 다른 객체의 자산을 생속받는 개념이다.
    

```jsx
class Animal {
  constructor(age, weight) {
    this.age = age;
    this.weight = weight;
  }

  eat() { return 'eat'; }
  move() { return 'move'; }
}

// 상속을 통해 Animal 클래스를 확장한 Bird 클래스
class Bird extends Animal {
  fly() { return 'fly'; }
}

const bird = new Bird(1, 5);

console.log(bird); // Bird {age: 1, weight: 5}
console.log(bird instanceof Bird); // true
console.log(bird instanceof Animal); // true

console.log(bird.eat());  // eat
console.log(bird.move()); // move
console.log(bird.fly());  // fly
```

<br />

## 7-2) extends 키워드

- extends 키워드를 사용하여 상속받을 클래스를 정의한다.
- 상속을 통해 확장된 클래스를 서브클래스(subclass) | 서브클래스에게 상속된 클래스를 수퍼클래스(superclass)라 부른다.
    - 서브클래스: 파생 클래스(derived class) || 자식 클래스(child class)
    - 수퍼클래스: 베이스 클래스(base class) || 부모 클래스(parent class)
- 프로토타입 체인을 통해 프로토타입 메서드, 정적 메서드 모두 상속이 가능하다.

```jsx
// 수퍼(베이스/부모)클래스
class Base {}

// 서브(파생/자식)클래스
class Derived extends Base {}
```

<br />

## 7-3) 동적 상속

- extends 키워드는 생성자 함수를 상속받아 클래스를 확장할 수도 있다. 이 경우 extends 키워드 앞에는 반드시 클래스가 와야 한다.

<br />

## 7-4) 서브 클래스의 constructor

- 서브 클래스에서 constructor를 생략하면 다음과 같은 constructor가 암묵적으로 정의된다.

```jsx
constructor(...args) { super(...args); }
```

<br />

## 7-5) super 키워드

- super를 호출하면 수퍼 클래스의 constructor를 호출한다.
- super를 참조하면 수퍼 클래스의 메서드를 호출할 수 있다.

```jsx
// 수퍼클래스
class Base {
  constructor(a, b) { // ④
    this.a = a;
    this.b = b;
  }
}

// 서브클래스
class Derived extends Base {
  constructor(a, b, c) { // ②
    super(a, b); // ③
    this.c = c;
  }
}

const derived = new Derived(1, 2, 3); // ①
console.log(derived); // Derived {a: 1, b: 2, c: 3}
```

<br />

### super 호출 주의사항

1. 서브클래스에서 constructor를 생략하지 않는 경우 constructor에서는 반드시 super를 호출해야 한다.
2. 서브클래스에서 super를 호출하기 전에는 this를 참조할 수 없다.
3. super는 반드시 서브클래스의 constructor에서만 호출한다. ⇒ 그 외에는 에러 발생

<br />

### super 참조

- 메서드 내에서 super를 참조하면 수퍼클래스의 메서드를 호출할 수 있다.

```jsx
// 수퍼클래스
class Base {
  constructor(name) {
    this.name = name;
  }

  sayHi() {
    return `Hi! ${this.name}`;
  }
}

// 서브클래스
class Derived extends Base {
  sayHi() {
    // super.sayHi는 수퍼클래스의 프로토타입 메서드를 가리킨다.
    return `${super.sayHi()}. how are you doing?`;
  }
}

const derived = new Derived('Lee');
console.log(derived.sayHi()); // Hi! Lee. how are you doing?
```

<br />

# 🤔 문제

1. 클래스의 `constructor` 메서드에 대한 설명으로 **옳지 않은 것**은?

1) 인스턴스를 생성하고 초기화하기 위한 특수한 메서드이고, 이름을 변경할 수 없다.

2) constructor는 생략할 수 있고, 두 개 이상의 constructor가 작성될 경우 가장 마지막에 작성된 메서드가 동작한다.

3) 프로퍼티가 추가되어 초기화된 인스턴스를 생성하려면 constructor 내부에서 this에 인스턴스 프로퍼티를 추가한다.

4) 인스턴스를 생성할 때 초기값을 전달하려면 constructor에 매개변수를 선언하여 전달한다.

5) 별도의 반환문을 갖지 않아야 하지만 반환문을 작성해도 에러는 발생하지 않는다.

<br />

- 답
    
    **2)**
    
    - constructor는 최대 한 개만 존재할 수 있고, 생략할 수도 있다.
        - 중복될 경우 SyntaxError 발생
        - 생략할 경우 빈 constructor(`constructor () {}`)가 암묵적으로 정의된다.

<br />

2. 다음 코드 동작 시 에러가 발생하는데, 왜 에러가 발생할까요?

```jsx
class Base {}

class Derived extends Base {
  constructor() {
    console.log('constructor call');
  }
}

const derived = new Derived();
```

<br />

- 답
    - 서브클래스에서 **constructor를 생략하지 않는 경우** 서브클래스의 constructor에는 **반드시 super를 호출**해야 한다.
    - 서브클래스에서 constructor를 생략하는 경우 암묵적으로
        
        `constructor(...args) { super(...args); }` 가 정의된다.
        
    
    ※ 발생되는 에러: 
    
    `ReferenceError: Must call super constructor in derived class before accessing 'this' or returning from derived constructor`