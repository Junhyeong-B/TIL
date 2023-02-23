# D3 심화

# 1. D3 기본

## 1-1) Selection

D3는 Selection 객체를 사용하고, select 메서드를 통해 querySelector 처럼 DOM 요소를 Selection 객체로 반환받아 D3 메서드를 통해 데이터를 시각화할 수 있다.

```html
// index.html
<div id="chart-area"></div>
```

```jsx
// main.js
const svg = d3
  .select("#chart-area")
  .append("svg")
  .attr("width", 400)
  .attr("height", 400);

svg
  .append("circle")
  .attr("cx", 200)
  .attr("cy", 200)
  .attr("r", 100)
  .attr("fill", "blue");
```

<div align="center">
  <img width="200" src="https://user-images.githubusercontent.com/85148549/211194944-e6a9f1a5-4f96-4363-89b5-5cef29585bd7.png" />
</div>

<br />

## 1.2) Data Join

`Selection.data().join()` 메서드를 통해 셀렉션 객체에 데이터를 바인딩하고, 데이터 조인할 수 있다.

```jsx
const data = [25, 20, 10, 12, 15];

const svg = d3
  .select("#chart-area")
  .append("svg")
  .attr("width", 400)
  .attr("height", 400);

const circles = svg.selectAll("circle");

circles
  .data(data)
  .join("circle")
  .attr("cx", (_, i) => 50 * i + 50)
  .attr("cy", 250)
  .attr("r", (d) => d)
  .attr("fill", "red");
```

<div align="center">
  <img width="400" src="https://user-images.githubusercontent.com/85148549/211194961-0c204dca-35f8-4825-bf4c-923c7854b94a.png" />
</div>

<br />

## 1.3) Scale (척도)

`d3.scaleLinear()`, `d3.scaleBand()`메서드를 통해 척도를 생성할 수 있다.(그 외 Log Scale, Time Scale, Ordinal Scale 등의 척도도 생성 가능하다.)

```jsx
// buildings.json
[
  {
    name: "Burj Khalifa",
    height: "350",
  },
  {
    name: "Shanghai Tower",
    height: "263.34",
  },
  {
    name: "Abraj Al-Bait Clock Tower",
    height: "254.04",
  },
  {
    name: "Ping An Finance Centre",
    height: "253.20",
  },
  {
    name: "Lotte World Tower",
    height: "230.16",
  },
  {
    name: "Testing Tower",
    height: "200.56",
  },
  {
    name: "Testing Centre",
    height: "181.24",
  },
];
```

```jsx
async function makeChart() {
  const data = await d3.json("data/buildings.json");

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.height)])
    .range([0, 300]);

  const x = d3
    .scaleBand()
    .domain(data.map((d) => d.name))
    .range([0, 200])
    .paddingInner(0.3)
    .paddingOuter(0.2);

  // ...

  svg
    .selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", (d) => x(d.name))
    .attr("y", 0)
    .attr("width", x.bandwidth)
    .attr("height", (d) => y(d.height))
    .attr("fill", "lightblue");
}

makeChart();
```

<div align="center">
  <img width="300" src="https://user-images.githubusercontent.com/85148549/211194960-915a564e-ad86-4b35-beec-46a6667c3007.png" />
</div>

<br />

## 1-4) 축 (Axis)

`d3.axisTop()`, `axisBottom()`, `axisLeft()`, `axisRight()` 메서드를 통해 d3에서 제공하는 축을 간단하게 만들 수 있다. 각 메서드들은 인자로 x, y 축 척도를 넘겨준다.

```jsx
const x = d3
  .scaleBand()
  .domain(data.map((d) => d.name))
  .range([0, WIDTH]);

// X Axis
const xAxis = d3.axisBottom(x);
g.append("g").call(xAxis);

const y = d3
  .scaleLinear()
  .domain([0, d3.max(data, (d) => d.height)])
  .range([HEIGHT, 0]);

// Y Axis
const yAxis = d3
  .axisLeft(y)
  .ticks(3)
  .tickFormat((d) => d + "m");
g.append("g").call(yAxis);
```

