# 8장 경계

# 1. 외부 코드 사용하기

- 프로젝트를 진행하다 보면 모든 기능을 직접 개발하기 보다는 패키지를 구매하거나 오픈 소스를 적절히 이용한다.
- 인터페이스 제공자는 적용성을 최대한 넓히려 애쓰지만, 사용자는 자신의 요구에 집중하는 인터페이스를 바라는 특성으로 시스템 경계에 문제가 생길 우려가 커진다.

<br />

### 1-1) 자바스크립트의 Map

- 자바스크립트에서의 Map은 몇 가지의 기능을 제공하는데, `Map.prototype` 키워드로 특정 메서드를 추가할 수도 있다.

<br />

```jsx
const sensor = new Map();

const sensorId = 1;
const s = sensor.get(sensorId);
```

- 위 코드는 Map을 사용하여 특정 반환 값을 변수 s에 할당하는 코드이다. 이 경우 Map이 반환하는 객체를 올바른 유형으로 변환할 책임이 클라이언트에 있다.

<br />

```jsx
class Sensor {
	constructor() {
		this.sensor = new Map();
	}

	getById(sensorId) {
		return this.sensor.get(sensorId);
	}
}
```

- 위와 같이 작성하면, 클라이언트 쪽에서 Map 사용 여부에 신경을 쓸 필요가 없어진다.
- 그냥 s 변수에 할당하여 사용하는 코드보다 상대적으로 깨끗한 코드라고 볼 수 있다.
- Map의 인터페이스(또는 패키지 인터페이스)가 변하더라도 위와 같이 작성하면 나머지 프로그램에는 영향을 미치지 않는다.

<br />

# 2. 경계 살피고 익히기

- 외부 코드를 사용하면 적은 시간으로 더 많은 기능을 출시하기 쉬워진다.
- 하지만, 사용하는 측에서 사용할 외부 코드를 테스트하는 것이 바람직하다.
    - 특정 라이브러리를 가져와서 사용할 경우 일정시간 이상 지나면 그 라이브러리를 이해하여 프로젝트에 적용할 수 있다.
    - 이 때 버그가 발생하면 그것이 라이브러리 버그인지, 프로젝트의 버그인지 찾아내기 어려워지기 때문이다.
- 라이브러리를 곧바로 우리쪽 코드에 작성해 외부 코드를 호출하는 대신 먼저 간단한 테스트 케이스를 작성해 외부 코드를 익히는 것을 짐 뉴커스는 **학습 테스트**라고 불렀다.

<br />

# 3. 학습 테스트는 공짜 이상

- 학습 테스트를 하기 위해선 어쨌든 API를 배워야 하므로 학습 테스트에 드는 비용은 없다.
- 새 버전이 나온다면 학습 테스트를 돌려 차이가 있는지 확인하는 등 공짜 이상의 성과를 낼 수 있다.
- 학습 테스트를 사용하기 시작하면 새 버전으로 이전하기 쉬워진다. 그렇지 않다면 낡은 버전을 필요 이상으로 오랫동안 사용하기 쉬워진다.

<br />

# 4. 깨끗한 경계

- 소프트웨어 설계가 우수하다면 변경하는데 많은 재작업이 필요하지 않다.
- 통제하지 못하는 코드는 변경에 너무 많은 투자를 하거나 변경 비용이 지나치게 커질 수 있다.
- 위와 같은 문제에 당면하지 않기 위해 경계에 위치하는 코드는 깔끔히 분리한다.
    - 통제가 불가능한 외부 패키지에 의존하는 대신 통제가 가능한 우리 코드에 의존하는 것이 훨씬 좋다.
    - 외부 패키지에 의존하게 되면 외부 코드에 휘둘리게 된다.
- 외부 패키지를 호출하는 코드를 가능한 줄여 경계를 관리하자.