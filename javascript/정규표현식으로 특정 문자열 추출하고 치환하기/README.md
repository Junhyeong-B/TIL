# 정규표현식으로 특정 문자열 추출하고 치환하기

# 1. Javascript에서의 정규 표현식의 사용

정규 표현식은 문자열에서 특정 문자 조합을 찾기 위한 패턴으로 사용되는데, 문자열(`String`)의 `match()`, `replace()`, `search()`, `split()` 메서드와 함께 사용할 수 있다. 정규 표현식 객체(`new RegExp`)를 사용한 `exec()`, `test()` 메서드도 사용할 수 있다.

<br />

### ※ String 메서드 + 정규표현식의 사용

1. `String.match(RegExp)`: 문자열이 정규식과 일치하면 일치하는 전체 문자열을 첫 번째 요소로 포함하는 Array를 반환한다. 만약, 일치하는 부분이 2가지 이상이고 정규 표현식의 Global Flag(`//g`)를 사용하면 2개 이상의 요소를 갖는 Array를 반환한다.
2. `String.replace(RegExp, 변경하려는 문자열)`: 문자열이 정규식과 일치하면 일치하는 전체 문자열을 두 번째 파라미터로 받은 변경하려는 문자열로 치환한다. Global Flag를 사용하면 String에 존재하는 정규식과 일치하는 2개 이상의 문자열을 모두 치환할 수 있다.
3. `String.search(RegExp)`: 정규식과 첫 번째로 일치하는 부분의 `index`를 반환한다. 만약 일치하는 부분이 존재하지 않는다면 `-1`을 반환한다.
4. `String.split(RegExp)`: 문자열을 정규식과 일치하는 문자열을 기준으로 여러 개의 문자열로 나눈 배열을 반환한다.

<br />

### ※ RegExp 객체의 메서드

1. `RegExp.exec(string)`: 정규 표현식 검색을 수행할 문자열(string)에 대해 정규표현식 검색에 성공하면 일치한 문자열을 첫 번째 원소로, 각각의 캡처 그룹을 이후 원소로 포함하는 배열을 반환한다. 실패하면 null을 반환한다.
2. `RegExp.test(string)`: 정규 표현식 검색을 수행할 문자열에 대해 일치하는 부분이 있으면 `true`, 없으면 `false` 값을 반환한다.

<br />

# 2. 정규 표현식을 사용해서 특정 문자열 추출하기

특정 문자열에서 원하는 부분을 추출하려면 `match()` 메서드를 사용하여 추출하거나 `replace()`로 일치하지 않는 문자열을 빈 문자열로 치환하여 추출할 수 있다. 만약, 숫자와 그 외 문자가 복잡하게 섞인 문자열에서 **숫자만 추출**한다고 가정하고 추출해보자.

<br />

## 2-1) match() 사용하기

```jsx
const rawText = "a!1w82  @3106 $5^a1ASSD060a3280";
const reg = new RegExp(/[0-9]+/, "g");
console.log(rawText.match(reg).join("")); // 1823106510603280
```

<br />

## 2-2) replace() 사용하기

```jsx
const rawText = "a!1w82  @3106 $5^a1ASSD060a3280";
const reg = new RegExp(/[^0-9]/, "g");
console.log(rawText.replace(reg, "")); // 1823106510603280
```

여기서 `/[0-9]+/`는 숫자 0~9까지 1개 이상인 것을 모두 찾는다는 것을 의미하고, `/^[0-9]/` 는숫자를 제외한 나머지를 찾는다는 것을 의미한다.

<br />

## 2-3) 특수 문자만 추출하기

```jsx
const rawText = "a!1w82  @3106 $5^a1ASSD060a3280";
const reg = new RegExp(/[0-9a-z ]+/, "gi");
console.log(rawText.replace(reg, "")); // !@$^
```

`i Flag`는 알파벳의 대소문자를 모두 검사할 때 사용하고, 띄어쓰기를 포함한 숫자, 영어 알파벳을 모두 빈 문자열로 치환하면 특수문자만 추출할 수 있게 된다.

<br />

# 3. 특정 문자열 치환하기

## 3-1) 서식자 치환

파이썬에서는 문자열을 작성할 때 서식 지정자를 사용해 포매팅할 수 있다. 

```python
name = 'maria'
print('I am %s.' % name)
>>> 'I am maria.'
```

위 코드의 경우 `%s` 키워드를 name 변수로 포매팅한 것이다. Javascript에서 정규표현식을 이용해 이를 구현해보자.

<br />

### Javascript로 파이썬 서식자 치환 구현하기

```jsx
const name = "maria";
const text = "I am %s.";
console.log(text.replace(/%s/, name)); // I am maria.
```

특정 서식자 하나를 바꾸는 것은 생각보다 쉽다.

<br />

## 3-2) 파이썬 format 메서드 구현하기

파이썬에서는 format 메서드를 사용해 여러 개의 서식자를 각각 포매팅할 수 있는데, 이는 다음과 같다.

```python
print('Hello, {0} {2} {1}'.format('Python', 'Script', 3.6))
>>> 'Hello, Python 3.6 Script'
```

이를 자바스크립트로 구현해보자.

<br />

### Javascript로 파이썬 format 메서드 구현하기


```jsx
const text = "Hello, {0} {2} {1}";

String.prototype.format = function (...arg) {
  let str = this;
  const reg = new RegExp(/{[0-9]+}/);

  while (reg.test(str)) {
    str = str.replace(reg, arg[str.match(reg)[0].match(/[0-9]+/)]);
  }

  return str;
};

console.log(text.format("Python", "Script", 3.6)); // Hello, Python 3.6 Script
```

위 예제처럼 동일하게 구현하기 위해 `prototype` 키워드로 String 객체에 추가하는 방식으로 작성했다.

<br />

1. `function` 키워드

`String.prototype.format`에 `fuction` 키워드를 통해 작성했지만 화살표 함수로도 될까?

해당 format 메서드에서는 불가능하다. this 키워드를 통해 string에 접근하고 있는데, 화살표 함수로 작성하게 되면 this는 본인보다 상위 스코프의 this를 참조하므로 빈 객체 {} 를 반환하게 되어 화살표함수 대신 function 키워드를 통해 함수를 정의해야 한다.

<br />

2. `...arg`

Rest 파라미터를 통해 파라미터 갯수에 상관 없이 받아온다. 여기서 arg를 조회하면 모든 파라미터가 포함된 배열을 확인할 수 있다.

<br />

3. `arg[str.match(reg)[0].match(/[0-9]+/)]`

여기서 str에 대해 `match`를 두번 사용하고 있는데 이는 중괄호를 포함한 문자열을 먼저 찾고, 그 안에 포함된 숫자를 추출하기 위해 두 번 사용한 것이다. `match(reg)`만 수행하게 되면 `{0}` 같은 문자열을 반환하기 때문에 `arg` 배열에서 index로 접근할 수 없게 되기에 `match`를 1회 더 수행해서 그 내부에서 숫자만 뺀 후 그 숫자를 통해 index로 접근한다.

<br />

4. `reg.test(str)`

`{숫자}` 형태의 정규표현식을 사용해서 str에 해당 정규 식이 포함되어있으면 true를 반환하므로 str에 재할당하는 방식 + while문을 이용하여 모든 `{숫자}` 문자열을 치환할 때 까지 순회할 수 있게 된다.