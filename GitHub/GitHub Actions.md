# GitHub Actions

# GitHub Actions?

- 개발자의 workflow를 자동화할 수 있도록 GitHub에서 제공하는 도구이다.
- GitHub 저장소에 Commit, Push 등으로 코드를 올린 후 Actions를 사용하게 되면 **runner**라고 하는 컴퓨터를 대여할 수 있게 되고, 해당 저장소에 push한 코드나 데이터들을 **runner**에서 구동하여 워크플로우를 자동화할 수 있게 되는 것이다.
    - 예를 들어, 테스트를 자동으로 진행하거나, 테스트가 성공했을 때 자동 배포하거나 배포 이후에 이메일을 보내는 등의 자동화가 가능하다.

<br />

# 사용 방법

1\) Github에 Repository를 생성한다.

2\) 해당 Repository의 Tab에는 Code, Issues, Pull requests 등등이 있는데, Actions 탭을 눌러 Actions 탭에 진입한 뒤 set up a workflow yourself를 클릭하여 생성한다.

<div align="center">
 <img src="https://user-images.githubusercontent.com/85148549/158562527-c5721fc2-21ff-4933-a7ef-e0c2f16f89ab.png">
</div>

<br />

3\) 그럼 repository명 / .github / workflows / main.yml 파일에 지정된 템플릿이 생성되는데 이에 대한 정보는 아래와 같다.

- [.yml 파일에서 사용될 키워드는 여기서 확인할 수 있음](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

<br />

<div align="center">
 <img src="https://user-images.githubusercontent.com/85148549/158562536-2821b126-3bf2-4eb5-ad4b-ba2843713d16.png">
</div>

  1. **name**: 해당 Actions의 이름
  2. **on**: Actions는 이벤트 기반의 도구인데, 워크플로우를 트리거 시키는 이벤트를 작성한다.
    - push 했다거나 folk 했다거나 여러가지를 작성할 수 있다.
        - push의 경우 바로 작성이 가능하지만, issues의 경우 issue를 생성, 삭제, 수정 등등 여러가지 작업이 가능하므로 issues 내부에서 type을 다시 지정해줘야 한다.
        - [이벤트 타입은 여기서 확인할 수 있음](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
  3. **runs-on**: Action이 실행될 때 runner에서 사용할 OS
    - 기본은 ubuntu-latest 로 작성돼있는데 window, macOS, linux 등도 사용할 수 있다.
  4. **steps**: 실제로 해야하는 일을 작성하는 곳.
       1. **uses**: 다른 사람이 만든 Actions을 실행하고 싶을 때 해당 키워드에 작성하면 동작한다.
       2. **name**, **run**: runs-on에서 작성한 운영체제에서 run 시킬 코드를 작성한다.
           - name은 이름이고, 실질적인 동작은 run에서 진행된다.

4\) 작성을 모두 마치면 오른쪽 상단의 Start commit을 눌러 Commit한다.

- Commit하게 되면 저장소에 .github / workflows 폴더가 생성되고 해당 폴더에 아까 작성한 내용들이 담긴 main.yml 파일이 생성된다.

<br />

## uses: actions/checkout@v2 ?

- runner를 만들게 되면 아무것도 들어있지 않은데, 해당 uses를 사용하게 되면 액션이 실행되고있는 저장소를 clone, checkout하여 다음 명령어들을 실행할 수 있게 해주는 actions이다.

<br />

# Action Contexts

- runner가 실행되는 시점에 여러가지 환경변수를 사용할 수 있다.
- [환경 변수는 여기서 확인](https://docs.github.com/en/actions/learn-github-actions/contexts#about-contexts)

```yaml
name: context

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: "context"
        env:
          COMMIT_ID: ${{ github.sha }}
        run: echo "Commit id => $COMMIT_ID"
```

- 이런식으로  `${{ environment }}` 형태로 사용하면 된다.
- 위 코드는 push가 됐을 때 commit id를 COMMIT_ID라는 환경변수에 저장하고(github.sha는 commit id를 확인하는 약속된 cotnext이다.) 이를 출력해주는 코드이다.

<div align="center">
 <img src="https://user-images.githubusercontent.com/85148549/158562535-b85ca31c-a9a4-4689-8371-88c4552e6eb7.png">
</div>

<br />

# Secrets

- yml 파일을 생성할 때 공개되면 안되는 API_KEY, Password 등의 정보가 담기면 보안에 문제가 생길 수 있다.
- 이를 해결하기 위해선 github repository ⇒ settings ⇒ Secrets ⇒ actions 탭에서 공개되면 안되는 정보를 저장하여 환경변수로 사용할 수 있다.
- 만약 Secrets의 name: PASSWORD, value: 1234라고 작성한 후 이를 다음과 같이 사용하면

```yaml
name: Secrets

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Print Password
        env:
          MY_PASSWORD: ${{ secrets.PASSWORD }}
        run: echo My password is $MY_PASSWORD
```

<div align="center">
 <img src="https://user-images.githubusercontent.com/85148549/158562533-037a464a-b60b-49e7-819f-213ae65579d3.png">
</div>

위와 같이 *** 형태로 나타나게 된다.