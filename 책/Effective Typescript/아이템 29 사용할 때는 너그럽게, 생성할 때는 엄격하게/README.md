# item 29 사용할 때는 너그럽게, 생성할 때는 엄격하게

- 함수의 매개변수는 타입의 범위가 넓어도 되지만, 결과를 반환할 때는 일반적으로 타입의 범위가 더 구체적이어야 한다.

<br />

## 1. 자유로운 타입을 가지는 카메라 위치 지정 함수만들기

```tsx
declare function viewportForBounds(bounds: LngLatBounds): CameraOptions;
declare function setCamera(camera: CameraOptions): void;
```

- 여기서 viewportForBounds의 결과가 setCamera로 바로 전달될 수 있다면 편리할 것이다.

<br />

```tsx
type LngLat =
	{ lng: number; lat: number; } |
	{ lon: number; lat: number; } |
	[number, number];

interface CameraOptions {
	center?: LngLat;
	zoom?: number;
	bearing?: number;
	pitch?: number;
}

type LngLatBounds =
	{ northeast: LngLat, southwest: LngLat } |
	[LngLat, LngLat] |
	[number, number, number, number];
```

- `CameraOptions`는 독립적으로 값을 설정할 수 있어야 하므로 모든 필드가 선택적이다.
- `LngLat`은 setCamera의 매개변수 범위를 넓혀주는데, `{lng, lat}`, `{Ion, lat}`, `[Ing, lat]` 을 모두 넣을 수 있기 때문에 함수 호출을 쉽게 할 수 있다.
- `LanLatBounds`는 위도/경도 쌍, 4-튜플을 사용하여 경계를 지정할 수 있어서 19가지 이상의 형태가 가능한 자유로운 타입이다.

<br />

```tsx
function focusOnFeature(f: Feature) {
  const bounds = calculateBoundingBox(f);
  const camera = viewportForBounds(bounds);
  setCamera(camera);
  const {center: {lat, Ing}, zoom} = camera;
								// ~      ... 형식에 'lat' 속성이 없습니다.
								//      ~ ... 형식에 'lng' 속성이 없습니다.
  zoom;  // 타입이 number | undefined
  window.location.search = `?v=@${lat},${lng}z${zoom}`;
}
```

여기서 오류는 카메라에 `lat`과 `lng` 속성이 없고 `zoom` 속성만 존재하기 때문에 발생했지만, 타입이 `number` | `undefined`로 추론되는 것 역시 문제다.

`camera` 값을 안전한 타입으로 사용하는 유일한 방법은 유니온 타입의 각 요소별 코드를 분기하는 것이다.

`viewportForBounds`의 매개변수 타입, 반환 타입 모두 자유로운데, 매개변수 타입의 범위가 넓으면 사용하기 편리하지만, 반환 타입의 범위가 넓으면 불편하다.

<br />

## 2. 반환 타입이 엄격한 함수로 변경하기

```tsx
interface LngLat {
  lng: number;
  lat: number;
}

type LngLatLike = LngLat | { Ion: number; lat: number } | [number, number];

interface Camera {
  center: LngLat;
  zoom: number;
  bearing: number;
  pitch: number;
}

interface CameraOptions extends Omit<Partial<Camera>, "center"> {
  center?: LngLatLike;
}

type LngLatBounds =
  | { northeast: LngLatLike; southwest: LngLatLike }
  | [LngLatLike, LngLatLike]
  | [number, number, number, number];

declare function setCamera(camera: CameraOptions): void;
declare function viewportForBounds(bounds: LngLatBounds): Camera;
```

- 여기서 `Camera` 타입은 엄격하다.
- 조건을 완화하는 `CameraOptions`를 따로 작성했다.

<br />

```tsx
function focusOnFeature(f: Feature) {
	const bounds = calculateBoundingBox(f);
	const camera = viewportForBounds(bounds);
	setCamera(camera);
	const {center: {lat, lng}, zoom} = camera; // 정상
	zoom; // 타입이 number
	window.location.search = `?v=@${lat},${lng}z${zoom}`;
}
```

- 이제 camera에 center가 `LanLat` 타입이므로 lat, lan 값이 존재하고, zoom 타입도 `number`이다.
- 이제 `viewportForBounds` 함수를 사용하기 훨씬 쉬워졌다.

<br />

## 요약

- 보통 매개변수 타입은 반환 타입에 비해 범위가 넓은 경향이 있다. 어쩔 수 없이 다양한 타입을 허용해야 하는 경우가 생기지만 반환 타입이 넓다면 나쁜 설계라는 사실을 잊어서는 안된다.
- 매개변수와 반환 타입의 재사용을 위해서 기본 형태(반환 타입)와 느슨한 형태(매개변수 타입)를 도입하는 것이 좋다.