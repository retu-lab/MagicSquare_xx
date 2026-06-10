# MagicSquare_xx — Product Requirements Document (PRD)

**버전:** 0.1.0  
**일자:** 2026-06-10  
**상태:** 세션 3 — 하네스·Rule·Command·Skill 골격 완료, `validate_lines` 구현·RED 테스트 진행 전

**SSOT 계층:** 본 문서(`docs/PRD.md`) ↔ `.cursorrules` ↔ 코드. 충돌 시 **도메인 API·FR**는 본 PRD와 `.cursorrules`를 우선하고, TDD 절차·Command 상세는 `.cursor/commands/`·Skills를 따른다.

---

## 1. 제품 개요

### 1.1 한 줄 요약

4×4 마방진 **10선(행·열·대각선) 합 검증**을 TDD·Mom Test 검증 습관과 연계해 구현하는 학습·도메인 프로젝트다.

### 1.2 Mom Test 배경 (진짜 문제)

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4 부분 마방진(ECB 과제)을 손 계산·코드로 다루는 **학습자** |
| **진짜 문제** | 행·열 합이 34로 맞아 보여도 **대각선 검증을 끝까지 하지 않은 채** ‘계산 실수’만 의심하며 약 20분을 헤맨다. |
| **증거 ①** | 행·열은 맞아 보였으나 대각선 하나를 빼먹어 시간 낭비 |
| **증거 ②** | 20분 동안 대각선을 직접 확인하지 않고 계산 실수만 의심 |
| **증거 ③** | 대각선 확인은 20분이 지난 뒤에야 처음 수행 |

> 제품 가설이 아니라 **검증 순서·판정 습관**이 핵심이다. 자동 풀이·ECB 분류기 전체·체크리스트 UI는 본 단계 범위 밖이다.

### 1.3 프로젝트 주제 (솔루션 최소화)

**행·열 합이 34로 맞아 보여도 대각선(2개)을 끝까지 확인하지 않고 ‘맞음’이라고 말하지 않도록, API·Test Loop·Rule/Command로 검증 행동을 고정한다.**

---

## 2. 목표 · 비목표

### 2.1 목표 (Goals)

| ID | 목표 |
|----|------|
| G-01 | `validate_lines` API로 10선 합(=34) 검증을 **코드로 재현** |
| G-02 | Mom Test **성공 기준 3개**를 Test Loop에서 검증 가능하게 유지 |
| G-03 | Dual-Track TDD(ARRR/C2C)로 RED→GREEN→REFACTOR·문서 Export 파이프라인 운영 |
| G-04 | 검증 순서 **R1→…→D2** 고정 및 `incomplete` 상태로 “미완료 판정” 표현 |

### 2.2 비목표 (Non-Goals)

| 항목 | 이유 |
|------|------|
| 마방진 **자동 풀이**/솔버 | 검증 끝까지가 목표 |
| ECB **분류기 전체** | Mom Test 문제는 합 검증 누락 |
| 체크리스트 **UI**·앱 | 세션 3은 Rule·Command·Test Loop |
| Subagent·Hook·MCP·Canvas | 8계층 중 이번 범위 밖 |

---

## 3. 성공 기준 (Mom Test 연계)

| # | 성공 기준 | PRD·구현 연결 |
|---|-----------|----------------|
| **SC-1** | 행·열이 모두 34여도 **D1·D2 검증 전** `pass` / “맞음” 금지 | FR-05, `status: incomplete` |
| **SC-2** | 행·열 OK + 대각선 미검증 시 **대각선·불일치**를 먼저 짚음 | FR-05, Test `TRAP_ROWS_COLS_OK` |
| **SC-3** | 검증 순서 **행→열→대각선** 고정, 함정 케이스가 Test Loop에서 잡힘 | FR-06, `VERIFICATION_ORDER` |

**수학적 함정 참고:** 1~16 중복 없이 행·열 8선 합이 모두 34이면 대각선 합도 34이다. “행·열=34, 대각선≠34” **데이터 함정 격자는 존재하지 않음**. Mom Test 함정은 **검증 미완(`incomplete`)** 으로 모델링한다 (`Report/04`).

---

## 4. 도메인 (ECB)

