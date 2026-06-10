import pytest


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """4×4 G1 격자, 빈칸 0 두 개 — (2,2)·(3,3) 1-index, row-major."""
    return [
        [1, 3, 2, 13],
        [5, 0, 11, 8],
        [9, 6, 0, 12],
        [4, 15, 14, 16],
    ]
