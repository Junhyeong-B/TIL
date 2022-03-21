# 21장 백엔드 프로그래밍: Node.js의 Koa 프레임워크

## 21.1.2 Node.js

- 처음엔 자바스크립트를 웹 브라우저에서만 사용했다.
- 그러다 구글이 크롬 웹 브라우저를 소개하면서 V8 자바스크립트 엔진을 공개했다.
- 이러한 자바스크립트 엔진을 기반으로 웹 브라우저뿐만 아니라 서버에서도 자바스크립트를 사용할 수 있는 런타임을 개발했는데, 그것이 Node.js이다.

<br />

## 21.1.3 Koa

- Koa는 Express의 개발 팀이 개발한 프레임워크다.
- Express는 미들웨어, 라우팅, 템플릿, 파일 호스팅 등의 기능이 자체적으로 내장되어 있지만,
    
    Koa는 미들웨어 기능만 갖추고 있으며 나머지는 다른 라이브러리를 적용하여 사용한다.
    
- Koa는 async / await 문법을 정식 지원한다.

<br />

# 21.3 Koa 기본 사용법

## 21.3.1 서버 띄우기

- `src/index.js`

```jsx
const Koa = require('koa');

const app = new Koa();

app.use((ctx) => {
  ctx.body = 'hello world';
});

app.listen(4000, () => {
  console.log('Liistening to port 4000');
});
```

- app.listen을 통해 서버를 포트 4000번으로 열고,
    
    ctx.body에 문자열을 할당하여 해당 포트로 접속하면 `'hello world'` 텍스트가 보인다.
    
- 서버 실행 방법은 다음과 같다.(src 폴더의 index.js이므로 index.js는 생략한다.)

```jsx
$node src
```

<br />

## 21.3.2 미들웨어

- new Koa().use 함수는 미들웨어 함수를 어플리케이션에 등록한다.
- 미들웨어 함수는 다음과 같은 구조로 이루어져있다.

```jsx
(ctx, next) => {}
```

- **ctx(Context)**: 웹 요청과 응답에 관한 정보
- **next**: 현재 처리 중인 미들웨어의 다음 미들웨어를 호출하는 함수
- 미들웨어는 app.use를 사용하여 등록하는 순서대로 처리된다.

```jsx
const Koa = require('koa');

const app = new Koa();

app.use((ctx, next) => {
  console.log(ctx.url);
  console.log(1);
  next();
});

app.use((ctx, next) => {
  console.log(2);
  next();
});

app.use((ctx) => {
  ctx.body = 'hello world';
});

app.listen(4000, () => {
  console.log('Liistening to port 4000');
});
```

```jsx
>	$node src
Liistening to port 4000
/
1
2
/favicon.ico
1
2
```

- /favicon.ico가 한번 더 나타나는 이유는 사용자가 웹 페이지에 들어가면 크롬 브라우저가 해당 사이트의 아이콘 파일인 /favicon.ico 파일을 서버에 요청하기 때문에 나타난다.
- next를 호출하지 않으면 다음 미들웨어를 실행하지 않으니 조건에 따라 미들웨어를 호출할지 안할지를 지정할 수 있다.

<br />

## 21.3.2.1 next 함수는 Promise를 반환

- next 함수는 Promise를 반환하는데, 이는 다음에 처리해야 할 미들웨어가 끝나야 완료된다.

```jsx
app.use((ctx, next) => {
  console.log(ctx.url);
  console.log(1);
  next().then(() => {
    console.log('END');
  });
});

app.use((ctx, next) => {
  console.log(2);
  next();
});

app.use((ctx) => {
  ctx.body = 'hello world';
});
```

```jsx
>	$node src
Liistening to port 4000
/
1
2
END
```

<br />

## 21.3.2.2 async / await 사용하기

- Koa에서는 async / await를 정식으로 지원해서 편하게 사용할 수 있다.
- Express의 경우 오류를 처리하는 부분이 제대로 작동하지 않을 수 있어 이를 해결하려면 express-async-errors라는 라이브러리를 따로 사용해야 한다.

