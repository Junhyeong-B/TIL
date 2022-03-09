# 45장 프로미스

- 자바스크립트는 비동기 처리를 위해 하나의 패턴으로 콜백 함수를 사용한다.
    - 다만, 전통적인 콜백 패턴은 콜백 헬로 인해 가독성이 나쁘고 여러 개의 비동기 처리를 한번에 처리하는 데도 한계가 있다.
    - 이러한 단점을 보완하기 위해 ES6에서 비동기 처리를 위한 **프로미스(Promise)**가 도입되었다.

<br />

# 1. 비동기 처리를 위한 콜백 패턴의 단점

## 1-1) 콜백 헬

- 비동기 함수 내부의 비동기로 동작하는 코드는 비동기 함수가 종료된 이후에 완료된다.
    
    ⇒ 따라서 비동기 함수 내부의 비동기로 동작하는 코드에서 처리 결과를 외부로 반환하거나 상위 스코프의 변수에 할당하면 기대한 대로 동작하지 않는다.
    
    - 이때 비동기 함수에 비동기 처리 결과에 대한 후속처리를 수행하는 콜백함수를 전달하면 범용적으로 사용은 가능하다. ⇒ 이렇게 작성할 경우 콜백 함수가 중첩되고, 가독성이 나빠지는데 이를 **콜백 헬**이라고 한다.

<br />

## 1-2) 에러 처리의 한계

```jsx
try {
  setTimeout(() => { throw new Error('Error!'); }, 1000);
} catch (e) {
  // 에러를 캐치하지 못한다
  console.error('캐치한 에러', e);
}
```

- setTimeout이 호출되면 setTimeout 함수의 실행 컨텍스트가 생성되어 콜 스택에 푸시되고 실행된다.
- setTimeout은 비동기 함수이므로 콜백 함수가 호출되는 것을 기다리지 않고 즉시 종료되어 콜 스택에서 제거된다.
- 타이머가 만료되면 setTimeout 함수의 콜백 함수는 태스크 큐로 푸시되고 콜 스택이 비어졌을 때 이벤트 루프에 의해 콜 스택으로 푸시되어 실행된다.
- 에러는 호출자 방향으로 전파된다. ⇒ 콜 스택의 아래 방향(실행 중인 실행 컨텍스트가 푸시되기 직전에 푸시된 실행 컨텍스트 방향)으로 전파된다.
- 따라서 setTimeout 함수의 콜백 함수가 발생시킨 에러는 catch 블록에서 캐치되지 않는다.

<br />

# 2. 프로미스의 생성

- new 연산자와 함께 호출하면 프로미스(Promise 객체)를 생성한다.
- Promise는 콜백 함수를 인수로 전달 받고, 콜백 함수는 resolve와 reject 함수를 인수로 전달받는다.

```jsx
// 프로미스 생성
const promise = new Promise((resolve, reject) => {
  // Promise 함수의 콜백 함수 내부에서 비동기 처리를 수행한다.
  if (/* 비동기 처리 성공 */) {
    resolve('result');
  } else { /* 비동기 처리 실패 */
    reject('failure reason');
  }
});
```

- 만약 비동기 처리가 성공하면 resolve 함수에 인수로 전달하면서 호출하고, 실패하면 reject 함수에 인수로 전달하면서 호출한다.
- 프로미스는 3가지 상태(state) 정보를 갖는다.

| 프로미스의 상태 정보 | 의미 | 상태 변경 조건 |
| --- | --- | --- |
| pending | 비동기 처리가 아직 수행되지 않은 상태 | 프로미스가 생성된 직후 기본 상태 |
| fulfilled | 비동기 처리가 수행된 상태(성공) | resolve 함수 호출 |
| rejected | 비동기 처리가 수행된 상태(실패) | reject 함수 호출 |

<br />

# 3. 프로미스의 후속 처리 메서드

- 프로미스는 fulfilled 상태가 되면 무엇을 하고, rejected 상태가 되면 무엇을 해야 할지 등에 대한 후속 처리 메서드 **then**, **catch**,  **finally**를 제공한다.
- 모든 후속 처리 메서드는 프로미스를 반환하며 비동기로 동작한다.

<br />

## 3-1) Promise.prototype.then