### 4.1 Example

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 (`GRID_SIZE = 4`) |
| 칸 값 | 1~16 정수, **빈칸 0개**(완전 채움) — Logic Track 기본 |
| 마법상수 | **34** (`MAGIC_CONSTANT`) |
| 검증 선 | **10선**: R1~R4(행), C1~C4(열), D1(주대각 ↘), D2(부대각 ↙) |

**예시 완전 마방진 (`VALID_MAGIC_SQUARE`):**

```
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
```

### 4.2 Constraint

| ID | 제약 |
|----|------|
| C-01 | `grid`는 4×4 이중 리스트; 행·열 길이·원소 범위 불일치 시 **fail** |
| C-02 | 1~16은 격자 내 **중복 없이** 각 1회 |
| C-03 | 각 선 합 ≠ 34이면 해당 선 ID를 `failed_lines`에 포함 |
| C-04 | 행·열만 맞고 대각선 미검증 상태는 **incomplete** — `pass` 금지 |

### 4.3 Behavior (API)

```python
validate_lines(grid: list[list[int]]) -> ValidateLinesResult
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | `"pass"` \| `"fail"` \| `"incomplete"` | 종합 판정 |
| `failed_lines` | `list[str]` | 불합격·미검증 선 ID (예 `["D1"]`, `[]`) |

| status | 조건 |
|--------|------|
| `pass` | 10선 모두 합=34, 형식·중복 OK |
| `fail` | 형식 오류, 중복, 또는 합≠34인 선 존재 |
| `incomplete` | 검증 순서상 아직 확인하지 않은 선이 남음 (대각선 미검증 포함) |

### 4.4 검증 순서 (고정)

```
R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2
```

상수: `LINE_IDS`, `VERIFICATION_ORDER` (`src/validate_lines.py`).

---

## 5. 기능 요구사항 (FR)

C2C Rule1: **FR 한 줄 인용 → To-Do 1개 → Test ID** (`/red-test-plan`).

| FR ID | 요구사항 (인용문) | Test ID (권장) | 우선순위 |
|-------|-------------------|----------------|----------|
| **FR-01** | 완전 4×4 마방진에서 10선 합이 모두 34이면 `status`는 `pass`이고 `failed_lines`는 `[]`이다. | T-001 | P0 |
| **FR-02** | 격자가 4×4가 아니거나 원소가 1~16 범위 밖이면 `status`는 `fail`이다. | T-002 | P0 |
| **FR-03** | 1~16이 중복되거나 누락되면 `status`는 `fail`이다. | T-003 | P0 |
| **FR-04** | 특정 선의 합이 34가 아니면 `status`는 `fail`이고 해당 선 ID가 `failed_lines`에 포함된다. | T-004 | P0 |
| **FR-05** | 행·열 검증만 끝나고 D1·D2가 아직 검증되지 않은 흐름에서는 `status`는 `incomplete`이며 `pass`가 아니다. | T-005 | P0 |
| **FR-06** | 선 검증은 `VERIFICATION_ORDER`(R1→…→D2)를 따른다. | T-005 (연계) | P0 |
| **FR-07** | 도메인 상수 4·16·34는 `entity/constants.py` SSOT에서만 정의·import한다. | (리팩터·GREEN) | P1 |
| **FR-08** | Logic Track(entity)에서는 E001~E005 에러 코드를 emit하지 않는다. | (ECB 점검) | P1 |
| **FR-09** | GREEN은 RED 1묶음(Test ID 범위)당 최소 구현만 추가한다. | (프로세스) | P1 |
| **FR-10** | PASS 후 Golden Master로 회귀를 검출한다 (`tests/golden/{id}.approved.txt`). | (golden-master) | P2 |

### 5.1 확장 (Track A · boundary — 범위 외·향후)

| FR ID | 요구사항 | 비고 |
|-------|----------|------|
| FR-A01 | 부분 격자(빈칸 `0` 두 개) 좌표는 row-major, `grid_g1` fixture | boundary/UI |
| FR-A02 | boundary에서 E001~E005 문자열 포맷 `E`+3자리 | UI Track 전용 |
| FR-A03 | 직렬화 `int[6]` 좌표는 **1-index** | golden·approval |

---

## 6. 에러 코드 (boundary · UI Track)

Logic Track(entity) **emit 금지**. boundary 구현 시에만 사용.

| 코드 | 의미 (초안) |
|------|-------------|
| E001 | 격자 형식 오류 |
| E002 | 값 범위 오류 (1~16) |
| E003 | 중복·누락 |
| E004 | 선 합 불일치 |
| E005 | 검증 미완 (incomplete) |

형식: `E` + 3자리 숫자 (예 `E001`).

---

## 7. Dual-Track

| | **Track A — UI** | **Track B — Logic** |
|---|------------------|---------------------|
| Layer | `boundary` | `entity` |
| 대상 | CLI·API·화면 | `validate_lines` |
| Domain Mock | boundary Mock 허용 | **금지** |
| E001~E005 | PRD 정의 시 | **금지** |
| 기본 | 향후 | **본 PRD Phase 1** |

---

## 8. 테스트 요구사항

### 8.1 프레임워크

- **pytest** ≥ 8.0 (`pyproject.toml`)
- `testpaths = ["tests"]`, `pythonpath = ["."]`
- 주 테스트 파일: `tests/test_validate_lines.py`

### 8.2 Fixture (현재 하네스)

| Fixture | 용도 | FR |
|---------|------|-----|
| `VALID_MAGIC_SQUARE` | 완전 마방진 pass | FR-01 |
| `INVALID_GRID_SIZE` | 형식 오류 fail | FR-02 |
| `FAIL_ROW_SUM` | 행 합≠34, `R1` 등 | FR-04 |
| `TRAP_ROWS_COLS_OK` | Mom Test — incomplete 시나리오 | FR-05 |
| `grid_g1` (conftest, 예정) | 부분 격자, 0 두 칸 row-major | FR-A01 |

### 8.3 Test ID 명명

- 형식: `T-{NNN}` (3자리, `T-001`부터)
- AAA: Arrange(fixture) → Act(`validate_lines`) → Assert(`status`, `failed_lines`)
- RED ④: `pytest.fail("RED: {Test ID} — …")` 한 줄만 (스켈레톤)

### 8.4 Golden Master (Approval Test)

| 항목 | 값 |
|------|-----|
| 헬퍼 | `tests/_approval.py` → `assert_matches_golden` |
| 기준 파일 | `tests/golden/{Test ID}.approved.txt` |
| 생성 | `UPDATE_GOLDEN=1 pytest …` (의도적 갱신만) |
| 검증 | `UPDATE_GOLDEN` 없이 matched |
| 직렬화 | `status=…`, `failed_lines=…` 키 순서 고정; `int[6]` 1-index |

### 8.5 TDD 절대 금지

- RED에서 `src/` 수정
- `@pytest.mark.skip` / `xfail`
- assert 완화·테스트 삭제
- Logic Track Domain Mock
- 채팅에 없는 pytest 결과를 Report에 기재

---

## 9. TDD · ARRR 워크플로

### 9.1 ARRR ↔ TDD 매핑

| ARRR | TDD | Command |
|------|-----|---------|
| **A** Ask | RED ③④ | `/red-test-plan`, `/red-skeleton`, `/tdd-red` |
| **R** Respond | GREEN | `/green-minimal`, `/golden-master` |
| **R** Refine | REFACTOR | `/refactor-smell`, `/refactor-safe` |
| 문서 | repeat | `/export`, magic-square-docs Skill |

### 9.2 Phase 선언 (응답 첫 줄)

| 단계 | 형식 |
|------|------|
| RED | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |
| Export | `Phase: repeat` 또는 `Phase: REPORT` |

### 9.3 C2C Rule 1~3

| Rule | 내용 |
|------|------|
| Rule1 | 본 PRD **FR 한 줄** → To-Do 1개 |
| Rule2 | To-Do 1개 → Test ID 1개, Given/When/Then |
| Rule3 | Mom Test·검증 순서·`incomplete` 함정 반영 점검 |

### 9.4 Command 체인

```
/red-test-plan → /red-skeleton → /tdd-red
       → /green-minimal → /golden-master
       → /refactor-smell → /refactor-safe
       → /export (magic-square-docs)
