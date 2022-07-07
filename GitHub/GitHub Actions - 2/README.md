# Github Actions

# 1. 소개

개발자로 프로덕트를 만들거나 프로젝트를 진행할 때 `코드 작성 → 테스트 → 빌드 → 배포 → 버그, 개선 등 코드 수정` 이라는 일련의 과정이 반복되고 다시 코드 작성부터 시작하게 되는 사이클을 돌게 된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/177785213-01eb6dbe-a174-47fe-9387-84bc98d5c7ce.png" />
</div>

> 이미지 출처: [https://www.supportpro.com/blog/ci-cd/](https://www.supportpro.com/blog/ci-cd/)
> 

<br />

### 1-1) CI (Continuous Integration) - 지속적 통합

원격 저장소에 존재하는 코드 저장소로부터 너무 많은 작업량들이 쌓이기 전에 자동화된 빌드 및 테스트가 수행된 후 코드 변경 사항을 중앙 코드 저장소에 정기적으로 통합하는 개발 방식이다. 이를 이용하면 수동 작업에 대한 부담을 덜고 버그를 더 빠르게 발견할 수 있으며 업데이트를 더 빠르게 제공해줄 수 있다.

<br />

### 1-2) CD (Continuous Delivery | Deployment) - 지속적 배포

프로덕션에 적용시키기 위한 코드 변경 사항을 자동으로 배포하는 개발 방식을 말한다. 이를 이용하면 CI를 사용했을 때의 이점과 마찬가지로 개발자의 부담 감소, 버그를 더 빠르게 발견, 업데이트를 더 빠르게 제공할 수 있다.

- **Continuous Delivery**: 배포 단계를 수동화
    - CI를 마치고 릴리즈가 가능하지만 배포 단계에서 사람의 검증을 통해 수동적으로 배포가 이루어지면 Delivery 용어를 사용한다.
- **Continuous Deployment**: 배포 단계를 자동화
    - CI를 마치고 릴리즈가 가능하여 배포까지 자동으로 이루어질 때 Deployment 용어를 사용한다.

<br />

### 1-3) Github Actions

코드 저장소인 GitHub에서 제공하는 CI/CD를 위한 서비스로, 자동화된 빌드, 테스트, 배포 파이프라인을 제공한다. 또한 GitHub 코드를 관리하고 있는 프로젝트에서 누구나 사용할 수 있기 때문에 진입장벽이 낮다. GitHub Actions를 사용하면 자동으로 코드 저장소에서 어떤 이벤트(Commit, Push, Pull 등등)가 발생했을 때 특정 작업들을 주기적으로 반복해서 실행시킬 수 있다.

예를 들어, 특정 코드 변경 사항이 메인(main 또는 master) 저장소에 유입(push)되면 GitHub Actions를 통해 빌드(Build), 배포(Deploy)등을 자동으로 진행되도록 만들 수 있으며, 매일 특정 시각(자정 등)에 그날 하루에 대한 통계를 수집할 수도 있다.

이러한 작업들을 자동화된 작업들을 **Workflows(워크플로우)** 라고 부르는데, GitHub Actions Workflows를 실행시키기 위한 가상 OS(Linux, Windows, macOS)를 제공한다. 이 가상 OS는 **runner(러너)** 라고 한다.

<br />

# 2. Workflows

Workflows는 하나 이상의 작업을 실행하는 자동화 프로세스를 말한다. Workflows는 정의하고 싶은 저장소(Repository)에 YAML(.yml) 파일로 정의할 수 있고, 해당 YAML 파일에 정의된 특정 이벤트에 의해 트리거될 때 정의된 Workflows를 실행시킬 수 있다.

- Workflows는 저장소 내의 `.github/workflows` 디렉토리에 정의할 수 있다.
- 저장소에는 각각 다른 작업을 수행할 수 있는 여러 Workflows가 있을 수 있다.
- Workflows에는 크게 2가지를 정의하는데, 하나는 **on(이벤트, 트리거)**, 다른 하나는 **jobs(작업)** 이다.
    - 아래 코드는 ubuntu OS(runs-on) runner를 사용해서 아래 step에 기재될 작업들이 main 브랜치에 push가 되면 동작한다.

```yaml
on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

		step: ...
```

<br />

# 3. Jobs와 Steps

**Jobs(작업)** 는 독립된 가상 OS(runner)에서 돌아가는 하나의 처리 단위를 의미한다. 하나의 Workflows에는 여러 개의 Jobs로 구성되어 있어도 되지만 적어도 하나 이상의 Jobs는 있어야 한다.

정말 단순한 작업이 아닌 이상 하나의 작업은 일반적으로 여러 **단계(Steps)** 의 명령을 순차적으로 실행하는 경우가 많은데, 각 작업(Jobs)이 하나 이상의 단계(Steps)로 모델링된다.

- 각 단계(Steps)는 순서대로 실행되며 서로 종속된다.
- 각 단계(Steps)는 동일한 러너에서 실행되기 때문에 한 단계에서 다른 단계로 데이터를 공유할 수 있다.
- 각 작업(Jobs)은 서로 종속되지 않고 기본적으로(default) 병렬 실행된다.
    
    ⇒ 물론 의도적으로 특정 작업을 다른 작업에 종속시켜 종속 작업이 완료될 때까지 기다렸다가 실행할 수도 있다.
    

<br />

# 4. Actions

Actions(액션)은 GitHub Actions에서 빈번하게 필요한 반복 단계를 재사용하기 용이하도록 Jobs를 만들거나 Workflows를 커스터마이징하기 위한 작업(Tasks)이다.

[GitHub Market Place](https://github.com/marketplace?type=actions) 에 접속하면 수 많은 벤더(Vendor)가 공개해놓은 다양한 액션을 쉽게 접할 수 있는데, 사용자가 직접 Custom Actions를 생성할 수도 있고, 해당 페이지에서 공개된 Actions를 가져다 사용할 수도 있다.

<br />

# 5. Example

1) GitHub에서 GitHub Actions를 사용할 레포지토리를 새로 생성한다.(기존 사용중인 레포지토리에 Actions 사용 가능)

2) 해당 레포지토리의 Actions 탭에 접속한 후 직접 Workflow를 생성하거나 공개된 Actions를 선택하여 Actions를 생성한다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/177564172-50721d1a-82d1-4224-a139-73cdfcfd0860.png" />
</div>

