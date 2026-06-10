# golden-master — Golden Master (Approval Test)

**GREEN PASS** 후 대상 Test ID에 **Golden Master(Approval Test)** 를 구축·검증한다. 구현 회귀를 golden diff로 잡는다.

> `/green-minimal`로 PASS된 Test ID만 대상. RED·스켈레톤 단계에서는 실행하지 않는다.

**Skill 참조:** `magic-square-tdd` Skill이 있으면 **자동 따름** — golden 경로·직렬화 포맷이 Skill과 충돌하면 Skill 우선.

## Phase 선언 (필수)

응답 **첫 줄**은 반드시 다음 형식이다.

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 |
|------|-----|
| `Layer` | `entity` (기본) |
| `Track` | `Logic` (기본) |

이후 한국어로 진행한다.

## 전제 (필수)

| 조건 | 확인 |
|------|------|
| 대상 Test ID | `/red-test-plan`·채팅에서 범위 추출 (예: `T-001`) |
| pytest PASS | 대상 테스트 함수가 **이미 PASSED** (`/green-minimal` 완료) |
| `src/` | golden 생성 시점의 구현이 **의도된 GREEN** 상태 |

전제 미충족 시 golden 작업을 **중단**하고, 먼저 `/green-minimal`을 수행한다.

## 대상

| 항목 | 값 |
|------|-----|
| 수정 허용 | `tests/_approval.py`, `tests/golden/*.approved.txt`, 대상 테스트에 golden hook 추가 |
| 수정 금지 | `src/` (golden은 **출력 캡처**만; 구현 변경으로 우회 금지) |
| golden 파일 | `tests/golden/{id}.approved.txt` — `{id}` = Test ID 슬러그 (예: `T-001` → `T-001.approved.txt`) |

## 출력 직렬화 포맷 (고정)

golden 비교 대상 문자열은 **아래 포맷을 고정**한다. 테스트·헬퍼가 동일 규칙으로 직렬화한다.

### int[6] — 1-index

6개 정수 배열. **1-index** 좌표·선 번호 (0-index 금지).

```
# 예: 행1 열2, 행3 열4, 선ID 인덱스 … (도메인 정의 따름)
1,2,3,4,5,6
```

- 필드 의미는 Test ID·Skill 정의 따름
- 구분자: `,` (쉼표), 공백 없음
- 한 줄로 출력

### 에러 코드 문자열

```
E001
```

- 형식: `E` + 3자리 숫자 (`E001`~`E005`)
- entity Logic Track: golden에 에러 코드가 **없는** 케이스가 기본 (`.cursorrules`·`green-minimal`과 동일)
- boundary Track에서 에러 코드 golden을 쓸 때만 PRD·Skill 정의 따름

### 복합 출력 (한 golden 파일)

```text
status=pass
failed_lines=
coords=1,2,3,4,5,6
error=
```

- 키=`값` 한 줄씩, **키 순서 고정** (Skill이 정하면 Skill 우선)
- `validate_lines` 기본: `status`, `failed_lines` (쉼표 구분 선 ID 또는 `empty`)

## 절차 (필수 순서)

### 1. `tests/_approval.py` — `assert_matches_golden`

파일이 없으면 생성한다.

```python
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(test_id: str, actual: str) -> None:
    """Approval Test: actual 문자열을 golden 파일과 비교한다."""
    golden_path = GOLDEN_DIR / f"{test_id}.approved.txt"
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        return
    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch for {test_id}\n"
            f"  golden: {golden_path}\n"
            f"  expected ({len(expected)} chars) != actual ({len(actual)} chars)\n"
            f"--- expected ---\n{expected}\n--- actual ---\n{actual}"
        )
```

- 테스트에서 `from tests._approval import assert_matches_golden` 또는 상대 import 규칙은 프로젝트·Skill 따름
- `actual`은 **위 직렬화 포맷**으로 만든 문자열

### 2. `tests/golden/{id}.approved.txt` 연결

대상 테스트에 golden hook을 추가한다 (PASS assert **유지** + golden 검증).

