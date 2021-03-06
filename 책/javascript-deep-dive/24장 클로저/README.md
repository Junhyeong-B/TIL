# 24장 클로저

- 클로저는 자바스크립트 고유의 개념이 아니고 일급 객체를 취급하는 함수형 프로그래밍 언어에서 사용되는 특성이다.

```jsx
const x = 1;

function outerFunc() {
  const x = 10;

  function innerFunc() {
    console.log(x); // 10
  }

  innerFunc();
}

outerFunc();
```

- outerFunc 함수 내부에 innerFunc 함수가 중첩되었고, innerFunc의 상위 스코프는 외부 함수 outerFunc의 스코프다.
- outerFunc 외부에 innerFunc가 정의되었다면 outerFunc에 접근할 수 없다.

<br />

# 1. 렉시컬 스코프

- 자바스클비트 엔진은 함수를 어디서 호출했는지가 아니라 **어디에 정의했는지에 따라 상위 스코프를 결정**한다. ⇒ 이를 **렉시컬 스코프**(정적 스코프)라고 한다.
- 렉시컬 환경의 외부 렉시컬 환경에 대한 참조에 저장할 참조값은 함수 정의가 평가되는 시점에 함수가 정의된 환경(위치)에 의해 결정된다.

```jsx
const x = 1;

function foo() {
  const x = 10;
  bar();
}

function bar() {
  console.log(x);
}

foo(); // ?
bar(); // ?
```

- foo, bar 함수 모두 전역에서 정의된 함수로 두 함수 모두 상위 스코프는 전역이다.
- 따라서 두 함수의 실행 결과로 console에는 1이 찍힌다.

<br />

# 2. 함수 객체의 내부 슬롯 [[Environment]]

- 렉시컬 스코프가 가능하려면 함수가 호출되는 환경과 상관없이 정의된 환경(상위 스코프)를 기억해야 한다.
- 함수는 자신의 내부 슬롯 `[[Environment]]`에 자신이 정의된 환경(상위 스코프)의 참조를 저장한다.
- 외부 렉시컬 환경에 대한 참조에는 함수 객체의 내부 슬롯`[[Environment]]` 에 저장된 렉시컬 환경의 참조가 할당된다.

<br />

# 3. 클로저와 렉시컬 환경

```jsx
const x = 1;

// ①
function outer() {
  const x = 10;
  const inner = function () { console.log(x); }; // ②
  return inner;
}

// outer 함수를 호출하면 중첩 함수 inner를 반환한다.
// 그리고 outer 함수의 실행 컨텍스트는 실행 컨텍스트 스택에서 팝되어 제거된다.
const innerFunc = outer(); // ③
innerFunc(); // ④ 10
```

1. outer 함수를 호출하면 중첩함수 inner를 반환하고 생명 주기(life cycle)을 마감한다.
2. outer 함수 실행이 종료되면 outer 함수의 실행 컨텍스트는 스택에서 제거된다.
3. 이 때 지역변수 x와 값 10을 저장하고 있던 실행 컨텍스트가 제거되었으므로 지역 변수 x 역시 생명 주기를 마감한다.
4. outer 함수의 지역 변수는 유효하지 않다.
5. 그러나 outer 함수를 할당한 innerFunc를 실행하면 10이 출력된다.
6. 외부 함수보다 중첩 함수가 더 오래 유지되는 경우 중첩 함수는 이미 생명 주기가 종료한 외부 함수의 변수를 참조할 수 있는데 이를 중첩 함수의 **클로저(closure)** 라고 부른다.
7. 이때 outer 함수의 실행컨텍스트는 실행 컨텍스트 스택에서 제거되지만 렉시컬 환경까지 소멸하는 것은 아니다.

※ 함수는 어디서 호출하든 상관 없이 언제나 자신이 기억하는 상위 스코프의 식별자를 참조할 수 있고, 바인딩된 값을 변경할 수 있다.

※ 클로저는 중첩 함수가 상위 스코프의 식별자를 참조하고 있고 중첩 함수가 외부 함수보다 더 오래 유지되는 경우에 한정하는 것이 일반적이다.

<br />

# 4. 클로저의 활용

- 클로저는 상태를 안전하게 변경하고 유지하기 위해 사용한다.
- 상태를 안전하게 은닉하고 특정 함수에게만 상태 변경을 허용하기 위해 사용한다.

```jsx
// 카운트 상태 변경 함수
const increase = (function () {
  // 카운트 상태 변수
  let num = 0;

  // 클로저
  return function () {
    // 카운트 상태를 1만큼 증가 시킨다.
    return ++num;
  };
}());

console.log(increase()); // 1
console.log(increase()); // 2
console.log(increase()); // 3
```

- 위 코드를 실행하면 즉시 실행 함수가 호출되고, 반환한 함수가 increase에 할당된다.
- 즉시 실행 함수는 호출된 이후 소멸되지만, 반환한 클로저는 increase 변수에 할당되어 호출된다.
- 즉시 실행 함수가 반환한 클로저는 자신이 정의된 위치에 의해 결정된 상위 스코프인 즉시 실행 함수의 렉시컬 환경을 기억하고 있다.

<br />

# 5. 캡슐화와 정보 은닉

- 캡슐화(encapsulation)는 객체의 상태를 나타내는 프로퍼티와 프로퍼티를 참조하고 조작할 수 있는 동작인 메서드를 하나로 묶는 것을 말한다.
- 정보 은닉(information hiding)은 객체의 특정 프로퍼티나 메서드를 감출 목적으로 사용하는 것을 말한다.
- 대부분의 객체 지향 프로그래밍 언어에서 클래스를 정의하고 구성하는 멤버에 대해 public, private, protected 같은 접근 제한자를 선언하여 공개 여부를 정할 수 있지만, 자바스크립트는 제공하지 않는다.
- 따라서 자바스크립트에서의 객체는 모든 프로퍼티와 메서드가 기본적으로 public 하다.
- 2021년 TC39 프로세스의 stage 3에는 클래스에 private 필드를 정의할 수 있는 표준 사양이 제안되어 있다.

<br />

# 🤔 문제

1. 아래 실행 결과에 대한 설명 중 **옳지 않은 것**은?

```jsx
const x = 1;

function outer() {
  const x = 10;
  const inner = function () { console.log(x); };
  return inner;
}

const innerFunc = outer(); 
innerFunc(); // 10
```

1) outer 함수를 호출하면 중첩함수 inner를 반환하고 생명 주기(life cycle)를 마감한다.

2) outer 함수 실행이 종료되면 outer 함수의 실행 컨텍스트는 스택에서 제거된다.

3) outer 함수의 지역 변수는 innerFunc에서 사용되므로 유효하다.

4) 외부 함수보다 중첩 함수가 더 오래 유지되는 경우 중첩 함수는 이미 생명 주기가 종료한 외부 함수의 변수를 참조할 수 있는데 이를 중첩 함수의 클로저(closure) 라고 부른다.

5) 이때 outer 함수의 실행컨텍스트는 실행 컨텍스트 스택에서 제거되지만 렉시컬 환경까지 소멸하는 것은 아니다.

- 답
    
    **3)**
    
    outer함수의 생명 주기를 마감할 때 지역변수 x와 값 10을 저장하고 있던 실행 컨텍스트가 제거되었으므로 **지역 변수 x 역시 생명 주기를 마감**한다.
    
    이때 **outer 함수의 지역 변수는 유효하지 않다.**