# 이벤트 루프

## 1. 자바스크립트는 Single Thread로 동작한다.

- 자바스크립트 엔진의 Call Stack은 하나만 존재하고 Single Thread로 동작한다.
    - 그렇다면 브라우저에서 이벤트, 애니메이션 등을 어떻게 처리할 수 있을까?

<br />

## 2. Event Loop

- 브라우저의 Event Loop 시스템을 통해 브라우저에서 발생하는 이벤트 등을 처리할 수 있다.
- Event Loop는 자바스크립트 엔진에 포함된 개념이 아니고, 브라우저나 Node JS 자체적으로 관리하고 있다.

<img width="300px" align="center" src="https://user-images.githubusercontent.com/85148549/157390402-21730a0d-7d8a-4daa-9b79-e73220b7eb10.png">

<br />

- 클릭과 같은 DOM Events, 네트워크 호출, Timer 등은 브라우저에 위임된다.
    - Web API는 브라우저에서 제공하는 API이다.
    - 보통 Web API는 콜백 함수를 넘기게 되는데, 콜백 함수는 비동기 작업이 끝나면 Task Queue로 이동하여 순차적으로 Call Stack에 푸시되어 실행된다.
    - 이러한 과정들이 Multi Thread로 이루어지므로 자바스크립트가 Single Thread일뿐 브라우저는 Multi Thread로 동작하게 되어 이벤트 등이 가능한 것이다.

<br />

## 3. 이벤트 루프 동작 원리

1. 자바스크립트 코드가 실행되면 전역 스코프 내에서 실행된다.
2. 순차적으로 호출되는 함수는 Call Stack에 푸시한다.
3. 코드가 순차적으로 실행되어 DOM Events, AJAX, Timer 등과 같은 콜백 함수를 만나면 브라우저 내부적으로 Web API가 실행된다.
4. Call Stack에 쌓여있는 함수들은 실행이 종료되면 Call Stack에서 제거된다.
5. 모든 코드가 실행되었다면 스크립트가 종료되고 Call Stack은 비워지게 된다.
6. 이 때 Web API에 있던 콜백 함수들은 Task Queue로 이동한다.
7. Task Queue에 있는 콜백 함수들은 Call Stack이 완전히 비어있을 때 하나씩 Call Stack에 푸시한다.
8. 이벤트 루프는 Call Stack과 Task Queue를 감시하고 있다가 Task Queue에 콜백 함수가 존재할 때 Call Stack이 비어있는지 확인하고, 비어있다면 Task Queue에 있는 콜백 함수를 Call Stack으로 푸시하는 역할을 한다.