---
name: readme
description: "프로젝트를 분석하여 README.md를 자동 생성한다. '리드미', 'readme', 'README 생성' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - "Bash(git *)"
---

# README 생성 스킬

프로젝트를 자동으로 분석하여 README.md를 생성한다.

## 워크플로우

```
Step 1: 프로젝트 분석 (언어, 프레임워크, 구조 감지)
Step 2: 정보 수집 (실행 방법, 환경 변수, 의존성)
Step 3: README.md 생성
Step 4: 사용자 확인
```

## Step 1: 프로젝트 분석

아래 파일들을 확인하여 프로젝트 특성을 파악한다:

```
# 언어/프레임워크 감지
package.json          → Node.js / JavaScript / TypeScript
composer.json         → PHP / Laravel
pubspec.yaml          → Flutter / Dart
requirements.txt      → Python
pyproject.toml        → Python
Cargo.toml            → Rust
go.mod                → Go
build.gradle          → Java / Kotlin
Gemfile               → Ruby

# 빌드/설정 감지
Dockerfile            → Docker 사용
docker-compose.yml    → Docker Compose
.env.example          → 환경 변수
Makefile              → Make 빌드
```

## Step 2: 정보 수집

### 필수 수집 항목
- **프로젝트 이름**: 디렉토리명 또는 package 설정에서 추출
- **설명**: package 설정의 description 또는 기존 README에서 추출
- **기술 스택**: 감지된 언어, 프레임워크, 주요 라이브러리
- **설치 방법**: 패키지 매니저 기반 설치 명령어
- **실행 방법**: dev/start/serve 스크립트 확인
- **환경 변수**: `.env.example` 파일에서 추출

### 선택 수집 항목
- **디렉토리 구조**: 주요 디렉토리 설명
- **API 엔드포인트**: routes 파일에서 추출 (해당 시)
- **테스트 실행**: test 스크립트 확인
- **배포 방법**: Dockerfile, CI/CD 설정 확인

## Step 3: README 생성

### 기본 구조

```markdown
# 프로젝트명

프로젝트 설명

## 기술 스택

- 언어/프레임워크 목록

## 시작하기

### 사전 요구사항

- 필요한 소프트웨어 목록

### 설치

설치 명령어

### 환경 변수 설정

환경 변수 테이블 (변수명, 설명, 예시)

### 실행

실행 명령어

## 프로젝트 구조

주요 디렉토리 구조

## 테스트

테스트 실행 방법
```

## Step 4: 사용자 확인

- 생성된 README 내용을 사용자에게 보여주고 확인받는다
- 수정 요청이 있으면 반영한다
- 확인 후 파일을 저장한다

## 규칙
- 기존 README.md가 있으면 덮어쓰기 전에 사용자에게 확인받는다
- 실제 프로젝트 파일에서 추출한 정보만 사용한다 (추측 금지)
- `.env` 파일의 실제 값은 포함하지 않는다 (`.env.example` 기준)
- 한글로 작성한다
