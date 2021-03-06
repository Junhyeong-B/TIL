# 배열(Array)과 연결 리스트(Linked List)의 특징

# 1. 배열

- 연관된 데이터를 연속적인 형태로 구성된 구조인 자료구조.
- 자바스크립트 배열의 길이는 언제든 늘어나거나 줄어들 수 있고, 연속적이지 않게 저장할 수 있어 밀집성을 보장하지 않는다.
- 인덱스를 통해 요소에 접근할 수 있고 반드시 정수로만 접근할 수 있다.
    - 대괄호 구문이나 속성 접근자를 사용할 경우 배열의 요소가 아니라 Array 객체에 연결된 변수를 참조한다.
    
    ```jsx
    const arr = [1, 2, 3, 4];
    
    console.log(arr[1]); // 2
    console.log(arr["length"]); // 4
    console.log(arr["1"]); // undefined
    ```
    
- 원하는 원소의 index를 알고 있다면 O(1)로 원소를 찾을 수 있다.
- 일반적인 의미의 배열은 메모리 영역을 연속적으로 사용한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/162158294-e41dfbf3-cde8-40c4-bae6-46680637d619.png">
</div>

<br />

## 1-1) 자바스크립트 배열의 메모리

### ※ 일반적인 배열

일반적으로 배열은 동일한 크기의 메모리 공간이 빈틈없이 연속적으로 나열된 자료 구조를 말한다. 배열의 요소는 하나의 타입으로 통일되어 있으며 서로 연속적으로 인접해 있는데, 이러한 배열을 **밀집 배열(dense array)** 이라 한다.

<br />

### ※ 자바스크립트의 배열

자바스크립트의 배열은 배열의 요소를 위한 각각의 **메모리 공간은 동일한 크기를 갖지 않아도 되며 연속적으로 이어져 있지 않을 수도 있다.** 배열의 요소가 연속적으로 이어져 있지 않는 배열을 **희소 배열(sparse array)** 이라 한다.

- 자바스크립트의 배열은 일반적인 배열의 동작을 흉내낸 해시 테이블로 구현된 객체이다.
- 인덱스로 배열 요소에 접근하는 경우, 일반적인 배열보다 성능적인 면에서 느릴 수 밖에 없는 구조적인 단점을 갖는다.
- 특정 요소를 탐색하거나 요소를 삽입 또는 삭제하는 경우에는 일반적인 배열보다 빠른 성능을 기대할 수 있다.

<br />

## 1-2) 배열 요소 추가, 제거

배열의 요소 추가, 제거에는 다음과 같은 순서에 따라 동작한다.

### 추가

1) 추가하려는 index부터 **index 뒤의 모든 요소를 1칸씩 뒤로 미룬다.**

2) index에 자리가 비어있으므로 해당 자리에 요소를 추가한다.

<br />

### 제거

1) 삭제하려는 index의 요소를 제거한다.

2) index는 비워진다.(Javascript에서는 null 또는 undefined)

3) **index부터 뒤의 모든 요소를 1칸씩 앞으로 당긴다.**

- 위의 과정을 따르므로 배열의 요소 추가, 제거에 걸리는 총 시간은 **O(n)** 이다.

<br />

## 1-3) 배열 요소 검색

배열 원소 검색에는 선형 검색(Linear Search)과 이진 검색(Binary Search)로 나뉜다.

### 선형 검색(Linear Search)

- 첫 번째 요소부터 차례대로 찾으려는 원소와 동일한 요소가 있는지 확인한다.
- 모든 요소를 확인하므로 정렬되지 않은 배열에서도 사용할 수 있다.
- **O(n)** 시간 복잡도를 가진다.

<br />

### 이진 검색(Binary Search)

- 분할 정복 알고리즘의 규칙에 따라 중간에 있는 요소부터 비교한다.
- 배열을 분할하면서 검색하여 찾으려는 원소와 동일한 요소가 있는지 확인한다.
- 반드시 정렬된 배열이어야 한다.
- **O($logn$)** 시간 복잡도를 가진다.

<br />

---

# 2. 연결 리스트(Linked List)

- 각 요소를 포인터로 연결하여 관리하는 선형 자료구조이다.
- 각 요소는 노드라고 부리고, 데이터 | 포인터 영역으로 구성된다.
- 한쪽 방향으로만 포인터가 존재하면 단일 연결 리스트(Singly Linked List), 양쪽 방향으로 포인터가 존재하면 이중 연결 리스트(Doubly Linked List)라고 부른다.
- 메모리가 허용하는 한 요소를 제한없이 추가할 수 있다.
- 탐색은 O(n) 시간 복잡도를 가진다.
- 요소 추가, 제거에는 O(1) 시간 복잡도를 가진다.
- 연결 리스트는 포인터를 사용하여 연결되어 있으므로 메모리가 퍼져있다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/162158296-3623703c-7aa0-4ee0-ac37-eabd53911584.png">
</div>

<br />

## 2-1) 연결 리스트 요소 추가, 제거

### 추가

1) 새로운 노드의 포인터를 추가하려는 노드가 가리키는 노드를 가리킨다.

2) 추가하려는 노드의 포인터를 새로운 노드를 가리키도록 수정한다.

<br />

### 제거

1) 삭제하려는 노드 이전 노드가 삭제하려는 노드의 포인터를 가리키도록 수정한다.

2) 삭제하려는 노드의 포인터를 제거한다.

- 위의 과정을 따르므로 연결 리스트의 요소 추가, 제거에 걸리는 총 시간은 **O(1)**이다.

<br />

## 2-2) 연결 리스트 요소 검색

- 첫 번째 노드의 데이터 영역부터 포인터 영역을 통해 순서대로 검색한다.
- 요소의 index를 알거나 모르거나 상관없이 요소 탐색에 걸리는 시간은 **O(n)** 이다.

<br />
<hr />

# 3. 정리

지금까지는 자바스크립트의 배열도 일반적인 배열(밀집 배열)의 특징을 갖고 있다고 잘못 생각했다.

결과적으로 자바스크립트의 배열은 일반적인 의미의 배열이 아니라 해시 테이블로 구현된 특수 객체이고, 메모리도 연속적으로 이어져있지 않을 수도 있다는 사실을 알게 되었다.

다음에는 해시 테이블에 대해서도 정리하는 시간을 가져보면 좋을 것 같다는 생각도 들었다.

<hr />

## 참고

[https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array)

[https://poiemaweb.com/js-array-is-not-arrray](https://poiemaweb.com/js-array-is-not-arrray)

[https://levelup.gitconnected.com/array-vs-linked-list-data-structure-c5c0ff405f16](https://levelup.gitconnected.com/array-vs-linked-list-data-structure-c5c0ff405f16)