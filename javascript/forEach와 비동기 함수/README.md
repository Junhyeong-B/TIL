# forEach와 비동기 함수

# 1. Vanilla Javascript 학습 중 forEach 사용

- Vanilla Javascript 학습 도중 함수형 프로그래밍으로 작성 중이어서 **for문 대신 forEach와 비동기 HTTP 요청을 함께 사용**했다.
- forEach 외부에 배열을 생성하고, forEach 내부에서 HTTP 요청으로 받아온 응답을 push 해주는 형태로 아래와 같이 작성했다.

```jsx
this.fetchDatas = async () => {
  const productIds = 리스트 배열[];
  const productList = [];

	productIds.forEach(async (id) => {
		const result = await api(id);
		productList.push(result);
		console.log(productList); // [..., ...] => 내부에선 잘 확인되는 데이터
	})
	console.log(productList); // [] => ??
};
```

- 그런데 forEach 내부에서는 잘만 들어가던 데이터가 forEach 외부에서 console을 찍어보면 빈 배열만 나오는 것이었다.
- 그러다 찾아보니 **forEach 내부에서 async/await를 사용하더라도 그 과정을 기다리는 것이 아니라 callback을 순서대로 실행 후 빠져나오는 것**이었다.
    - 이 사실을 알고 다시보니 forEach 외부 console.log가 먼저 찍히고 그 다음 forEach 내부의 console.log가 찍히고 있었다.

# 2. 해결 방법

- 이를 해결하기 위한 방법을 알아보니 대부분 `for`, `for ... of` 문을 사용하여 해결하는 것 같다.
- 함수형 프로그래밍을 사용하려고 했으므로 for문 대신 forEach를 사용하는 것으로 찾아보니 **Promise.all 메서드를 사용하여 해결**할 수 있었다.

## ※ Promise.all([비동기 배열])

- Promise.all은 비동기로 동작하는 코드 배열을 파라미터로 받고 배열의 모든 비동기 로직이 병렬 실행된다.
- 전달 받은 프로미스 중 **하나라도 rejected 상태가 되면** 나머지 프로미스가 fulfilled 상태가 되는 것을 기다리지 않고 **즉시 종료**한다.
- 이를 이용하기 위해 forEach 대신 map 함수를 사용해서 배열 상태를 유지했고 Promise.all에 해당 배열을 넘겨주는 방식으로 해결했다.
- Promise.all 메서드를 사용하여 다음과 같이 코드를 수정하니 배열에 정상적으로 데이터가 push 되는 것을 확인했다.

```jsx
this.fetchDatas = async () => {
  const productIds = 리스트 배열[];
  const productList = [];

	const promises = productIds.map(async (id) => {
    const result = await api(id);
    productList.push(result);
  });
  await Promise.all(promises);

  console.log(productList); // [..., ...] => 데이터 잘 들어감.
};
```