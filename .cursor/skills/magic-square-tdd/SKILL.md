---
name: magic-square-tdd
description: >-
  MagicSquare_xx Dual-Track TDD (ARRR/C2C): validate_lines 4×4 magic square,
  RED pytest.fail skeletons, GREEN minimal bundles, golden approval, safe refactor.
  Use when Phase is red|green|refactor; Commands /red-test-plan, /red-skeleton,
  /green-minimal, /refactor-safe; or user mentions TDD, RED, GREEN, REFACTOR,
  Dual-Track, C2C, pytest.fail.
disable-model-invocation: true
---

# magic-square-tdd

MagicSquare_xx **Dual-Track TDD** 워크플로. Command·명시 Skill 호출 시에만 적용.

**SSOT:** `.cursorrules`, `docs/PRD.md` (없으면 `.cursorrules` ECB + 채팅). Command 상세는 `.cursor/commands/*.md`.

**응답 언어:** 한국어.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | 단계 | Command | 수정 범위 |
|------|-----|------|---------|-----------|
| **A** Ask | RED ③④ | 설계·스켈레톤 | `/red-test-plan`, `/red-skeleton`, `/tdd-red` | `tests/` (플랜은 파일 없음) |
| **R** Respond | GREEN | 최소 구현 | `/green-minimal`, `/golden-master` | `src/` (+ 해당 묶음 `tests/`) |
| **R** Refine | REFACTOR | 스멜·safe | `/refactor-smell`, `/refactor-safe` | smell=읽기만; safe=Budget 내 |

---

## 2. Phase 선언 (응답 첫 줄)

| 단계 | 형식 |
|------|------|
| RED 설계 | `Phase: red \| Layer: entity \| Track: Logic` |
| RED (legacy) | `Phase: RED` — `/tdd-red` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

- `Layer`: `entity` \| `boundary`
- `Track`: `Logic` \| `UI` (smell만 `Logic+UI`)

---

## 3. C2C Rule 1~3

| Rule | 내용 |
|------|------|
| **Rule1** | PRD **FR 한 줄 인용** → 검증 가능한 **To-Do 1개** (솔루션·UI 가설 금지) |
| **Rule2** | To-Do 1개 → **Test ID 1개** (`T-001`…). **Given / When / Then** 분리 |
| **Rule3** | Mom Test·검증 순서 R1→…→D2·`incomplete` 함정이 Test ID에 반영됐는지 점검 |

**Test ID:** `T-{NNN}` 3자리. API: `validate_lines(grid) -> {status, failed_lines}`.

**도메인 (.cursorrules):** 4×4, 1~16 중복 없음, 마법상수 34, 10선 R1~R4·C1~C4·D1·D2. 검증 순서 고정. 행·열만 34여도 D1·D2 전 `pass` 금지 → `incomplete`.

---

## 4. RED 절대 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 담당 |
| `@pytest.mark.skip` / `xfail` | 실패 숨김 |
| assert 완화·테스트 삭제 | RED 회피 |
| **Logic Track Domain Mock** | `validate_lines`·격자는 **실제 fixture** |
| E001~E005 emit (Logic) | boundary 전용 |
| GREEN / REFACTOR 선행 | 단계 분리 |

**RED ④ 스켈레톤 Then:** `pytest.fail("RED: {Test ID} — …")` **한 줄만** — assert 본문·`pass` 더미 금지.

**상수:** `34`/`4`/`16`은 `entity/constants.py` import. 픽스처 격자 숫자만 리터럴 허용.

---

## 5. GREEN

| 규칙 | 내용 |
|------|------|
| 범위 | **RED 1묶음** Test ID만 — 묶음 밖 동시 해결 금지 |
| 구현 | `src/` **최소** 분기만 |
| 커밋 | **1 RED 묶음 = 1 커밋** — 사용자 **명시 요청 시만** |
| 상수 SSOT | `entity/constants.py` — `GRID_SIZE`, `MAGIC_CONSTANT`, `CELL_COUNT` |
| 금지 | 하드코딩 매직넘버, E001~E005, entity→boundary/control import, ECB 풀이·UI |

절차: RED 재확인 → `src/` 최소 구현 → `pytest.fail`→assert → PASS.

---

## 6. REFACTOR

**전제:** `python -m pytest tests/ -v` 전부 PASS.

| 항목 | 내용 |
|------|------|
| `/refactor-smell` | 탐지만 — **코드·commit 금지** |
| `/refactor-safe` | 스멜 **1건**만 |
| **Change Budget** | 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3 |
| 계약 | 입출력·예외·`int[6]` **1-index** 불변 |
| golden | `UPDATE_GOLDEN` 없이 **matched** — 비의도 diff → 롤백; 의도적 → ISS + `UPDATE_GOLDEN=1` |
| 금지 | 기능 추가·버그 수정 (→ `/green-minimal`), golden 수동 편집 |

---

## 7. Track A (UI) vs Track B (Logic)

