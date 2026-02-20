---
name: create-agent
description: "새 에이전트를 생성한다. '에이전트 만들어', 'agent 생성', 'create agent' 키워드 시 자동 활성화."
disable-model-invocation: true
argument-hint: "[에이전트명] [설명]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# 에이전트 생성 스킬

새 Claude Code 에이전트 파일을 생성한다.

## 워크플로우

```
Step 1: 요구사항 확인 (이름, 목적, 필요 도구)
Step 2: 기존 에이전트 패턴 참조
Step 3: 에이전트 파일 생성
Step 4: 검증
```

## Step 1: 요구사항 확인

`$ARGUMENTS`에서 에이전트 정보를 파악한다. 부족한 정보는 사용자에게 질문한다:

- **이름**: kebab-case (예: `code-reviewer`, `data-analyst`)
- **목적**: 에이전트가 수행할 역할
- **배치 플러그인**: 기본값 `modak-core`
- **필요 도구**: 에이전트가 사용할 도구 목록
- **모델**: sonnet(기본), opus, haiku
- **스킬 연동**: 함께 사용할 스킬이 있는지

## Step 2: 기존 패턴 참조

프로젝트 내 기존 에이전트를 확인한다:

```
plugins/**/agents/*.md
```

기존 에이전트의 frontmatter 구조와 본문 패턴을 참고하여 일관성을 유지한다.

## Step 3: 에이전트 파일 생성

### 파일 경로
```
plugins/{plugin-name}/agents/{agent-name}.md
```

### Frontmatter 템플릿

```yaml
---
name: {agent-name}
description: "{역할 설명}. '{키워드1}', '{키워드2}' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  # 필요한 도구 추가
model: sonnet
---
```

### Frontmatter 필드 레퍼런스

| 필드 | 필수 | 타입 | 설명 |
|------|------|------|------|
| name | O | string | kebab-case, 3-50자 |
| description | O | string | 역할 설명 + 자동 활성화 키워드 |
| allowed-tools | O | array | 허용 도구 목록 |
| model | - | string | sonnet, opus, haiku, inherit |
| skills | - | array | 프리로드할 스킬 |
| maxTurns | - | integer | 최대 턴 수 |
| color | - | string | blue, cyan, green, yellow, magenta, red |
| memory | - | string | user, project, local |
| permissionMode | - | string | default, acceptEdits, dontAsk, plan |
| background | - | boolean | 백그라운드 실행 |
| isolation | - | string | worktree |

### 본문 템플릿

```markdown
# {에이전트 한글명}

## 역할
{에이전트가 수행하는 역할 설명}

## 핵심 원칙
1. {원칙1}
2. {원칙2}
3. {원칙3}

## 작업 흐름
1. {Step 1}
2. {Step 2}
3. {Step 3}

## 규칙
- {규칙1}
- {규칙2}
- {규칙3}
```

### 도구 지정 문법

```yaml
# 내장 도구
- Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch

# Bash 제한
- "Bash(git *)"         # git 명령만
- "Bash(git diff:*)"    # git diff만
- "Bash(npm *)"         # npm 명령만

# MCP 와일드카드
- "mcp__notion__*"      # Notion MCP 전체
- "mcp__playwright__*"  # Playwright MCP 전체
- "mcp__figma__*"       # Figma MCP 전체

# Task 제한 (서브에이전트 생성)
- "Task(worker, researcher)"  # 특정 에이전트만
```

## Step 4: 검증

- [ ] YAML frontmatter 문법 올바른지
- [ ] name이 kebab-case인지
- [ ] description에 자동 활성화 키워드 포함되어 있는지
- [ ] allowed-tools가 최소 권한을 따르는지
- [ ] 파일 경로가 `plugins/{plugin}/agents/{name}.md`인지

## 규칙
- 기존 에이전트 패턴을 반드시 참조한 후 생성한다
- 불필요한 도구 권한을 부여하지 않는다 (최소 권한 원칙)
- 본문은 한글로 작성한다
- description에 자동 활성화 키워드를 반드시 포함한다
- 에이전트의 description 키워드가 기존 스킬의 키워드와 겹치지 않는지 반드시 확인한다 (아래 참조)

## 에이전트 vs 스킬 키워드 충돌 주의

에이전트의 description 키워드가 스킬의 description 키워드와 겹치면, **스킬이 먼저 매칭되어 에이전트가 호출되지 않는 문제**가 발생한다.

### 원인
- Skill 도구는 시스템 레벨에서 "매칭 시 다른 응답보다 먼저 호출"하라는 지시가 있음
- Task 도구(에이전트)에는 이런 강제 지시가 없음
- 결과: 같은 키워드에 스킬과 에이전트가 모두 매칭되면 스킬이 우선 실행됨

### 에이전트 생성 시 확인 절차
1. **기존 스킬 키워드 확인**: `plugins/**/skills/**/SKILL.md`의 description을 검색한다
2. **키워드 겹침 여부 확인**: 새 에이전트의 키워드가 기존 스킬과 충돌하지 않는지 확인한다
3. **충돌 발견 시 해결**:
   - 해당 스킬이 레퍼런스/가이드 성격이면 → 스킬에 `disable-model-invocation: true` 추가 권고
   - 키워드 영역을 분리 (에이전트: 작업/실행 키워드, 스킬: 가이드/레퍼런스 키워드)
