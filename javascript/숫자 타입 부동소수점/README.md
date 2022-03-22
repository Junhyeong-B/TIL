# 숫자 타입 부동소수점

# 0.1 + 0.2 = 0.30000000000000004 ?

```jsx
console.log(0.1 + 0.2); // 0.30000000000000004
```

<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159435450-95a99243-8799-428a-a8f3-f7ff6372f8ea.png">
</div>

- Javascript에서 0.1 + 0.2 의 결과로 0.3000000004 의 값이 반환된다.
- 왜 이런 현상이 발생할까?

<br />

# 배정밀도 64비트 부동소수점 형식

- Javascript의 숫자타입의 값은 배정밀도 64비트 부동소수점 형식을 따른다.
- 즉, 모든 수를 실수로 처리한다.

<br />

### ※ 단정밀도, 배정밀도?

- IEEE 754: IEEE에서 개발한 컴퓨터에서 부동소수점을 표현하는 표준.
- 여기서 `32비트`로 표현하는 것을 **단정밀도**, `64비트`로 표현하는 것을 **배정밀도**라고 한다.

<br />

### ※ 고정소수점, 부동소수점 ?

- **고정 소수점(fixed point)**: 실수를 표현하는 간단한 방식으로 소수부의 자릿수를 미리 정하여 고정된 자릿수의 소수를 표현하는 방식이다.
    - 정수부와 소수부로 나누게되고, 자릿수가 크지 않아 표현할 수 있는 범위가 적다는 단점이 있다.

<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159435455-f2a511e4-4855-41a8-a45d-2c9c3dfd53ed.png">
</div>

<br />

- **부동 소수점(floating point)**: 실수를 정수부와 소수부가 아닌 가수부와 지수부로 나누어 표현하는 방식이다.
    - 고정 소수점에 비해 매우 큰 실수까지 표현할 수 있다.

<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159435453-2debfbc0-ed86-4cb7-94f8-da91f68dac26.png">
</div>

<br />

# Javascript에서 0.1 + 0.2 = 0.30 ... 04 의 원인

- 64비트 배정밀도 부동소수점 표현 방식을 따르고 있기에 Javascript는 숫자형 타입의 데이터를 숫자, 지수, 부호로 나누어 저장한다.
    - **0~51 bit**(52 bits): 숫자
    - **52~62 bit**(11 bits): 지수
    - **63 bit**(1 bit): 부호
- 이런 숫자형 데이터를 저장, 계산하는 과정에서 10진법 ⇒ 2진법 | 2진법 ⇒ 10진법 변환 과정이 동작하는데 몇몇 소수는 10진법 ⇒ 2진법으로 변환하는 과정에서 무한 소수가 되어버린다.

```jsx
const number1 = 10;
const number2 = 0.1;
console.log(number1.toString(2)); // '1010'
console.log(number2.toString(2)); // '0.00011001100110011001100110011001100110011101'
```

<div align="center">
    <img src="https://user-images.githubusercontent.com/85148549/159435451-c1e041a8-1861-4661-8613-1f5e37936a57.png">
</div>

- 따라서, 무한소수로 변환되는 과정에서 미세한 값들은 소실되거나 초과하여 해당 오류가 발생하는 것이다.

<br />

# 해결방법

1. **Number.prototype.toFixed()**
    - toFixed(n): n번째 자리까지 반올림 처리로, n은 0 ~ 20 사이의 값을 사용할 수 있다.
    - 소수점 이하의 값을 반올림 처리하므로 소수 계산 과정에서 발생하는 미세한 값 손실, 초과 부분을 반올림하여 보정할 수 있다.

```jsx
function add(a, b, n) {
  return Number((a + b).toFixed(n));
}

add(0.1, 0.2, 2) // 0.3
```

<br />

2. 소수에서 정수가 될 때까지 10을 곱해준 후 마지막 계산 결과에서 곱해준 10의 숫자만큼 10을 나눠준다.

```jsx
console.log(((0.2 * 10) + (0.1 * 10)) / 10); // 0.3
```

<br />

# 참고

- [https://ko.wikipedia.org/wiki/IEEE_754](https://ko.wikipedia.org/wiki/IEEE_754)
- [http://www.tcpschool.com/cpp/cpp_datatype_floatingPointNumber](http://www.tcpschool.com/cpp/cpp_datatype_floatingPointNumber)
- [https://www.secmem.org/blog/2020/05/15/float/](https://www.secmem.org/blog/2020/05/15/float/)