---
name: figma-spec
description: "Figma 디자인 파일을 분석하여 기능명세서 엑셀(.xlsx)을 생성하는 에이전트. 반드시 uv와 create_excel.py 스크립트를 사용해야 함."
allowed-tools:
  - "mcp__figma__*"
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

## 필수 워크플로우

### Step 1: Figma 분석
```
mcp__figma__get_metadata → 전체 구조 파악
```

### Step 2: spec.json 생성
```json
{
  "requirements": [
    {"no": 1, "category": "카테고리", "name": "기능명", "description": "상세설명", "note": "비고"}
  ]
}
```

### Step 3: 엑셀 생성 (필수 명령어)
```bash
uv run --with openpyxl python plugins/laravel-basic/skills/functional-spec/scripts/create_excel.py --data spec.json --output 기능명세서.xlsx
```

## MCP 도구

| 도구 | 용도 |
|-----|-----|
| `mcp__figma__get_metadata` | 파일 구조 파악 |
| `mcp__figma__get_design_context` | 화면별 상세 분석 |
| `mcp__figma__get_screenshot` | 스크린샷 |