<div align="center">
  <img width="500" src="https://user-images.githubusercontent.com/85148549/211194959-a10fc88e-7783-49c0-b767-bbbf7b9164cf.png" />
</div>

<br />
<hr />

# 2. 데이터의 변화를 한 눈에 보여주는 방법

D3의 기본을 알고 있으면 D3 공식 홈페이지를 참고하여 대부분의 데이터를 시각화하는 것이 가능해 집니다. (단, 복잡한 인터랙션이 가능한 데이터는 추가적인 학습이 필요)

## 2-1) 데이터 구조 확인

- 국가들에 대한 정보, 연도가 담긴 배열이 있다고 가정
- 국가들에 대한 정보는 대륙, 국가명, 수입, 기대 수명, 인구 수 등의 정보가 있고, 배열의 길이는 약 200개이다.
- 연도는 1800 ~ 2014 까지 있다. (약 4만개의 정보가 있는 것.)

```json
// data.json
[
  {
    "countries": [
      {
        "continent": "africa",
        "country": "Congo, Rep.",
        "income": 576,
        "life_exp": 32.7,
        "population": 314465
      },
      {
        "continent": "asia",
        "country": "Vietnam",
        "income": 861,
        "life_exp": 32,
        "population": 6551000
      },
      {
        "continent": "asia",
        "country": "South Korea",
        "income": 575,
        "life_exp": 25.8,
        "population": 9395000
      }
      // ...
    ],
    "year": 1800
  },
  // ...
  {
    // ...
    "year": 2014
  }
]
```

<br />

## 2-2) 데이터 시각화 디자인

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194958-79ee344c-8a11-434b-b9ea-f2d291aebe6b.png" />
</div>

각 연도별 국가, 수입, 수명, 인구 수가 있는 데이터를 표현하고 싶은데 3가지 정보를 표현해야 하니 일반적으로 생각할 수 있는 Bar Chart는 적합하지 않습니다.

3개의 Bar를 붙이거나 각각의 정보별 차트를 나눠도 되지만, 국가가 약 200개 정도로 많다면 차트의 모양이 의도한대로 나오기 어렵습니다.

여기선 X축, Y축, 원의 크기 3가지로 차트를 그려줄 수 있는 Scatter Plot Chart로 결정하겠습니다.

<div align="center">
  <img width="500" src="https://user-images.githubusercontent.com/85148549/211194957-027d7ce1-dc9f-47e0-9830-cf6289d127a2.png" />
</div>

<br />

## 2-3) svg의 크기 상수 선언 및 svg 태그 생성하기

```jsx
const MARGIN = { LEFT: 100, TOP: 10, RIGHT: 10, BOTTOM: 100 };
const WIDTH = 960 - MARGIN.LEFT - MARGIN.RIGHT;
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM;

const svg = d3
  .select("#chart-area")
  .append("svg")
  .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
  .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM);

const g = svg
  .append("g")
  .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`);
