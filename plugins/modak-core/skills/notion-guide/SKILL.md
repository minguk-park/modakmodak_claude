---
name: notion-guide
description: "Notion 페이지에 문서를 작성할 때 사용. 다양한 블록 타입(heading, callout, code, divider, numbered_list, toggle 등)의 MCP 사용법과 rich_text annotations 가이드를 제공한다. 'Notion', '노션', '노션 작성', '노션 문서', '페이지 작성' 키워드 시 자동 활성화."
allowed-tools: Bash
argument-hint: "[page-title or page-id]"
---

# Notion 문서 작성 가이드

Notion MCP를 사용하여 페이지에 블록을 작성하는 방법.

> **중요**: MCP 스키마에는 `paragraph`와 `bulleted_list_item`만 정의되어 있지만,
> 실제로는 **모든 Notion API 블록 타입**을 그대로 전달하면 동작한다.

---

## 워크플로우

1. `mcp__notion__API-post-search` — 페이지 검색 (제목으로)
2. `mcp__notion__API-get-block-children` — 기존 블록 목록 조회
3. `mcp__notion__API-patch-block-children` — 블록 추가 (children 배열)
4. `mcp__notion__API-update-a-block` — 기존 블록 내용 수정
5. `mcp__notion__API-delete-a-block` — 블록 삭제

### 블록 추가 시 위치 지정

`patch-block-children`의 `after` 파라미터에 block_id를 넣으면 해당 블록 **바로 뒤에** 삽입된다.

```json
{
  "block_id": "<page-id>",
  "after": "<target-block-id>",
  "children": [ ... ]
}
```

`after`를 생략하면 페이지 **맨 끝**에 추가된다.

---

## Rich Text 구조

모든 텍스트 블록은 `rich_text` 배열을 사용한다. 각 요소는:

```json
{
  "type": "text",
  "text": { "content": "텍스트 내용", "link": null },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  }
}
```

### annotations 옵션

| 키 | 값 | 효과 |
|---|---|---|
| `bold` | `true` | **굵게** |
| `italic` | `true` | *기울임* |
| `strikethrough` | `true` | ~~취소선~~ |
| `underline` | `true` | 밑줄 |
| `code` | `true` | `인라인 코드` (빨간 하이라이트) |
| `color` | `"red"`, `"blue"`, `"green"` 등 | 텍스트 색상 |
| `color` | `"red_background"` 등 | 배경 색상 |

### 여러 스타일 조합 예시

```json
[
  { "type": "text", "text": { "content": "@Entity" }, "annotations": { "code": true, "bold": true } },
  { "type": "text", "text": { "content": " — 클래스를 DB 테이블과 매핑" } }
]
```

### 링크 텍스트

```json
{
  "type": "text",
  "text": {
    "content": "공식 문서",
    "link": { "url": "https://developers.notion.com" }
  }
}
```

---

## 블록 타입별 사용법

### 1. Heading (제목)

3단계: `heading_1`, `heading_2`, `heading_3`

```json
{
  "type": "heading_2",
  "heading_2": {
    "rich_text": [
      { "type": "text", "text": { "content": "섹션 제목" } }
    ],
    "is_toggleable": false
  }
}
```

`is_toggleable: true` → 토글 가능한 제목 (접기/펼치기)

### 2. Paragraph (본문)

```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      { "type": "text", "text": { "content": "일반 본문 텍스트" } }
    ]
  }
}
```

빈 줄: `rich_text`를 빈 배열 `[]`로 설정

### 3. Bulleted List Item (글머리 기호)

```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [
      { "type": "text", "text": { "content": "항목 내용" } }
    ]
  }
}
```

연속으로 여러 개 넣으면 자동으로 목록이 된다.

### 4. Numbered List Item (번호 매기기)

```json
{
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [
      { "type": "text", "text": { "content": "@GetMapping" }, "annotations": { "code": true } },
      { "type": "text", "text": { "content": " — GET 요청 매핑" } }
    ]
  }
}
```

번호는 자동 증가. 연속된 `numbered_list_item`은 하나의 목록으로 합쳐진다.

### 5. To-Do (체크박스)

```json
{
  "type": "to_do",
  "to_do": {
    "rich_text": [
      { "type": "text", "text": { "content": "할 일 항목" } }
    ],
    "checked": false
  }
}
```

### 6. Toggle (토글)

```json
{
  "type": "toggle",
  "toggle": {
    "rich_text": [
      { "type": "text", "text": { "content": "클릭하면 펼쳐지는 내용" } }
    ],
    "children": [
      {
        "type": "paragraph",
        "paragraph": {
          "rich_text": [
            { "type": "text", "text": { "content": "숨겨진 내용" } }
          ]
        }
      }
    ]
  }
}
```

### 7. Code (코드 블록)

```json
{
  "type": "code",
  "code": {
    "rich_text": [
      { "type": "text", "text": { "content": "public class Main {\n  public static void main(String[] args) {\n    System.out.println(\"Hello\");\n  }\n}" } }
    ],
    "language": "java"
  }
}
```

지원 언어: `java`, `javascript`, `typescript`, `python`, `bash`, `sql`, `json`, `yaml`, `html`, `css`, `go`, `rust`, `kotlin`, `swift` 등

