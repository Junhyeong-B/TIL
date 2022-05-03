# 9장 유닛 테스트

# 1. TDD 법칙 세가지

1\) **첫째 법칙**: 실패하는 단위 테스트를 작성할 때까지 실제 코드를 작성하지 않는다.

2\) **둘째 법칙**: 컴파일은 실패하지 않으면서 실행이 실패하는 정도로만 단위 테스트를 작성한다.

3\) **셋째 법칙**: 현재 실패하는 테스트를 통과할 정도로만 실제 코드를 작성한다.

- 위 세가지 법칙을 모두 따르면 테스트 코드와 실제 코드는 함께 나오지만 실제 코드를 전부 테스트하는 테스트 케이스가 나올 수 있다.
- 실제 코드와 맞먹는 정도의 테스트 코드는 심각한 관리 문제를 유발하기도 한다.

<br />

# 2. 깨끗한 테스트 코드 유지하기

- 실제 코드가 진화하면 테스트 코드도 변해야 한다.
    - 지저분한 테스트 코드는 있느니만 못하다.
- 테스트 코드가 복잡할수록 실제 코드를 짜는 시간보다 테스트 케이스를 추가하는 시간이 더 걸린다.
- **테스트 코드는 실제 못지않게 중요하다.**
- 테스트 케이스가 없다면 모든 변경은 잠정적인 버그가 될 수 있고, 있다면 코드 변경이 수월해진다.

<br />

# 3. 깨끗한 테스트 코드

- 깨끗한 테스트 코드를 만드는 데에 가장 중요한 것은 **가독성**이다.
    - 경우에 따라 다를 수 있지만, 실제 코드보다 중요할 수도 있다.
- 가독성을 높이려면 명료성, 단순성, 풍부한 표현력 등이 필요하다.

<br />

```java
public void testGetPageHieratchyAsXml() throws Exception
{
	crawler.addPage(root, PathParser.parse("PageOne"));
	crawler.addPage(root, PathParser.parse("PageOne.ChildOne"));
	crawler.addPage(root, PathParser.parse("PageTwo"));

	request.setResource("root");
	request.addInput("type", "pages");
	Responder responder = new SerializedPageResponder();
	SimpleResponse response =
		(SimpleResponse) responder.makeResponse(
			new FitNesseContext(root), request);
	String xml = response.getContent();

	assertEquals("text/xml", response.getContentType());
	assertSubString("<name>PageOne</name>", xml);
	assertSubString("<name>PageTwo</name>", xml);
	assertSubString("<name>ChileOne</name>", xml);
}
```

- 위 테스트 코드는 addPage, assertSubString을 부르느라 중복되는 코드가 매우 많고, 읽는 사람을 고려하지 않는 코드이다.

<br />

```java
public void testGetPageHierarchyAsXml() throws Exception
{
	makePages("PageOnd", "PageOne.ChildOne", "PageTwo");

	submitRequest("root", "type:pages");

	assertResponseIsXML();
	assertResponseContains(
		"<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChileOne</name>"
	);
}
```

- 위 코드는 테스트 자료를 만든다는 코드 내용을 이해하기 수월하다.
- 잡다하고 세세한 코드들을 거의 없애고 중복되는 코드를 최소화하여 읽는 사람이 수행하는 기능을 빠르게 이해할 수 있도록 돕는다.

<br />

# 4. 이중 표준

- 테스트 코드와 실제 코드에 적용하는 표준은 다르다.
    - 테스트 코드에서는 실제 코드만큼 효율적일 필요가 없기 때문

<br />

```java
@Test
public void turnOnLoTempAlarmAtThreashold() throws Exception {
	hw.setTemp(WAY_TOO_COLD);
	controller.tic();
	assertTrue(hw.heaterState());
	assertFalse(hw.coolerState());
}
```

- 위 코드는 자연스럽게 읽히지 않는다.
- 코드가 길어질수록 가독성은 더 떨어질 것이다.
- 먼저 heaterState() 같은 상태를 보고난 후 assertTrue로 시선이 오른쪽에서 왼쪽으로 흐른다.

<br />

```java
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
	wayTooCold();
	assertEquals("HBchL", hw.getState());
}

public String getState() {
	String state = "";
	state += heater ? "H" : "h";
	state += blower ? "B" : "b";
	state += cooler ? "C" : "c";
	state += hiTempAlarm ? "H" : "h";
	state += loTempAlarm ? "L" : "l";
	return state;
}
```

- 위 코드는 의미만 안다면 문자열을 따라 움직이며 의미를 자연스럽게 이해할 수 있다.
- 여기선 대문자가 켜짐(on), 소문자가 꺼짐(off)를 의미하고, 순서대로 heater, blower, cooler, hi temp alarm, lo temp alarm 순서이다.
- getState에서의 String Buffer(문자열을 append하여 조합하는 것)가 보기 흉할 수 있지만 해당 코드에서는 효율적이다.

<br />

# 5. 테스트 당 assert 하나

- 테스트 코드를 짤 때 함수마다 assert 문을 단 하나만 사용해야 한다고 주장하는 학파가 있다.
- 단일 assert 문 규칙은 다소 가혹해보일 수 있으나 코드를 읽고 이해하기 쉬워진다는 장점이 있다.
- 단일 assert 문은 훌륭하지만 때로는 주저 없이 함수 하나에 assert 문을 여러개 작성해야 하는 경우도 분명히 존재한다.
- 하지만 assert 문은 줄일 수록 좋다.

<br />

# 6. 테스트 당 개념 하나

- 테스트 함수마다 한 개념만 테스트 하라는 규칙이다.
- 이것 저것 잡다한 개념을 연속으로 테스트하는 긴 함수는 피한다.
- assert 문이 여러개 이더라도 개념을 하나만 가져간다면 assert 문 속에 감춰진 일반적인 규칙을 이해하기 쉬워진다.

<br />

# 7. F.I.R.S.T

### 7-1) Fast

- 테스트는 빨라야 한다.(빨리 돌아야 한다.)
- 테스트가 느리면 자주 돌릴 수 없고, 자주 돌릴 수 없으면 초반에 문제를 찾아내 고치지 못한다.

<br />

### 7-2) Independent

- 각 테스트는 서로 의존하면 안된다.
- 어떤 순서로 실행해도 괜찮아야 한다.
- 테스트끼리 의존하게되면 특정 테스트의 실패에 의존된 다른 테스트도 잇달아 실패하기 때문이다.

<br />

### 7-3) Repeatable

- 어떤 환경에서도 반복 가능해야 한다.
- 돌아가지 않는 환경이 하나라도 생기면 테스트가 실패한 이유를 둘러댈 변명이 생긴다.

<br />

### 7-4) Self-Validating

- 테스트는 Boolean 값으로 결과를 내야 한다.
- 성공 or 실패 | true or false

<br />

### 7-5) Timely

- 테스트는 적시에 작성해야 한다.
- 단위 테스트는 테스트하려는 실제 코드를 구현하기 직전에 구현한다.
- 실제 코드를 먼저 만들면 테스트 코드를 구현하기 어렵다고 판단하게 될 수도 있고, 테스트가 불가능하게 설계할지도 모른다.