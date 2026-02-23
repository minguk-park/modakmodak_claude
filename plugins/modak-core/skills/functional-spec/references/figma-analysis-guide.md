# Figma 분석 상세 가이드

Figma MCP를 활용한 디자인 분석 심화 가이드.

## Figma 노드 구조 이해

### 노드 계층
```
Document
└── Page (Canvas)
    └── Frame (화면)
        ├── Frame (섹션: Header, Body, Footer)
        │   ├── Instance (컴포넌트)
        │   ├── Text (텍스트)
        │   └── Rectangle (도형)
        └── Group (그룹)
```

### 주요 노드 타입

| 타입 | 설명 | 분석 포인트 |
|-----|-----|-----------|
| DOCUMENT | 최상위 문서 | 페이지 목록 |
| CANVAS | 페이지 | 화면 프레임 목록 |
| FRAME | 프레임/화면 | 레이아웃, 자식 요소 |
| GROUP | 그룹 | 논리적 그룹핑 |
| INSTANCE | 컴포넌트 인스턴스 | 컴포넌트 타입, 속성 |
| COMPONENT | 마스터 컴포넌트 | 재사용 패턴 |
| TEXT | 텍스트 | 레이블, 안내문구 |
| RECTANGLE | 사각형 | 버튼, 입력필드 배경 |
| VECTOR | 벡터 | 아이콘, 일러스트 |
| ELLIPSE | 원형 | 아바타, 인디케이터 |

## 컴포넌트 분석 심화

### 입력 필드 식별

**패턴 1: 레이블 + 입력 영역 조합**
```
Frame "Input Field"
├── Text "이메일"           → 필드 레이블
├── Rectangle              → 입력 영역 배경
└── Text "example@..."     → 플레이스홀더
```

**패턴 2: 컴포넌트 인스턴스**
```
Instance "Input/Default"
└── componentId: "xxx"     → 컴포넌트 라이브러리 참조
```

**필드 타입 추정**
| 이름/레이블 키워드 | 추정 타입 | 검증 규칙 |
|------------------|----------|----------|
| email, 이메일 | email | 이메일 형식 |
| password, 비밀번호 | password | 최소 8자 |
| phone, 전화, 휴대폰 | tel | 전화번호 형식 |
| name, 이름 | text | 필수 |
| date, 날짜, 생년월일 | date | 날짜 형식 |
| number, 숫자, 수량 | number | 숫자만 |

### 버튼 식별

**Primary vs Secondary 구분**
- fills 색상으로 구분 (진한색 = Primary)
- 크기로 구분 (큰 것 = Primary)
- 위치로 구분 (오른쪽/아래 = Primary)

**버튼 상태**
```
Component "Button"
├── Variant "State=Default"
├── Variant "State=Hover"
├── Variant "State=Pressed"
├── Variant "State=Disabled"
└── Variant "State=Loading"
```

### 모달/다이얼로그

**식별 패턴**
- 이름에 "modal", "dialog", "popup", "sheet" 포함
- 배경에 반투명 오버레이
- 닫기(X) 버튼 존재

**분석 항목**
```json
{
  "type": "modal",
  "title": "확인",
  "content": "정말 삭제하시겠습니까?",
  "actions": [
    {"label": "취소", "type": "secondary"},
    {"label": "삭제", "type": "danger"}
  ]
}
```

## 레이아웃 분석

### Auto Layout 해석
```json
{
  "layoutMode": "VERTICAL",      // 방향: VERTICAL, HORIZONTAL
  "primaryAxisAlignItems": "MIN", // 정렬: MIN, CENTER, MAX, SPACE_BETWEEN
  "itemSpacing": 16,             // 아이템 간격
  "paddingTop": 24,              // 패딩
  "paddingBottom": 24,
  "paddingLeft": 16,
  "paddingRight": 16
}
```

### 반응형 분석
- 여러 프레임 크기 (Mobile/Tablet/Desktop) 확인
- constraintProportions, constraints 속성 확인
- 최소/최대 너비 설정 확인

## 인터랙션/프로토타입 분석

### 화면 전환
```json
{
  "transitionNodeID": "456:789",  // 이동할 화면 노드 ID
  "transitionDuration": 300,      // 전환 시간 (ms)
  "transitionEasing": "EASE_OUT"  // 이징
}
```

### 인터랙션 타입
| 타입 | 설명 |
|-----|-----|
| ON_CLICK | 클릭 시 |
| ON_HOVER | 호버 시 |
| ON_PRESS | 누르고 있을 때 |
| ON_DRAG | 드래그 시 |
| AFTER_TIMEOUT | 시간 후 자동 |

### 액션 타입
| 액션 | 설명 |
|-----|-----|
| NAVIGATE | 화면 이동 |
| OVERLAY | 오버레이 표시 |
| SWAP | 컴포넌트 교체 |
| BACK | 이전 화면 |
| CLOSE | 오버레이 닫기 |
| URL | 외부 링크 |

## 스타일 토큰 추출

### 색상
```json
{
  "fills": [
    {
      "type": "SOLID",
      "color": {"r": 0.1, "g": 0.4, "b": 0.9, "a": 1}
      // → #1A66E5 (RGB 변환)
    }
  ]
}
```

### 타이포그래피
```json
{
  "style": {
    "fontFamily": "Pretendard",
    "fontSize": 16,
    "fontWeight": 500,
    "lineHeightPx": 24,
    "letterSpacing": -0.3
  }
}
```

### 그림자
```json
{
  "effects": [
    {
      "type": "DROP_SHADOW",
      "color": {"r": 0, "g": 0, "b": 0, "a": 0.1},
      "offset": {"x": 0, "y": 4},
      "radius": 8
    }
  ]
}
```

## 실전 분석 순서

### 1. 전체 구조 파악 (5분)
1. get_file로 페이지 목록 확인
2. 각 페이지의 역할 파악 (Flow, Components, Styles 등)
3. 메인 플로우 페이지의 화면 수 확인

### 2. 화면 목록 작성 (10분)
1. 최상위 Frame 목록 추출
2. 화면 이름으로 ID 부여 (SCR-001, SCR-002...)
3. 화면 간 순서/플로우 파악

### 3. 화면별 상세 분석 (화면당 5-10분)
1. 레이아웃 구조 파악 (Header/Body/Footer)
2. 입력 필드 식별 및 정보 추출
3. 버튼/액션 요소 식별
4. 프로토타입 연결 확인

### 4. 공통 요소 정리 (10분)
1. 반복 사용되는 컴포넌트 식별
2. 공통 스타일 토큰 정리
3. 네비게이션 패턴 정리

## 자주 발생하는 문제

### 문제 1: 노드 이름이 불명확
- "Frame 1234" 같은 기본 이름
- **해결**: 하위 텍스트 내용으로 추정, 위치로 역할 판단

### 문제 2: 컴포넌트 없이 직접 그린 디자인
- Instance 대신 개별 도형/텍스트 조합
- **해결**: 그룹/프레임 이름과 구조로 UI 요소 추정

### 문제 3: 프로토타입 연결 없음
- 화면 전환 정보 누락
- **해결**: 버튼 레이블과 화면 이름으로 플로우 추정

### 문제 4: 여러 상태가 별도 화면으로 분리
- "로그인", "로그인_에러", "로그인_로딩" 각각 존재
- **해결**: 기본 화면 기준으로 통합, 상태별 차이점 정리