```

- svg 태그는 가로 960px, 세로 500px를 갖고, 그 안에 있는 g 태그 내부에 차트를 그려줍니다.
- LEFT, BOTTOM 마진이 더 큰 것은 LEFT에 **Y축 Label**, BOTTOM에 **X축 Label**을 붙여줄 것이기에 미리 공간을 더 띄워 놓습니다.
- 이렇게 하면 차트가 그려질 g 태그는 margin left, top 만큼 translate 되어서 적절하게 공간을 활용할 수 있게 되고, 마진값을 제외한 WIDTH, HEIGHT 값을 유용하게 활용할 수 있습니다.

<br />

## 2-4) 척도 생성

```jsx
const x = d3.scaleLog().domain([142, 150000]).range([0, WIDTH]);
const y = d3.scaleLinear().domain([0, 90]).range([HEIGHT, 0]);
const area = d3.scaleLinear().domain([2000, 1400000000]).range([25, 1500]);
const continentColor = d3.scaleOrdinal(d3.schemePastel1);
```

- `d3.scaleLog()`: 로그 스케일 척도를 생성합니다. 여기서 input 값으로 기대되는 최소값, 최대값을 domain의 인자로 넘겨주는데, Log(0)은 정의되지 않은 값이므로 0보다 큰 값을 최소값으로 지정해야 합니다.(`domain([0, 100])` 형태로 넘겨주면 에러 발생)
  - X축이 나타내는 정보에 사용합니다.(income (GDP))
  - 선형 척도가 아닌 로그 스케일을 사용하는 이유는 최소, 최대값이 차이가 많이 나고, 특정 국가 및 연도에서 GDP의 급격한 변화가 있기 때문에 자연스러운 변화를 보여주기 위해 사용합니다.
- `d3.scaleLinear()`: 선형 척도를 생성합니다.
  - Y축이 나타내는 정보(life_exp) 및 원의 크기(population)에 사용합니다.
  - population는 연도별 변화는 크지 않아서 선형 척도를 사용하지만, 최소, 최대값 차이가 많이 나기에 `Math.sqrt()` 메서드를 활용하기 위해 일부러 값을 크게 생성합니다.
- `d3.scaleOrdinal()`: 지정된 범위와 영역을 갖는 서수 척도를 생성합니다.
  - 대륙 정보는 `asia`, `europe`, `americas`, `africa` 4개의 정보가 있는데, 각 대륙별로 색상을 다르게 가져가기 위해 사용합니다.
  - `d3.schemePastel1`은 d3에서 제공하는 색상 스키마입니다.
    - 그 외 Color Scheme 정보 - [https://observablehq.com/@d3/color-schemes](https://observablehq.com/@d3/color-schemes)

<br />

## 2-5) 축 생성

```jsx
const xAxis = d3.axisBottom(x).ticks(3).tickFormat(d3.format("$"));
g.append("g").attr("transform", `translate(0, ${HEIGHT})`).call(xAxis);

const yAxis = d3.axisLeft(y);
g.append("g").call(yAxis);
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194956-99275c57-f1c5-44f5-bfb5-d3827826582c.png" />
</div>

- x축을 그냥 사용하면 g태그에서의 좌표 (0, 0)(좌측 최상단)에 붙어버리기에 transform 속성을 통해 HEIGHT 만큼 아래로 내려줍니다.

<br />

## 2-6) 최초 하나의 데이터만 그리기

```jsx
d3.json("data/data.json").then((data) => {
  const formattedData = data.map((year) =>
    year.countries.filter((country) => country.income && country.life_exp)
  );

  g.selectAll("circle")
    .data(formattedData[0])
    .join("circle")
    .attr("cx", (d) => x(d.income))
    .attr("cy", (d) => y(d.life_exp))
    .attr("r", (d) => Math.sqrt(area(d.population)))
    .attr("fill", (d) => continentColor(d.continent));
});
```

- `d3.json` 메서드는 Promise 기반입니다. async, await 키워드와 함께 사용 가능합니다.
- data에서 income, life_exp 값이 없는 데이터도 존재하기 때문에 filter 함수로 제거해줍니다.
- `d3.data().join()` 함수로 데이터를 d3와 연결시키고, 각각을 익명 함수로 넘겨 척도를 활용해 시각화 합니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194954-a0728bc5-8fe5-49c0-8e77-43280eb06dbe.png" />
</div>

<br />

## 2.7) d3.interval / transition 를 이용해 데이터 변화 표현하기

```jsx
let time = 0;

d3.json("data/data.json").then((data) => {
  const formattedData = data.map((year) =>
    year.countries.filter((country) => country.income && country.life_exp)
  );
  const n = formattedData.length;

  const interval = d3.interval(() => {
    update(formattedData[time]);
    time++;
    if (time === n) {
      interval.stop();
    }
  }, 100);
});

function update(data) {
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("fill", (d) => continentColor(d.continent))
    .transition()
    .duration(100)
    .attr("cx", (d) => x(d.income))
    .attr("cy", (d) => y(d.life_exp))
    .attr("r", (d) => Math.sqrt(area(d.population)));
}
```

