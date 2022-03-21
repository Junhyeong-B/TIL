# 8장 제어문
 
1. 블록문은 0개 의상의 문을 중괄호로 묶은 것으로 언제나 자체 종결성을 갖기 때문에 블록문의 끝에는 세미콜론을 붙이지 않는다.

```jsx
// 블록문
{
	var a = 10;
}
```

<br />

2. if ~ else 문(조건문)에서 조건식으로 평가된 값이 Boolean 값이 아닐 경우 암묵적 boolean 타입 변환이 이루어진다.
  
<br />

3. if ~ else 문은 표현식이 아닌 문이므로 변수에 할당할 수 없고, 삼항 연산자는 표현식이므로 변수에 할당할 수 있다.

<br />

4. switch 문에서 각각의 case에 break, return 등을 사용하지 않으면 switch 문이 끝날 때까지 모든 case문을 실행하는데 이를 폴 스루(fall through)라고 한다.
    - default 문에는 break를 생략하는 것이 일반적이다.

```jsx
switch (value) {
	case 1:
	case 2:
		var a = value;
		break;
	default:
		var a = 0;
}
// 1, 2 case에 대해 폴 스루를 이용한 switch 문이다.
```

<br />

5. for 문에서 선언문, 조건식, 증감식은 모두 옵션이다. 따라서 아무것도 작성하지 않는다면 무한히 반복한다.( for ( ; ; ) {  } )

<br />

6. break 문은 레이블 문, 반복문, switch 문에서 동작한다.
   
<br />

7. 중첩 for 문에서 break문을 사용하면 내부 for 문에서 탈출하여 외부 for 문으로 진입한다.
    - 만약 외부 for 문을 종료하고 싶다면 레이블을 붙여 레이블 문으로 만들어주면 된다.
    - break문을 사용하기 위해 레이블 문으로 만드는 것은 외부 for 문을 종료할 때 외에 권장되지는 않는다.

```jsx
outer: for (let i = 0; i < 5; i++) {
	for (let j = 0; j < 10; j++) {
		if (조건식) {
			break outer;
		}
		// ...
	}
}
```

<br />

# 🤔 문제

1. 폴 스루(fall through)란 무엇인가?
- 답

    switch 문에서 각각의 case에 break, return 등을 사용하지 않으면 switch 문이 끝날 때까지 모든 case문을 실행하는데 이를 폴 스루(fall through)라고 한다.
    

<br />

2. 블록문의 경우 자체 종결성을 갖고 있기 때문에 세미콜론을 생략해야 한다.
    
    ( O or X )

- 답
    
    O