# innerHTML vs insertAdjacentHTML vs appendChild

# 1. Element.innerHTML

- Element에 포함된 HTML, XML 마크업을 가져오거나 설정한다.
    - 요소(Element)의 내용을 변경하는 것이 아니라 HTML 문서를 삽입하려면 insertAdjacentHTML, appendChild 등의 메서드도 사용할 수 있다.

```jsx
const element = document.createElement('div');

element.innerHTML = '<h1>안녕</h1>';
```

<br />

## 2. Element.insertAdjacentHTML(position, text)

- 특정 위치에 원하는 node들을 추가 한다.
    - 여기서 node는 element의 상위 개념이다.
    - 이미 사용중인 element는 다시 파싱하지 않는다.
        
        ⇒ 삽입하려는 element 안에 존재하는 다른 elemen는 건드리지 않는다.
        
    - 위와 같은 이유로 innerHTML보다 작업이 덜 드므로 속도가 더 빠르다.

<br />

1. `'beforebegin'`: element 앞에
2. `'afterbegin'`: element 안에 가장 첫번째 child
3. `'beforeend'`: element 안에 가장 마지막 child
4. `'afterend'`: element 뒤에

<br />

**Note:** `beforebegin`, `afterend` position은 element의 부모가 존재해야 하고, node가 tree 안에 있어야 한다.

```jsx
document.body.insertAdjacentHTML('beforeend', '<div>TEXT</div>');
```

<br />

## 3. Node.appendChild(element)

- Node의 자식 노드 중 마지막 자식으로 element를 붙인다.
- 단 하나의 element만 파라미터로 받을 수 있다.
- 이동시킬 element를 현재 위치에서 새로운 위치로 이동시킨다.
    
    ⇒ 두 지점에 동시에 존재할 수 없다는 것을 의미
    

<br />

### 참고: Node.cloneNode()

- 새로운 부모의 밑으로 붙기 전에 노드를 복사한다.

```jsx
const element = document.createElement('div');

document.body.appendChild(element);
```

<br />

## 4. 성능 비교

- 그럼 innerHTML, insertAdjacentHTML, appendChild로 새로운 element를 추가시킬 때 어떤 메서드가 가장 빠를까?

```jsx
box1 = document.createElement("div");

box2 = document.createElement("div");
box2HTML = box2.innerHTML;
```

```jsx
/* 1. innerHTML */
box1.innerHTML += box2HTML;

/* 2. insertAdjacentHTML*/
box1.insertAdjacentHTML('beforeend', box2HTML);

/* 3. appendChild */
box1.appendChild(box2);
```

<img width="400px" align="center" src="https://user-images.githubusercontent.com/85148549/157390726-d3941cf8-daf8-4b47-83f4-eb1fbfc6ca9d.png" />

<br />

## ※ 결과

- insertAdjacentHTML이 가장 빠르고 innerHTML이 가장 느리다.
- element를 특정 노드에 추가하는 경우라면 insertAdjacentHTML을 사용하는 것이 좋겠다.
- 참고 사이트
  - https://www.measurethat.net/Benchmarks/Show/16493/1/innerhtml-vs-insertadjacenthtml-vs-appendchild-vs-inser