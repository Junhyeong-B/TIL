# 6장 객체와 자료구조

# 1. 구체적인 자료와 추상화된 자료

변수를 비공개(private)로 정의하는 이유는 변수를 은닉하여 특정 액션에 의해서만 데이터를 조작하기 위해 사용한다. 

```java
public class Point {
	public double x;
	public double y;
}
```

위와 같이 작성된 `Point class`는 Point를 사용하는 쪽에서 자료의 형태를 확인할 수 있다. 외부에서 내부 변수를 조회할 수 있다는 말이다.

<br />

```java
public interface Point {
	double getX();
	double getY();
	void setCartesian(double x, double y);
	double getR();
	double getTheta();
	void setPolar(double r, double theta);
}
```

위와 같이 작성된 `Point interface`는 내부 변수가 어떻게 이루어져 있는지 알 수 없다. Point 이름을 통해 좌표인 것을 예측할 수는 있으나 직교 좌표계인지, 극좌표계인지 알 수가 없다. 이런식으로 사용자가 구현을 모른 채 자료의 핵심을 조작할 수 있는 자료 형태가 구현을 외부로 노출하는 자료 형태보다 낫다.

<br />

# 2. 자료/객체 비대칭

- **객체**: 내부 변수를 숨기고(은닉) 해당 변수들을 다루는 함수만 외부로 공개한다.
- **자료 구조**: 자료(객체에서의 내부 변수)를 그대로 노출하고 그 외의 함수는 제공하지 않는다.

<br />

### 2-1) 절차적인 도형

```java
public class Square {
  public double side;
}

public class Rectangle {
  public double height;
	public double width;
}

public class Geometry {
	public double area(Object shape) throws NoSuchShapeException
	{
		if (shape instanceof Square) {
			Square s = (Square)shape;
			return s.side * s.side;
		}
		else if (shape instanceof Rectangle) {
			Rectangle r = (Rectangle)shape;
			return r.height * r.width;
		}
	}
}
```

위 구조는 절차 지향적이다. 만약 Geometry 클래스에 둘레 길이를 구하는 함수를 추가하고 싶다면 그냥 추가하면 된다. Geometry 클래스는 아무런 영향도 받지 않는다. 다만, 새로운 도형을 추가한다면 area 내부에 새로운 도형에 대한 로직을 추가해야 하고, 만약 새롭게 추가된 함수가 100개라면 100개의 코드에 전부 추가해줘야 한다.

<br />

### 2-2) 다형적인 도형

```java
public class Square implements Shape {
	private double side;
	
	public double area() {
		return side * side;
	}
}

public class Rectangle implements Shape {
	private double height;
	private double width;
	
	public double area() {
		return height * width;
	}
}
```

위 구조는 객체 지향적이다. 여기서 area는 다형(polymorphic) 메서드인데, 새 도형을 추가하더라도 area는 아무런 영향을 받지 않는다. 다만, 새로운 함수를 추가하고 싶다면 각각의 도형에 새로운 함수를 추가해주어야 한다.

- 자료 구조를 사용하는 절차적인 코드는 기존 자료 구조를 변경하지 않으면서 새 함수를 추가하기 쉽고, 새로운 자료 구조를 추가하기 어렵다.
- 객체를 사용하는 객체지향 코드는 기존 함수를 변경하지 않으면서 새 클래스를 추가하기 쉽고, 새로운 함수를 추가하기 어렵다.

<br />

# 3. 디미터 법칙

- 디미터 법칙: 모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다는 법칙

<br />

```java
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
```

이 코드는 디미터 법칙을 어기는(것 처럼 보이는) 코드이다. 이러한 코드를 기차 충돌(Train Wreck)이라고 부른다. 기차 충돌은 일반적으로 조잡한 것처럼 보여서 그대로 작성하는 것이 아니라 아래처럼 나누어서 작성하는 편이 더 좋다.

<br />

```java
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

그런데 아래 코드와 같이 나누어서 코드를 작성했다 하더라도 opts, scartchDir, outputDir이 객체라면 내부 구조를 숨겨야 하므로 디미터 법칙을 위반한 것이고, 자료 구조라면 그 특성으로 인해 디미터 법칙이 적용되지 않는다.

<br />

만약 객체라면 체이닝하여 메서드를 호출하는 것이 아니라 내부 구조를 감춰야 하니까 해당 코드가 어떤 역할을 할지 생각하고 절적히 메서드를 부여해야 한다. 위 코드가 임시 파일을 생성하려는 목적이었다고 가정하면 아래와 같이 작성했을 때 내부 구조를 드러내지 않으면서 해당 함수는 몰라야 하는 여러 객체를 탐색할 필요가 없다.

```java
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

<br />

# 4. 자료 전달 객체(자료 구조체)

자료 구조체는 공개 변수만 있고 함수가 없는 클래스다. 이는 데이터베이스에 저장된 정보를 어플리케이션 코드에서 사용할 객체로 변환하는 일련의 단계에서 가장 처음으로 사용하는 구조체이다.

<br />

# 5. 정리

- 객체: 동작을 공개하고 자료를 숨긴다.
- 자료 구조: 자료를 공개하고 별다른 동작을 제공하지 않는다.

위의 특성에 따라 어플리케이션을 구축할 때 새로운 자료 타입을 추가하고 싶으면 객체가 더 적합하고, 새로운 동작을 추가하고 싶으면 자료 구조가 더 적합하다.