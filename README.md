# MagicSquare_xx

4×4 마방진 **10선(행·열·대각선) 합 검증** 학습 프로젝트. Mom Test에서 도출한 **검증 습관**(대각선까지 확인하기)을 `validate_lines` API와 Dual-Track TDD로 구현한다.

**상세 요구사항:** [docs/PRD.md](docs/PRD.md)  
**도메인 Rule:** [.cursorrules](.cursorrules)

---

## 배경 (Mom Test)

행·열 합이 34로 맞아 보여도 **대각선 검증을 끝까지 하지 않고** ‘계산 실수’만 의심하며 시간을 쓰는 패턴을 줄이는 것이 목표다. 자동 풀이·ECB 분류기 전체·UI는 범위 밖이다.

| 성공 기준 | 요약 |
|-----------|------|
| SC-1 | D1·D2 검증 전 `pass` / “맞음” 금지 → `incomplete` |
| SC-2 | 행·열 OK여도 대각선·미검증을 먼저 짚음 |
| SC-3 | 검증 순서 R1→…→D2 고정, Test Loop에서 함정 재현 |

---

## API

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)
# result["status"]       -> "pass" | "fail" | "incomplete"
# result["failed_lines"] -> list[str]  e.g. ["R1"], ["D1"], []
```

| 항목 | 값 |
|------|-----|
| 격자 | 4×4, 1~16 각 1회, 빈칸 없음 (Logic Track) |
| 마법상수 | 34 |
| 10선 | R1~R4, C1~C4, D1, D2 |
| 검증 순서 | `R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2` |

**현재 상태:** `validate_lines`는 stub(`...`) — 구현·RED 테스트 진행 전 ([PRD §11](docs/PRD.md#11-구현-상태-2026-06-10)).

---

## 빠른 시작

**요구:** Python ≥ 3.10

```bash
# 개발 의존성
pip install -e ".[dev]"

# 테스트 수집 (현재: fixture만, 테스트 함수 0)
pytest --collect-only