```python
def test_T001_valid_magic_square_passes():
    # Given / When / Act …
    result = validate_lines(grid)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []

    # Golden Master
    actual = f"status={result['status']}\nfailed_lines=\n"
    assert_matches_golden("T-001", actual)
```

- `{id}` = Test ID와 동일 (`T-001.approved.txt`)
- 한 Test ID ↔ golden 파일 **1:1**

### 3. 기준 파일 생성 — `UPDATE_GOLDEN=1`

**최초 1회** (또는 의도적 기준 갱신 시만):

```bash
UPDATE_GOLDEN=1 pytest tests/test_validate_lines.py::test_T001_valid_magic_square_passes -v
```

또는 묶음 전체:

```bash
UPDATE_GOLDEN=1 pytest tests/test_validate_lines.py -v
```

- 환경 변수 `UPDATE_GOLDEN=1`일 때만 `tests/golden/{id}.approved.txt` **쓰기**
- 생성 후 golden 파일 내용이 직렬화 포맷·PASS assert와 **일치**하는지 눈으로 확인

### 4. matched 확인 — `UPDATE_GOLDEN` 없음

```bash
pytest tests/test_validate_lines.py::test_T001_valid_magic_square_passes -v
```

```bash
pytest tests/test_validate_lines.py -v
```

- **기대:** 대상 Test ID **PASSED**, `assert_matches_golden` **matched** (AssertionError 없음)
- mismatch 시 diff 메시지로 expected/actual 비교 후 **`src/` 또는 직렬화 로직** 수정 — golden 수동 편집으로 통과시키지 않음

## 금지

| 금지 | 이유 |
|------|------|
| golden 파일 **수동 편집**으로 테스트 통과 | Approval Test 우회 |
| PASS 전 golden 생성 | 기준이 RED·잘못된 구현에 고정됨 |
| `UPDATE_GOLDEN=1` 없이 golden 덮어쓰기 | 의도치 않은 기준 변경 |
| 직렬화 포맷 임의 변경 (0-index, 키 순서 뒤섞기) | diff 불가·회귀 감지 실패 |
| `src/` 수정으로 golden만 맞추기 | 동작 변경은 GREEN에서; golden은 캡처 검증 |
| 임의 git commit | 사용자 요청 시만 |

의도적 golden 갱신은 **반드시** `UPDATE_GOLDEN=1 pytest …`로만 수행한다.

## 보고 형식 (필수)

```markdown
Phase: green | Layer: entity | Track: Logic

## 대상 Test ID
- T-001 (pytest PASS 전제 확인됨)

## Golden 경로
| Test ID | golden 파일 |
|---------|-------------|
| T-001 | tests/golden/T-001.approved.txt |

## matched 여부
| Test ID | UPDATE_GOLDEN | matched |
|---------|---------------|---------|
| T-001 | (없음) | yes / no |

## diff 요약
- (matched=yes) 차이 없음
- (matched=no) 키·줄 단위 요약 — 예: `failed_lines`: expected `empty` vs actual `R1`

## pytest 명령
- 생성: `UPDATE_GOLDEN=1 pytest tests/test_validate_lines.py::test_T001_... -v`
- 검증: `pytest tests/test_validate_lines.py::test_T001_... -v`

## 변경 파일
| 파일 | 변경 |
|------|------|
| tests/_approval.py | assert_matches_golden (신규/유지) |
| tests/golden/T-001.approved.txt | 기준 생성·검증 |
| tests/test_validate_lines.py | golden hook 추가 |
```

## 참조

- `.cursor/commands/green-minimal.md` — GREEN PASS 선행
- `.cursor/commands/red-test-plan.md` — Test ID·Then 기대값
- `magic-square-tdd` Skill — 직렬화·golden 경로
- `.cursorrules` — API `status` / `failed_lines`

## 다음 단계

1. 다음 Test ID → `/green-minimal` PASS 후 본 커맨드 반복
2. REFACTOR 후 golden 재검증 (`UPDATE_GOLDEN` 없이 matched 확인)
3. `/export` — 세션 보고 (해당 시)
