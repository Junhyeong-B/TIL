# Promise 내장 함수들

# 1. Promise.all(iterable)

- 여러 promise를 동시에 처리할 때 유용하다.
- 여러 개의 promise를 배열로 받아서 해당 promise들을 병렬로 실행시키고, 모두 처리가 완료되면 then이 호출 된다.
- 만약 하나라도 reject되면 즉시 종료하고 첫 번째로 reject된 결과 값을 반환하는 Promise를 반환한다.
- 매개 변수로 전달받은 iterable이 비어있다면 이미 이행한 Promise(fulfilled 상태)를 반환한다.
- 한 번에 여러 개의 API를 호출할 때 해당 내장 함수를 이용하여 병렬 실행, 모두 처리된 이후 데이터를 다루고 싶을 때 사용하면 유용하다.

```jsx
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const promise1 = delay(1000);
const promise2 = delay(2000);
const promise3 = delay(3000);

Promise.all([promise1, promise2, promise3]).then(() => console.log("finished"));
// 3초 후 finished 콘솔 출력
```

<br />

# 2. Promise.race(iterable)

- 여러 promise를 동시에 처리하는 것은 동일하나 promise 중 하나라도 resolve 또는 reject되면 종료하고 해당 promise의 결과값을 전달하는 Promise를 반환한다.
- 매개 변수로 전달받은 iterable이 비어있다면 영원히 대기(pending 상태)인 Promise를 반환한다.

- 사용처 예측
    - 전달 받은 iterable 중 하나라도 resolve, reject된다면 해당 결과값을 반환하는 Promise를 반환한다.
    - 만약, 이미 비동기 로직이 수행된 Promise라면(이미 요청이 실행되어 fulfilled 상태, 해당 결과 값을 value 프로퍼티로 갖고 있는 Promise) 해당 Promise를 반환한다.
    - 여러 개의 API 요청을 보내야 하고, 그 작업이 여러번 수행 되는 상황에서 요청 보낸 API들의 응답과 상관 없이 최대한 빠르게 결과를 보여줘야 한다면, 이미 수행 된 Promise를 사용해 즉시 값을 나타내게 할 수 있다. ⇒ 로딩 시간을 줄일 수 있다.

```jsx
const promises = [Promise.resolve(33), Promise.resolve(44)];

Promise.race(promises).then(value=> console.log(value)); // 33
```

<br />

# 3. Promise.any(iterable)

- 여러 promise를 파라미터로 받아 병렬로 처리하며 이 중 하나라도 resolve 되면 종료된다.
- 가장 먼저 수행된 promise가 만약 reject라면 무시하고 resolve가 될 때 까지 로직을 수행한다.
- resolve된 promise가 있다면 해당 promise를 반환한다.

```jsx
const promise1 = Promise.reject(0);
const promise2 = new Promise((resolve) => setTimeout(resolve, 100, 'quick'));
const promise3 = new Promise((resolve) => setTimeout(resolve, 500, 'slow'));

const promises = [promise1, promise2, promise3];

Promise.any(promises).then((value) => console.log(value)); // quick
```

<br />

# 4. Promise.allSettled(iterable)

- promise가 resolve, reject 여부와 상관 없이 모든 작업이 수행 되어야 종료된다.
- 일반적으로 성공 여부와 관계 없는 여러 비동기 작업을 수행해야 할 때나 각 프로미스의 결과를 확인하고 싶을 때 사용한다.
- Promise.all은 하나라도 reject되면 종료되므로 사용의 차이가 있다.(all은 하나라도 reject됐을 때 종료하고 싶을 때 사용한다.)

```jsx
const promise1 = Promise.resolve(3);
const promise2 = new Promise((resolve, reject) => setTimeout(reject, 100, 'foo'));
const promises = [promise1, promise2];

Promise.allSettled(promises).
  then((results) => results.forEach((result) => console.log(result.status)));
// fulfilled
// rejected
```