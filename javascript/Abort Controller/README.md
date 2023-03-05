# 1. Abort Controller

Abort Controller는 Javascript에서 제공하는 기능 중 하나로, XMLHttpRequest나 fetch 같은 비동기 작업의 실행을 취소할 수 있는 객체이다. MDN 설명에 따르면 하나 이상의 웹 요청을 취소할 수 있게 해준다.

이를 사용하면 비동기 작업 중에 작업을 취소하거나 중단시킬 수 있어서, 불필요한 네트워크 트래픽을 방지하거나, 불필요한 리소스 소모를 막을 수 있다.

생성자 키워드를 통해 `new AbortController()` 인스턴스를 생성하면 다음과 같은 요소들을 갖고 있다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222945865-2f9ea8ce-a109-4675-8992-75568dedb600.png">
</div>

`signal` 이라고 하는 항목만 보이는데, Prototype 부분을 확인해보면 `abort` 함수도 가지고 있다.

이를 활용해서 어떻게 웹 요청을 취소하는지 알아보자.

<br />

# 2. AbortSignal과 addEventListener

`new AbortController()` 로 생성된 인스턴스는 `abort` 함수를 갖는데, `abort` 함수를 호출하면 `AbortSignal` 객체를 반환한다.

`Element.addEventListener()` 함수로 이벤트 리스너 함수를 등록시킬 때 다음과 같은 매개변수를 갖는다.

```jsx
Element.addEventListener(type, listener, options);
```

- **type**: click, change와 같은 동작 문자열
- **listener**: type으로 명시한 동작이 발생했을 때 실행할 콜백 함수
- **options**: 이벤트 리스너의 특성을 지정할 수 있는 객체(Optional)

여기서 options에 signal 항목으로 `AbortSignal` 객체를 넘겨줄 수 있다. 만약 다음과 같이 이벤트 리스너가 동작하고 있을 때, `abort()` 함수가 실행되는 순간 이벤트 리스너는 제거된다.

```jsx
const controller = new AbortController();
const signal = controller.signal;

window.addEventListener(
  "keyup",
  (e) => {
    // do something

    if (condition) {
      controller.abort(); // 이 코드가 실행되면 이벤트 리스너는 제거된다.
    }
  },
  { signal }
);
```

이를 잘 활용하면 `removeEventListener()` 함수를 사용하지 않고도 이벤트 리스너를 적절하게 제거할 수 있다.

<br />

# 3. fetch와 Abort Controller

특정 리소스를 가져오기 위해 `fetch()` 함수를 사용할 때 다음과 같은 매개변수를 받는다.

```jsx
fetch(resource, options);
```

- **resource**: 가져오려는 리소스를 정의한다. (리소스의 url 등)
- **options**: 해당 fetch 함수에 적용할 사용자 정의 설정 객체.

options에는 method, headers, body 등의 요소를 갖는 객체를 넘겨줄 수 있는데, 여기도 `addEventListener`와 마찬가지로 signal 항목을 같이 넘겨줄 수 있다. 해당 signal 항목으로 AbortSignal 객체를 넘겨주고, 해당 fetch 요청을 통해 리소스를 가져오기 전 Abort Controller의 abort 함수를 실행시키면 요청을 중단할 수 있다.

```jsx
const controller = new AbortController();
const signal = controller.signal;

fetch("url", { signal })
  .then((response) => {
    // do something
  })
  .catch((error) => {
    if (error.name === "AbortError") {
      // abort controller에 의해 취소됐을 때 error.name의 값은 "AbortError"인 에러가 발생한다.
    } else {
      console.error(error);
    }
  });
```

fetch() 함수를 abort controller를 이용해 중단한다면 에러가 발생하게 되고, try catch 문이나 Promise.catch 에서 캐치되는 Error에서 `error.name` 값은 `AbortError` 가 된다.

<br />

# 4. 예시

### 4-1) 일반 Javascript

```jsx
const controller = new AbortController();
const signal = controller.signal;

const fetchData = async () => {
  try {
    const response = await fetch(url, { signal });
    console.log(response);
  } catch (error) {
    console.error(error);
    if (error.name === "AbortError") {
      console.log("요청이 취소되었습니다.");
    } else {
      console.log("에러가 발생했습니다.");
    }
  }
};

setTimeout(() => {
  controller.abort();
}, 2000);

fetchData();
```