- then 메서드는 두 개의 콜백 함수를 인수로 전달받는다.
    - 첫 번째 인수: fulfilled(성공) 상태가 되면 호출된다.
    - 두 번째 인수: rejected(실패) 상태가 되면 호출된다.

```jsx
// fulfilled
new Promise(resolve => resolve('fulfilled'))
  .then(v => console.log(v), e => console.error(e)); // fulfilled

// rejected
new Promise((_, reject) => reject(new Error('rejected')))
  .then(v => console.log(v), e => console.error(e)); // Error: rejected
```

<br />

## 3-2) Promise.prototype.catch

- catch 메서드는 한 개의 콜백 함수를 인수로 전달받는다.
- 인수로 전달 받은 콜백 함수는 rejected 상태인 경우만 호출된다.
- then 메서드에서 첫 번째 인수에 undefined를 입력하여 rejected 상태에 대한 후속 처리도 가능하다.

```jsx
// rejected
new Promise((_, reject) => reject(new Error('rejected')))
  .catch(e => console.log(e)); // Error: rejected

// then 첫 번째 인수 undefined를 이용한 rejected 후속 처리
new Promise((_, reject) => reject(new Error('rejected')))
  .then(undefined, e => console.log(e)); // Error: rejected
```

<br />

## 3-3) Promise.prototype.finally

- finally 메서드는 한 개의 콜백 함수를 인수로 전달받는다.
- fulfilled, rejected 상태와 상관 없이 무조건 1회 호출된다.
- 상태와 상관 없이 공통적으로 수행해야 할 처리 내용이 있을 때 유용하다.

```jsx
new Promise(() => {})
  .finally(() => console.log('finally')); // finally
```

<br />

# 4. 프로미스의 에러 처리

- 기존 콜백 함수의 에러 처리의 한계와 달리 Promise는 에러를 문제없이 처리할 수 있다.
- then 메서드의 두 번째 인수를 이용하거나, catch 메서드를 사용하여 에러를 처리한다.
- catch 메서드를 호출하면 내부적으로 `then(undefined, onRejected)`을 호출한다.
- then, catch 메서드를 모두 사용하는 것이 가독성이 좋고 명확하다.

```jsx
new Promise(() => {})
  .then(res => console.xxx(res))
  .catch(err => console.error(err)); // TypeError: console.xxx is not a function
```

<br />

# 5. 프로미스 체이닝

- 프로미스는 then, catch, finally를 통해 콜백 헬을 해결한다.
- then, catch, finally 메서드는 언제나 프로미스를 반환하므로 연속적으로 호출할 수 있다.
- 콜백 헬은 발생하지 않지만 프로미스도 콜백 패턴을 사용하므로 가독성이 좋지 않을 수 있다.
- 이를 해결하기 위해 ES8에서 async/await가 도입되었다.

<br />

# 6. 프로미스의 정적 메서드

## 6-1) Promise.resolve, Promise.reject

- 이미 존재하는 값을 래핑하여 프로미스를 생성하기 위해 사용한다.

<br />

## 6-2) Promise.all

- 여러 개의 비동기 처리를 모두 병렬 처리할 때 사용한다.
- 배열 등 이터러블을 인수로 받고, 처리 결과를 배열에 저장해 새로운 프로미스를 반환한다.
- 전달 받은 프로미스 중 **하나라도 rejected 상태가 되면** 나머지 프로미스가 fulfilled 상태가 되는 것을 기다리지 않고 **즉시 종료**한다.

```jsx
const requestData1 = () => new Promise(resolve => setTimeout(() => resolve(1), 3000));
const requestData2 = () => new Promise(resolve => setTimeout(() => resolve(2), 2000));
const requestData3 = () => new Promise(resolve => setTimeout(() => resolve(3), 1000));

// 프로미스 체이닝, 세 개의 비동기 처리를 순차적으로 처리
const res = [];
requestData1()
  .then(data => {
    res.push(data);
    return requestData2();
  })
  .then(data => {
    res.push(data);
    return requestData3();
  })
  .then(data => {
    res.push(data);
    console.log(res); // [1, 2, 3] ⇒ 약 6초 소요
  })
  .catch(console.error);

// Promise.all, 세 개의 비동기 처리를 병렬적으로 처리
Promise.all([requestData1(), requestData2(), requestData3()])
  .then(console.log) // [ 1, 2, 3 ] ⇒ 약 3초 소요
  .catch(console.error);
```

