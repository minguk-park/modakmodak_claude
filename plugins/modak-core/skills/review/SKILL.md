---
name: review
description: "코드 리뷰를 수행한다. 파일, 디렉토리, PR 번호, git diff 대상을 지정할 수 있다. '리뷰', 'review', '코드 리뷰' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  - Grep
  - Glob
  - "Bash(git diff:*)"
  - "Bash(git log:*)"
  - "Bash(git show:*)"
  - "Bash(gh pr diff:*)"
  - "Bash(gh pr view:*)"
---

# 코드 리뷰 스킬

코드 변경사항을 빠르게 리뷰하여 주요 이슈를 찾아낸다.

## 리뷰 대상 결정

`$ARGUMENTS`에 따라 리뷰 대상을 결정한다:

| 인자 | 동작 |
|------|------|
| 파일 경로 | 해당 파일의 현재 코드를 리뷰 |
| 디렉토리 경로 | 디렉토리 내 파일들을 리뷰 |
| PR 번호 (예: `#123`) | `gh pr diff 123`으로 PR 변경사항 리뷰 |
| `--staged` | `git diff --staged`로 스테이징 변경사항 리뷰 |
| 인자 없음 | `git diff`로 현재 변경사항 리뷰 |

## 워크플로우

```
Step 1: 리뷰 대상 파악 및 코드 읽기
Step 2: 정확성 / 보안 / 성능 / 유지보수성 관점 분석
Step 3: 심각도별 분류 및 결과 출력
```

## Step 1: 리뷰 대상 파악

- 파일/디렉토리면 직접 Read로 읽기
- PR이면 `gh pr diff`로 변경사항 확인
- git diff면 `git diff` 또는 `git diff --staged` 실행

## Step 2: 분석 관점

### 정확성
- 로직 오류, 엣지 케이스 누락
- 타입 불일치, null 처리

### 보안
- 인젝션 취약점 (SQL, XSS)
- 인증/인가 누락, 민감 정보 노출

### 성능
- N+1 쿼리, 불필요한 연산
- 메모리 이슈, 캐싱 가능 영역

### 유지보수성
- 코드 중복, 과도한 복잡도
- 네이밍, 매직 넘버

## Step 3: 결과 출력

### 심각도 분류

| 심각도 | 표시 | 설명 |
|--------|------|------|
| Critical | :red_circle: | 즉시 수정 필요 |
| Warning | :yellow_circle: | 수정 권장 |
| Info | :blue_circle: | 개선 제안 |

### 출력 형식

```markdown
## 코드 리뷰 결과

### 요약
- 리뷰 대상: [대상]
- Critical: N개, Warning: N개, Info: N개

### :red_circle: Critical
- **[파일:라인]** 문제 설명 → 제안

### :yellow_circle: Warning
- **[파일:라인]** 문제 설명 → 제안

### :blue_circle: Info
- **[파일:라인]** 개선 제안

### 잘된 점
- 긍정적 피드백
```

## 규칙
- 코드를 수정하지 않는다 (읽기 전용)
- 프로젝트의 기존 패턴과 컨벤션을 존중한다
- 사소한 스타일보다 실질적 문제에 집중한다