<br />

3) Simple workflow를 선택했다면 아래와 같은 `blank.yml` 파일이 `.github/workflows` 디렉토리에 생성하려고 하는데, 각각에 대한 설명은 다음과 같다.

```yaml
name: CI

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run a one-line script
        run: echo Hello, world!

      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
```

1. **name**: 해당 Actions의 이름.
2. **on**: Actions는 이벤트 기반의 도구인데, 워크플로우를 트리거 시키는 이벤트를 작성한다.
    - push 했다거나 folk 했다거나 여러가지를 작성할 수 있다.
        - push, folk 같은 경우 push 했을 때, folk 했을 때 바로 이벤트 트리거가 가능하지만, issues, pull_request같은 경우 issue를 생성, 삭제, 수정 등등 여러가지 작업이 가능하므로 issues 내부에서 type을 지정해 줄 수 있다.
        
        ```yaml
        on:
          issues:
            types: [opened, edited, milestoned]
        ```
        
    - [이벤트 타입은 여기서 확인할 수 있다.](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
3. **runs-on**: Action이 실행될 때 runner에서 사용할 OS
    - 기본은 ubuntu-latest 로 작성돼있는데 window, macOS, linux 등도 사용할 수 있다.
4. **steps**: 실제로 해야하는 일을 작성하는 곳.
    1. **uses**: 다른 사람이 만든 Actions을 실행하고 싶을 때 해당 키워드에 작성하면 동작한다.
    2. **name**, **run**: runs-on에서 작성한 운영체제에서 run 시킬 코드를 작성한다.
        - name은 이름이고, 실질적인 동작은 run에서 진행된다.

<br />

- 결국 위 Workflows는 main 브랜치에 push 이벤트가 발생하면 ubuntu-latest runner 내부에서 1줄, 2줄 스크립트가 실행된다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/177564169-568195d6-f4ee-4024-8e0c-1a93e95f2da6.png" />
</div>

<br />

### ※ uses: actions/checkout@v3 이란??

- runner를 만들게 되면 아무것도 들어있지 않은데, 해당 uses를 사용하게 되면 액션이 실행되고있는 저장소를 clone, checkout하여 Git 명령어들을 실행할 수 있게 해주는 actions이다.


<br />

# 6. Actions 내부 데이터 활용

### 6-1) Action Contexts

Contexts는 Workflows의 실행, Runner 환경, Jobs, Steps 등에서 정보(information)에 접근하는 방법으로 `${{ <context> }}` 형태로 정보에 접근할 수 있다.

runner가 실행되는 시점에 여러가지 Contexts를 사용할 수 있는데, github 정보(commit ID, repository url 등)나 Workflows, Jobs, Steps, Runner 등을 사용할 수 있다.

- [환경 변수는 여기서 확인](https://docs.github.com/en/actions/learn-github-actions/contexts#about-contexts)

<br />

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

- 이런식으로  `${{ github.sha }}` 형태로 사용하면 된다.
- env는 환경변수로, 여기선 COMMIT_ID라는 환경변수에 github.sha(commit id) 정보를 저장하고, 이를 run 시점에 출력하는 코드이다.

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/177564162-134a7c64-b0fc-4141-81f4-b6553f86ec76.png" />
</div>

<br />

### 6-2) Secrets

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
  <img src="https://user-images.githubusercontent.com/85148549/177564157-332657e1-fe63-477d-ac3f-c7d0f91e547a.png" />
</div>

위와 같이 *** 형태로 나타나게 된다.

<br />

# 7. 실전

1일 1알고리즘 공부를 하던 중 문제를 푼 코드를 개인 public repo에 저장하고 있었는데, 당일 푼 문제에 대한 js 파일을 push하는 것은 쉬우나 이를 readme에 어떤 문제인지, 해당 js파일 링크를 연결하는 코드를 매번 문제를 풀 때마다 작성해줘야 했다.

이를 GitHub Actions를 이용해서 문제풀이를 한 js, ts 파일만 push하면 Actions가 실행되면서 자동으로 readme 파일을 수정하도록 구성하였다.

```yaml
name: README.me auto update

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Get current date
        id: date
        run: echo "::set-output name=date::$(date +'%Y-%m-%d')"
      - uses: actions/checkout@v2
      - name: Set up Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"
      - name: Update .md File
        run: |
          python update.py
      - name: Push the change
        run: |
          git config --global user.name 'Junhyeong-B'
          git config --global user.email 'aowlr0513@gmail.com'
          git add .
          git commit -m "update README.md | ${{ steps.date.outputs.date }}"
          git push
```

1. 문제 풀이 push
2. actions/checkout@v2로 git clone, checkout
3. actions/setup-python@v2로 python을 사용가능하도록 셋업
4. 해당 레포지토리에 존재하는 update py 파일 실행
5. update py 내부에서 readme 파일을 업데이트 해주고 git 명령어로 push

<br />

# 참고 문서

---

- [Continuous-Integration](https://aws.amazon.com/ko/devops/continuous-integration/)
- [Continuous-Delivery](https://aws.amazon.com/ko/devops/continuous-delivery/)
- [Github Actions](https://docs.github.com/en/actions)
- [Github Actions Basics/](https://www.daleseo.com/github-actions-basics/)
- [카카오웹툰은 GitHub Actions를 어떻게 사용하고 있을까?](https://fe-developers.kakaoent.com/2022/220106-github-actions/)