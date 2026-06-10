# export — 보고서·Transcript Export

세션 산출물 **보고서 생성 전용** 커맨드. 대화·작업 결과를 정리해 파일로보낸다.

## Phase 선언 (필수)

응답 **첫 줄**은 반드시 다음 형식이다.

```
Phase: REPORT
```

이후 한국어로 진행한다.

## 산출물 (2개 필수)

| # | 경로 | 용도 |
|---|------|------|
| 1 | `Report/` | 세션 **보고서** (결과·요약·판단) |
| 2 | `Prompting/` | **Transcript** (사용한 프롬프트·대화 export) |

두 파일 모두 **`{NN}.{슬러그}` 형식**으로 저장한다.

## 파일명 규칙 — `{NN}.{슬러그}`

- 형식: `{NN}.{슬러그}_Report.md` / `{NN}.{슬러그}_Transcript.md` — 예: `04.Session3_TDD_RED_Report.md`, `04.Session3_TDD_RED_Transcript.md`
- `{NN}`: 해당 폴더 기존 파일의 **다음 순번** (2자리, `01`~`99`). `Report/README.md`·폴더 목록을 확인해 중복·건너뛰기 방지.
- `{슬러그}`: 세션 주제를 영문·PascalCase 또는 snake (공백·한글 파일명 금지)
- Report와 Transcript는 **같은 NN·슬러그**를 공유하고 접미사만 구분:
  - 보고서: `Report/{NN}.{슬러그}_Report.md`
  - Transcript: `Prompting/{NN}.{슬러그}_Transcript.md`

현재 Report 최대 순번 참고: `03.Session3_Workbook_Report.md` → 다음 세션은 `04....`부터.  
Prompting은 기존 `{NN}_` 접두 파일(`01_STEP1_...` ~ `06_Session3_Workbook.md`)과 병행 가능; **신규 Transcript**는 `{NN}.{슬러그}_Transcript.md` 규칙을 따른다.

## Report 작성 절차

1. **수집** — 이번 세션의 목표, 입력(Mom Test·커서룰·하네스), 수행 내용, pytest/TDD 결과(해당 시)
2. **구조화** — 아래 보고서 템플릿에 맞춰 작성
3. **저장** — `Report/{NN}.{슬러그}_Report.md` 생성 (기존 파일 덮어쓰기는 사용자 확인 후)

## Transcript Export 절차

1. **포함** — 이번 세션에서 사용자가 보낸 **프롬프트 원문**, 핵심 AI 응답 요약, 실행한 slash command (`/tdd-red` 등)
2. **형식** — 프롬프트는 fenced code block, 턴 순서대로 번호 매김
3. **저장** — `Prompting/{NN}.{슬러그}_Transcript.md` 생성

Transcript 템플릿:

```markdown
# {세션 제목} — Transcript

**일자:** YYYY-MM-DD  
**대응 보고서:** `Report/{NN}.{슬러그}_Report.md`

---

## Turn 1 — 사용자

\`\`\`
(프롬프트 원문)
\`\`\`

## Turn 1 — AI (요약)

(핵심 응답 3~5줄)

---

## Turn 2 — 사용자
...
```

## 보고서 템플릿

```markdown
# MagicSquare_xx — {세션 제목}

**프로젝트:** 4×4 마방진 (ECB 분류 과제)  
**일자:** YYYY-MM-DD  
**기반:** (Mom Test / .cursorrules / 이전 보고서 링크)

---

## 1) 세션 목표

(한 문장)

## 2) 수행 내용

| 항목 | 내용 |
|------|------|
| ... | ... |

## 3) 산출물

| 파일 | 설명 |
|------|------|
| ... | ... |

## 4) 검증·결과 (해당 시)

- pytest / TDD Phase / Test Loop 결과

## 5) Mom Test·성공 기준 연계 (해당 시)

| 성공 기준 | 이번 세션 충족 여부 |
|-----------|---------------------|
| ... | ... |

## 6) 다음 단계

- (한두 항목)

---

## 멘토 코멘트

(솔루션 최소화, 진짜 문제·습관 관점 2~4문장)
```

## 완료 보고 형식

작업 마무리 시 아래로 보고한다.

```markdown
Phase: REPORT

## 생성 파일
| 경로 | 설명 |
|------|------|
| Report/{NN}.{슬러그}_Report.md | 세션 보고서 |
| Prompting/{NN}.{슬러그}_Transcript.md | Transcript export |

## 요약
(보고서 핵심 3줄)

## 다음 권장 작업
(한 줄)
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | 보고서 커맨드 범위 밖 (TDD GREEN 담당) |
| `tests/` assert 완화·skip·xfail | TDD RED/GREEN 담당 |
| Report·Prompting **외** 폴더에 산출물 저장 | 경로 규격 |
| 순번 `{NN}` 중복·임의 건너뛰기 | `{NN}.{슬러그}`命名 일관성 |
| Transcript 없이 Report만 저장 | Export 쌍 필수 |
| 임의 git commit | 사용자 요청 시만 |

위반 시 작업을 중단하고, 위반 항목을 명시한다.

## 참조

- 기존 보고서: `Report/01.MomTest_Report.md`, `Report/02.MomTest_Simulation_Report.md`, `Report/03.Session3_Workbook_Report.md`
- 기존 프롬프트: `Prompting/01_STEP1_...` ~ `06_Session3_Workbook.md`
- 프로젝트 규칙: `.cursorrules`
