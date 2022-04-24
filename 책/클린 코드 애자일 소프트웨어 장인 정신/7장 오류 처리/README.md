# 7장 오류 처리

# 1. 오류 코드보다 예외

예외를 지원하지 않는 프로그래밍 언어가 많았는데, 그런 언어에서는 오류 플래그를 설정하거나 오류 코드를 반환하는 방식으로 오류를 처리했다. 어떤 상태이냐에 따라 조건문을 통해 특정 상태에서는 특정 오류코드를 반환하는 방식인데, 호출자 코드가 복잡해지기 때문에 예외를 지원하는 언어에서는 예외를 던지는 편이 호출자 코드가 훨씬 깔끔해진다.

```java
/**
 * 오류 코드를 반환하는 방식
 */
public void sendShutDown() {
	DeviceHandle handle = getHandle(DEV1);
	if (handle != DeviceHandle.INVALID) {
		retrieveDeviceRecord(handle);
	}
}
```

```java
/**
 * 예외를 던지는 방식
 */
public void sendShutDown() {
	try {
		tryToShutDown();
	} catch (DeviceShutDownError e) {
		logger.log(e);
	}

	private void tryToShutDown() throws DeviceShutDownError {}
}
```

예외를 던지는 방식으로 코드를 작성하게 되면 코드가 깔끔해진 것뿐만 아니라 함수 종료와 오류 처리를 분리했기 때문에 코드 품질도 나아진다.

<br />

# 2. Try-Catch

try-catch 문을 사용하면 try 블록에 들어가는 코드를 실행했을 때 어느 시점에서든 실행이 중단된 후 catch문으로 넘어갈 수 있다. try 블록에서 무슨 일이 생기든지 호출자가 기대하는 상태를 정의하기 쉬워진다.

```java
public List<RecordedGrip> retrieveSection(String sectionName) {
	try {
		FileInputStream stream = new FileInputStream(sectionName);
		stream.close();
	} catch (Exception e) {
		throw new StorageException("retrieval error", e);
	}

	return new ArrayList<RecordedGrip>();
}
```

위 코드에서는 try-catch로 범위를 정의한 코드다. 여기서 추가적으로 테스트를 진행하고 싶다면 stream 정의와 close() 함수 사이에 코드를 추가하되 오류가 발생하지 않는다고 가정하여 코드를 작성한다.

<br />

# 3. 예외에 의미를 제공하기

예외를 던질 때는 전후 상황을 충분히 고려하여 오류 메세지에 정보를 담아 덧붙인다. 그렇게 하면 오류가 발생한 원인과 위치를 찾기가 쉬워진다.

<br />

# 4. null을 반환하거나 전달하지 않기

오류를 처리할 때 null을 반환한다면 한줄 건너 하나씩 null을 확인하는 코드가 계속 작성될 것이다. null을 확인하는 코드가 많아진 것이 왜 좋지 못하냐면 일거리를 늘릴뿐만 아니라 누구하나 null 확인을 깜빡한다면 어플리케이션을 통제하기 어려워질 수 있다.

```java
/**
 * 이것은 좋지 못한 코드다.
 */
public void registerItem(Item item) {
	if (item != null) {
		// ...
		if (registry != null {
			// ...
		}
	}
}
```

<br />

그래서 null을 반환하여 처리하고 싶은 오류가 있다면 대신 예외를 던지거나 특수 사례 객체를 반환하여 처리하는 방식이 더 나은 코드가 될 수 있다.

null을 전달하는 방식도 좋지 않다. 정상적인 인수로 null을 기대한다면 사용할 수는 있겠지만, 그게 아니라면 의도하지 않은 에러나 예외가 발생할 수 있다.

<br />

# 5. 정리

깨끗한 코드는 읽기도 좋아야 하지만 안정성도 높아야 한다. 이번 장에서 중요하게 생각되는 부분은 비즈니스 논리와 오류 처리 코드의 분리이다. 이를 적절히 분리하여 에러를 처리한다면 에러 핸들링하기도 비교적 쉬워질 것이고 코드도 깔끔해질것이라고 생각한다.