```

| Command | 역할 |
|---------|------|
| `red-test-plan` | C2C·테스트 플랜 (파일 생성 없음) |
| `red-skeleton` | `pytest.fail` 스켈레톤 (`tests/`만) |
| `tdd-red` | assert 채우기 (`tests/`만) |
| `green-minimal` | RED 1묶음 최소 구현 (`src/`) |
| `golden-master` | Approval Test 구축·검증 |
| `refactor-smell` | 스멜 탐지 (수정 금지) |
| `refactor-safe` | 스멜 1건, Budget 내 리팩터 |
| `export` | Report + Transcript 쌍 |

### 9.5 REFACTOR Change Budget

파일 ≤3 · 클래스 ≤1 · 메서드 ≤3. 계약(입출력·`int[6]` 1-index) 불변.

### 9.6 git

- **commit은 사용자 명시 요청 시만**
- GREEN: 1 RED 묶음 = 1 커밋 권장

---

## 10. 아키텍처 · 파일 구조

### 10.1 ECB 레이어 (목표)

| 레이어 | 경로 (목표) | 현재 |
|--------|-------------|------|
| entity | `entity/`, `src/validate_lines.py` | `src/validate_lines.py` (stub) |
| constants SSOT | `entity/constants.py` | 상수 in `validate_lines.py` (이전) |
| boundary | (향후) | 범위 밖 |
| control | (향후) | 범위 밖 |

**규칙:** entity는 boundary/control **import 금지**.

### 10.2 저장소 레이아웃

```
MagicSquare_xx/
├── docs/
│   └── PRD.md                 # 본 문서
├── src/
│   └── validate_lines.py      # 핵심 API (구현 stub)
├── tests/
│   ├── test_validate_lines.py # fixture + 테스트
│   ├── conftest.py            # grid_g1 (예정)
│   ├── _approval.py           # golden (예정)
│   └── golden/                # *.approved.txt (예정)
├── entity/
│   └── constants.py           # SSOT (예정)
├── .cursorrules
├── .cursor/commands/          # TDD·export Command
├── .cursor/skills/
│   ├── magic-square-tdd/
│   └── magic-square-docs/
├── Report/                    # 세션 보고서
├── Prompting/                 # Transcript
└── pyproject.toml
```

---

## 11. 구현 상태 (2026-06-10)

| 항목 | 상태 |
|------|------|
| `.cursorrules` | ✅ ECB·API·TDD·검증 순서 |
| pytest 하네스 | ✅ fixture 4종, 테스트 함수 0 |
| `validate_lines` | ⏳ stub (`...`) |
| RED 테스트 | ⏳ 미작성 |
| Command (TDD 전체) | ✅ red-test-plan ~ refactor-safe |
| Skills | ✅ magic-square-tdd, magic-square-docs |
| `entity/constants.py` | ⏳ 예정 |
| FR-01~FR-06 테스트·구현 | ⏳ 다음 스프린트 |

---

## 12. 비기능 요구사항

| ID | 요구사항 |
|----|----------|
| NFR-01 | Python ≥ 3.10 |
| NFR-02 | AI·문서 응답 **한국어** |
| NFR-03 | TDD Phase **첫 줄 선언** |
| NFR-04 | Report/Transcript `{NN}.{슬러그}_*` 쌍 Export |
| NFR-05 | Mom Test 증거·성공 기준 추적 가능 |

---

## 13. 참조 문서

| 문서 | 용도 |
|------|------|
| `.cursorrules` | Rule 계층·TDD·Test Loop |
| `Report/01.MomTest_Report.md` | Mom Test 인터뷰 |
| `Report/03.Session3_Workbook_Report.md` | R-G-I-O·8계층 |
| `Report/04.Session3_Harness_Commands_Report.md` | 하네스·함정 격자 검증 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | Dual-Track TDD |
| `.cursor/skills/magic-square-docs/SKILL.md` | Report Export |
| `pyproject.toml` | pytest 설정 |

---

## 14. 용어

| 용어 | 정의 |
|------|------|
| 마방진 | 4×4에 1~16을 한 번씩 배치, 10선 합이 동일(34) |
| 10선 | 행 4 + 열 4 + 대각선 2 |
| Mom Test | 과거 행동 기반 문제 검증 인터뷰 |
| C2C | PRD FR → To-Do → Test ID 설계 체인 |
| ARRR | Ask · Respond · Refine · (repeat) |
| RED 묶음 | `/red-test-plan`에서 한 번에 스켈레톤/GREEN할 Test ID 범위 |

---

## 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1.0 | 2026-06-10 | 초안 — Mom Test·세션 3 산출물·Command/Skill 통합 |