```jsx
app.use(async (ctx, next) => {
  console.log(ctx.url);
  console.log(1);
  await next();
  console.log('END');
});

app.use((ctx, next) => {
  console.log(2);
  next();
});

app.use((ctx) => {
  ctx.body = 'hello world';
});
```

```jsx
>	$node src
Liistening to port 4000
/
1
2
END
```

<br />

# 21.4 nodemon 사용하기

- 지금까지의 내용에서 코드를 수정하면 바로 반영되는 것이 아니고 서버를 재시작해야 했다.
- 이를 nodemon 이라는 도구를 사용하면 코드가 변경될 때마다 서버를 자동으로 재시작해준다.

```jsx
yarn add -D nodemon
```

```json
/* package.json */
{
	"scripts": {
	  "start": "node src",
	  "start:dev": "nodemon --watch src/ src/index.js"
	}
}
```

- nodemon를 설치하고, package.json에 scripts 부분을 추가한다.
- 만약 **yarn start** 하면 기존처럼 node src가 실행되고,(재시작이 필요 없을 때)
    
    **yarn start:dev** 하면 src/ 폴더 내부의 어떤 파일이 변경되면 이를 감지하여 src/index.js 파일을 재시작해준다.
    

<br />

# 21.5 koa-router 사용하기

- Koa를 사용할 때 다른 주소로 요청이 들어올 경우 다른 작업을 처리할 수 있도록 라우터를 사용해야 한다.
- 다만, 내장되어 있지 않으니 koa-router 모듈을 설치하여 사용할 수 있다.

```json
yarn add koa-router
```

<br />

## 21.5.1 기본 사용법

```jsx
const Koa = require('koa');
const Router = require('koa-router');

const app = new Koa();
const router = new Router();

router.get('/', (ctx) => {
  ctx.body = '홈';
});

router.get('/about', (ctx) => {
  ctx.body = '소개';
});

app.use(router.routes()).use(router.allowedMethods());

app.listen(4000, () => {
  console.log('Liistening to port 4000');
});
```

- router.get() 함수는 첫 번째 파라미터에 라우트의 경로를 넣고, 두 번째 파라미터에 해당 라우트에 적용할 미들웨어 함수를 넣는다.
- get 키워드는 HTTP 메서드를 의미한다.(post, put, delete 등을 넣을 수 있다.)
- 위 코드는 / 경로에서 홈 문자열을 띄우고, /about 경로에서 소개 문자열을 띄우는 코드이다.

<br />

## 21.5.3 REST API

- 클라이언트가 서버에 자신이 데이터를 조회, 생성, 삭제, 업데이트하겠다고 요청하면, 서버는 REST API 요청 종류에 따라 다른 HTTP 메서드를 사용하며, 필요한 로직에 따라 데이터베이스에 접근하여 작업을 처리한다.

<br />

## 21.5.4 라우트 모듈화

- 라우터를 여러 파일에 분리시켜서 작성하고 불러와서 사용하는 방법을 알아보자
- `src/api/index.js`

```jsx
const Router = require('koa-router');

const api = new Router();

api.get('/test', (ctx) => {
  ctx.body = 'Test 성공';
});

module.exports = api;
```

- `src/index.js`

```jsx
const Koa = require('koa');
const Router = require('koa-router');

const api = require('./api');

const app = new Koa();
const router = new Router();

router.use('/api', api.routes());

app.use(router.routes()).use(router.allowedMethods());

app.listen(4000, () => {
  console.log('Liistening to port 4000');
});
```

- http://localhost:4000/api/test 에 접속하면 Test 성공 문자열이 보인다.

<br />

## 21.5.5.2 컨트롤러 파일 작성

- 라우트를 작성하는 과정에서 특정 경로에 미들웨어를 등록할 때 다음과 같이 바로 넣어줄 수 있다.

```jsx
router.get("/", ctx => {
	
})
```

