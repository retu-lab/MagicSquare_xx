# refactor-smell — ARRR R단계 (Refine ⑦)

`src/`·`tests/` 코드 **스멜 탐지만** 수행한다. **수정·commit 금지** — 후보는 `/refactor-safe`에 넘긴다.

> ARRR **R**(Refine) = TDD **REFACTOR ⑦**: 냄새 목록화. 실제 리팩터는 `/refactor-safe` 담당.

**Skill 참조:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

## Phase 선언 (필수)

응답 **첫 줄**은 반드시 다음 형식이다.

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | 값 |
|------|-----|
| `Scope` | `src/` · `tests/` (읽기·분석만) |
| `Track` | `Logic+UI` — entity·boundary·테스트 하네스 모두 스캔 |

이후 한국어로 진행한다.

## 전제 (필수)

작업 시작 전 **반드시** 전체 테스트를 실행한다.

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| **전부 PASS** | 스멜 탐지 진행 |
| **1건이라도 FAIL** | **즉시 중단** — 스멜 표 출력하지 않음. `/green-minimal`·`/golden-master` 등으로 GREEN 복구 후 재실행 |

## 대상

| 항목 | 값 |
|------|-----|
| 허용 | 파일 **읽기**, 스멜 표·후보 목록 **출력** |
| 금지 | `src/`·`tests/` **코드 수정** |
| 금지 | **git commit** (사용자 요청 포함 — 본 커맨드에서는 커밋하지 않음) |
| 금지 | 리팩터 제안을 코드 패치로 적용 |

## 스멜 유형 (탐지 기준)

아래 유형으로 `src/`·`tests/`를 스캔한다.

| 유형 | 설명 | 힌트 |
|------|------|------|
| **Long Method** | 한 함수·메서드가 과도하게 김 (관심사 혼재) | ~40줄 이상·다중 분기·중첩 |
| **Duplicated Code** | 동일·유사 로직 반복 | 합 계산·격자 검증·직렬화 중복 |
| **Mysterious Name** | 의도 불명 변수·함수명 | `x`, `tmp`, `data2` |
| **Magic Number** | `entity/constants.py` 밖 리터럴 | `34`, `4`, `16` in `src/` |
| **ECB 위반** | 레이어 침범 | entity→boundary/control import, 풀이·UI in entity |
| **Feature Envy** | 타 모듈 데이터를 과도하게 조작 | 다른 레이어 필드 연쇄 접근 |

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트·도메인 정확성·ECB 경계 위협 | Magic Number in `src/`, ECB 위반, 검증 순서 훼손 가능 중복 |
| **P1** | 유지보수 비용·가독성 | Long Method, Duplicated Code, Mysterious Name |
| **P2** | 미미한 정리 | 네이밍 취향, 주석 부족, 사소한 중복 |

## Change Budget (`/refactor-safe` 참고)

본 커맨드는 수정하지 않지만, 후보 제안 시 **한 번의 safe 리팩터** 예산을 명시한다.

| 항목 | 상한 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

후보가 예산을 초과하면 **분할**하여 `/refactor-safe`를 여러 번 실행하도록 안내한다.

## 작업 절차

1. **전제 확인** — `python -m pytest tests/ -v` 전부 PASS
2. **스캔** — `src/`, `tests/`, `entity/` (있으면) 읽기
3. **스멜 표 작성** — 아래 출력 형식
4. **후보 선정** — `/refactor-safe`에 넘길 **1~3개** (P0 우선)
5. **다음 안내** — 사용자에게 **P0 1개만** 골라 `/refactor-safe` 실행하라고 안내

## 출력 형식 (필수)

### 블록 1 — 스멜 표

| # | P | 유형 | 위치 (파일:줄·심볼) | 요약 | Change Budget 적합 |
|---|-----|------|---------------------|------|-------------------|
| 1 | P0 | Magic Number | `src/validate_lines.py:…` | `34` 리터럴 | yes (파일1·메서드1) |
| 2 | P1 | Long Method | `src/validate_lines.py:validate_lines` | 분기 과다 | yes |
| … | … | … | … | … | yes / no (초과 시 분할) |

- **P**: `P0` \| `P1` \| `P2`
- **유형**: Long Method \| Duplicated Code \| Mysterious Name \| Magic Number \| ECB 위반 \| Feature Envy
- 빈 스멜이면 한 줄: `스멜 없음 (PASS 유지)` — 후보 블록은 생략 가능

### 블록 2 — `/refactor-safe` 후보 (1~3개)

| 후보 | P | 유형 | 제안 작업 (한 줄) | 예상 touched |
|------|-----|------|-------------------|--------------|
| A | P0 | Magic Number | `MAGIC_CONSTANT` import로 치환 | 1 file, 1 method |
| B | P1 | Duplicated Code | 행 합 계산 헬퍼 추출 | 2 files, 1 method |
| C | … | … | … | … |

- 후보는 **구체적**이되 **코드 패치 없이** 설명만
- P0 후보가 있으면 **최소 1개** 포함

### 블록 3 — 다음 안내 (필수)

```markdown
## 다음 단계
- **P0 후보 1개만** 골라 `/refactor-safe` 실행 (예: 후보 A)
- PASS 유지: 리팩터 후 `python -m pytest tests/ -v`는 `/refactor-safe`에서 수행
- 본 커맨드(`/refactor-smell`)에서는 코드 수정·commit 하지 않음
```

## 보고 형식 (필수)

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## 전제
- `python -m pytest tests/ -v` → N passed, 0 failed ✅

## 스멜 표
(블록 1 표)

## /refactor-safe 후보
(블록 2 표)

## 다음 단계
P0 1개만 골라 `/refactor-safe` 실행 — 권장: 후보 A (…)
```

## 금지 (본 커맨드 위반)

| 금지 | 이유 |
|------|------|
| **코드 수정** (`src/`·`tests/`·`entity/`) | Refine ⑦은 탐지만 |
| **git commit** | `/refactor-safe`·사용자 요청 단계 |
| pytest FAIL 상태에서 스멜 표 출력 | GREEN 전제 위반 |
| 후보 없이 임의 리팩터 제안을 패치로 적용 | safe 분리 |
| assert 완화·테스트 삭제 제안 | RED 회피 |

위반 시 작업을 중단하고, 위반 항목을 명시한다.

## 참조

- `.cursor/commands/green-minimal.md` — GREEN 선행
- `.cursor/commands/golden-master.md` — Approval Test 선행 (해당 시)
- `.cursor/commands/refactor-safe.md` — 스멜 후보 **실행** (후행)
- `.cursorrules` — ECB·TDD·검증 순서
- `entity/constants.py` — Magic Number 판별 SSOT

## 파이프라인 위치

1. RED → GREEN (`/green-minimal`) → (선택) `/golden-master`
2. **`/refactor-smell`** — 스멜 탐지 (수정 없음)
3. **`/refactor-safe`** — P0 1건 리팩터 + pytest PASS 유지
