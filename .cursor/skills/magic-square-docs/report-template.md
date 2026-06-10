# Report 템플릿 — `{NN}.{슬러그}_Report.md`

SSOT 형식 참조: `Report/05.REPORT.md` (신규 세션은 `Report/{NN}.{슬러그}_Report.md`로 저장).

```markdown
# MagicSquare_xx — {세션 제목}

**프로젝트:** 4×4 마방진 (ECB 분류 과제)  
**일자:** YYYY-MM-DD  
**세션:** N  
**Phase:** {red | green | refactor | repeat}  
**기반:** `.cursorrules`, `docs/PRD.md`, (이전 보고서 링크)

---

## 0) 메타 (Step A 수집)

| 항목 | 값 |
|------|-----|
| git status | (실행 결과 요약 — clean / M files / ?? untracked) |
| pytest | `python -m pytest tests/ -v` → (실행 결과만 기재) |
| Phase 선언 | (세션 최종 Phase 첫 줄) |
| Test ID | T-001 … (해당 시) |
| Command | /red-test-plan, /green-minimal, … |

---

## 1) 세션 목표

(한 문장 — ARRR 사이클·세션 N 주제)

---

## 2) Phase별 STEP

### STEP — RED (해당 시)

| 항목 | 내용 |
|------|------|
| Command | `/red-test-plan`, `/red-skeleton`, `/tdd-red` |
| Test ID | T-… |
| 산출 | C2C 표 / pytest.fail 스켈레톤 / assert |
| pytest | (실행 명령 + **실제** 결과) |

### STEP — GREEN (해당 시)

| 항목 | 내용 |
|------|------|
| Command | `/green-minimal`, `/golden-master` |
| RED 묶음 | T-… |
| 변경 | `src/` 최소 구현 요약 |
| pytest | (실행 명령 + **실제** 결과) |
| golden | matched yes/no/n/a |

### STEP — REFACTOR (해당 시)

| 항목 | 내용 |
|------|------|
| Command | `/refactor-smell`, `/refactor-safe` |
| 스멜 | # / 후보, 유형, P |
| Budget | 파일 N/3 · 클래스 N/1 · 메서드 N/3 |
| pytest + golden | (실행 결과) |

### STEP — repeat (ARRR 1사이클 완료, 해당 시)

| 항목 | 내용 |
|------|------|
| 사이클 요약 | Ask(RED) → Respond(GREEN) → Refine(REFACTOR) 한 바퀴 |
| PASS Test ID | … |
| 미완 | 다음 사이클 항목 |
| Mom Test 연계 | 성공 기준 1~3 충족 여부 |

---

## 3) 산출물

| 파일 | 설명 |
|------|------|
| … | … |

---

## 4) 검증·결과

- pytest: (명령 + 실측 결과만)
- TDD Phase / Test Loop / golden (해당 시)

---

## 5) Mom Test·성공 기준 연계 (해당 시)

| 성공 기준 | 이번 세션 충족 여부 |
|-----------|---------------------|
| 1 — 대각선 확인 전 pass 금지 | ✅ / ⏳ / ❌ |
| 2 — 계산 실수 의심 전 대각선 짚기 | … |
| 3 — 검증 순서·Test Loop | … |

---

## 6) 다음 단계

- (한두 항목)

---

## 멘토 코멘트

(솔루션 최소화, 진짜 문제·습관 관점 2~4문장)
```

## 슬러그·경로

- 저장: `Report/{NN}.{슬러그}_Report.md`
- `{슬러그}`: 영문 PascalCase/snake, 공백·한글 파일명 금지
- 예: `05.Session3_TDD_ARRR_Cycle1_Report.md`
