# new CustomEvent()로 Route 처리하기

# 1. new CustomEvent

- 자바스크립트에서 Route 처리하는 방법은 여러가지가 있겠지만, CustomEvent를 통해 커스텀 이벤트를 발생시키고 해당 이벤트 발생 시 Route 처리를 해주면 된다.
- 첫 번째 파라미터로 커스텀 이벤트 타입(문자열)을 받고, 두 번째 파라미터로 옵션을 지정할 수 있는데, detail에 객체 형태로 작성한다.
- 이벤트 타입을 작성할 때 오타가 발생할 수도 있으므로 변수로 빼서 작성하자.
- new CustomEvent는 이벤트를 발생시키고 싶은 Element에 `Element.dispatchEvent(new CustomEvent())` 형태로 작성해주면 되는데, Route 처리를 해주고 싶으니 window에 이벤트 바인딩 해주자.
- history와 연계하기 위해 push 이름으로 함수를 작성하면 다음과 같다.

```jsx
const ROUTE_CHANGE = 'ROUTE_CHANGE';

const push = (url) => {
	window.dispatchEvent(new CustomEvent(ROUTE_CHANGE, {
		detail: {
			url;
		}
	}));
}
```

# 2. 뒤로 가기

- 만약 사용자가 뒤로가기 버튼을 눌렀다면 해당 이벤트는 `'popstate'` 이벤트로 바인딩 해주면 된다.

```jsx
window.addEventListener("popstate", (e) => {});
```

# 3. Route 구현

```jsx
const ROUTE_CHANGE = "ROUTE_CHANGE";

export const initRouter = (onRoute) => {
  window.addEventListener(ROUTE_CHANGE, (e) => {
    const { url } = e.detail;
    if (!url) {
      return;
    }

    history.pushState(null, null, url);
    onRoute();
  });

  window.addEventListener("popstate", (e) => {
    onRoute();
  });
};

export const push = (url) => {
  window.dispatchEvent(
    new CustomEvent(ROUTE_CHANGE, {
      detail: {
        url,
      },
    })
  );
};
```