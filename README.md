# modakmodak_claude

Laravel & Flutter 개발을 위한 Claude Code 플러그인 모음

## 설치 방법

아래 두 단계 모두 **최초 1회**만 실행하면 됩니다. 유저 레벨로 설치되어 모든 프로젝트에서 사용 가능합니다.

### 1. 마켓플레이스 추가
```
/plugin marketplace add minguk-park/modakmodak_claude
```

### 2. 플러그인 설치
```
/plugin install modak-core@modakmodak-tools
/plugin install laravel@modakmodak-tools
```

## 플러그인 목록

| 플러그인 | 설명 |
|---------|------|
| `modak-core` | 모든 프로젝트에서 공통으로 사용하는 핵심 명령어 및 도구 |
| `laravel` | Laravel 프로젝트 개발 규칙 및 명령어 |
| `flutter` | Flutter 프로젝트 개발 규칙 및 명령어 (예정) |

## MCP 서버 설치

플러그인의 모든 기능을 활용하려면 아래 MCP 서버들을 설치하세요.

### 필수 MCP 서버

```bash
# Figma MCP (Figma 디자인 연동)
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp

# Context7 (라이브러리 문서 조회)
claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse

# Sequential Thinking (복잡한 분석)
claude mcp add --scope user sequential-thinking -- npx -y @anthropics/claude-mcp-server-sequential-thinking

# 21st Magic (UI 컴포넌트 생성)
claude mcp add --scope user magic -- npx -y @anthropics/claude-mcp-server-magic
```

### 선택적 MCP 서버

```bash
# Playwright (E2E 테스트, 브라우저 자동화)
claude mcp add --scope user playwright -- npx -y @anthropics/claude-mcp-server-playwright
```

### 설치 확인

```bash
/mcp
```

`User MCPs` 섹션에 설치한 서버들이 `connected` 상태로 표시되면 정상입니다.

## modak-core 포함 기능

### Commands
- `/commit` - 변경사항을 하나의 커밋으로 생성
- `/commit-all` - 변경사항을 논리적 단위로 그룹화하여 여러 커밋 생성
- `/pr` - PR(Pull Request) 생성

### Agents
- `code-reviewer` - 코드 리뷰 (정확성/보안/성능/유지보수성 분석)
- `notion` - 노션에 내용 작성
- `notion-writer` - 마크다운 → Notion 페이지 변환
- `agent-builder` - 에이전트/스킬 설계 및 생성

### Skills
- `/review` - 코드 리뷰 (파일/디렉토리/PR/git diff 대상)
- `/readme` - 프로젝트 분석 후 README.md 자동 생성
- `/notion-guide` - Notion MCP 블록 타입별 레퍼런스
- `/create-agent` - 새 에이전트 생성
- `/create-skill` - 새 스킬 생성

## laravel 포함 기능

### Agents
- `figma` - Figma 디자인 기반 UI 구현
- `test` - E2E 시나리오 작성, API 테스트
