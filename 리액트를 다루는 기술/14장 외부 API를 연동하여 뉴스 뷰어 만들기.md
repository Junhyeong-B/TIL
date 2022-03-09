# 14장 외부 API를 연동하여 뉴스 뷰어 만들기

# 14.1 비동기 작업의 이해

- 웹 어플리케이션에서 서버 쪽 데이터가 필요할 때는 Ajax 기법을 사용하여 API를 호출함으로써 데이터를 수신한다.
    - 이러한 과정은 시간이 걸리기 때문에 응답을 받을 때까지 기다렸다가 전달받은 응답 데이터를 처리한다.
- 비동기 작업을 할 때 가장 흔히 사용하는 방법은 콜백 함수를 사용하는 것이다.
- 그러나 콜백 함수를 활용하여 비동기 코드를 작성하다보면 중첩이 늘어나 콜백 지옥 형태의 코드가 작성될 수 있다.

<br />

## 14.1.1 Promise

- Promise는 콜백 지옥 코드가 형성되지 않게 하는 방안으로 ES6에 도입된 기능이다.
- 비동기 코드들을 중첩되게 여러번 작성하지 않고, 후처리 메서드 체이닝(then, catch, finally)을 활용하여 콜백 지옥이 형성되지 않는다.

<br />

## 14.1.2 async / await

- Promise를 더 쉽게 사용할 수 있도록 해주는 ES8 문법이다.
- 함수 앞에 async 키워드를 사용하면 해당 함수 내부에서 Promise 비동기 로직 앞에 await 키워드를 사용할 수 있다.
    - 이 경우 해당 Promise가 모두 끝날때 까지 기다렸다가 다음 코드가 진행된다.
    - 동기적으로 코드가 실행되는 것처럼 동작한다.

<br />

# 14.2 Axios

- axios는 자바스크립트 HTTP 클라이언트이다.
- axios는 HTTP 요청을 Promise 기반으로 처리한다.

<br />

# 14.5 비동기 요청 데이터 연결하기

- useEffect를 사용하여 처음 렌더링되는 시점에 API를 요청하면 된다.
- useEffect에서 반환해야하는 값은 뒷정리 함수 이므로 useEffect에 등록하는 함수에는 async 키워드를 사용하면 안되고, 사용하고 싶다면 또 다른 함수를 생성하여 사용하면 된다.
- loading state를 활용하여 API 요청이 대기중인지에 따라 UI 변동에 활용할 수 있다.
- 데이터를 불러와서 해당 데이터 배열을 map 함수를 사용하여 컴포넌트 배열로 변환할 때 map 함수를 사용하기 전 해당 배열을 조회하여 값이 null인지 아닌지 꼭 검사할 필요가 있다.
    - 데이터가 없을 때 null에는 map 함수가 없기 때문에 렌더링 과정에서 오류가 발생한다.

```jsx
import axios from 'axios';
import { useEffect, useState } from 'react';

const NewsList = () => {
  const [articles, setarticles] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchData = async(() => {
      setIsLoading(true);
      try {
        const response = await axios.get('');
        setarticles(response.data.articles);
      } catch (error) {
        console.log(error);
      }
      setIsLoading(false);
    });

    fetchData();
  }, []);

  if (isLoading) {
    return <div>대기 중</div>;
  }

  if (!articles) {
    return null;
  }

  return <div>내용</div>;
};

export default NewsList;
```

<br />

# 14.8 usePromise 커스텀 Hook 만들기

```jsx
import { useEffect, useState } from 'react';

export default function usePromise(promiseCreator, deps) {
  const [loading, setLoading] = useState(false);
  const [resolved, setResolved] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const process = async () => {
      setLoading(true);
      try {
        const resolved = await promiseCreator();
        setResolved(resolved);
      } catch (error) {
        setError(error);
      }
      setLoading(false);
    };

    process();
  }, [deps]);

  return [loading, resolved, error];
}
```

- 프로젝트의 다양한 곳에서 사용될 수 있는 유틸 함수들은 보통 src/lib 디렉터리 내부에 작성한다.
- usePromise는 Promise의 대기, 결과, 에러에 대한 상태를 관리하고, 의존 배열인 deps를 파라미터로 받는다.
- usePromise를 위 NewsList에서 사용하게 된다면

<br />

**사용 전**

```jsx
const [articles, setarticles] = useState(null);
const [isLoading, setIsLoading] = useState(false);

useEffect(() => {
  const fetchData = async(() => {
    setIsLoading(true);
    try {
      const response = await axios.get('');
      setarticles(response.data.articles);
    } catch (error) {
      console.log(error);
    }
    setIsLoading(false);
  });

  fetchData();
}, []);
```

**사용 후**

```jsx
const [loading, response, error] = usePromise(() => {
	return axios.get('');
}, [])
```

- useEffect 사용을 직접 하지 않아도 돼서 코드가 훨씬 간결해진다.