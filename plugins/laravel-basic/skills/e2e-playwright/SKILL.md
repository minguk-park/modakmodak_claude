---
name: e2e-playwright
description: "작성된 E2E 시나리오를 기반으로 Playwright MCP를 이용해 실제 브라우저 E2E 테스트를 수행한다. 'Playwright', '브라우저 테스트', 'E2E 실행', 'e2e test' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - "mcp__playwright__*"
---

# Playwright E2E 테스트 스킬

작성된 E2E 시나리오 문서를 기반으로 Playwright MCP를 이용하여 실제 브라우저에서 E2E 테스트를 수행한다.

## 워크플로우

```
Step 1: 시나리오 문서 로드 및 파싱
Step 2: 테스트 환경 확인 (서버 실행 여부)
Step 3: Playwright MCP로 브라우저 테스트 실행
Step 4: 스크린샷 캡처 및 결과 수집
Step 5: 테스트 리포트 생성
```

## Step 1: 시나리오 문서 로드

E2E 시나리오 문서를 읽어 테스트 대상을 파악한다:

```bash
# 시나리오 문서 위치
tests/scenarios/e2e-scenarios.md
```

시나리오 문서가 없으면 `/e2e-scenario` 스킬을 먼저 실행하도록 안내한다.

## Step 2: 테스트 환경 확인

### 서버 실행 확인

```bash
# Laravel 서버 확인
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000
```

서버가 실행 중이 아니면 사용자에게 안내한다:
```
⚠️ 서버가 실행되지 않고 있습니다.
다른 터미널에서 아래 명령어로 서버를 실행해주세요:
php artisan serve
```

### 앱 URL 확인

```bash
# .env에서 APP_URL 확인
grep APP_URL .env
```

## Step 3: Playwright MCP 브라우저 테스트

### 기본 테스트 패턴

각 시나리오를 아래 순서로 실행한다:

#### 1. 페이지 이동
```
mcp__playwright__browser_navigate → 대상 URL 접속
mcp__playwright__browser_snapshot → 페이지 상태 확인
```

#### 2. 요소 확인 및 인터랙션
```
mcp__playwright__browser_snapshot → 페이지 요소 목록 확인 (ref 값 획득)
mcp__playwright__browser_click → 버튼/링크 클릭
mcp__playwright__browser_type → 텍스트 입력
mcp__playwright__browser_fill_form → 폼 작성
mcp__playwright__browser_select_option → 셀렉트 박스 선택
```

#### 3. 결과 검증
```
mcp__playwright__browser_snapshot → 변경된 상태 확인
mcp__playwright__browser_take_screenshot → 스크린샷 캡처
mcp__playwright__browser_console_messages → 콘솔 에러 확인
mcp__playwright__browser_network_requests → 네트워크 요청 확인
```

### 시나리오별 테스트 패턴

#### 인증 테스트 (로그인)
```
1. browser_navigate → /login 접속
2. browser_snapshot → 로그인 폼 확인
3. browser_fill_form → 이메일, 비밀번호 입력
4. browser_click → 로그인 버튼 클릭
5. browser_wait_for → 대시보드 텍스트 확인
6. browser_snapshot → 로그인 후 상태 확인
7. browser_take_screenshot → 결과 캡처
```

#### CRUD 테스트 (생성)
```
1. browser_navigate → /[resource]/create 접속
2. browser_snapshot → 생성 폼 확인
3. browser_fill_form → 필드 입력
4. browser_click → 저장 버튼 클릭
5. browser_wait_for → 성공 메시지 확인
6. browser_snapshot → 생성된 데이터 확인
7. browser_take_screenshot → 결과 캡처
```

#### CRUD 테스트 (목록 조회)
```
1. browser_navigate → /[resource] 접속
2. browser_snapshot → 목록 테이블/카드 확인
3. browser_take_screenshot → 목록 화면 캡처
```

#### 유효성 검증 테스트
```
1. browser_navigate → /[resource]/create 접속
2. browser_click → 빈 폼으로 저장 클릭
3. browser_snapshot → 에러 메시지 확인
4. browser_take_screenshot → 에러 상태 캡처
```

#### 다이얼로그 처리
```
1. browser_click → 삭제 버튼 클릭
2. browser_handle_dialog → 확인 다이얼로그 승인/거절
3. browser_snapshot → 결과 확인
```

## Step 4: 스크린샷 관리

스크린샷을 체계적으로 저장한다:

```
tests/screenshots/
├── auth/
│   ├── login-form.png
│   ├── login-success.png
│   └── login-fail.png
├── [resource]/
│   ├── list.png
│   ├── create-form.png
│   ├── create-success.png
│   ├── edit-form.png
│   └── delete-confirm.png
└── errors/
    └── validation-error.png
```

스크린샷 파일명 규칙: `{기능}-{상태}.png`

## Step 5: 테스트 리포트

### 리포트 형식

```markdown
# E2E 테스트 리포트

## 실행 정보
- 실행일시: [날짜/시간]
- 대상 URL: [APP_URL]
- 브라우저: Chromium (Playwright)

## 테스트 결과 요약

| 시나리오 | 결과 | 스크린샷 | 비고 |
|---------|------|---------|------|
| 로그인 (정상) | ✅ Pass | auth/login-success.png | - |
| 로그인 (실패) | ✅ Pass | auth/login-fail.png | 에러 메시지 표시 확인 |
| 목록 조회 | ✅ Pass | resource/list.png | 3건 표시 |
| 생성 | ✅ Pass | resource/create-success.png | DB 반영 확인 |
| 수정 | ❌ Fail | resource/edit-form.png | 저장 버튼 미반응 |
| 삭제 | ✅ Pass | resource/delete-confirm.png | 다이얼로그 정상 |
| 유효성 검증 | ✅ Pass | errors/validation-error.png | 에러 메시지 5건 |

**결과**: 6/7 통과 (85.7%)

## 실패 상세

### 수정 기능 실패
- **증상**: 저장 버튼 클릭 후 반응 없음
- **콘솔 에러**: `TypeError: Cannot read property 'id' of undefined`
- **네트워크**: PUT /api/resources/1 요청 발생하지 않음
- **원인 추정**: JS 이벤트 핸들러 미바인딩
- **스크린샷**: resource/edit-form.png

## 콘솔 에러 로그
- [에러가 있으면 기록]

## 네트워크 이슈
- [실패한 요청이 있으면 기록]
```

### 리포트 저장

```
tests/reports/
└── e2e-report-[date].md
```

## 사용법

```
/e2e-playwright                     # 전체 시나리오 기반 E2E 테스트
/e2e-playwright 인증                 # 인증 관련 시나리오만 테스트
/e2e-playwright http://localhost:3000  # 특정 URL 대상 테스트
```

`$ARGUMENTS`로 특정 시나리오나 URL을 지정할 수 있다.

## 주의사항

1. **서버 실행 필수**: 테스트 전 반드시 대상 서버가 실행 중이어야 한다
2. **시나리오 먼저**: 시나리오 문서가 없으면 `/e2e-scenario`를 먼저 안내한다
3. **snapshot 우선**: 스크린샷보다 `browser_snapshot`을 먼저 사용해 요소 ref를 파악한다
4. **대기 처리**: 페이지 전환/AJAX 후에는 `browser_wait_for`로 대기한다
5. **에러 수집**: 테스트 중 콘솔 에러와 네트워크 실패를 반드시 수집한다
6. **브라우저 정리**: 테스트 완료 후 `browser_close`로 브라우저를 닫는다
7. **SPA 대응**: Inertia.js 등 SPA 사용 시 페이지 전환 대기를 추가한다
