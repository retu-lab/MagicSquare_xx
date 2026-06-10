# Phase Export Checklist

`/export-session` 또는 Report Export 요청 시 **순서대로** 확인. 미충족 시 해당 Step에서 중단.

## Step A — 입력 수집

- [ ] `git status` (또는 `git status -sb`) **실행** — 결과 요약 확보
- [ ] `python -m pytest tests/ -v` **실행** (세션에서 검증 주장이 있을 때만 Report에 기재)
- [ ] 채팅에서 **Phase** 선언 수집 (`red` / `green` / `refactor` / `repeat`)
- [ ] **Test ID** 목록 (T-001 …)
- [ ] 실행한 **Command** 목록 (/red-test-plan, /green-minimal, …)
- [ ] 세션 제목·슬러그·세션 N 번호 확정

**금지:** 위 명령을 실행하지 않고 pytest·git 결과 **작성**

---

## Step B — 순번 NN

- [ ] `Report/`에서 `{NN}.` 접두 최대값 조회
- [ ] `Prompting/`에서 `{NN}.` 접두 최대값 조회 (예: `04.Session3_…`)
- [ ] `NN = max(Report_MAX, Prompting_MAX) + 1` (2자리 `01`~`99`)
- [ ] 동일 NN·슬러그가 이미 있으면 **건너뛰기·중복 없음** 확인

현재 참고: Report `04.*` → 다음 `05` (SSOT 예시 `05.REPORT.md`).

---

## Step C — Report 작성

- [ ] [report-template.md](report-template.md) 구조 따름
- [ ] Phase에 맞는 **STEP** 섹션만 채움 (RED / GREEN / REFACTOR / repeat)
- [ ] `Report/{NN}.{슬러그}_Report.md` 저장
- [ ] 기존 파일 **덮어쓰기 없음** (사용자 확인 없이)

---

## Step D — Transcript 작성

- [ ] [transcript-template.md](transcript-template.md) 구조 따름
- [ ] User / Cursor 턴 번호 매김
- [ ] `_Exported on` · `_Source {uuid}` 헤더
- [ ] `Prompting/{NN}.{슬러그}_Transcript.md` 저장 (Report와 NN·슬러그 일치)

---

## Step E — README 갱신

- [ ] `Report/README.md` 표에 신규 Report 행 추가
- [ ] `Prompting/README.md` 표에 신규 Transcript 행 추가
- [ ] 대응 관계(Report ↔ Transcript) 한 줄 링크

---

## Step F — 완료 보고 (채팅)

- [ ] `Phase: repeat` 또는 `Phase: REPORT` 선언
- [ ] 생성 경로 **2개** 명시
- [ ] 보고서 요약 3줄
- [ ] 다음 권장 작업 1줄

```markdown
Phase: repeat

## 생성 파일
| 경로 | 설명 |
|------|------|
| Report/{NN}.{슬러그}_Report.md | … |
| Prompting/{NN}.{슬러그}_Transcript.md | … |

## 요약
(3줄)

## 다음 권장 작업
(1줄)
```

---

## 금지 (체크리스트 공통)

- [ ] 임의 **git commit** 하지 않음
- [ ] **UPDATE_GOLDEN=1** 임의 실행·기록하지 않음
- [ ] 채팅·터미널에 **없는** pytest 결과 Report/Transcript에 기재하지 않음
- [ ] Report만 저장하고 Transcript 생략하지 않음
