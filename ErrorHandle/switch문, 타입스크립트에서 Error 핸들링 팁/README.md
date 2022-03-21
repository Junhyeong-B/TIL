# switch문, 타입스크립트에서 Error 핸들링 팁

- `throw new Error()` 형태의 에러 발생 코드를 통해 개발자에게 에러 발생 요소를 알려줄 수 있다.
- 다만, 코드를 실행한 다음 에러를 발생하기 때문에 경우에 따라 에러가 발생하지 않다가 배포 후에 발생할 수도 있고 에러 발생 타이밍이 한동작 늦어지게 된다.
- 타입스크립트 `never` 타입을 이용해 switch문에서의 에러를 **컴파일 단계**에서 확인할 수 있다.

```tsx
type Direction = "up" | "down" | "left" | "right";

function move(direction: Direction): void {
  switch (direction) {
    case "up":
      position.y += 1;
      break;
    case "down":
      position.y -= 1;
      break;
    case "left":
      position.x -= 1;
      break;
    case "right":
      position.x += 1;
      break;
    default:
      const invalid: never = direction;
      throw Error(`unknown direction ${invalid}`);
  }
}
```

- Union Type으로 지정한 모든 타입의 case가 처리된 후 default case로 들어오는 값은 never 타입이다.
- 만약 위 Direction 타입에 새로 합류한 개발자가 `'he'` 라는 타입을 추가했다면, default문에서 invalid 상수에 string 타입을 할당할 수 없다는 에러가 발생하게 되고, 개발자는 이를 컴파일 단계에서 확인할 수 있게 된다.