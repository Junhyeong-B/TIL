# 1. 무한스크롤 UI

**무한스크롤 UI**는 특정 콘텐츠를 보여주는 화면에서 스크롤을 내려서 콘텐츠가 모두 보여지거나(View Port 상 콘텐츠가 모두 보여질 경우) 스크롤이 바닥에 닿았을 때 콘텐츠를 추가로 불러와서 보여지는 UI를 말한다.

UI를 이렇게 처리하는 이유는 사용자가 이미지를 보여주는 웹 페이지에 들어왔을 때 모든 이미지를 다 불러올 필요 없이 화면에 보여지는 이미지만 불러왔다가 스크롤을 내렸을 때 추가로 이미지를 불러올 수 있으니 서버 부하 측면에서도 이점이 있고, 사용자도 모든 이미지를 한번에 받지 않아도 되니 페이지를 빠르게 로딩할 수 있게 된다.

<br />

# 2. 무한스크롤 UI 적용 방법 2가지

## 2-1) Scroll Event

무한스크롤 UI를 적용하는 첫 번째 방법은 `element.addEventListener` 이벤트 리스너를 통해 scroll event를 걸어 놓는 것.

사용자가 페이지에서 스크롤하면 해당 이벤트가 발생했을 때의 스크롤 위치(top, right, bottom, left 등)를 알 수 있으니 스크롤이 View Port 상 바닥 또는 바닥보다 조금 더 위를 지날 때 콘텐츠를 추가하도록 처리할 수 있다.

이 경우 scroll event가 너무 많이 발생할 수도 있어서 적절하게 `Throttle`을 적용시키면 이벤트가 너무 많이 발생하는 현상을 줄이고, 사용자 입장에서도 크게 불편하지 않도록 최적화할 수 있다.

<br />

## 2-2) IntersectionObserver

Intersection Observer는 특정 요소와 View Port 사이의 변화를 비동기적으로 관찰하는 방법이다.

예를 들어, 여러 개의 `li` 요소가 있다고 했을 때 가장 마지막 `li` 요소를 Observe하면 해당 요소가 화면에 나타나기 전까지는 아무런 이벤트를 발생시키지 않다가 사용자가 설정한 옵션(`threshold` 등)에 따라 `li` 요소가 view port 상 첫 등장했다거나 완전히 나왔다거나 절반만 나왔을 때 이벤트를 동작시킬 수 있다.

Intersection Observer를 사용하면 사용자가 위에서 부터 스크롤하면서 내려올 때 굳이 조건문을 거쳐서 페이지 하단에 위치하는지 확인할 필요 없이, 가장 마지막 요소만 감시하고 있도록 하면 불필요한 이벤트 발생을 줄일 수 있다.

```jsx
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Do something
      }
    });
  },
  {
    // Options
  }
);

const lastLiElement = document.querySelector("li:last-child");
observer.observe(lastLiElement);
```

- `new IntersectionObserver(callback, options)` 형태로 observer 인스턴스를 생성한다.
- 생성된 인스턴스의 `.observe(element)` 메서드를 호출하여 인자로 넘겨준 element를 감지한다.

<br />

# 3. IntersectionObserver로 무한스크롤 구현하기

1. 구조

```html
<div class="container">
  <div class="image show">첫 번째 이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">이미지</div>
  <div class="image">마지막 이미지</div>
</div>
```

위와 같은 구조를 갖는 페이지가 있고, 적절히 스타일링하면 아래와 같다. (기본은 안보이는 상태, `show` 클래스명이 있을 때만 보이도록 설정)

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222316822-781c2b3f-46f0-4bf4-871d-4fac088aea87.png">
</div>

<br />

2. Observer 생성

```jsx
const images = document.querySelectorAll(".image");

const observer = new IntersectionObserver((entries) => {
  console.log(entries);
});

observer.observe(images[0]);
```

image 클래스를 갖는 모든 element 요소를 불러오고, 이를 감지할 때 사용한다.

우선 observer에 `callback`으로 console.log를 찍도록 하고, 첫 번째 요소를 감지하도록 하면 페이지에 진입하자마자 console에 감지된 요소가 찍힌다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222316819-afac893a-d721-4eff-96c8-c4428d3c2b40.png">
</div>

