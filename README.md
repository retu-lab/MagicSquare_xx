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

## 테스트 Fixture

| Fixture | 용도 |
|---------|------|
| `VALID_MAGIC_SQUARE` | 완전 마방진 → `pass` |
| `INVALID_GRID_SIZE` | 형식 오류 → `fail` |
| `FAIL_ROW_SUM` | 행 합≠34 → `fail`, `R1` |
| `TRAP_ROWS_COLS_OK` | Mom Test 함정 → `incomplete` |

---

## 기능 요구사항 (요약)

| FR | 내용 | Test ID |
|----|------|---------|
| FR-01 | 10선 합 34 → `pass` | T-001 |
| FR-02 | 형식·범위 오류 → `fail` | T-002 |
| FR-03 | 1~16 중복·누락 → `fail` | T-003 |
| FR-04 | 선 합≠34 → `fail` + 선 ID | T-004 |
| FR-05 | 대각선 미검증 → `incomplete` | T-005 |

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