- 데이터를 그려주는 부분을 update 함수로 빼어 interval 내부에서 호출해줍니다.
- d3.interval은 setInterval과 매우 유사하게 동작하고, clearInterval 하기 위해선 `d3.interval()` 반환 값을 변수에 할당하고, `interval.stop()` 메서드를 사용하면 됩니다.

그런데 여기서 의도하지 않은 문제가 발생합니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194963-40858708-a814-4a48-99bf-036948b17b3c.gif" />
</div>

interval 내에서 update를 정상적으로 실행시키고 있지만, 데이터가 중구난방으로 마구 움직입니다.

<br />

## 2-8) Data Join 시 기준이 되는 데이터 값을 D3에 알려주기

- 문제의 원인은 D3가 Data Join 시 각각의 데이터를 이어지는 값으로 보는 것이 아니라 독립적인 값으로 해석하기 때문입니다.
- 예를 들어, 1800년 한국의 GDP: 576 → 1801년 한국의 GDP: 575 라고 한다면 기존의 576이라는 값에서 1 감소된 575로 보는 것이 아니라 1800년 576, 1801년 575 각각을 새로운 GDP 값으로 인식해서 transition 하는 동안 값이 계속 움직이는 것입니다.
- transition을 빼면 정상적인 것처럼 보이지만 각각의 데이터는 모두 새로운 데이터로 인식한 것이고, transition이 없으니 부자연스럽게 이어집니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194962-9c9b7afa-ffb6-4663-95d5-bbba26575680.gif" />
</div>

이를 해결하기 위해선 D3가 각각의 데이터를 그려줄 때 그 데이터가 동일한 값임을(위의 예제에서 한국임을) 알려주기 위해 기준이되는 값을 data의 두 번째 인자로 넘겨줍니다.

```jsx
g.selectAll("circle")
  .data(data, (d) => d.country)
  .join("circle")
  .attr("fill", (d) => continentColor(d.continent))
  .transition()
  .duration(100)
  .attr("cx", (d) => x(d.income))
  .attr("cy", (d) => y(d.life_exp))
  .attr("r", (d) => Math.sqrt(area(d.population)));
```

그러면 country를 기준으로 값의 변화를 정확하게 해석해서 데이터 변화를 시각화해줍니다. 한국 1800년 GDP: 576 > 1801년 GDP: 575 로 1 감소된 값으로 해석하고, 해당 값이 transition으로 변화할 때 576 > 575로 이동하게 됩니다.

<br />
<hr />

# 3. 코인 캔들 차트 만들어보기

코인 입출금 데이터들을 가지고 데이터 시각화하는 방법을 알아보기 위해 캔들이 있는 차트를 만들어 보겠습니다.

## 3-1) 데이터 구조 확인

```json
[
  {
    "time": 1671607800000,
    "open": 693.5,
    "high": 699.5,
    "low": 684.5,
    "close": 695.5,
    "volume": 105607.8043
  }
  // ...
]
```

여기서 각 값이 의미하는 것은 아래 그림과 같습니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194953-8d512b8c-43f4-4153-930a-1c7617f86a1a.png" />
</div>

<br />

## 3-2) svg의 크기 상수 선언 및 svg 태그 생성하기

```jsx
const MARGIN = { LEFT: 50, TOP: 50, RIGHT: 50, BOTTOM: 50 };
const WIDTH = window.innerWidth - MARGIN.LEFT - MARGIN.RIGHT;
const HEIGHT = window.innerHeight - MARGIN.TOP - MARGIN.BOTTOM;

const svg = d3
  .select("#chart-area")
  .append("svg")
  .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
  .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM);

const g = svg
  .append("g")
  .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`);
