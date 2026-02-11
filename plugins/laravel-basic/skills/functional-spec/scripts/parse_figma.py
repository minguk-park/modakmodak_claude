#!/usr/bin/env python3
"""
Figma 노드 데이터를 요구사항 명세서 JSON으로 변환

사용법:
    python parse_figma.py --input figma_data.json --output spec.json
    cat figma_data.json | python parse_figma.py --output spec.json
"""

import json
import argparse
import re
import sys
from datetime import datetime
from typing import Any


# 컴포넌트 타입 식별 패턴
FIELD_PATTERNS = {
    "email": (r"email|이메일|메일", "email", "이메일 형식"),
    "password": (r"password|비밀번호|패스워드", "password", "최소 8자"),
    "phone": (r"phone|전화|휴대폰|연락처", "tel", "전화번호 형식"),
    "name": (r"name|이름|성명", "text", "필수"),
    "date": (r"date|날짜|생년월일", "date", "날짜 형식"),
    "number": (r"number|숫자|수량|금액", "number", "숫자만"),
    "search": (r"search|검색", "search", ""),
    "textarea": (r"textarea|내용|메시지|설명|비고", "textarea", ""),
}

BUTTON_PATTERNS = {
    "primary": r"primary|주요|확인|저장|등록|로그인|가입|제출|완료",
    "secondary": r"secondary|취소|닫기|이전|뒤로",
    "danger": r"danger|삭제|제거|탈퇴",
}

COMPONENT_PATTERNS = {
    "input": r"input|field|text|입력",
    "button": r"button|btn|cta|버튼",
    "checkbox": r"checkbox|check|체크",
    "radio": r"radio|option|라디오",
    "select": r"select|dropdown|드롭다운|선택",
    "modal": r"modal|dialog|popup|sheet|모달|팝업",
    "card": r"card|카드",
    "nav": r"nav|menu|header|footer|네비|메뉴|헤더|푸터",
    "tab": r"tab|탭",
    "list": r"list|리스트|목록",
}


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """RGB 0-1 값을 HEX로 변환"""
    return "#{:02x}{:02x}{:02x}".format(
        int(r * 255), int(g * 255), int(b * 255)
    ).upper()


def identify_field_type(name: str) -> tuple[str, str, str]:
    """필드 이름으로 타입 추정"""
    name_lower = name.lower()
    for field_type, (pattern, html_type, validation) in FIELD_PATTERNS.items():
        if re.search(pattern, name_lower, re.IGNORECASE):
            return field_type, html_type, validation
    return "text", "text", ""


def identify_button_type(name: str) -> str:
    """버튼 이름으로 타입 추정"""
    name_lower = name.lower()
    for btn_type, pattern in BUTTON_PATTERNS.items():
        if re.search(pattern, name_lower, re.IGNORECASE):
            return btn_type
    return "primary"


def identify_component_type(name: str) -> str | None:
    """노드 이름으로 컴포넌트 타입 추정"""
    name_lower = name.lower()
    for comp_type, pattern in COMPONENT_PATTERNS.items():
        if re.search(pattern, name_lower, re.IGNORECASE):
            return comp_type
    return None


def has_required_marker(node: dict, siblings: list) -> bool:
    """필수 표시(*) 여부 확인"""
    # 노드 이름에 * 포함
    if "*" in node.get("name", ""):
        return True

    # 형제 노드 중 * 텍스트 존재
    for sibling in siblings:
        if sibling.get("type") == "TEXT":
            chars = sibling.get("characters", "")
            if chars.strip() == "*":
                return True

    return False


def extract_placeholder(node: dict) -> str:
    """플레이스홀더 텍스트 추출"""
    if node.get("type") == "TEXT":
        return node.get("characters", "")

    for child in node.get("children", []):
        if child.get("type") == "TEXT":
            text = child.get("characters", "")
            # 레이블이 아닌 플레이스홀더 추정
            if len(text) > 5 or "@" in text or "..." in text:
                return text

    return ""


def extract_fields(node: dict, parent_children: list = None) -> list[dict]:
    """입력 필드 추출"""
    fields = []
    node_name = node.get("name", "")
    node_type = node.get("type", "")

    comp_type = identify_component_type(node_name)

    if comp_type == "input" or (node_type == "INSTANCE" and "input" in node_name.lower()):
        field_type, html_type, validation = identify_field_type(node_name)

        # 레이블 찾기
        label = node_name
        for child in node.get("children", []):
            if child.get("type") == "TEXT":
                text = child.get("characters", "")
                if len(text) < 20 and not "@" in text:
                    label = text
                    break

        fields.append({
            "name": label,
            "type": html_type,
            "required": has_required_marker(node, parent_children or []),
            "validation": validation,
            "error_message": f"올바른 {label}을(를) 입력해주세요" if validation else "",
            "placeholder": extract_placeholder(node),
            "figma_node_id": node.get("id", ""),
        })

    # 재귀 탐색
    children = node.get("children", [])
    for child in children:
        fields.extend(extract_fields(child, children))

    return fields


def extract_buttons(node: dict) -> list[dict]:
    """버튼 추출"""
    buttons = []
    node_name = node.get("name", "")
    node_type = node.get("type", "")

    comp_type = identify_component_type(node_name)

    if comp_type == "button" or (node_type == "INSTANCE" and "button" in node_name.lower()):
        # 버튼 레이블 찾기
        label = node_name
        for child in node.get("children", []):
            if child.get("type") == "TEXT":
                label = child.get("characters", "")
                break

        btn_type = identify_button_type(label)

        # 프로토타입 연결 확인
        transition = node.get("transitionNodeID")

        buttons.append({
            "label": label,
            "type": btn_type,
            "action": "navigate" if transition else "submit",
            "target": transition,
            "figma_node_id": node.get("id", ""),
        })

    # 재귀 탐색
    for child in node.get("children", []):
        buttons.extend(extract_buttons(child))

    return buttons


