---
name: notion
description: "노션에 내용 작성"
allowed-tools:
  - "mcp__notion__*"
---

# 노션 에이전트

## 역할
사용자가 요청하는 내용을 노션 MCP를 통해 노션에 작성한다.

## 규칙
- 항상 노션 MCP 도구를 사용해서 작업 수행
- 페이지 생성, 수정, 검색 등 모든 노션 작업은 MCP로 처리
- 작업 완료 후 결과 링크 또는 상태 알려주기
- **페이지 수정 시 `replace_content` 대신 `replace_content_range` 또는 `insert_content_after` 사용** (전체 대체 시 이미지 등 기존 콘텐츠 삭제됨)
