# TDD RED — validate_lines

`validate_lines` TDD **RED 단계 전용** 커맨드. 실패하는 테스트만 추가한다.

## Phase 선언 (필수)

응답 **첫 줄**은 반드시 다음 형식이다.

```
Phase: RED
```

이후 한국어로 진행한다.

## 대상

| 항목 | 값 |
|------|-----|
| 함수 | `validate_lines(grid) -> {status, failed_lines}` |
| status | `"pass"` \| `"fail"` \| `"incomplete"` |
| 수정 허용 | `tests/` **만** (`tests/test_validate_lines.py` 중심) |
| 도메인 | 4×4, 빈칸 0, 1~16, 마법상수 34, 10선 R1~R4·C1~C4·D1·D2 |
| 참조 | `.cursorrules`, 하네스 fixture (`VALID_MAGIC_SQUARE` 등) |

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순서로 작성한다.

1. **Arrange** — 격자 fixture·상수 준비 (기존 fixture 재사용 우선)
2. **Act** — `result = validate_lines(grid)` 호출
3. **Assert** — `status`와 `failed_lines`를 **구체적으로** 검증 (모호한 assert 금지)

RED 완료 조건: `pytest` 실행 시 **새 테스트가 실패**해야 한다 (미구현 `...` 또는 NotImplemented).

## pytest 예시

```python
def test_valid_magic_square_passes():
    # Arrange
    grid = VALID_MAGIC_SQUARE
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_invalid_grid_size_fails():
    # Arrange
    grid = INVALID_GRID_SIZE
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"]  # 형식 오류 시 불합격 선 ID


def test_wrong_row_sum_fails_with_line_id():
    # Arrange
    grid = FAIL_ROW_SUM
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "fail"
    assert "R1" in result["failed_lines"]


def test_trap_rows_cols_ok_not_pass_before_diagonals():
    # Arrange — Mom Test 함정: 행·열=34, 대각선 미검증 → incomplete
    grid = TRAP_ROWS_COLS_OK
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "incomplete"
    assert result["status"] != "pass"
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

기대: RED 단계에서는 **FAILED** (구현 전).

## 보고 형식

RED 작업 마무리 시 아래 템플릿으로 보고한다.

```markdown
Phase: RED

## 추가한 테스트
- `test_...` — (한 줄: 무엇을 검증하는지)

## AAA 요약
| 테스트 | Arrange | Assert (status / failed_lines) |
|--------|---------|--------------------------------|
| test_... | ... | ... |

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N failed, M passed (FAILED 목록)

## 다음 단계
- GREEN: `src/validate_lines.py` 구현 → `/tdd-green` (또는 사용자 지시)
```

## 금지 (RED 위반)

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 담당 |
| assert 완화 (`==` → `in`, 값 축소, 조건 삭제) | RED 회피 |
| `@pytest.mark.skip` / `xfail` | 실패 숨김 |
| 테스트 삭제·이름만 변경 | RED 회피 |
| `src/`에 맞춰 테스트 뒤집기 | 구현 주도 TDD 아님 |
| 임의 git commit | 사용자 요청 시만 |

위반 시 작업을 중단하고, 위반 항목을 명시한다.