```

- 위의 예제와 같지만, 여기선 차트 크기를 최대로 활용하기 위해 window.innerHeight, innerWidth 값을 사용하겠습니다.
- 또 X축, Y축 라벨도 달지 않을 것이기 때문에 Top, Right, Bottom, Left 마진도 동일하게 설정했습니다.

<br />

## 3-3) 데이터 불러오기 / 데이터 값에 의거한 척도 생성

```jsx
async function makeChart() {
  const data = (await d3.json("data/data.json")).map((loadedData) => ({
    ...loadedData,
    time: new Date(loadedData.time),
  }));

  // 시간(x축) 최소, 최대
  const [xMin, xMax] = d3.extent(data, (d) => d.time);
  // 아래 두 줄을 작성한 것과 동일합니다.
  // const xMin = d3.min(data, (d) => d.time);
  // const xMax = d3.max(data, (d) => d.time);

  // 가격(y축) 값 최소, 최대
  const yMin = d3.min(data, (d) => d.low);
  const yMax = d3.max(data, (d) => d.high);

  // Scale
  const x = d3.scaleTime().domain([xMin, xMax]).range([0, WIDTH]);
  const y = d3.scaleLinear().domain([yMin, yMax]).range([HEIGHT, 0]);
}
```

- 여기선 Promise 대신 async, await를 사용해보겠습니다.
- X축에 시간 척도(`scaleTime()`) 를 사용할 수 있으므로 time 값을 Date 객체로 변환(`Array.map`)해 줍니다.
- `d3.min`, `d3.max` 로 데이터 중 최소, 최대값을 구할 수도 있고, `d3.extent` 메서드를 통해 한 번에 [min, max] 값을 구할 수도 있습니다.
  - d3.min, d3.max는 Date 객체에 대해서도 최소(가장 과거), 최대(가장 미래)값을 구할 수 있습니다.

<br />

## 3-4) 축 생성

```jsx
// Axis
const xAxis = d3.axisBottom(x);
g.append("g").attr("transform", `translate(0, ${HEIGHT})`).call(xAxis);

const yAxis = d3.axisRight(y);
g.append("g").attr("transform", `translate(${WIDTH}, 0)`).call(yAxis);
```

- 생성한 척도를 인자로 넘겨준 후 g태그를 append하여 call 메서드를 통해 축을 생성해줍니다.
- 축은 append하려는 g 태그의 (0, 0) 좌상단에 위치하게 되므로, 적절하게 Transform 시켜줍니다.

<br />

## 3-5) open, close 캔들 만들기

```jsx
// Rect
const barWidth = WIDTH / data.length - 0.5;
const rects = g.append("g").selectAll("rect").data(data);
rects
  .join("rect")
  .attr("x", (d) => x(d.time))
  .attr("y", (d) => y(d.open > d.close ? d.open : d.close))
  .attr("width", barWidth)
  .attr("height", (d) => Math.abs(y(d.open) - y(d.close)))
  .attr("fill", (d) => (d.open - d.close > 0 ? "#ff4e4e" : "#4ffb9c"));
```

- 여태까지 사용했던대로 `d3.data().join()` 메서드로 데이터를 조인한 후 Rect 태그를 그려줍니다.
- Rect 태그를 그리면 height 값만큼 시작지점 y 속성으로부터 아래로 height만큼 그려지므로 open값 또는 close값 중 더 큰 값을 기준으로 y 속성을 부여해줍니다.
  - **height 값이 음수이면 rect 태그가 그려지지 않아**서 Open을 기준으로 잡고 양수, 음수에 따라 그래프를 그리는 것은 불가능합니다. 따라서 open 또는 close 값 중 더 높은 값을 기준으로 Rect 태그를 그려줍니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194951-792b04fe-699c-4e3c-95bb-01fa7164e94d.png" />
</div>

<hr />

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194949-3d172d24-8b71-49cd-a7f5-5df3c058bcbc.png" />
</div>

<br />

## 3-6) low, high 선 만들기

```jsx
// Line (Small Rect)
const lines = g.append("g").selectAll("rect").data(data);
const lineWidth = barWidth / 4;
const offset = (3 / 2) * lineWidth;
lines
  .join("rect")
  .attr("x", (d) => x(d.time) + offset)
  .attr("y", (d) => y(d.high))
  .attr("width", lineWidth)
  .attr("height", (d) => y(d.low) - y(d.high))
  .attr("fill", (d) => (d.open - d.close > 0 ? "#ff4e4e" : "#4ffb9c"));
