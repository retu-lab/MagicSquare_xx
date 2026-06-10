import pytest

from entity.constants import CELL_COUNT, GRID_SIZE, MAGIC_CONSTANT

# 상수 SSOT 참조 (스켈레톤 — /tdd-red 에서 Given 검증에 사용)
_DOMAIN = (GRID_SIZE, MAGIC_CONSTANT, CELL_COUNT)


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개)
    grid = grid_g1

    # When: find_blank_coords(grid_g1) 호출
    # result = find_blank_coords(grid)

    # Then: [(2,2),(3,3)] 반환 (1-index, row-major)
    pytest.fail("RED: D-LOC-01 — 구현 없음, 의도적 실패")