- 다만, 위와 같이 작성했는데 코드가 너무 길어지면 라우터 설정을 보기 힘들어진다.
- 따라서 라우트 처리 함수들을 따로 분리해서 관리할 수 있는데 라우트 처리 함수만 모아놓은 파일을 컨트롤러라고 한다.
- 컨트롤러를 작성해보자
    - 작성하기 전에 koa-bodyparser 미들웨어를 적용하자
    - POST, PUT, PATCH 같은 메서드의 Request Body에 JSON 형식으로 데이터를 넣어주면 이를 파싱하여 서버에서 사용할 수 있게 해준다.

```jsx
yarn add koa-bodyparser
```

```jsx
const Koa = require('koa');
const bodyParser = require('koa-bodyparser');

const app = new Koa();
app.use(bodyParser());
```

<br />

### 컨트롤러 작성

- `src/api/posts/index.ctrl.js`

```jsx
let postId = 1;

const posts = [
  {
    id: 1,
    title: '제목',
    body: '내용',
  },
];

/*
  포스트 작성
  POST /api/posts
  { title, body }
*/

exports.write = (ctx) => {
  const { title, body } = ctx.request.body;
  postId += 1;
  const post = { id: postId, title, body };
  posts.push(post);
  ctx.body = post;
};

/*
  포스트 목록 조회
  GET /api/posts
*/

exports.list = (ctx) => {
  ctx.body = posts;
};

/*
  특정 포스트 조회
  GET /api/posts/:id
*/

exports.read = (ctx) => {
  const { id } = ctx.params;
  const post = posts.find((post) => post.id.toString() === id);
  if (!post) {
    ctx.status = 404;
    ctx.body = {
      message: '포스트가 존재하지 않습니다.',
    };
    return;
  }

  ctx.body = post;
};

/*
  특정 포스트 제거
  DELETE /api/posts/:id
 */

exports.remove = (ctx) => {
  const { id } = ctx.params;
  const index = posts.findIndex((post) => post.id.toString === id);
  if (index === -1) {
    ctx.status = 404;
    ctx.body = {
      message: '포스트가 존재하지 않습니다.',
    };
  }

  posts.splice(index, 1);
  ctx.status = 204; // No Content
};

/*
  포스트 수정(교체)
  PUT /api/posts/:id
  { title, body }
*/

exports.replace = (ctx) => {
  const { id } = ctx.params;
  const index = posts.findIndex((post) => post.id.toString() === id);
  if (index === -1) {
    ctx.status = 404;
    ctx.body = {
      message: '포스트가 없습니다.',
    };
    return;
  }

  posts[index] = {
    id,
    ...ctx.request.body,
  };

  ctx.body = posts[index];
};

/*
  포스트 수정(특정 필드 변경)
  PATCH /api/posts/:id
  { title, body }
*/

exports.update = (ctx) => {
  const { id } = ctx.params;
  const index = posts.findIndex((post) => post.id.toString() === id);
  if (index === -1) {
    ctx.status = 404;
    ctx.body = {
      message: '포스트가 없습니다.',
    };
    return;
  }

  posts[index] = {
    ...posts[index],
    ...ctx.request.body,
  };
  ctx.body = posts[index];
};
```

<br />

- exports.이름 형태로 작성하고 있는데 이를 사용할 때는 모듈이름.이름() 형태로 사용할 수 있다.

```jsx
const 모듈이름 = require("파일 이름");
모듈이름.이름();
```

<br />

- 위 코드에서 `require('./posts.ctrl')`을 불러온다면 다음과 같은 JSON을 불러오게 된다.

```json
{
	write: Function,
	list: Function,
	read: Function,
	remove: Function,
	replace: Function,
	update: Function,
}
```

- 이를 라우터에 연결시켜 보자
- `src/api/posts/index.js`

```jsx
const Router = require('koa-router');
const postsCtrls = require('./index.ctrl');
const posts = new Router();

posts.get('/', postsCtrls.list);
posts.post('/', postsCtrls.write);
posts.get('/:id', postsCtrls.read);
posts.delete('/:id', postsCtrls.remove);
posts.put('/:id', postsCtrls.replace);
posts.patch('/:id', postsCtrls.update);

module.exports = posts;
```

- `src/api/index.js`

```jsx
const Router = require('koa-router');
const posts = require('./posts');

const api = new Router();

api.use('/posts', posts.routes());

module.exports = api;
```