# 전체 테스트 (구현 후)
python -m pytest tests/ -v
```

---

## 저장소 구조

```
├── docs/PRD.md              # 기능 요구사항 (FR-01~), SSOT
├── src/validate_lines.py    # 핵심 API
├── tests/                   # pytest · fixture
├── .cursorrules             # ECB · TDD Rule
├── .cursor/commands/        # slash command (TDD 체인)
├── .cursor/skills/          # magic-square-tdd, magic-square-docs
├── Report/                  # 세션 보고서
└── Prompting/               # Transcript
```

---

## TDD 워크플로 (ARRR)

| 단계 | Command |
|------|---------|
| RED 설계 | `/red-test-plan` |
| RED 스켈레톤 | `/red-skeleton` → `/tdd-red` |
| GREEN | `/green-minimal` → `/golden-master` |
| REFACTOR | `/refactor-smell` → `/refactor-safe` |
| 문서 | `/export` |

- **RED:** `tests/`만 수정 · `pytest.fail` / assert · `src/` 수정 금지  
- **GREEN:** RED 1묶음당 최소 구현 · 1커밋=1묶음 (사용자 요청 시)  
- **C2C:** PRD FR → To-Do → Test ID (`T-001` …)

Skill: `.cursor/skills/magic-square-tdd/SKILL.md`

---

## 테스트 플랜

Logic Track · entity · `tests/test_validate_lines.py` 기준. [PRD §8.2](docs/PRD.md#82-fixture-현재-하네스) Fixture와 C2C Rule1~3에 따른 RED 설계표다. 다음 단계: `/red-skeleton` → `/tdd-red`.

### Fixture (현재 하네스)

| Fixture | 격자 요약 | 용도 | FR |
|---------|-----------|------|-----|
| `VALID_MAGIC_SQUARE` | 4×4 완전 마방진, 1~16 각 1회, 10선 합=34 | `pass` | FR-01 |
| `INVALID_GRID_SIZE` | 3×2 — 4×4 형식 위반 | `fail` (형식) | FR-02 |
| `FAIL_ROW_SUM` | 4×4, R1 합=10 (≠34) | `fail`, `R1` ∈ `failed_lines` | FR-04 |
| `TRAP_ROWS_COLS_OK` | `VALID_MAGIC_SQUARE`와 동일 — 행·열 8선=34 | Mom Test — `incomplete` | FR-05 |
| `DUPLICATE_VALUE` (예정) | 4×4, 1~16 중복 또는 누락 | `fail` | FR-03 |
| `grid_g1` (`conftest`, 예정) | 4×4, 빈칸 `0` 두 칸, row-major 좌표 | boundary/UI | FR-A01 |

> **Mom Test 함정:** 1~16·행·열=34인데 대각선≠34인 격자는 **수학적으로 존재하지 않음**. `TRAP_ROWS_COLS_OK`는 **대각선 미검증 흐름**을 `incomplete`로 모델링한다 ([PRD §3](docs/PRD.md#3-성공-기준-mom-test-연계)).

### C2C (FR → Test ID)

| FR (PRD 인용) | To-Do | Test ID | Given | When | Then |
|---------------|-------|---------|-------|------|------|
| FR-01: 완전 4×4 마방진에서 10선 합이 모두 34이면 `status`는 `pass`이고 `failed_lines`는 `[]`이다. | 10선 전부 합=34 판정 | T-001 | `VALID_MAGIC_SQUARE` | `validate_lines(grid)` | `status=="pass"`, `failed_lines==[]` |
| FR-02: 격자가 4×4가 아니거나 원소가 1~16 범위 밖이면 `status`는 `fail`이다. | 형식·범위 위반 판정 | T-002 | `INVALID_GRID_SIZE` | `validate_lines(grid)` | `status=="fail"` |
| FR-03: 1~16이 중복되거나 누락되면 `status`는 `fail`이다. | 중복·누락 판정 | T-003 | `DUPLICATE_VALUE` (예정) | `validate_lines(grid)` | `status=="fail"` |
| FR-04: 특정 선의 합이 34가 아니면 `status`는 `fail`이고 해당 선 ID가 `failed_lines`에 포함된다. | 불합격 선 ID 보고 | T-004 | `FAIL_ROW_SUM` | `validate_lines(grid)` | `status=="fail"`, `"R1" in failed_lines` |
| FR-05: 행·열 검증만 끝나고 D1·D2가 아직 검증되지 않은 흐름에서는 `status`는 `incomplete`이며 `pass`가 아니다. | Mom Test 미완 판정 | T-005 | `TRAP_ROWS_COLS_OK` | `validate_lines(grid)` | `status=="incomplete"`, `status != "pass"` |
| FR-06: 선 검증은 `VERIFICATION_ORDER`(R1→…→D2)를 따른다. | 검증 순서 invariant | T-005 (연계) | `TRAP_ROWS_COLS_OK` | `validate_lines(grid)` | `VERIFICATION_ORDER` 준수, D1·D2 전 `pass` 금지 |

### 테스트 설계 (Track B)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T-001 | `validate_lines` | `VALID_MAGIC_SQUARE` → `pass`, `[]` | 10선 합=34, 1~16 중복 없음, `MAGIC_CONSTANT=34` | `NotImplementedError` / stub `...` |
| T-002 | `validate_lines` | `INVALID_GRID_SIZE` → `fail` | 4×4·1~16 형식 (C-01) | 동일 |
| T-003 | `validate_lines` | `DUPLICATE_VALUE` → `fail` | 1~16 각 1회 (C-02) | 동일 |
| T-004 | `validate_lines` | `FAIL_ROW_SUM` → `fail`, `R1` | 합≠34 선 ID 보고 (C-03) | 동일 |
| T-005 | `validate_lines` | `TRAP_ROWS_COLS_OK` → `incomplete` | R1→…→C4 후 D1·D2 미검증 시 `pass` 금지 (C-04, SC-1~3) | 동일 |

### 실행 메타

| 항목 | 값 |
|------|-----|
| 파일 | `tests/test_validate_lines.py` |
| import | `from src.validate_lines import validate_lines` (+ 필요 시 `LINE_IDS`, `VERIFICATION_ORDER`) |
| 테스트 함수명 (권장) | `test_T001_valid_magic_square_passes`, `test_T002_invalid_grid_size_fails`, … (Test ID 1:1) |
| AAA | Arrange(fixture) → Act(`validate_lines`) → Assert(`status`, `failed_lines`) |
| pytest | `pytest tests/test_validate_lines.py -v` |
| RED 묶음 | `T-001`~`T-005` (Logic Track P0) |
| Golden Master (GREEN 후) | `tests/golden/{Test ID}.approved.txt`, `UPDATE_GOLDEN=1 pytest …` |

### ECB · Mock 점검

| # | 항목 | 결과 | 비고 |
|---|------|------|------|
| 1 | Domain Mock 미사용 | OK | 실제 fixture 격자만 사용 |
| 2 | E001~E005 미포함 | OK | Logic Track emit 금지 |
| 3 | ECB·풀이·UI 범위 밖 | OK | `validate_lines` 10선 합만 |
| 4 | Mom Test / 검증 순서 반영 | OK | `TRAP_ROWS_COLS_OK` → T-005, `VERIFICATION_ORDER` |

`/red-skeleton` 으로 넘길 준비됐다.

---

## 기능 요구사항 (요약)

| FR | 내용 | Test ID |
|----|------|---------|
| FR-01 | 10선 합 34 → `pass` | T-001 |
| FR-02 | 형식·범위 오류 → `fail` | T-002 |
| FR-03 | 1~16 중복·누락 → `fail` | T-003 |
| FR-04 | 선 합≠34 → `fail` + 선 ID | T-004 |
| FR-05 | 대각선 미검증 → `incomplete` | T-005 |
| FR-06 | 검증 순서 R1→…→D2 | T-005 (연계) |

전체 FR·에러 코드·Dual-Track: [docs/PRD.md](docs/PRD.md)

---

## 참고 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | PRD · FR · 테스트 · TDD |
| [Report/01.MomTest_Report.md](Report/01.MomTest_Report.md) | Mom Test 인터뷰 |
| [Report/03.Session3_Workbook_Report.md](Report/03.Session3_Workbook_Report.md) | 세션 3 워크북 |
| [Report/README.md](Report/README.md) | 보고서 목록 |
| [Prompting/README.md](Prompting/README.md) | 프롬프트·Transcript 목록 |

---

## 라이선스 · 기여

학습·세션 산출물 프로젝트. git commit은 사용자 명시 요청 시에만 수행한다 (`.cursorrules`).
