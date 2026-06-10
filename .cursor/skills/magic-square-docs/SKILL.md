---
name: magic-square-docs
description: >-
  MagicSquare_xx Report and Transcript export: ARRR cycle completion docs,
  session N reports, git/pytest collection, NN numbering, README updates.
  Use for Report Export, Transcript, /export-session, Phase repeat;
  ARRR 1-cycle completion report, or session N report requests.
disable-model-invocation: true
---

# magic-square-docs

세션 **Report + Transcript** 쌍 Export. `/export-session`·`/export`·「ARRR 1사이클 완료 보고」·「세션 N 보고서」 시 적용.

**Export 요청 시 magic-square-docs Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행.**

**SSOT 형식:** `Report/05.REPORT.md`, `Prompting/05.Export-Transcript.md` (구조 참조 — 실제 저장은 `{NN}.{슬러그}_*`).

**연동:** `.cursor/commands/export.md`, `.cursor/skills/magic-square-tdd/SKILL.md` (Phase·Test ID·Command).

**응답 언어:** 한국어.

---

## Phase 선언 (Export 완료 시)

```
Phase: repeat
```

ARRR 1사이클 완료·세션 Export 마무리용. 단순 `/export`는 `Phase: REPORT` 허용.

---

## 워크플로 (Step A → F)

### Step A — 입력 수집

터미널·채팅에서 **실측**만 수집한다.

| 입력 | 수집 방법 |
|------|-----------|
| git status | `git status -sb` 실행 |
| pytest | `python -m pytest tests/ -v` 실행 (세션에서 검증을 주장할 때) |
| Phase | 채팅 최종 선언: `red` \| `green` \| `refactor` \| `repeat` |
| Test ID | `T-001` … — `/red-test-plan`·GREEN 보고에서 |
| Command | `/red-test-plan`, `/red-skeleton`, `/green-minimal`, … |

**금지:** 실행하지 않은 pytest·git 결과를 Report에 **기재**.

---

### Step B — NN = max(Report, Prompting) + 1

1. `Report/` — `^\d{2}\.` 패턴 파일명에서 NN 최대값
2. `Prompting/` — 동일 (`04.Session3_Harness_Commands_Transcript.md` → `04`)
3. `NN = max + 1` (2자리, `05`, `06`, …)
4. `{슬러그}`: 세션 주제 영문 (PascalCase/snake). Report·Transcript **동일 NN·슬러그**

예: Report max `04`, Prompting max `04` → **NN = `05`**

---

### Step C — Report

- 템플릿: [report-template.md](report-template.md)
- 저장: `Report/{NN}.{슬러그}_Report.md`
- **Phase별 STEP** — 해당 Phase 섹션만 채움:

| Phase | STEP 섹션 |
|-------|-----------|
| RED | STEP — RED (`/red-test-plan`, `/red-skeleton`, `/tdd-red`) |
| GREEN | STEP — GREEN (`/green-minimal`, `/golden-master`) |
| REFACTOR | STEP — REFACTOR (`/refactor-smell`, `/refactor-safe`) |
| repeat | STEP — repeat (ARRR 1사이클 요약 + Mom Test 연계) |

메타 표(§0)에 Step A 수집값 반영.

---

### Step D — Transcript

- 템플릿: [transcript-template.md](transcript-template.md)
- 저장: `Prompting/{NN}.{슬러그}_Transcript.md`
- **User** — 프롬프트 원문 (fenced)
- **Cursor** — 응답 요약 3~5줄
- 헤더: `_Exported on {timestamp}_`, `_Source {uuid}_` (uuid 없으면 `unknown` 명시)
- Command 실행 턴에 `**Command:**` 기록

---

### Step E — README 갱신

| 파일 | 작업 |
|------|------|
| `Report/README.md` | 표에 `{NN}.{슬러그}_Report.md` 행 추가 |
| `Prompting/README.md` | 표에 `{NN}.{슬러그}_Transcript.md` 행 추가 |

기존 행 형식·순서 유지. 대응 Report↔Transcript 링크.

---

### Step F — 완료 보고 (채팅)

생성 **경로 2개** 필수:

```markdown
Phase: repeat

## 생성 파일
| 경로 | 설명 |
|------|------|
| Report/{NN}.{슬러그}_Report.md | 세션 보고서 |
| Prompting/{NN}.{슬러그}_Transcript.md | Transcript |

## 요약
(핵심 3줄)

## 다음 권장 작업
(1줄)
```

---

## ARRR 1사이클 완료 보고

「ARRR 1사이클 완료」「세션 N 보고서」 요청 시:

1. [phase-checklist.md](phase-checklist.md) 전 Step 실행
2. Report **STEP — repeat** + RED/GREEN/REFACTOR 각 STEP 요약
3. `Phase: repeat` 선언
4. magic-square-tdd 파이프라인 위치 명시 (어느 Command까지 완료했는지)

| ARRR | TDD | Report STEP |
|------|-----|-------------|
| Ask | RED | STEP — RED |
| Respond | GREEN | STEP — GREEN |
| Refine | REFACTOR | STEP — REFACTOR |
| (사이클 닫기) | — | STEP — repeat |

---

## `/export-session` 연동

`.cursor/commands/export-session.md`(또는 `/export`) 실행 시:

1. **magic-square-docs** Skill 로드
2. [phase-checklist.md](phase-checklist.md) Step A→F 순서 준수
3. Report·Transcript **쌍** 필수 — 단독 Report 금지
4. 완료 보고 Step F 형식

`/export` (legacy)와 동일 산출물 규칙; 본 Skill이 NN·Phase STEP·Transcript 메타를 **표준화**.

---

## 산출물 규칙

| 규칙 | 내용 |
|------|------|
| 쌍 저장 | Report + Transcript 항상 함께 |
| NN | 중복·건너뛰기 금지 |
| 덮어쓰기 | 기존 `{NN}.*` 덮어쓰기 금지 (사용자 확인 후만) |
| pytest | **실행한 명령 + 실측 결과**만 |
| golden | `UPDATE_GOLDEN` 임의 실행·문서화 금지 (golden-master Command 따름) |
| 코드 | `src/`·`tests/` **수정 금지** (문서만) |

---

## 금지

| 금지 | 이유 |
|------|------|
| 임의 **git commit** | 사용자 요청 시만 |
| **UPDATE_GOLDEN=1** 임의 | golden-master 절차 |
| 채팅·터미널에 **없는** pytest 결과 | 허위 검증 기록 |
| Transcript 없이 Report만 | Export 쌍 규격 |
| Report/Prompting **외** 경로 저장 | 폴더 규격 |
| 추정 프롬프트·가상 턴 | Transcript 신뢰성 |

---

## 참조 파일

| 파일 | 용도 |
|------|------|
| [report-template.md](report-template.md) | Report 본문 골격 |
| [transcript-template.md](transcript-template.md) | Transcript 본문·메타 |
| [phase-checklist.md](phase-checklist.md) | Step A~F 체크리스트 |
| `Report/05.REPORT.md` | SSOT 형식 예 (구조 참조) |
| `Prompting/05.Export-Transcript.md` | SSOT 형식 예 (구조 참조) |
| `.cursor/commands/export.md` | legacy export Command |

---

## 빠른 참조 — 기존 산출물

| NN | Report | Transcript |
|----|--------|------------|
| 01 | MomTest | (Prompting 01~04 워크플로) |
| 02 | MomTest Simulation | 05 simulation |
| 03 | Session3 Workbook | 06 workbook |
| 04 | Harness Commands | 04 Harness Transcript |
| **05+** | **본 Skill로 생성** | **본 Skill로 생성** |
