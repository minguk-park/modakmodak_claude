---
name: functional-spec
description: "Figma 분석 결과로 기능명세서 엑셀 생성. '기능명세서', '기능정의서', '화면정의서', '스펙문서', '엑셀' 키워드 시 자동 활성화. @figma-spec 에이전트와 함께 사용."
---

# 기능명세서 스킬

Figma 디자인 분석 → JSON → 엑셀 변환 워크플로우.

## 워크플로우

```
Step 1: @figma-spec으로 Figma 분석
Step 2: requirements 형식으로 JSON 생성
Step 3: uv로 엑셀 생성
```

## JSON 형식 (필수)

엑셀 스크립트와 호환되는 형식:

```json
{
  "requirements": [
    {
      "no": 1,
      "category": "인증",
      "name": "회원가입",
      "description": "1. 이메일, 이름 입력\n2. 중복 체크",
      "note": ""
    },
    {
      "no": 2,
      "category": "인증",
      "name": "로그인",
      "description": "1. 이메일/비밀번호 입력\n2. 실패 시 에러 표시",
      "note": ""
    }
  ]
}
```

| 필드 | 설명 |
|-----|-----|
| `no` | 기능 번호 (1, 2, 3...) |
| `category` | 화면/기능 카테고리 (인증, 홈, 마이페이지) |
| `name` | 기능명 |
| `description` | 상세 설명 (줄바꿈: \n) |
| `note` | 비고 |

## 스크립트 실행

**중요**: pip install 금지. macOS에서 에러 발생. 반드시 uv 사용.

### 엑셀 생성
```bash
# JSON → 엑셀
uv run --with openpyxl python plugins/laravel-basic/skills/functional-spec/scripts/create_excel.py --data spec.json --output 기능명세서.xlsx

# 샘플 생성
uv run --with openpyxl python plugins/laravel-basic/skills/functional-spec/scripts/create_excel.py --sample --output sample.xlsx
```

### Figma 데이터 파싱
```bash
uv run python plugins/laravel-basic/skills/functional-spec/scripts/parse_figma.py --input figma.json --output spec.json
```

## 엑셀 출력

| 열 | 내용 |
|---|-----|
| 번호 | 기능 번호 |
| 카테고리 | 화면/기능 분류 |
| 기능/요구사항명 | 기능명 |
| 상세설명 | 구체적 기능 설명 |
| 비고 | 참고사항 |

## 주의사항

1. **pip 사용 금지** - `externally-managed-environment` 에러 발생
2. **uv 필수** - `uv run --with openpyxl` 형식으로 실행
3. **JSON 형식** - requirements 배열 형식 준수

## 상세 가이드

Figma 노드 분석, 컴포넌트 식별 패턴: [references/figma-analysis-guide.md](references/figma-analysis-guide.md)
