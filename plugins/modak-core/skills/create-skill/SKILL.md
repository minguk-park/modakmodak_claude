---
name: create-skill
description: "새 스킬을 생성한다. '스킬 만들어', 'skill 생성', 'create skill' 키워드 시 자동 활성화."
argument-hint: "[스킬명] [설명]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# 스킬 생성 스킬

새 Claude Code 스킬(SKILL.md)을 생성한다.

## 워크플로우

```
Step 1: 요구사항 확인 (이름, 목적, 필요 도구)
Step 2: 기존 스킬 패턴 참조
Step 3: 스킬 파일 생성
Step 4: 에이전트 연동 (필요 시)
Step 5: 검증
```

## Step 1: 요구사항 확인

`$ARGUMENTS`에서 스킬 정보를 파악한다. 부족한 정보는 사용자에게 질문한다:

- **이름**: kebab-case (예: `api-test`, `deploy-check`)
- **목적**: 스킬이 수행할 작업
- **배치 플러그인**: 기본값 `modak-core`
- **필요 도구**: 스킬이 사용할 도구 목록
- **호출 방식**: 사용자 호출 / Claude 자동 호출 / 둘 다
- **실행 격리**: fork 컨텍스트 필요 여부
- **에이전트 연동**: 특정 에이전트에서 프리로드할지

## Step 2: 기존 패턴 참조

프로젝트 내 기존 스킬을 확인한다:

```
plugins/**/skills/**/SKILL.md
```

기존 스킬의 frontmatter 구조와 워크플로우 패턴을 참고한다.

## Step 3: 스킬 파일 생성

### 파일 경로
```
plugins/{plugin-name}/skills/{skill-name}/SKILL.md
```

### Frontmatter 템플릿

```yaml
---
name: {skill-name}
description: "{작업 설명}. '{키워드1}', '{키워드2}' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  # 필요한 도구 추가
---
```

### Frontmatter 필드 레퍼런스

| 필드 | 필수 | 타입 | 설명 |
|------|------|------|------|
| name | - | string | kebab-case, 최대 64자 (기본: 디렉토리명) |
| description | 권장 | string | 역할 설명 + 자동 활성화 키워드 |
| allowed-tools | - | array | 허용 도구 목록 |
| argument-hint | - | string | 자동완성 힌트 (예: `[filename]`) |
| model | - | string | sonnet, opus, haiku |
| context | - | string | `fork`으로 격리 실행 |
| agent | - | string | fork 시 에이전트 타입 (Explore, Plan, general-purpose, 커스텀) |
| disable-model-invocation | - | boolean | true면 사용자만 `/name`으로 호출 가능 |
| user-invocable | - | boolean | false면 `/` 메뉴에 안 보임 (Claude만 호출) |

### 본문 템플릿

```markdown
# {스킬 한글명}

{스킬 설명 한 줄}

## 워크플로우

Step 1: {단계1}
Step 2: {단계2}
Step 3: {단계3}

## Step 1: {단계1 제목}

{상세 내용}

## Step 2: {단계2 제목}

{상세 내용}

## 규칙
- {규칙1}
- {규칙2}
```

### 스킬 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `$ARGUMENTS` | 전체 인자 | `/skill-name arg1 arg2` → `arg1 arg2` |
| `$0`, `$1` | N번째 인자 | `/skill-name hello` → `$0` = `hello` |
| `` !`command` `` | 쉘 명령 결과 주입 | `` !`git branch --show-current` `` |

### 호출 제어 조합

| 설정 | 사용자 호출 | Claude 호출 | 용도 |
|------|------------|------------|------|
| (기본값) | O | O | 범용 스킬 |
| `disable-model-invocation: true` | O | X | 부작용 있는 스킬 (배포, 커밋 등) |
| `user-invocable: false` | X | O | 배경 지식 스킬 |

## Step 4: 에이전트 연동

스킬을 특정 에이전트에서 프리로드하려면 해당 에이전트의 `skills` 배열에 추가한다:

```yaml
# agents/some-agent.md
---
skills:
  - {new-skill-name}           # 같은 플러그인 내
  - "other-plugin:skill-name"  # 다른 플러그인
---
```

## Step 5: 검증

- [ ] `plugins/{plugin}/skills/{name}/SKILL.md` 경로가 올바른지
- [ ] YAML frontmatter 문법이 올바른지
- [ ] name이 kebab-case인지
- [ ] description에 자동 활성화 키워드 포함되어 있는지
- [ ] 워크플로우가 명확한 단계로 구성되어 있는지
- [ ] 에이전트 연동이 필요한 경우 skills 배열에 추가했는지

## 규칙
- 기존 스킬 패턴을 반드시 참조한 후 생성한다
- 부작용이 있는 스킬은 `disable-model-invocation: true` 설정한다
- 500줄 이내로 작성한다 (상세 내용은 별도 파일로 분리)
- 본문은 한글로 작성한다
- 워크플로우는 명확한 Step으로 구성한다