위 코드는 특정 리소스를 가지고 오는데 2초가 지나면 요청 자체를 중단하는 코드이다. 이를 확인하면 일반적으로 2초 보단 빠르게 리소스를 가져오므로 확인이 안되지만, 크롬 브라우저 개발자 도구 네트워크 탭에서 속도를 Slow 3G 같이 느린 속도로 바꾸면 확인이 가능하다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222945864-f228a60d-7d1f-4299-8987-e5e91a81f5db.png">
</div>

<br />

### 4-2) React

어떤 특정 페이지에 접근했을 때 API 요청이 이루어진다고 가정했을 때, 이 요청이 너무 느려서 사용자가 다른 페이지로 이동할 때 해당 요청을 중단하는 방법을 알아보자.

```jsx
import React, { useEffect } from "react";

const MyComponent = () => {
  useEffect(() => {
    const controller = new AbortController();
    (async () => {
      try {
        const response = await fetch(url, { signal: controller.signal });
        console.log(response);
      } catch (error) {
        console.error(error);
        if (error.name === "AbortError") {
          console.log("요청이 취소되었습니다.");
        } else {
          console.log("에러가 발생했습니다.");
        }
      }
    })();

    return () => {
      controller.abort();
    };
  }, []);

  return <></>;
};

export default MyComponent;
```

1. useEffect에 종속성 배열을 빈 배열로 넘겨줘서 mount 됐을 때만 실행

2. 해당 컴포넌트가 렌더링될 때 즉시 실행 함수에서 fetch

3. 정상 fetch가 된다면 적절하게 response 사용

4. useEffect의 리턴 함수에서 abort() 함수를 실행시켜 해당 컴포넌트가 마운트 해제될 때 요청 중단

<br />

# 5. 정상 처리된 후 abort() 하면?

특정 fetch 함수의 options로 AbortSignal 객체를 넘겨주고, 의도한 시점에 abort() 함수를 호출하도록 코드를 작성해놨을 때 요청이 진행 중인 상태에서 abort() 함수를 호출하면 요청이 즉시 중단된다.

만약 요청이 정상적으로 처리되어 이미 response를 반환한 이후 abort() 함수를 호출하면 **아무런 영향을 미치지 않는다**.

이미 받은 응답이 삭제된다거나 변경되지는 않는다. 그러므로 요청 중인지 요청이 끝났는지를 확인할 필요 없이 의도한 시점에 abort() 함수를 호출하여 불필요한 네트워크 트래픽을 줄일 수 있다.

<br />

# 정리

new 키워드로 AbortController 를 생성하면 인스턴스는 signal 이라고 하는 AbortSignal을 갖고 있고, 이를 addEventListener 또는 fetch 의 options 매개변수로 넣어줄 수 있다. AbortSignal을 넘겨준 addEventListener, fetch는 해당 signal을 가지고 있는 인스턴스의 abort() 함수를 호출하면 이벤트 리스너는 제거되고, fetch 요청은 즉시 중단된다.

이번에 2023 프론트엔드 Dev Matching 상반기-1 채용 프로그램을 신청해서 바닐라 자바스크립트를 연습하고 있던 중 Javascript의 여러 메서드를 확인하다가 Abort Controller라는 처음 보는 이름을 들어봤다. 실제로 사용하는 것을 보진 못했고, 이름도 처음 들어봤지만 내용을 봤을 때 이를 유용하게 사용할 수 있을 것 같아서 정리해 보았다.

이벤트 리스너를 제거하는 방법으로 removeEventListener()만 알고 있었고, fetch 요청도 요청을 보내기 전에 일부 코드를 개선하여 호출 자체를 하지 않는 방법만 알고 있었다.

이번 정리를 통해 이미 요청을 보낸 상태에서 중단하는 방법도 있다는 것을 알았고, 사용 방법도 그리 어렵지 않으니 적절하게 잘 사용하면 불필요한 함수 호출 등을 줄일 수 있을 것 같다.

---

# 참조

- [https://developer.mozilla.org/en-US/docs/Web/API/AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)
- [https://developer.mozilla.org/en-US/docs/Web/API/fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch)
- [https://www.youtube.com/watch?v=-ZWrN-TGr2Y](https://www.youtube.com/watch?v=-ZWrN-TGr2Y)
