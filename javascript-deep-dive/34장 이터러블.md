# 34장 이터러블

# 1. 이터레이션 프로토콜

- ES6에서 도입된 **이터레이션 프로토콜**은 **순회 가능한(iterable)** 데이터 컬렉션(자료 구조)를 만들기 위해 ECMAScript 사양에 정의하여 미리 약속한 규칙이다.
    - ES6 이전
        - 배열, 문자열, 유사 배열 객체, DOM 컬렉션 등 통일된 규약 없이 **for 문**, **for ... in 문**, **forEach** 메서드 등으로 순회 가능했다.
    - ES6 이후
        - 이터레이션 프로토콜을 준수하는 이터러블은 **for ... of 문**, **스프레드 문법**, **배열 디스트럭처링 할당**이 가능하다.

<br />

### 👋 이터러블 프로토콜

- `Symbol.iterator` 를 프로퍼티 키로 사용한 메서드를 직접 구현하거나 프로토타입 체인을 통해 상속받은 `Symbol.iterator` 메서드를 호출하면 이터레이터 프로토콜을 준수한 이터레이터를 반환하는데 이를 **이터러블 프로토콜**이라 한다.
- 이터러블 프로토콜을 준수한 객체를 **이터러블**이라 한다.

<br />

### 👋 이터레이터 프로토콜

- 이터러블의 `Symbol.iterator` 메서드를 호출하면 이터레이터 프로토콜을 준수한 **이터레이터**를 반환한다.
- 이터레이터는 **next 메서드**를 소유하며 next 메서드를 호출하면 이터러블을 순회하며 value와 done 프로퍼티를 갖는 **이터레이터 리절트 객체를 반환**하는데 이를 이터레이터 프로토콜이라 한다.
- 이터레이터 프로토콜을 준수한 객체를 이터레이터라 한다.

<br />

## 1-1) 이터러블

- 이터러블 프로토콜을 준수한 객체를 **이터러블**이라 한다.
- 이터러블을 확인하는 함수는 다음과 같이 구현할 수 있다.

```jsx
const isIterable = v => v !== null && typeof v[Symbol.iterator] === 'function';

// 배열, 문자열, Map, Set 등은 이터러블이다.
isIterable([]);        // -> true
isIterable('');        // -> true
isIterable(new Map()); // -> true
isIterable(new Set()); // -> true
isIterable({});        // -> false
```

<br />

## 1-2) 이터레이터

- 이터레이터 프로토콜을 준수한 객체를 **이터레이터**라 한다.
- 이터러블의 Symbol.iterator 메서드가 반환한 이터레이터는 **next 메서드**를 갖는다.

```jsx
// 배열은 이터러블 프로토콜을 준수한 이터러블이다.
const array = [1, 2, 3];

// Symbol.iterator 메서드는 이터레이터를 반환한다.
const iterator = array[Symbol.iterator]();

// Symbol.iterator 메서드가 반환한 이터레이터는 next 메서드를 갖는다.
console.log('next' in iterator); // true

// next 메서드를 호출하면 이터러블을 순회하며 순회 결과를 나타내는 이터레이터 리절트 객체를
// 반환한다. 이터레이터 리절트 객체는 value와 done 프로퍼티를 갖는 객체다.
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

- done 프로퍼티는 이터러블의 순회 완료 여부를 나타낸다.

<br />

# 2. for ... of 문

- for ... of 문은 이터러블을 순회하면서 이터러블의 요소를 변수에 할당한다.
- 내부적으로 이터레이터의 next 메서드를 호출하여 이터러블을 순회하며 **next 메서드**가 반환한 이터레이터 리절트 객체의 **value 프로퍼티 값**을 for ... of 문의 **변수에 할당**한다.
- done 프로퍼티 값이 `false`면 **순회**, `true`이면 **순회를 중단**한다.

<br />

# 3. 이터러블과 유사 배열 객체

- 유사 배열 객체는 인덱스로 프로퍼티 값에 접근 가능하고 length 프로퍼티를 갖는 객체를 말한다.
- for 문으로 순회할 수 있지만 **이터러블이 아닌 일반 객체**이므로 for ... of 문으로 순회할 수 없다.
- 단, arguments, NodeList, HTMLCollection은 **유사 배열 객체이면서 이터러블**이다.
    - ES6에서 Symbol.iterator 메서드를 구현하여 이터러블이 되었다.
    - length 프로퍼티를 가지며 인덱스로 접근 가능하므로 유사 배열 객체이면서 이터러블이다.

```jsx
// 유사 배열 객체
const arrayLike = {
  0: 1,
  1: 2,
  2: 3,
  length: 3
};

// 유사 배열 객체는 length 프로퍼티를 갖기 때문에 for 문으로 순회할 수 있다.
for (let i = 0; i < arrayLike.length; i++) {
  // 유사 배열 객체는 마치 배열처럼 인덱스로 프로퍼티 값에 접근할 수 있다.
  console.log(arrayLike[i]); // 1 2 3
}

