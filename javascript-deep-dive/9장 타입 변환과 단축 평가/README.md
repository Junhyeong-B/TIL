# 9장 타입 변환과 단축 평가

1. 개발자가 의도하여 타입을 변환하는 것을 **명시적 타입 변환(explicit coercion)** 또는 **타입 캐스팅(type casting)** 이라 하고,
    
    의도하지 않은 타입 변환은 **암묵적 타입 변환(implicit coercion)** 또는 타입 **강제 변환(type coercion)** 이라 한다.
    

```jsx
let a = 10;

let str1 = a.toString() // '10', 명시적 타입 변환
let str2 = a + '' // '10', 암묵적 타입 변환
```

<br />

2. 암묵적 타입 변환으로 boolean, null, undefined, object, NaN, Infinity 등의 값도 문자열로 바꿀 수 있다.
    - ex) true + '' ⇒ "true" // null + '' ⇒ "null"

<br />

3. 산술 연산자, 비교 연산자 등은 피연산자를 숫자 타입으로 변환하고, 숫자 타입으로 변환할 수 없을 경우 평가 결과는 NaN이 된다.
    - \+ 단항 연산자는 피연산자를 숫자 타입으려 변환하고, 다항 연산자는 피연산자 중 문자열이 하나 이상 있으면 문자열로 변환한다.

<br />

4. 명시적 타입 변환
    1. 문자
        1. String(값)
        2. 값 + ''
        3. 값.toString()
    2. 숫자
        1. Number(값)
        2. parseInt(값), parseFloat(값)
        3. +값
        4. 값 * 1
    3. 불리언
        1. Boolean(값)
        2. !!값

<br />

5. 논리합(||, or), 논리곱(&&, and) 연산자 표현식은 언제나 2개의 피연산자 중 어느 한쪽으로 평가된다.
    - 이를 이용해 if문 대신 논리합, 논리곱 연산자로 대체할 수 있다.(단축 평가)

```jsx
'Cat' && 'Dog' // "Dog" => 두 개의 피연산자를 모두 평가해야 하므로 좌항에서 우항으로 평가되어 "Dog"가 반환된다.
'Cat' || 'Dog' // "Cat" => 하나의 결과만 true여도 true를 반환하므로 좌항인 "Cat"이 반환된다.

var done = true;
var message = '';
message = done && "완료" // message = "완료"

var yet = false;
message = yet || "미완료" // message = "미완료"

// 객체
var a = null;
var value = a && a.value; // null (논리곱을 사용하지 않으면 에러가 발생한다.)

// 함수
function getStringLength(str) {
	str = str || '';
	return a.length;
}

getStringLength() // 0
```

<br />

6. 옵셔널 체이닝(?.)
    
 - ES11(ECMAScript2020)에서 도입된 ?. 키워드
    
 - 좌항의 피연산자가 null 또는 undefined라면 undefined를 반환하고 아니면 우항의 프로퍼티 참조를 이어간다.
    
 - 좌항이 null, undefined가 아닌 falsy 값(0, '', NaN)이라면 undefined를 반환하는 것이 아닌 참조를 이어간다.
    

```jsx
var a = null;
var value = a?.value; // undefined
```

<br />

7. null 병합 연산자(??)
    
    ES11(ECMAScript2020)에서 도입된 ?? 키워드
    
    좌항의 피연산자가 null 또는 undefined인 경우 우항의 피연산자를 반환하고, 아니라면 좌항의 피연산자를 반환한다.
    
    변수에 기본 값을 설정할 때 유용하다.
    
    ```jsx
    var a = null ?? "default string"; // "default string"
    var b = "" ?? "default string"; // ""
    ```

<br />

# 🤔 문제

1. 다음 중 평가 결과가 true인 것은?
    
    ```jsx
    1) Boolean([])
    2) Boolean('0')
    3) Boolean(NaN)
    4) Boolean(null)
    5) Boolean({})
    6) Boolean(0)
    7) Boolean(-Infinity)
    ```
    
- 답
    
    1, 2, 5, 7
    

<br />

1. 논리 연산자를 사용한 단축평가에서 논리합(&&)의 경우 모든 표현식을 평가해야 하고, 논리곱(||)의 경우 평가 결과가 확정된 경우 나머지 평과 과정은 생략된다.
    
    ( O or X )

<br />

- 답
    
    X
    
    논리합, 논리곱 모두 연산이 확정되면 나머지 평가 과정을 생략한다.