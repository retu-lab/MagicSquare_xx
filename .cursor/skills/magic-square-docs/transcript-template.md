# Transcript 템플릿 — `{NN}.{슬러그}_Transcript.md`

SSOT 형식 참조: `Prompting/05.Export-Transcript.md` (신규는 `Prompting/{NN}.{슬러그}_Transcript.md`).

```markdown
# {세션 제목} — Transcript

**일자:** YYYY-MM-DD  
**세션:** N  
**Phase:** {red | green | refactor | repeat}  
**대응 보고서:** `Report/{NN}.{슬러그}_Report.md`

_Exported on {ISO-8601 또는 YYYY-MM-DD HH:MM TZ}_  
_Source {uuid}_

---

## Turn 1 — User

\`\`\`
(사용자 프롬프트 원문 — 채팅에서 그대로)
\`\`\`

## Turn 1 — Cursor

(핵심 응답 3~5줄: 수행 작업, Phase 선언, 변경 파일)

**Command:** (해당 시 `/red-test-plan` 등)

---

## Turn 2 — User

\`\`\`
(프롬프트 원문)
\`\`\`

## Turn 2 — Cursor

(요약)

**Command:** …

---

## Turn N — User

\`\`\`
…
\`\`\`

## Turn N — Cursor

(요약)

---

## 세션 메타 (Export 시 채움)

| 항목 | 값 |
|------|-----|
| Commands 실행 | /… |
| Test ID | T-… |
| pytest (실행한 경우만) | 명령 + 실측 결과 |
| 생성·수정 파일 | (경로 목록) |
```

## 필드 규칙

| 필드 | 규칙 |
|------|------|
| **User** | 사용자 메시지 원문 — fenced code block |
| **Cursor** | AI 응답 요약 (전문 붙여넣기 불필요, 핵심만) |
| **_Exported on** | Export 수행 시각 (로컬 또는 UTC 명시) |
| **_Source** | 세션·에이전트 transcript uuid (채팅·agent transcript에서 확보; 없으면 `unknown` 명시) |
| **Command** | slash command 실행 턴에만 기록 |

## 슬러그·경로

- 저장: `Prompting/{NN}.{슬러그}_Transcript.md`
- Report와 **동일 NN·슬러그**, 접미사만 `_Transcript`
- 예: `05.Session3_TDD_ARRR_Cycle1_Transcript.md`

## 금지

- 채팅에 없는 턴·프롬프트 **추정 작성**
- 실행하지 않은 pytest 결과 기재