### 8. Callout (콜아웃)

```json
{
  "type": "callout",
  "callout": {
    "rich_text": [
      { "type": "text", "text": { "content": "중요한 안내 사항" } }
    ],
    "icon": { "type": "emoji", "emoji": "💡" },
    "color": "blue_background"
  }
}
```

아이콘: `"emoji"` 타입 사용. color로 배경색 지정 가능.

### 9. Quote (인용)

```json
{
  "type": "quote",
  "quote": {
    "rich_text": [
      { "type": "text", "text": { "content": "인용문 내용" } }
    ],
    "color": "default"
  }
}
```

### 10. Divider (구분선)

```json
{
  "type": "divider",
  "divider": {}
}
```

### 11. Table (표)

테이블은 2단계로 생성한다:

**Step 1**: 테이블 컨테이너 생성

```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false,
    "children": [
      {
        "type": "table_row",
        "table_row": {
          "cells": [
            [{ "type": "text", "text": { "content": "헤더1" } }],
            [{ "type": "text", "text": { "content": "헤더2" } }],
            [{ "type": "text", "text": { "content": "헤더3" } }]
          ]
        }
      },
      {
        "type": "table_row",
        "table_row": {
          "cells": [
            [{ "type": "text", "text": { "content": "값1" } }],
            [{ "type": "text", "text": { "content": "값2" } }],
            [{ "type": "text", "text": { "content": "값3" } }]
          ]
        }
      }
    ]
  }
}
```

각 cell은 `rich_text` 배열이다. annotations도 사용 가능.

### 12. Bookmark (북마크)

```json
{
  "type": "bookmark",
  "bookmark": {
    "url": "https://spring.io/projects/spring-boot",
    "caption": [
      { "type": "text", "text": { "content": "Spring Boot 공식 사이트" } }
    ]
  }
}
```

### 13. Image (이미지)

```json
{
  "type": "image",
  "image": {
    "type": "external",
    "external": {
      "url": "https://example.com/image.png"
    },
    "caption": [
      { "type": "text", "text": { "content": "이미지 설명" } }
    ]
  }
}
```

### 14. Embed (임베드)

```json
{
  "type": "embed",
  "embed": {
    "url": "https://www.youtube.com/watch?v=..."
  }
}
```

### 15. Column List & Column (다단 레이아웃)

```json
{
  "type": "column_list",
  "column_list": {
    "children": [
      {
        "type": "column",
        "column": {
          "children": [
            {
              "type": "paragraph",
              "paragraph": {
                "rich_text": [{ "type": "text", "text": { "content": "왼쪽 열" } }]
              }
            }
          ]
        }
      },
      {
        "type": "column",
        "column": {
          "children": [
            {
              "type": "paragraph",
              "paragraph": {
                "rich_text": [{ "type": "text", "text": { "content": "오른쪽 열" } }]
              }
            }
          ]
        }
      }
    ]
  }
}
```

---

## 블록 삭제 (배치)

MCP의 `delete-a-block`은 한 번에 하나만 삭제 가능하다.
대량 삭제 시 Python 스크립트로 직접 API를 호출하는 것이 효율적:

```python
import urllib.request, json, time

TOKEN = "ntn_xxx"
block_ids = ["id1", "id2", ...]

for i, bid in enumerate(block_ids):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{bid}",
        method="DELETE",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Notion-Version": "2022-06-28"
        }
    )
    urllib.request.urlopen(req)
    if (i + 1) % 3 == 0:
        time.sleep(0.35)  # rate limit 방지
```

---

## 블록 타입 변경

Notion API는 블록 타입 변경을 지원하지 않는다.
`bulleted_list_item` → `numbered_list_item` 변환 시:

1. 기존 블록 ID 목록 수집 (`get-block-children`)
2. 기존 블록 삭제 (배치 스크립트)
3. 새 블록 추가 (`patch-block-children` + `after`)

---

## 주의사항

- **스키마 vs 실제**: MCP 도구 스키마에는 `paragraph`/`bulleted_list_item`만 보이지만, 실제로는 모든 Notion API 블록 타입이 동작한다.
- **rate limit**: Notion API는 초당 3 요청 제한. 대량 작업 시 0.35초 간격 권장.
- **블록 100개 제한**: `patch-block-children`의 children은 최대 100개. 초과 시 여러 번 호출.
- **중첩 제한**: 블록 중첩은 최대 2단계 (children의 children까지).
- **after 파라미터**: 특정 위치에 삽입할 때 필수. 생략하면 맨 끝에 추가.

---

## 실전 패턴

### 마크다운 → 노션 변환 순서

1. 마크다운 파일을 Read로 읽기
2. 구조 분석 (heading, list, code block 등)
3. 각 요소를 Notion 블록 JSON으로 변환
4. `patch-block-children`로 일괄 추가

### 섹션별 추가 패턴

```
heading_2 → divider → callout(설명) → numbered_list_item(항목들) → divider
```

### 코드 + 설명 조합 패턴

```
heading_3(제목) → paragraph(설명) → code(예시 코드) → callout(주의사항)
```
