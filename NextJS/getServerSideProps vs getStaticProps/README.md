# getServerSideProps vs getStaticProps

# 1. CSR(Client Side Rendering)의 단점

- CSR(Client Side Rendering)형태의 SPA(Single Page Application) 페이지는 코드 스플리팅 작업이 되어 있지 않고, 빌드 시 번들링이 진행된다면 최초 페이지 진입 시 모든 Javascript 파일을 로드하여 진입 시 로딩 시간이 프로젝트 크기에 비례하여 늘어난다.
- 또한, 모든 요소들을 Client Side에서 생성하기 때문에 로딩되는 HTML은 비어있고, Javascript 파일의 로드가 완료되면 동적으로 컨텐츠를 보여준다.
- 이는 SEO(Search Engine Optimization) 측면에서 불리하다. ⇒ 아무런 내용이 없어 검색 엔진으로부터 어떤 웹페이지인지 정보를 주기 어렵기 때문.

<br />

### 이를 해결하기 위한 Next JS에서의 함수?

- Next JS에서는 `getServerSideProps`, `getStaticProps` 함수를 이용하여 페이지를 pre-render하여 해당 함수 내부의 로직을 실행한 후 props로 반환문을 전달해줄 수 있다.
- 두 가지 함수의 차이를 알아보자

<br />

# 2. getServerSideProps

- 해당 함수를 사용하면 각 페이지의 request 시 호출되어 데이터를 서버로부터 가져와 반환한다.

<br />

### 2-1) 동작 순서

1. Page Request 시 getServerSideProps가 호출된다.
2. 해당 페이지는 getServerSideProps 함수 로직에 의해 pre-rendered되어 props를 반환한다.
3. 만약, NextJS에서 제공하는 route, link 등의 기능을 통해 페이지 이동 시 Next.js에서 해당 페이지에 존재하는 getServerSideProps를 server에 요청하여 동작시킨다.

<br />

### 2-2) 기본 구조

```jsx
export async function getServerSideProps(context) {
  return {
    props: {}, // will be passed to the page component as props
  }
}
```

<br />

### 2-3) 특징

- 빌드와 상관 없이 페이지 요청시마다 동작한다.
- Server Side에서만 동작하며, 브라우저에서는 동작하지 않는다.
- JSON을 반환한다.
- page 파일에서만 사용할 수 있고, non-page 파일에서는 동작하지 않는다.(non-page 파일에서는 export 할 수 없다.)

<br />

### 2-4) 그럼 언제 사용해야 할까?

- 페이지 요청 시 서버로부터 Data를 fetch하여 page를 pre-render하고 싶을 때 사용한다.
- getStaticProps에 비해 요청에서부터 응답까지의 시간이 더 길다.
    - getServerSideProps는 Page 요청시마다 동작하고, cache-control에 의해서만 캐싱할 수 있는데, 추가 구성이 필요하기 때문이다.
- 만약, pre-render할 필요 없는 Data라면 client side에서 Data를 fetch하여 사용하길 권장하고 있다.

<br />

### 2-5) 만약 getServerSideProps 내부에서 fetch할 때 에러가 발생한다면?

- pre-render를 위해 getServerSideProps를 사용했는데, fetch할 때(또는 `throw new Error` 등 에러가 발생하면) 에러가 발생하면 `pages/500.js` 페이지를 보여준다.
- `pages/500.js`는 추가적인 파일을 추가하지 않아도 Next.js에서 기본으로 제공해주는 페이지이다.
    - 물론 파일을 생성하여 Customizing할 수 있다.

<br />

# 3. getStaticProps

- 해당 함수를 사용하면 빌드할 때 호출되어 데이터를 서버로부터 가져와 반환한다.

<br />

### 3-1) 동작 순서

1. Build Time 시 동작하여 Data를 서버로부터 가져온다.
2. 해당 페이지는 getStaticProps 함수 로직에 의해 pre-rendered되어 props를 반환한다.

<br />

### 3-1-1) revalidate prop 작성 시 동작 순서

1. Build Time 시 동작하여 Data를 서버로부터 가져온다.
2. 해당 페이지는 getStaticProps 함수 로직에 의해 pre-rendered되어 props를 반환한다.
3. 생성된 페이지는 캐시된다.
4. revalidate에 작성한 number seconds만큼 흐른 뒤 Next.js는 해당 페이지를 background에서 재생성한다.
5. 만약 생성에 실패했다면 기존 캐시된 페이지를 그대로 사용하고, 새로운 페이지를 재생성했다면 캐시된 페이지를 무효화하고 생성된 페이지로 update한 후 보여준다.
6. 3~5 까지의 작업이 revalidate seconds마다 반복된다.

<br />

### 3-2) 기본 구조

```jsx
export async function getStaticProps(context) {
  return {
    props: {}, // will be passed to the page component as props
  }
}
```

<br />

### 3-3) 특징

- 빌드할 때 호출되고 Server Side에서만 동작한다. 브라우저에서는 동작하지 않는다.
- JSON을 반환한다.
- 반환하는 JSON에 revalidate prop을 추가하여 Number를 작성해주면 해당 Number마다 페이지는 재생성된다.
    
    ```jsx
    export async function getStaticProps() {
      return {
        props: {
        },
        // Next.js will attempt to re-generate the page:
        // - When a request comes in
        // - At most once every 10 seconds
        revalidate: 10, // In seconds
      }
    }
    ```
    
- 페이지 전환시에는 동작하지 않는다.
- getStaticProps에 의해 생성된 HTML, JSON 파일들은 CDN에 캐시되고, 상대적으로 빠르다.

<br />

### 3-4) 그럼 언제 사용해야 할까?

- Build할 때 페이지를 pre-render 해야 하고, 해당 Data를 가지고 rendering할 수  있으면 사용한다.
- 최초 Data Fetch 이후 데이터의 변동이 없다면 해당 데이터를 캐시하여 사용하므로 성능 측면에서 유리하다.

<br />

# 4. 비교

- getServerSideProps는 페이지 전환 시마다 동작한다.(page Request)
- getStaticProps는 Build 시에 동작한다. 추가 prop을 지정해줘서 해당 시간이 흐른 뒤 Background에서 Page를 재생성되게 만들 수 있다.
- 페이지에서 사용해야하는 데이터가 동적으로 계속 변한다면 getServerSideProps를 사용하고, 변하지 않는다면 getStaticProps를 사용하는 것이 더 유리하다.