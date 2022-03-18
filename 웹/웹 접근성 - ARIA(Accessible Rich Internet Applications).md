# 웹 접근성 - ARIA(Accessible Rich Internet Applications)

# ARIA란?

HTML 내부 <div>나 <span> 태그 등은 정보를 제공하지 않고 있다. 따라서 해당 태그를 사용하여 웹사이트를 구성하면 이유가 어떻게 되었든 시각 장애인은 이를 볼 수 없다는 문제가 발생한다. **ARIA**는 장애를 가진 사용자가 스크린리더 같은 보조기기에서 필요한 정보들을 추가하는 방법을 제공하는 여러 특성을 말한다.

- 브라우저에서 자동으로 해석되고 변환되도록 설계되었다.

<br />

### 구현하려는 기능을 구현할 때 이미 의미를 가진 HTML이 있다면?

- ARIA보다 의미를 가진 HTML을 사용하는 것이 좋다.
- 이는 ARIA에서 저의하는 특성들은 대부분 HTML5에 통합되었고, 의미를 가지는 HTML 태그는 이미 접근성, 역할, 상태 등을 내장(Built-in)하고 있기 때문이다.

<br />

# ARIA의 사용

- ARIA는 roles(역할), states(상태), properties(특징) 3가지를 분할하여 정의한다.

<br />

### ARIA 사용 전의 HTML 모습

```jsx
<ol>
  <li id="ch1Tab">
    <a href="#ch1Panel">Chapter 1</a>
  </li>
  <li id="ch2Tab">
    <a href="#ch2Panel">Chapter 2</a>
  </li>
  <li id="quizTab">
    <a href="#quizPanel">Quiz</a>
  </li>
</ol>

<div>
  <div id="ch1Panel">Chapter 1 content goes here</div>
  <div id="ch2Panel">Chapter 2 content goes here</div>
  <div id="quizPanel">Quiz content goes here</div>
</div>
```

- 일반 사용자는 웹에 그려진 모습을 통해 해당 내용을 유추할 수 있지만, 마크업만 보게되면 해당 내용을 확인할 수 없으며 보조기기 같은 기계들도 이를 구분할 수 없다.

<br />

### ARIA 사용 후의 HTML 모습

```jsx
<ol role="tablist">
  <li id="ch1Tab" role="tab">
    <a href="#ch1Panel">Chapter 1</a>
  </li>
  <li id="ch2Tab" role="tab">
    <a href="#ch2Panel">Chapter 2</a>
  </li>
  <li id="quizTab" role="tab">
    <a href="#quizPanel">Quiz</a>
  </li>
</ol>

<div>
  <div id="ch1Panel" role=”tabpanel” aria-labelledby="ch1Tab">Chapter 1 content goes here</div>
  <div id="ch2Panel" role=”tabpanel” aria-labelledby="ch2Tab">Chapter 2 content goes here</div>
  <div id="quizPanel" role=”tabpanel” aria-labelledby="quizTab">Quiz content goes here</div>
</div>
```

- \<li> 태그의 역할(role)이 “tab” 이라고 명시된 것.
- \<div> 태그의 역할은 tabpanel이고, 무엇으로 부터 명시된 것(aria-labelledby)인지 표시(”ch1Tab” 등)되어 있다.

<br />

# 참고

1. [An overview of accessible web applications and widhg](https://developer.mozilla.org/ko/docs/Web/Accessibility/An_overview_of_accessible_web_applications_and_widgets)
2. [ARIA - 접근성](https://developer.mozilla.org/ko/docs/Web/Accessibility/ARIA)