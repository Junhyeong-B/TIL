# 19장 프로토타입

# 1. 객체지향 프로그래밍

- 자바스크립트를 이루고 있는 **거의 모든 것이 객체**다.
- **객체지향 프로그래밍**은 여러 개의 독립적 단위의 객체의 집합으로 프로그램을 표현하려는 프로그래밍 패러다임이다.
    - 객체의 **상태(state)**와 상태를 조작할 수 있는 **동작(behavior)**를 하나의 논리적인 단위로 묶어 생각한다.
    
    ※ **명령형 프로그래밍**은 명령어 또는 함수의 목록으로 보는 프로그래밍 패러다임
    

<br />

- 실체는 특징이나 성질을 나타내는 **속성(attribute/property)**이고, 필요한 속성만 간추려 표현하는 것을 **추상화(abstraction)**라고 한다.

<br />

# 2. 상속과 프로토타입

- **상속(inheritance)**은 어떤 객체의 프로퍼티 또는 메서드를 다른 객체가 상속받아 그대로 사용할 수 있는 것을 말한다.
- 자바스크립트는 프로토타입을 기반으로 상속을 구현하여 불필요한 중복을 제거한다.

<br />

## 1) 생성자 함수에서의 코드 중복

```jsx
function Circle(radius) {
	this.radius = radius;
	this.getArea = function () {
		return Math.PI * this.radius ** 2;
	}
}

const circle1 = new Circle(1);
const circle2 = new Circle(2);
console.log(circle1.getArea === circle2.getArea) // false 
```

- getArea는 하나만 생성하고 모든 인스턴스가 공유하는 것이 바람직하지만 생성자 함수에서는 **내용이 동일한 메서드도 중복 생성**한다.
- 10개의 인스턴스를 생성하면 내용이 동일한 메서드도 10개가 생성된다.

<br />

## 2) 프로토타입 기반 상속으로 인한 코드 중복 제거

```jsx
function Circle(radius) {
	this.radius = radius;
}

Circle.prototype.getArea = function () {
	return Math.PI * this.radius ** 2;
}

const circle1 = new Circle(1);
const circle2 = new Circle(2);
console.log(circle1.getArea === circle2.getArea) // true
```

- Circle 생성자 함수가 생성한 인스턴스가 메서드를 공유할 수 있도록 프로토타입에 추가했고, 이 경우 프로토타입은 Circle 생성자 함수의 prototype 프로퍼티에 바인딩되어 있다.
- Circle 생성자 함수가 생성한 **모든 인스턴스**는 부모 객체의 역할을 하는 프로토타입인 **Circle.prototype으로부터 메서드를 상속**받는다.

※ 상속은 코드의 재사용이란 관점에서 매우 유용하다.

<br />

# 3. 프로토타입 객체

- **프로토타입 객체**는(또는 줄여서 프로토타입) 어떤 객체의 상위 객체의 역할을 하는 객체로 **다른 객체에게 공유 프로퍼티를 제공**한다.
- 프로토타입을 상속받은 하위 객체는 상위 객체의 프로퍼티를 자신의 프로퍼티처럼 자유롭게 사용할 수 있다.
- 모든 객체는 `[[prototype]]` 내부슬롯을 갖고, 하나의 프로토타입을 갖는다.
- `[[prototype]]` 내부 슬롯에는 직접 접근할 수 없지만 `__proto__` 접근자 프로퍼티를 통해 자신의 프로토타입에 간접적으로 접근할 수 있다.

<br />

## 1) `__proto__` 접근자 프로퍼티

- 모든 객체는 `__proto__`  접근자 프로퍼티를 통해 자신의 프로토타입 내부슬롯에 간접적으로 접근할 수 있다.
- 접근자 프로퍼티는 자체적으로 값을 갖지 않고 다른 데이터의 값을 읽거나 저장할 때 사용하는 [[get]], [[set]] 프로퍼티 어트리뷰트로 구성된 프로퍼티다.

<br />

### `__proto__` 접근자 프로퍼티의 특징

1. __proto__는 접근자 프로퍼티다.
2. __proto__는 상속을 통해 사용된다.
    - 객체가 직접 소유하는 프로퍼티가 아니라 Object.prototype의 프로퍼티다.
    - 모든 객체는 프로토타입의 계층 구조인 프로토타입 체인에 묶여있다.
        
        프로토타입 체인의 종점(최상위 객체)은 Object.prototype이다.
        
3. __proto__를 통해 상호 참조에 의한 프로토타입 체인이 생성되는 것을 방지한다.
4. __proto__를 코드 내에서 직접 사용하는 것은 권장하지 않는다.
    - Object.prototype을 상속받지 않는 객체를 생성할 수도 있기 때문.

```jsx
// 프로토타입 체인의 종점이므로 Object.__proto__를 상속받을 수 없다.
const obj = Object.create(null);

// obj는 Object.__proto__를 상속받을 수 없다.
console.log(obj.__proto__); // undefined

// 따라서 __proto__보다 Object.getPrototypeOf 메서드를 사용하는 편이 좋다.
console.log(Object.getPrototypeOf(obj)); // null
```

<br />

# 19장 프로토타입 문제

1. 다음 코드의 실행 결과는?

```jsx
const obj = {};
const parent = { x: 1 };

// setter 함수를 호출하고 obj의 프로토타입을 교체한다.
obj.__proto__ = parent;

console.log(obj.x); // (1)
console.log(obj);   // (2)
```

<br />

- 답
    
    (1) 1
    
    (2) {}
    
    (2)의 실행 결과는 다음과 같다. 객체 자체는 변동되는 것이 아니라, __proto__ 접근자 프로퍼티를 통해 setter함수를 실행시켜 **프로토타입을 교체**했으므로 obj 그대로 반환되고, obj 프로토타입은 변경된다.