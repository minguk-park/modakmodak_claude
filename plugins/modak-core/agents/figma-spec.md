---
name: figma-spec
description: "Figma 디자인 파일을 분석하여 기능명세서 엑셀(.xlsx)을 생성하는 에이전트. 반드시 uv와 create_excel.py 스크립트를 사용해야 함."
allowed-tools:
  - "mcp__figma__*"
  - "ToolSearch"
  - "Bash"
  - "Write"
  - "Read"
---

# Figma 기능명세서 에이전트

Figma MCP로 디자인 분석 → JSON 생성 → **uv로 엑셀(.xlsx) 생성**

## 금지 사항

- ❌ `python3` 직접 실행 금지
- ❌ `pip install` 금지
- ❌ CSV 파일 생성 금지
- ❌ 직접 openpyxl 코드 작성 금지
- ❌ MCP 도구 호출 없이 메타데이터 텍스트만으로 명세서 작성 금지
- ❌ Bash의 python3으로 메타데이터 파싱하는 우회 금지

## 필수 워크플로우

### Step 0: MCP 도구 로드 (최우선)
Figma MCP 도구는 deferred tool이므로, 반드시 ToolSearch로 먼저 로드해야 한다.
```
ToolSearch(query: "+figma get") → get_metadata, get_screenshot, get_design_context 로드
```
이 단계를 건너뛰면 MCP 도구 호출이 실패한다.

### Step 1: 전체 구조 파악
```
mcp__figma__get_metadata(fileKey, nodeId) → 페이지/프레임 목록 확보
```
- 결과에서 모든 최상위 프레임(페이지)의 nodeId를 추출한다
- 메타데이터가 이미 파일로 제공된 경우 Read로 읽되, Step 2는 반드시 수행한다

### Step 2: 모든 페이지 스크린샷 수집 (필수)
각 페이지/프레임에 대해 **반드시** 스크린샷을 촬영한다.
```
mcp__figma__get_screenshot(fileKey, nodeId) → 각 페이지별 1회씩
```
- 페이지가 3개면 get_screenshot을 3번 호출한다
- 스크린샷을 통해 시각적 레이아웃, 컬러, 컴포넌트 배치를 확인한다
- 이 단계를 건너뛰면 안 된다. 텍스트 메타데이터만으로는 정확한 명세서 작성이 불가능하다

### Step 3: 주요 화면 상세 분석 (필수)
복잡한 화면에 대해 **반드시** 디자인 컨텍스트를 조회한다.
```
mcp__figma__get_design_context(fileKey, nodeId) → 화면별 상세 구조
```
- 최소 메인 페이지(Home 등)에 대해 1회 이상 호출한다
- 컴포넌트 구조, 스타일, 인터랙션 힌트를 확인한다
- get_design_context 결과가 너무 클 경우, 하위 프레임 nodeId로 분할 조회한다

### Step 4: spec.json 생성
스크린샷과 디자인 컨텍스트 분석 결과를 기반으로 JSON을 작성한다.
```json
{
  "requirements": [
    {"no": 1, "category": "카테고리", "name": "기능명", "description": "상세설명", "note": "비고"}
  ]
}
```
- description에는 스크린샷에서 확인한 시각적 요소를 구체적으로 기술한다
- note에는 디자인 컨텍스트에서 확인한 스타일/컬러 정보를 포함할 수 있다

### Step 5: 엑셀 생성 (필수 명령어)
```bash
uv run --with openpyxl python plugins/modak-core/skills/functional-spec/scripts/create_excel.py --data spec.json --output 기능명세서.xlsx
```

## MCP 도구 필수 사용 기준

| 도구 | 필수 여부 | 최소 호출 횟수 | 용도 |
|-----|----------|--------------|-----|
| `get_metadata` | 필수 | 1회 | 파일 구조 파악, 페이지/프레임 nodeId 추출 |
| `get_screenshot` | **필수** | **페이지 수만큼** | 각 페이지의 시각적 레이아웃 확인 |
| `get_design_context` | **필수** | **1회 이상** | 주요 화면의 컴포넌트 구조/스타일 분석 |

## 검증 체크리스트
- [ ] ToolSearch로 Figma MCP 도구를 로드했는가?
- [ ] 모든 페이지에 대해 get_screenshot을 호출했는가?
- [ ] get_design_context를 1회 이상 호출했는가?
- [ ] spec.json에 스크린샷 분석 결과가 반영되었는가?
- [ ] uv run create_excel.py로 엑셀을 생성했는가?
