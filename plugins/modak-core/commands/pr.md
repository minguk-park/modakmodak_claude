---
description: "PR(Pull Request) 생성"
allowed-tools:
  - "Bash(git *)"
  - "Bash(gh *)"
---

# PR 생성

## 프로세스

1. 현재 브랜치의 변경사항 분석
2. PR 제목과 본문 자동 작성
3. 사용자 확인 후 PR 생성

## Step 1: 변경사항 분석

```bash
# 현재 브랜치 확인
git branch --show-current

# base 브랜치 대비 커밋 목록
git log main...HEAD --oneline

# base 브랜치 대비 변경사항
git diff main...HEAD --stat
```

- base 브랜치는 `main`을 기본으로 사용
- `$ARGUMENTS`에 base 브랜치가 지정되면 해당 브랜치 사용

## Step 2: PR 내용 작성

### 제목 규칙
- 70자 이내
- 변경사항의 핵심을 한 문장으로 요약
- 커밋이 1개면 해당 커밋 메시지를 제목으로 사용

### 본문 형식

```markdown
## Summary
- 변경사항 요약 (1-3줄)

## Changes
- 주요 변경 파일과 내용

## Test Plan
- [ ] 테스트 항목 1
- [ ] 테스트 항목 2
```

## Step 3: 사용자 확인

작성된 PR 제목과 본문을 사용자에게 보여주고 확인받는다.
수정 요청이 있으면 반영한 후 다시 확인받는다.

## Step 4: PR 생성

```bash
gh pr create --title "제목" --body "본문"
```

- 리모트에 브랜치가 없으면 `git push -u origin <branch>` 먼저 실행
- PR 생성 후 URL을 사용자에게 알려준다

## 규칙
- PR 생성 전에 반드시 사용자 확인을 받는다
- `--draft` 옵션이 지정되면 Draft PR로 생성한다
- 커밋이 없는 브랜치에서는 PR을 생성하지 않는다
- 한글로 PR 내용을 작성한다
