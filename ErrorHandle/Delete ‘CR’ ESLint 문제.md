# Delete ‘CR’ ESLint 문제

## 운영체제(Mac, Window)에 따른 Delete ‘CR’ ESLint 문제

- 프로젝트를 세팅하다 Mac, Window 운영체제에 따라 에러가 발생하는 경우가 있다.
- 오늘 ESLint를 .js, .ts 파일을 동시에 작업 가능하도록 수정할 때 아래와 같은 `Delete `cr`` ESLint 에러가 발생했다.

<img src="https://user-images.githubusercontent.com/85148549/157398516-213e139f-3994-4089-9e53-2e52affff2df.png">

<br />

## 해결 방법

### 1) CR, LF의 차이

- **CR(Carrage Return)**: 현재 커서를 줄 올림 없이 가장 앞으로 옮기는 동작
- **LF(Line Feed)**: 커서는 그대로, 종이만 한 줄 올려 줄을 바꾸는 동작

### 2) Window와 Mac에서의 줄 바꿈 차이

- Mac OS: **LF**(`\n`)만으로 줄바꿈 처리
- Window OS: **CRLF**(`\r\n`) 모두 입력으로 줄바꿈 처리

### 3) ESLint Rule 추가

- 운영체제에 따라 다르게 동작하는 줄바꿈 처리로 인해 발생한 에러로, 아래에 해당하는 Rule을 `.eslintrc` 파일에 추가한다.

```jsx
'prettier/prettier': ['error', { 'endOfLine': 'auto' }]
```

- Window OS를 사용하면 endOfLine은 `CRLF`가 되므로 `endOfLine: 'auto'` 룰을 추가하여 해당 에러를 해결할 수 있다.