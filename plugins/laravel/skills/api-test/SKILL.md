---
name: api-test
description: "Laravel API 엔드포인트를 테스트하고 테스트 데이터를 정리한다. Feature Test 생성, 실행, 데이터 클린업을 수행한다. 'API 테스트', 'api test', '테스트 실행', '테스트 생성' 키워드 시 자동 활성화."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# API 테스트 스킬

Laravel Feature Test로 API 엔드포인트를 테스트하고, 테스트 생성 데이터를 정리한다.

## 워크플로우

```
Step 1: 테스트 대상 분석 (라우트, 컨트롤러, Request, Resource)
Step 2: Feature Test 파일 생성
Step 3: 테스트 실행
Step 4: 결과 확인 및 리포트
Step 5: 테스트 데이터 정리 (필요 시)
```

## Step 1: 테스트 대상 분석

테스트 대상 API의 관련 파일을 분석한다:

```bash
# 라우트 확인
routes/api.php

# 컨트롤러 코드 확인
app/Http/Controllers/Api/[Controller].php

# Form Request 확인 (유효성 규칙)
app/Http/Requests/[Request].php

# Resource 확인 (응답 형식)
app/Http/Resources/[Resource].php

# 모델 및 팩토리 확인
app/Models/[Model].php
database/factories/[Model]Factory.php

# 기존 테스트 패턴 확인
tests/Feature/
```

## Step 2: Feature Test 생성

### 테스트 파일 구조

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;

class [Model]ApiTest extends TestCase
{
    use RefreshDatabase;

    private User $user;

    protected function setUp(): void
    {
        parent::setUp();
        // 공통 테스트 데이터 설정
        $this->user = User::factory()->create();
    }

    /**
     * 목록 조회 테스트
     */
    public function test_can_list_[models](): void
    {
        // Given
        [Model]::factory()->count(3)->create();

        // When
        $response = $this->actingAs($this->user)
            ->getJson('/api/[models]');

        // Then
        $response->assertStatus(200)
            ->assertJsonStructure([
                'status',
                'data' => [
                    '*' => ['id', 'name', /* fields */]
                ]
            ]);
    }

    /**
     * 단건 조회 테스트
     */
    public function test_can_show_[model](): void
    {
        // Given
        $[model] = [Model]::factory()->create();

        // When
        $response = $this->actingAs($this->user)
            ->getJson("/api/[models]/{$[model]->id}");

        // Then
        $response->assertStatus(200)
            ->assertJsonStructure([
                'status',
                'data' => ['id', 'name', /* fields */]
            ]);
    }

    /**
     * 생성 테스트
     */
    public function test_can_create_[model](): void
    {
        // Given
        $data = [
            'name' => 'Test Name',
            // ... required fields
        ];

        // When
        $response = $this->actingAs($this->user)
            ->postJson('/api/[models]', $data);

        // Then
        $response->assertStatus(201)
            ->assertJson([
                'status' => 'success',
            ]);
        $this->assertDatabaseHas('[models]', ['name' => 'Test Name']);
    }

    /**
     * 수정 테스트
     */
    public function test_can_update_[model](): void
    {
        // Given
        $[model] = [Model]::factory()->create();
        $data = ['name' => 'Updated Name'];

        // When
        $response = $this->actingAs($this->user)
            ->putJson("/api/[models]/{$[model]->id}", $data);

        // Then
        $response->assertStatus(200);
        $this->assertDatabaseHas('[models]', ['name' => 'Updated Name']);
    }

    /**
     * 삭제 테스트
     */
    public function test_can_delete_[model](): void
    {
        // Given
        $[model] = [Model]::factory()->create();

        // When
        $response = $this->actingAs($this->user)
            ->deleteJson("/api/[models]/{$[model]->id}");

        // Then
        $response->assertStatus(200);
        $this->assertDatabaseMissing('[models]', ['id' => $[model]->id]);
    }

    /**
     * 유효성 검증 실패 테스트
     */
    public function test_create_[model]_validation_fails(): void
    {
        // Given
        $data = []; // 필수값 누락

        // When
        $response = $this->actingAs($this->user)
            ->postJson('/api/[models]', $data);

        // Then
        $response->assertStatus(422)
            ->assertJsonValidationErrors(['name']);
    }

    /**
     * 미인증 접근 테스트
     */
    public function test_unauthenticated_access_denied(): void
    {
        // When (인증 없이)
        $response = $this->getJson('/api/[models]');

        // Then
        $response->assertStatus(401);
    }
}
```

### 테스트 파일 저장 위치

```
tests/Feature/[Model]ApiTest.php
```

## Step 3: 테스트 실행

```bash
# 특정 테스트 파일 실행
php artisan test tests/Feature/[Model]ApiTest.php

# 특정 메서드 실행
php artisan test --filter test_can_create_[model]

# 전체 테스트 실행
php artisan test

# 상세 출력
php artisan test --verbose
```

## Step 4: 결과 리포트

테스트 결과를 아래 형식으로 정리한다:

```markdown
## API 테스트 결과

| 테스트 | 상태 | 상세 |
|-------|------|------|
| 목록 조회 | ✅ Pass | 200, 3건 반환 |
| 단건 조회 | ✅ Pass | 200, 정상 응답 |
| 생성 | ✅ Pass | 201, DB 확인 완료 |
| 수정 | ❌ Fail | 500, [에러 메시지] |
| 삭제 | ✅ Pass | 200, DB 삭제 확인 |
| 유효성 실패 | ✅ Pass | 422, 에러 필드 확인 |
| 미인증 | ✅ Pass | 401 |

**결과**: 6/7 통과 (85.7%)
**실패 원인**: [분석 내용]
```

## Step 5: 테스트 데이터 정리

### RefreshDatabase 사용 시 (권장)
- `use RefreshDatabase` trait이 자동으로 트랜잭션 롤백 수행
- 별도 정리 불필요

### 실제 DB 테스트 시 (수동 정리)
테스트가 실제 DB를 사용하는 경우, 생성된 데이터를 정리한다:

```bash
# 테스트 데이터 확인
php artisan tinker --execute="App\Models\[Model]::where('name', 'like', 'Test%')->get()"

# 테스트 데이터 삭제
php artisan tinker --execute="App\Models\[Model]::where('name', 'like', 'Test%')->forceDelete()"
```

### API를 통한 데이터 정리
테스트에서 생성한 리소스의 ID를 추적하여 DELETE API로 정리:

```bash
# 생성된 리소스 삭제
curl -X DELETE http://localhost:8000/api/[models]/{id} \
  -H "Authorization: Bearer {token}"
```

## 사용법

```
/api-test                           # 프로젝트 전체 API 테스트
/api-test User                      # User API 테스트
/api-test PropertyController        # 특정 컨트롤러 테스트
/api-test POST /api/properties      # 특정 엔드포인트 테스트
```

`$ARGUMENTS`로 대상을 지정하면 해당 모델/컨트롤러/엔드포인트만 테스트한다.

## 주의사항

1. **RefreshDatabase 우선**: 가능하면 RefreshDatabase trait 사용
2. **테스트 DB 확인**: `.env.testing`이 있으면 테스트 DB 사용 확인
3. **팩토리 확인**: 모델 팩토리가 없으면 먼저 생성 안내
4. **기존 패턴 준수**: 프로젝트에 기존 테스트가 있으면 그 패턴을 따른다
5. **시드 데이터 주의**: 시더 의존 테스트는 시더 실행 여부를 확인한다
6. **멀티테넌트**: organization_id 스코프가 있으면 테스트에 반영한다