// 유사 배열 객체는 이터러블이 아니기 때문에 for...of 문으로 순회할 수 없다.
for (const item of arrayLike) {
  console.log(item); // 1 2 3
}
// -> TypeError: arrayLike is not iterable
```

<br />

# 4. 이터레이션 프로토콜의 중요성

- 만약 다양한 데이터 공급자가 각자의 순회 방식을 갖는다면 데이터 소비자는 다양한 데이터 공급자의 순회 방식을 모두 지원해야 한다.
- 이는 효율적이지 않으며 이터레이션 프로토콜을 준수하도록 규정하면 데이터 소비자는 이터레이션 프로토콜만 지원하도록 구현하면 된다.
- 즉, 이터러블을 지원하는 데이터 소비자는 내부에서 `Symbol.iterater` 메서드를 호출해 **이터레이터를 생성**하고 이터레이터의 **next 메서드를 호출**하여 이터러블을 순회하며 **이터레이터 리절트 객체를 반환**하여 리절트 객체의 **value/done 프로퍼티 값을 취득**한다.
    
    이렇게 되면 다양한 데이터 공급자가 하나의 순회 방식을 갖도록 규정하여 데이터 소비자와 데이터 공급자를 연결하는 인터페이스의 역할을 한다.
    

<br />

# 5. 사용자 정의 이터러블

## 5-1) 사용자 정의 이터러블 구현

- 사용자 정의 이터러블 피보나치 수열

```jsx
// 피보나치 수열을 구현한 사용자 정의 이터러블
const fibonacci = {
  // Symbol.iterator 메서드를 구현하여 이터러블 프로토콜을 준수한다.
  [Symbol.iterator]() {
    let [pre, cur] = [0, 1];
    const max = 10; // 수열의 최대값

    // Symbol.iterator 메서드는 next 메서드를 소유한 이터레이터를 반환해야 하고
    // next 메서드는 이터레이터 리절트 객체를 반환해야 한다.
    return {
      next() {
        [pre, cur] = [cur, pre + cur];
        // 이터레이터 리절트 객체를 반환한다.
        return { value: cur, done: cur >= max };
      }
    };
  }
};

// 이터러블인 fibonacci 객체를 순회할 때마다 next 메서드가 호출된다.
for (const num of fibonacci) {
  console.log(num); // 1 2 3 5 8
}

// 이터러블은 스프레드 문법의 대상이 될 수 있다.
const arr = [...fibonacci];
console.log(arr); // [ 1, 2, 3, 5, 8 ]

// 이터러블은 배열 디스트럭처링 할당의 대상이 될 수 있다.
const [first, second, ...rest] = fibonacci;
console.log(first, second, rest); // 1 2 [ 3, 5, 8 ]
```

- 사용자 정의 이터러블은
    1. Symbol.iterator 메서드를 구현
    2. next 메서드를 갖는 이터레이터를 반환
    3. next 메서드는 value/done 프로퍼티 값을 갖는 이터레이터 리절트 객체를 반환
    
    해야한다.
    
- for ... of 문은 done 값이 true일 때 순회를 중단한다.

<br />

## 5-2) 이터러블을 생성하는 함수

```jsx
const fibonacciFunc = function(max) {
	let [pre, cur] = [0, 1];

	return {
		[Symbol.iterator]() {
			return {
				next() {
					[pre, cur] = [cur, pre + cur];
					return { value: cur, done: cur >= max };
				}
			};
		}
	};
}

for (const num of fibonacciFunc(10)) {
  console.log(num); // 1 2 3 5 8
}
```

- next 메서드에서 done 값을 생략하면 무한 이터러블 생성이 가능하다.

<br />

## 5-3) 무한 이터러블과 지연평가

- 지연 평가(**lazy evaluation**)는 데이터가 필요한 시점 이전까지 데이터를 생성하지 않다가 **필요한 시점이 되면 데이터를 생성하는 기법**이다.
    
    즉, 평가가 필요할 때까지 평가를 늦추는 기법
    
- 위 `fibonacciFunc` 구현에서 next 메서드의 done 값을 생략하면 무한 이터러블이 되는데, 이는 데이터 소비자가 for ... of 문, 배열 디스트럭처링 할당 등이 실행되기 전까지 데이터를 생성하지 않는다.
- 빠른 실행속도를 기대할 수 있고 불필요한 메모리를 소비하지 않으며 무한도 표현할 수 있다.

<br />

# 🤔 문제

1. 다음 중 이터러블에 대한 설명으로 틀린 것은?

1\) 이터러블은 for ... of 문, 스프레드 문법(`...`), 배열 디스트럭처링 할당의 대상이 될 수 있다.

2\) 일반 객체는 이터러블이 아니지만 스프레드 문법(`...`)은 사용 가능하다.

3\) 이터러블로 무한을 표현하는 것은 불가능하다.

4\) for ... of 문으로 이터러블을 순회하면 `value` 프로퍼티 값을 변수에 할당하고, `done` 프로퍼티 값이 false/true 인지에 따라 더 순회할지, 중단할지 결정한다.

<br />

- 답
    
    **3)**
    
    사용자 정의 이터러블을 구현할 때 **done 프로퍼티를 생략하면 무한 이터러블이 생성**된다.
    
    무한 이터러블은 생성되는 순간 데이터가 생성되는 것이 아니라 평가 될 때 데이터가 생성되므로 실행 속도가 빠르고 불필요한 메모리를 소비하지 않는다.
    
    ```jsx
    // 무한 이터러블을 생성하는 함수
    const fibonacciFunc = function () {
      let [pre, cur] = [0, 1];
    
      return {
        [Symbol.iterator]() { return this; },
        next() {
          [pre, cur] = [cur, pre + cur];
          return { value: cur };
    			// 무한이 아닐경우 return { value: cur, done: cur >= max };
        }
      };
    };
    ```