# Next JS 배포 오류

# 1. Netlify로 배포하는데 export 오류

<img height="300px" src="https://user-images.githubusercontent.com/85148549/157398648-78f56766-3229-4354-afdb-4bb958df040e.png">

<img height="300px" src="https://user-images.githubusercontent.com/85148549/157398761-7c3196dd-1ba0-4e6e-a7bf-b272cb265159.png">

- 직접 만들어서 사용 중인 components를 export하려는데 Cannot find module 이라고 뜨면서 배포가 되지 않는다.
- 알아본 결과 Next JS에서 pages 폴더에 위치한 컴포넌트와 components 폴더에 위치한 컴포넌트의 파일 이름이 달라야 한다.
    - Netlify는 배포에 우분투(Ubuntu)를 사용하는데, 파일 이름의 시작이 대문자인지 소문자인지에 따라 문제가 발생한다.

> The problem was incorrect case for components. It works on Windows and macOS (that’s why it build successfully on my Windows laptop and you might be using either of the two), but, Netlify uses Ubuntu which is Linux based and Linux can’t work with the mixed cases. So, all your components are in the folders which start with a small case, while the pages start with a capital case. While importing the components, you need to maintain the case, but, instead, you were importing all the components with the starting letter capital.
> 

<br />

# 2. 폴더명, 파일명 다 수정했는데 해결 안됨

- 위의 사실을 알게된 후 폴더명, 파일명을 모두 소문자로 수정하고, pages에서 사용하는 module은 대문자로 시작하게 이름을 수정하여 commit 하였다.
- 그런데 정상적으로 변경된 것처럼 보였으나 배포 결과는 똑같이 에러가 발생했다.
- 이는 local에서 변경된 대소문자 변경은 github 저장소에 반영이 되지 않아서 local에서는 소문자로 보여도 github 저장소에서는 대문자로 보였다.

<br />

# 3. 폴더명, 파일명 변경하는 방법

```jsx
git mv 폴더/변경전_파일명 폴더/변경하려는_파일명
git mv 폴더/변경전_폴더 폴더/변경하려는_폴더
```

- `git mv` 명령어로 폴더, 파일명 변경이 가능하여 하나씩 소문자로 변경해준 후 commit하여 문제를 해결하였다.
    - `git mv components/Layout components/layout` ⇒ 최초 작성한 명령어인데, 동작하지 않아서
        
        
        1. `git mv components/layout components/temp`
        2. `git mv components/temp components/layout`
        
        두 번에 걸쳐서 폴더를 먼저 수정해주고 내부의 파일을 수정해주는 방식으로 진행했다.