<br />

## 6-3) Promise.race

- 배열 등의 이터러블을 인수로 전달받는다.
- Promise.all과 유사하게 병렬적으로 처리하지만, 인수 중 가장 먼저 fulfilled 상태가 된 프로미스의 처리 결과를 resolve하여 새로운 프로미스를 반환한다.
- 하나라도 rejected 상태가 되면 에러를 reject 하는 새로운 프로미스를 즉시 반환한다.

<br />

## 6-4) Promise.allSettled

- 배열 등의 이터러블을 인수로 전달받는다.
- 전달 받은 모든 프로미스가 fulfilled, rejected 상태가 되면 처리 결과를 배열로 반환한다.
- ES11에서 도입되었다.

<br />

# 7. 마이크로태스크 큐

- 프로미스의 후속 처리 메서드의 콜백 함수는 태스크 큐가 아니라 마이크로 태스크 큐에 저장된다.
- 콜백 함수나 이벤트 핸들러를 일시 저장한다는 점에서 태스크 큐와 동일하지만, 마이크로태스크 큐는 태스크 큐보다 우선순위가 높다.

```jsx
setTimeout(() => console.log(1), 0);

Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));

// 실행 순서 2 → 3 → 1
```

<br />

# 8. fetch

- **fetch 함수**는 HTTP 요청 전송 기능을 제공하는 클라이언트 사이드 Web API로, HTTP 응답을 나타내는 Response 객체를 래핑한 **Promise 객체를 반환**한다.

```jsx
const request = {
  get(url) {
    return fetch(url);
  },
  post(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: { 'content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  },
  patch(url, payload) {
    return fetch(url, {
      method: 'PATCH',
      headers: { 'content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  },
  delete(url) {
    return fetch(url, { method: 'DELETE' });
  }
};
```

<br />

## 8-1) GET 요청

```jsx
request.get('https://jsonplaceholder.typicode.com/todos/1')
  .then(response => {
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  })
  .then(todos => console.log(todos))
  .catch(err => console.error(err));
// {userId: 1, id: 1, title: "delectus aut autem", completed: false}
```

<br />

## 8-2) POST 요청

```jsx
request.post('https://jsonplaceholder.typicode.com/todos', {
  userId: 1,
  title: 'JavaScript',
  completed: false
}).then(response => {
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  })
  .then(todos => console.log(todos))
  .catch(err => console.error(err));
// {userId: 1, title: "JavaScript", completed: false, id: 201}
```

<br />

## 8-3) PATCH 요청

```jsx
request.patch('https://jsonplaceholder.typicode.com/todos/1', {
  completed: true
}).then(response => {
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  })
  .then(todos => console.log(todos))
  .catch(err => console.error(err));
// {userId: 1, id: 1, title: "delectus aut autem", completed: true}
```

<br />

## 8-4) DELETE 요청

```jsx
request.delete('https://jsonplaceholder.typicode.com/todos/1')
  .then(response => {
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  })
  .then(todos => console.log(todos))
  .catch(err => console.error(err));
// {}
```

<br />

# 🤔 문제

1. Promise에 대한 설명 중 **옳지 않은 것**은?

1\) Promise는 콜백 함수를 인수로 전달 받고, 콜백 함수는 resolve, reject 함수를 인수로 전달받는다.

2\) Promise는 fulfilled, rejected 2가지 상태(state\) 정보를 갖는다.

3\) Promise는 후속 처리 메서드 then, catch, finally를 제공한다.

4\) 후속 처리 메서드는 언제나 Promise를 반환하므로 연속적으로 호출할 수 있다.

5\) then 메서드를 통해 비동기 처리가 수행된 성공 상태, 실패 상태 각각에 대한 처리가 가능하다.

6\) Promise의 후속 처리 메서드의 콜백 함수는 태스크 큐가 아니라 마이크로 태스크 큐에 저장된다.

<br />

- 답
    
    **2)**
    
    Promise는 **pending**, **fulfilled**, **rejected** **3**가지 상태(state) 정보를 갖는다.