# Garbage Collection

# 1. 메모리 누수

메모리 누수(Memory Leak)는 부주의 또는 오류로 인해 더 이상 필요하지 않는 메모리를 해제하지 못하는 것을 의미한다. 한 가지 예시로 불필요한 var 키워드, this 키워드를 통해 전역 객체에 변수를 저장하는 것이 있다.

```jsx
function saveGlobalVariable() {
	this.memory = "leak";
}

saveGlobalVariable();
```

<div align="center">
	<img src="https://user-images.githubusercontent.com/85148549/160101676-f06b1e70-8345-4e38-9493-8ea757ad71cf.png">
</div>

위 코드는 함수 내에서 this 키워드를 통해 전역 객체의 memory 프로퍼티에 `'leak'` 문자열을 저장하고 있다. 이렇게 되는 이유는 만약 new 키워드를 통해 인스턴스를 생성했다면 생성된 인스턴스의 memory 프로퍼티에 저장했겠지만 **일반 함수로 호출**했기 때문에 **this는 전역 객체를 가리키게 되고** 전역 객체에 변수를 저장하게되는 것이다.

이러한 상황에서 메모리 누수가 발생될 수 있고, 메모리 누수는 성능 저하로 이어질 수 있다. 그럼 메모리 관리는 어떻게 이루어질까?

<br />

# 2. Garbage Collection

C, C++ 같은 저수준의 언어는 수동 정리 메커니즘을 사용하는데 자바스크립트는 가비지 컬렉션(GC, Garbage Collection)이라는 자동 메모리 관리 방법을 사용한다. 가비지 컬렉션은 도달 가능성(reachability)이라는 개념을 사용해 메모리 관리를 수행한다. 여기서 도달 가능한(reachable) 값이라는 것은 참조에 의해 어떻게든 접근하거나 사용할 수 있는 값을 의미하고 도달 가능한 값은 메모리에서 해제되지 않는다.

<br />

그래서, 현재 함수의 지역 변수 | 매개변수, 중첩 함수의 체인에 있는 함수에서 사용되는 변수 | 매개변수, 전역 변수 등은 명백한 이유 없이 메모리가 해제되지 않는다.

<br />

# 3. Garbage Collection에서의 메모리 관리 매커니즘

## 3-1) Reference-counting 방법

**더 이상 필요없는 객체**를 **다른 어떤 객체와도 참조되지 않는 객체**라고 정의하여 메모리를 해제하는 방식이다. 다음 그림과 같이 참조되고 있는 객체들이 있다고 가정하자.

<div align="center">
	<img src="https://user-images.githubusercontent.com/85148549/160101684-abff69d9-45a4-4fe4-8308-113a9e36dd89.png">
</div>

위 그림에서 참조되고 있지 않은 메모리는 없으므로 가비지 컬렉션에 의해 해제되는 메모리는 없다. 여기서 참조할 수 없는 메모리가 생긴다면 가비지 컬렉션에 의해 메모리가 해제된다.

<br />

### ※ Reference-counting의 단점 - 순환 참조

위 그림에서 만약 **빨간색 화살표로 연결된 참조를 해제**한다고 가정해보자. 그럼 root에서부터 주황색 메모리까지 도달할 수는 없지만 주황색 메모리들은 서로를 참조하고 있는 순환 참조 구조를 형성한다.

Reference-counting 방법에서는 위 순환 참조 구조에 대해 메모리를 해제하지 않는다.

<br />

## 3-2) Mark and Sweep

**더 이상 필요없는 객체**를 **닿을 수 없는 객체(unreachable)**라고 정의하여 메모리를 해제하는 방식이다. 이 방식은 root 객체(Javascript에서는 전역 변수)로부터 시작해서 닿을 수 있는 객체와 닿을 수 없는 객체로 나눈다.

<div align="center">
	<img src="https://user-images.githubusercontent.com/85148549/160101682-3484b1da-1030-411a-bec5-656f11978a76.png">
</div>

<br />

이 방식은 3-1) Reference-counting보다 효율적이다. 위 그림에서 보듯 순환 참조 구조가 있다고 하더라도 root에서 부터 닿을 수 없는 객체이기 때문에 메모리에서 해제한다. 따라서 최신 브라우저에서는 가비지 콜렉션에서 Mark and Sweep 방식을 사용하고 있다.

<br />

### ※ Mark and Sweep의 단점 - 수동 해제

자바스크립트의 GC는 자동으로 메모리를 관리하고 있어서 root에서부터 참조할 수 있는 데이터를 직접 삭제하고 싶어도 수동으로 해제할 수 없다.

<br />

### 3-2-1) Mark and Sweep의 동작 원리

1. 가비지 컬렉터는 Root의 정보를 기억(mark)한다.
2. Root에서 참조하고 있는 모든 객체를 방문하여 mark한다.
3. mark된 객체에서부터 참조하고 있는 모든 객체를 mark한다. 가비지 컬렉터는 정보를 기억(mark)해 놓음으로써 같은 객체를 두 번 이상 방문하지 않는다.
4. Root에서부터 도달 가능한 모든 객체가 확인될때 까지 3 과정이 반복된다.
5. 확인이 모두 끝나면 mark되지 않은 모든 객체를 메모리에서 삭제한다.

<br />

# 4. 정리

- 자바스크립트에서 가비지 컬렉션은 자동으로 메모리를 관리한다.
- 메모리 해제에 사용하는 알고리즘은 Mark and Sweep 방식이다.
- root에서부터 도달할 수 있는 객체의 메모리는 해제되지 않는다.

<br />

## 참고

- [https://ko.javascript.info/garbage-collection#ref-944](https://ko.javascript.info/garbage-collection#ref-944)
- [https://developer.mozilla.org/ko/docs/Web/JavaScript/Memory_Management#allocation_in_javascript](https://developer.mozilla.org/ko/docs/Web/JavaScript/Memory_Management#allocation_in_javascript)
- [https://ui.toast.com/weekly-pick/ko_20210611](https://ui.toast.com/weekly-pick/ko_20210611)