def extract_texts(node: dict) -> list[str]:
    """텍스트 내용 추출"""
    texts = []

    if node.get("type") == "TEXT":
        chars = node.get("characters", "").strip()
        if chars and len(chars) > 1:
            texts.append(chars)

    for child in node.get("children", []):
        texts.extend(extract_texts(child))

    return texts


def analyze_screen(frame: dict, index: int) -> dict:
    """화면(Frame) 분석"""
    screen_id = f"SCR-{index:03d}"
    name = frame.get("name", f"화면 {index}")

    # 크기 정보
    bbox = frame.get("absoluteBoundingBox", {})
    width = bbox.get("width", 0)
    height = bbox.get("height", 0)

    # 필드 추출
    fields = extract_fields(frame)

    # 버튼 추출
    buttons = extract_buttons(frame)

    # 텍스트 추출 (설명 추정용)
    texts = extract_texts(frame)
    description = texts[0] if texts else ""

    # 기능 정의 생성
    functions = []
    for btn in buttons:
        functions.append({
            "name": btn["label"],
            "trigger": f"{btn['label']} 버튼 클릭",
            "action": "API 호출" if btn["action"] == "submit" else "화면 이동",
            "result": "성공/실패 처리",
        })

    # 네비게이션 정보
    navigation_to = []
    for btn in buttons:
        if btn.get("target"):
            navigation_to.append(btn["target"])

    # path 추정 (화면 이름 기반)
    path = "/" + re.sub(r"[^a-z0-9]", "-", name.lower()).strip("-")

    return {
        "id": screen_id,
        "name": name,
        "figma_node_id": frame.get("id", ""),
        "description": description[:100] if description else f"{name} 화면",
        "path": path,
        "purpose": "",
        "access": "",
        "size": {"width": width, "height": height},
        "fields": [
            {
                "name": f["name"],
                "type": f["type"],
                "required": f["required"],
                "validation": f["validation"],
                "error_message": f["error_message"],
            }
            for f in fields
        ],
        "functions": functions,
        "apis": [],
        "navigation": {
            "from": [],
            "to": navigation_to,
        },
    }


def find_screens(node: dict, depth: int = 0) -> list[dict]:
    """화면(최상위 Frame) 찾기"""
    screens = []

    if node.get("type") == "FRAME" and depth <= 2:
        # 최상위 또는 2단계 이내의 Frame을 화면으로 간주
        bbox = node.get("absoluteBoundingBox", {})
        width = bbox.get("width", 0)
        height = bbox.get("height", 0)

        # 화면 크기로 필터링 (너무 작은 것 제외)
        if width >= 320 and height >= 400:
            screens.append(node)
            return screens  # 하위는 탐색하지 않음

    for child in node.get("children", []):
        screens.extend(find_screens(child, depth + 1))

    return screens


def parse_figma_data(figma_data: dict, project_name: str = "", figma_url: str = "") -> dict:
    """Figma 데이터를 요구사항 명세서 JSON으로 변환"""

    # 문서 정보
    doc_name = figma_data.get("name", project_name or "프로젝트")

    # 화면 찾기
    document = figma_data.get("document", figma_data)
    screen_frames = find_screens(document)

    # 화면 분석
    screens = []
    for idx, frame in enumerate(screen_frames, start=1):
        screen = analyze_screen(frame, idx)
        screens.append(screen)

    return {
        "info": {
            "project_name": doc_name,
            "figma_url": figma_url,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "version": "v1.0",
            "author": "",
        },
        "screens": screens,
        "summary": {
            "total_screens": len(screens),
            "total_fields": sum(len(s["fields"]) for s in screens),
            "total_functions": sum(len(s["functions"]) for s in screens),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Figma 노드 데이터를 요구사항 명세서 JSON으로 변환")
    parser.add_argument("--input", "-i", help="Figma JSON 데이터 파일")
    parser.add_argument("--output", "-o", default="spec.json", help="출력 파일 경로")
    parser.add_argument("--project", "-p", default="", help="프로젝트명")
    parser.add_argument("--url", "-u", default="", help="Figma 파일 URL")
    parser.add_argument("--pretty", action="store_true", help="JSON 포맷팅")
    args = parser.parse_args()

    # 입력 데이터 읽기
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            figma_data = json.load(f)
    else:
        print("Figma JSON 데이터를 입력하세요 (Ctrl+D로 종료):", file=sys.stderr)
        figma_data = json.load(sys.stdin)

    # 변환
    spec_data = parse_figma_data(figma_data, args.project, args.url)

    # 출력
    indent = 2 if args.pretty else None
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(spec_data, f, ensure_ascii=False, indent=indent)

    print(f"변환 완료: {args.output}", file=sys.stderr)
    print(f"  - 화면 수: {spec_data['summary']['total_screens']}", file=sys.stderr)
    print(f"  - 필드 수: {spec_data['summary']['total_fields']}", file=sys.stderr)
    print(f"  - 기능 수: {spec_data['summary']['total_functions']}", file=sys.stderr)


if __name__ == "__main__":
    main()