```

- `d3.line()` 메서드가 있지만, `d3.line()` 메서드는 HTML path 태그의 d 속성에 부여하는 path를 반환하거나, `d3.line()([x1, y1], [x2, y2])` 형태로 넘겨줘야 하는데, 그러기엔 메서드가 중첩되어 보기 좋지 않습니다.
- 그래서 캔들의 width보다 작은 width를 갖는 Rect 태그를 만들면 Line처럼 보이게되니 크기가 더 작은 Rect 태그를 만드는 것으로 작업했습니다.
- 해당 선의 크기는 Bar Width 의 1 / 4 크기만큼 차지하도록 지정하고, x의 위치를 line width의 크기를 고려하여 옆으로 이동시켜 줍니다.(offset)

<div align="center">
  <img width="700" src="https://user-images.githubusercontent.com/85148549/211194948-81375630-2ddd-4fa3-b6a6-d39d52c77833.png" />
</div>

<br />

## 3-7) 이동평균선 만들기

- 여기까지만 해도 차트는 만들어졌지만, 그 외에 이동평균선이나 거래량 등을 차트에 넣어보겠습니다.

```jsx
function getMovingAverageData(data, average) {
  return data.map((row, index, total) => {
    const start = Math.max(0, index - average);
    const end = index;
    const subset = total.slice(start, end + 1);
    const sum = subset.reduce((a, b) => a + b.close, 0);
    return {
      time: row.time,
      average: sum / subset.length,
    };
  });
}

// Moving Average
const average20 = getMovingAverageData(data, 20);
const average50 = getMovingAverageData(data, 50);
const averageLine = d3
  .line()
  .x((d) => x(d.time))
  .y((d) => y(d.average));

g.append("path")
  .attr("fill", "none")
  .attr("stroke", "#FFFBEB")
  .attr("stroke-width", 1)
  .attr("d", averageLine(average20));
g.append("path")
  .attr("fill", "none")
  .attr("stroke", "#F56EB3")
  .attr("stroke-width", 1)
  .attr("d", averageLine(average50));
```

- close 값을 기준으로 이동평균선을 구성했습니다.
- `d3.line()` 태그는 함수처럼 활용이 가능하고, 여기에 data를 인자로 넘겨주면 해당 data에 따라 path를 그려줍니다.

```jsx
console.log(averageLine(data)); // M0,375.19213882L1,...
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194946-d7037cb0-8dd8-4b0c-9ae2-81e45bcf289d.png" />
</div>

<br />

## 3-8) 거래량 차트 만들기

```jsx
// Scale
const y = d3
  .scaleLinear()
  .domain([yMin - 80, yMax]) // 기존 척도에서 아래 80px만큼 여유 공간을 줍니다.
  .range([HEIGHT, 0]);
// ...

// Volume
const yVolume = d3
  .scaleLog()
  .domain(d3.extent(data, (d) => d.volume))
  .range([100, 0]);

g.append("g")
  .selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", (d) => x(d.time))
  .attr("y", (d) => HEIGHT - yVolume(d.volume))
  .attr("width", barWidth)
  .attr("height", (d) => yVolume(d.volume))
  .attr("fill", (d, i) => {
    if (i === 0) {
      return "rgb(143 45 45)";
    } else {
      return data[i - 1].volume < d.volume
        ? "rgb(143 45 45)"
        : "rgb(45 160 97)";
    }
  });
```

- 거래량 편차가 크기때문에 새로운 volume 용 척도를 scaleLog 메서드를 통해 로그 척도로 만들고, 아래에 새로 그려줍니다.
- 새로운 내용 없이 캔들 추가하는 것처럼 추가해줬습니다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/211194945-f0d0ce3f-d379-4964-a9b1-15e3f96ff678.png" />
</div>

<br />
<hr />

# 참조

- [https://www.geeksforgeeks.org/](https://www.geeksforgeeks.org/)
- [https://observablehq.com/@d3](https://observablehq.com/@d3)
- [https://observablehq.com/@d3/d3-line](https://observablehq.com/@d3/d3-line)
- [https://benclinkinbeard.com/d3tips/make-any-chart-responsive-with-one-function/](https://benclinkinbeard.com/d3tips/make-any-chart-responsive-with-one-function/)
