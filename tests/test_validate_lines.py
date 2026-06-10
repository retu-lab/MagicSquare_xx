from src.validate_lines import (
    GRID_SIZE,
    LINE_IDS,
    MAGIC_CONSTANT,
    VERIFICATION_ORDER,
    validate_lines,
)

# Example — 완전 4×4 마방진 (빈칸 0, 1~16, 10선 합=34)
VALID_MAGIC_SQUARE = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# Constraint 위반 — 형식·범위 오류 (fail)
INVALID_GRID_SIZE = [
    [1, 2, 3],
    [4, 5, 6],
]

# Constraint 위반 — 합≠34 (fail, failed_lines에 해당 선 ID)
FAIL_ROW_SUM = [
    [1, 2, 3, 4],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# Mom Test 함정 — 행·열=34로 보이나 대각선 미확인 시 incomplete (RED에서 검증 순서·범위 테스트)
TRAP_ROWS_COLS_OK = VALID_MAGIC_SQUARE
