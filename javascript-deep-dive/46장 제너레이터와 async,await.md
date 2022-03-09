# 46장 제너레이터와 async/await

# 1. 제너레이터(Generator)란?

- 코드 블록의 실행을 일시 중지했다가 필요한 시점에 재개할 수 있는 특수한 함수로 ES6에서 도입되었다.
- 일반 함수는 호출되면 함수 코드를 일괄 실행하고 이를 제어할 수 없지만 제너레이터 함수는 일시 중지 시키거나 재개시킬 수 있다.
    
    ⇒ 함수의 제어권을 함수가 독점하는 것이 아니라 함수 호출자에게 양도(yield)할 수 있다.
 
<br />
   
- 일반 함수는 매개변수를 통해 외부 값을 받고, 실행되는 동안 변경할 수 없지만 제너레이터 함수는 함수 호출자와 양방향으로 함수의 상태를 주고받을 수 있다.
- 일반 함수는 호출하면 코드를 일괄 실행하고값을 반환하지만 제너레이터 함수를 호출하면 함수 코드를 실행하는 것이 아니라 이터러블이면서 동시에 이터레이터인 제너레이터 객체를 반환한다.

<br />

# 2. 제너레이터 함수의 정의

- `function*` 키워드로 선언한다.
- 하나 이상의 yield 표현식을 포함한다.
- 애스터리스크(`*`)의 위치는 function 키워드와 함수 이름 사이라면 어디든지 상관없지만 일관성을 유지하기 위해 function 바로 뒤에 붙이는 것을 권장한다.
- 화살표 함수로 정의할 수 없고, new 연산자와 함께 생성자 함수로 호출할 수 없다.

```jsx
// 제너레이터 함수 선언문
function* genDecFunc() {
  yield 1;
}

// 제너레이터 함수 표현식
const genExpFunc = function* () {
  yield 1;
};

// 제너레이터 메서드
const obj = {
  * genObjMethod() {
    yield 1;
  }
};

// 제너레이터 클래스 메서드
class MyClass {
  * genClsMethod() {
    yield 1;
  }
}
```

<br />

# 3. 제너레이터 객체

- 제너레이터 함수를 호출하면 일반 함수처럼 함수 코드 블록을 실행하는 것이 아니라 제너레이터 객체를 생성해 반환한다.
- 제너레이터 객체는 이터러블이면서 이터레이터 이다.
    
    ⇒ 즉, 이터레이터 리절트 객체를 반환하는 next 메서드를 소유한다.
    
<br />

- return 메서드를 호출하면 인수로 전달받은 값을 value 프로퍼티로, true를 done 프로퍼티 값으로 갖는 이터레이터 리절트 객체를 반환한다.

<br />

```jsx
function* genFunc() {
  try {
    yield 1;
    yield 2;
    yield 3;
  } catch (e) {
    console.error(e);
  }
}

const generator = genFunc();

console.log(generator.next()); // {value: 1, done: false}
console.log(generator.return('End!')); // {value: "End!", done: true}
```

<br />

# 4. 제너레이터의 일시 중지와 재개

- 제너레이터는 yield 키워드와 next 메서드를 통해 실행을 일시 중지했다가 필요한 시점에 다시 재개할 수 있다.
- yield 키워드는 제너레이터 함수의 실행을 일시 중지시키거나 yield 키워드 뒤에 오는 표현식의 평가 결과를 제너레이터 함수 호출자에게 반환한다.
- next 메서드를 호출하면 yield 표현식까지 표현되고 일시 중지된다.

<br />

# 5. 제너레이터의 활용

## 5-1) 이터러블의 구현

```jsx
// 무한 이터러블을 생성하는 **함수**
const infiniteFibonacci = (function () {
  let [pre, cur] = [0, 1];

  return {
    [Symbol.iterator]() { return this; },
    next() {
      [pre, cur] = [cur, pre + cur];
      // 무한 이터러블이므로 done 프로퍼티를 생략한다.
      return { value: cur };
    }
  };
}());

// infiniteFibonacci는 무한 이터러블이다.
for (const num of infiniteFibonacci) {
  if (num > 10000) break;
  console.log(num); // 1 2 3 5 8...2584 4181 6765
}

// 무한 이터러블을 생성하는 **제너레이터 함수**
const infiniteFibonacci = (function* () {
  let [pre, cur] = [0, 1];

  while (true) {
    [pre, cur] = [cur, pre + cur];
    yield cur;
  }
}());

// infiniteFibonacci는 무한 이터러블이다.
for (const num of infiniteFibonacci) {
  if (num > 10000) break;
  console.log(num); // 1 2 3 5 8...2584 4181 6765
}
```

<br />

# 6. async/await

- 비동기 처리를 동기 처리처럼 동작하도록 구현할 수 있는 키워드로 ES8에서 도입되었다.
- 프로미스를 기반으로 동작한다.
- 비동기 처리 결과를 후속 처리할 필요 없이 동기 처리처럼 프로미스를 사용할 수 있다.

<br />

## 6-1) async

- async 함수를 만드는 키워드로 함수 앞에 작성하여 async 함수로 선언할 수 있다.
- async 함수가 명시적으로 프로미스를 반환하지 않아도 반환값을 resolve하는 프로미스를 반환한다.

<br />

## 6-2) await

- 프로미스가 settled 상태(비동기 처리가 수행된 상태)가 될 때까지 대기하다가 settled 상태가 되면 프로미스가 resolve한 처리 결과를 반환한다.
- 반드시 프로미스 앞에서 사용해야 한다.
- 비동기 처리의 순서가 보장되어야 할 때 사용하여 동기적으로 작업을 수행할 수 있다.

<br />

## 6-3) 에러 처리

- async/await는 try ... catch 문으로 에러를 캐치할 수 있다.
- async 함수 내에서 catch 문을 사용해서 에러 처리를 하지 않으면 async 함수는 발생한 에러를 reject하는 프로미스를 반환한다.

```jsx
const fetch = require('node-fetch');

const foo = async () => {
  const wrongUrl = 'https://wrong.url';

  const response = await fetch(wrongUrl);
  const data = await response.json();
  return data;
};

foo()
  .then(console.log)
  .catch(console.error); // TypeError: Failed to fetch
```

<br />

# 🤔 문제

1. 제너레이터에 대한 설명 중 **옳지 않은 것**은?

1\) `function*` 키워드로 선언한다.

2\) 하나 이상의 yield 표현식을 포함한다.

3\) 애스터리스크(`*`)의 위치는 function 뒤에 공백 없이 붙여야 한다.

4\) 화살표 함수로 정의할 수 없다.

5\) new 연산자와 함께 생성자 함수로 호출할 수 없다.

6\) 제너레이터 객체는 이터러블이면서 이터레이터 이다.

<br />

- 답
    
    **3)**
    
    애스터리스크(`*`)의 위치는 function 키워드와 함수 이름 사이라면 어디든지 상관없지만 일관성을 유지하기 위해 function 바로 뒤에 붙이는 것을 권장한다.
    

<br />

2. 다음 코드는 try, catch 없이 작성된 async/await 함수로 fetch 동작에 에러가 발생했을 때 반환되는 data는 무엇인가요?

```jsx
const foo = async () => {
  const wrongUrl = 'https://wrong.url';

  const response = await fetch(wrongUrl);
  const data = await response.json();
  return data;
};
```

<br />

- 답
    
    async 함수 내에서 catch 문을 사용해서 에러 처리를 하지 않으면 async 함수는 **발생한 에러를 reject하는 프로미스를 반환**한다.