| | **Track A — UI** | **Track B — Logic** |
|---|------------------|---------------------|
| Layer | `boundary` | `entity` |
| 대상 | CLI·API·화면·상호작용 | `validate_lines` 등 도메인 |
| 테스트 | boundary Mock 허용 | **Domain Mock 금지** |
| E001~E005 | PRD 정의 시 | Logic RED/GREEN **emit 금지** |
| conftest | UI·입출력 fixture | `grid_g1` (0 두 칸, row-major), `VALID_MAGIC_SQUARE` 등 |
| Command | Layer=`boundary`로 선언만 바꿔 RED 플랜 재사용 | 기본 Track |

본 프로젝트 기본: **Track B · entity · Logic**.

---

## 8. Command 체인

```
/red-test-plan     → C2C·테스트 플랜 (파일 생성 없음)
       ↓
/red-skeleton      → pytest.fail 스켈레톤 (tests/만)
       ↓
/tdd-red           → assert 채우기 (tests/만) [선택·병행]
       ↓
/green-minimal     → RED 1묶음 최소 구현 (src/)
       ↓
/golden-master     → Approval Test (tests/golden/, UPDATE_GOLDEN)
       ↓
/refactor-smell    → 스멜 표 (수정 없음)
       ↓
/refactor-safe     → 스멜 1건 리팩터
```

| Command | 핵심 산출 |
|---------|-----------|
| `red-test-plan` | 4블록 표; 마지막 줄 `/red-skeleton 으로 넘길 준비됐다` |
| `red-skeleton` | AAA + `pytest.fail`; `tests/conftest.py` `grid_g1` |
| `green-minimal` | 묶음 PASS; 회귀 즉시 수정 |
| `golden-master` | `tests/_approval.py` `assert_matches_golden`; `{id}.approved.txt` |
| `refactor-smell` | P0/P1/P2 스멜 표; 후보 1~3 → safe |
| `refactor-safe` | Budget 내 1건; pytest + golden matched |

**ECB:** entity는 boundary/control import 금지. 풀이·ECB 분류·UI는 `.cursorrules` 범위 밖.

---

## 9. pytest 명령 패턴

```bash
# 전체 (전제·smell·safe 완료 검증)
python -m pytest tests/ -v

# RED 묶음 / 단일 Test ID
pytest tests/test_validate_lines.py -v
pytest tests/test_validate_lines.py::test_T001_valid_magic_square_passes -v

# 스켈레톤 추가 직후 (전부 FAILED 기대)
pytest tests/test_validate_lines.py -v

# golden 기준 생성 (최초·의도적 갱신만)
UPDATE_GOLDEN=1 pytest tests/test_validate_lines.py::test_T001_valid_magic_square_passes -v

# golden matched 확인 (UPDATE_GOLDEN 없음)
pytest tests/ -v
```

`pyproject.toml`의 `testpaths`·`pythonpath` 따름.

---

## 10. 완료 보고 형식

### RED (`red-test-plan`)

```markdown
Phase: red | Layer: entity | Track: Logic
(블록 1~4 표)
/red-skeleton 으로 넘길 준비됐다
```

### RED (`red-skeleton`)

```markdown
Phase: red | Layer: entity | Track: Logic
## 변경 파일 (tests/ 만)
## pytest 결과
| Test ID | FAIL 한 줄 |
```

### GREEN (`green-minimal`)

```markdown
Phase: green | Layer: entity | Track: Logic
## 이번 RED 묶음 · PASS Test ID · 변경 파일 · pytest · 회귀
```

### Golden (`golden-master`)

```markdown
Phase: green | Layer: entity | Track: Logic
## golden 경로 · matched 여부 · diff 요약
```

### REFACTOR

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI   # smell
Phase: refactor | Layer: entity | Track: Logic            # safe
## 스멜 표 / 대상 스멜 1건 · 변경 요약 · pytest · golden matched
```

---

## 부록: fixture · golden · 직렬화

| 항목 | 값 |
|------|-----|
| `VALID_MAGIC_SQUARE` | 완전 4×4 마방진 |
| `INVALID_GRID_SIZE` | 형식 오류 |
| `FAIL_ROW_SUM` | 행 합≠34 |
| `TRAP_ROWS_COLS_OK` | Mom Test — `incomplete` |
| `grid_g1` | 4×4, `0` 두 칸, row-major |
| golden 경로 | `tests/golden/{Test ID}.approved.txt` |
| `int[6]` | 1-index, `1,2,3,4,5,6` |
| 에러 코드 | `E001`~`E005` (Logic Track 금지) |

```python
# 스켈레톤 Then
pytest.fail("RED: T-001 — expect status pass, failed_lines []")

# golden 직렬화 예
actual = f"status={result['status']}\nfailed_lines=\n"
assert_matches_golden("T-001", actual)
```

---

## 금지 (공통)

- 임의 **git commit** (사용자 요청 시만)
- 단계·Track·Layer 무시한 일괄 수정
- Command 본문과 Skill 충돌 시 **Command + SSOT 우선** (동일하면 Skill)