<br />

3. 감지됐을 때 show 클래스명 부여하기

```jsx
const images = document.querySelectorAll(".image");

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    entry.target.classList.toggle("show", entry.isIntersecting);
  });
});

images.forEach((image) => {
  observer.observe(image);
});
```

- 화면에 보이는 모든 요소를 감지하도록 작성.
- IntersectionObserver를 생성할 때의 callback 인자도 배열 형태로 여러 개가 들어올 수 있으므로 forEach 메서드를 통해 순회하면서 로직을 실행시킨다.
- `entry.isIntersecting` 값을 통해 감지가 됐는지의 여부를 확인할 수 있다.
- 감지가 됐을 때 `show` 클래스 명을 토글한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222316818-a1c2b11b-216c-44c5-abaf-9bdfa8840a9e.gif">
</div>

> 스크롤 하면서 각 요소가 감지되면 클래스명이 Toggle 되면서 애니메이션이 동작한다.

<br />

4. 한 번 감지되면 반응하지 않도록 설정하기

위와 같이 설정하면 아래로 스크롤 후 다시 위로 올라가면 아래로 내린 것처럼 애니메이션이 동작한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222316813-c6678232-80e0-446f-84d7-e175cd5d6c58.gif">
</div>

> 아래로 스크롤 한 후 위로 스크롤 하면 클래스명이 계속 Toggle 된다.

<br />

이럴 때 `observer.unobserve(element)` 메서드를 사용하면 된다.

```jsx
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    entry.target.classList.toggle("show", entry.isIntersecting);
    if (entry.isIntersecting) {
      observer.unobserve(entry.target);
    }
  });
});
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/222316817-059df74e-ca00-4c8f-914c-3f065834f92f.gif">
</div>

> 한 번 감지된 요소는 unobserve() 메서드를 통해 더 이상 감지하지 않도록 한다.

<br />

# 4. options

Intersection Observer 인스턴스를 생성할 때 두 번째 인자로 options 객체를 넘겨줄 수 있는데, 설정할 수 있는 options는 다음과 같다.

- **root**(`element | null`): 감시하려는 View Port 요소. 지정하지 않으면 기본값으로 최상위 요소가 선택된다.
- **rootMargin**(`string`): CSS margin과 비슷하게 작용해서 감지할 요소의 margin을 부여한다. 만약 -50px 이라고 하면 감지할 요소가 root에서 지정한 요소보다 50px 만큼 줄어든 범위에서 감지한다.
- **threshold**(`number`): 감지할 요소가 어느정도 보일 지 설정. 1이면 완전히 보였을 때, 0.5면 절반, 0이면 드러나기 직전에 감지가 가능하다.

<br />

# 5. 정리

지금 예제에서는 class 명을 이용해서 감지가 어떻게 동작하는지 정도만 확인했는데, 실제로 사용할 때는 특정 `GET` 요청을 쿼리에 따라 몇 개만 응답할 때와 같은 상황에서 사용할 수 있을 것 같다.

최초 화면에서 보여질 정도만큼의 양만 데이터를 받아와서 보여주고, 가장 아래에 위치한 요소에 Observe를 걸어둔다. 사용자가 스크롤해서 마지막 요소가 감지됐을 때 추가로 API를 호출하여 나머지 부분들을 보여주도록 만들 수 있을 것이다.

꼭 API 호출이 아니더라도 페이지 진입 시 1회만 동작하는 Animation이 있다고 가정했을 때, 사용자 모니터에 따라, 모바일 화면에 따라 어떤 사용자는 화면이 너무 작아서 스크롤 하기 전에 Animation이 동작해서 Animation을 보지도 못했는데 이미 끝나있을 수도 있다.

이럴 때 Animation을 보여줘야 할 요소에 Observe를 걸어놓고, 감지가 됐을 때 Animation을 동작하도록 하면 scroll event 로 매 순간 계산할 필요 없이 필요한 순간에만 Animation을 동작시킬 수 있게 된다.

<br />
<hr />

# 참조

- [https://developer.mozilla.org/ko/docs/Web/API/Intersection_Observer_API](https://developer.mozilla.org/ko/docs/Web/API/Intersection_Observer_API)
