import pytest

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

# Constraint 위반 — 1~16 중복·누락 (fail)
DUPLICATE_VALUE = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 16],
]

# Mom Test 함정 — 행·열=34로 보이나 대각선 미확인 시 incomplete (RED에서 검증 순서·범위 테스트)
TRAP_ROWS_COLS_OK = VALID_MAGIC_SQUARE


def test_T001_valid_magic_square_passes():
    # Given
    grid = VALID_MAGIC_SQUARE

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-001 — expect status pass, failed_lines []")


def test_T002_invalid_grid_size_fails():
    # Given
    grid = INVALID_GRID_SIZE

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-002 — expect status fail for non-4x4 grid")


def test_T003_duplicate_value_fails():
    # Given
    grid = DUPLICATE_VALUE

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-003 — expect status fail for duplicate or missing 1~16")


def test_T004_fail_row_sum_fails_with_line_id():
    # Given
    grid = FAIL_ROW_SUM

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-004 — expect status fail, R1 in failed_lines")


def test_T005_trap_rows_cols_ok_incomplete():
    # Given
    grid = TRAP_ROWS_COLS_OK

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-005 — expect status incomplete, not pass before D1 D2")
