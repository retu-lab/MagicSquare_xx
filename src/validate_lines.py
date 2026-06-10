from typing import Literal, TypedDict

GRID_SIZE = 4
MAGIC_CONSTANT = 34
VALID_VALUES = frozenset(range(1, GRID_SIZE * GRID_SIZE + 1))

LINE_IDS = ("R1", "R2", "R3", "R4", "C1", "C2", "C3", "C4", "D1", "D2")
VERIFICATION_ORDER = LINE_IDS


class ValidateLinesResult(TypedDict):
    status: Literal["pass", "fail", "incomplete"]
    failed_lines: list[str]


def validate_lines(grid: list[list[int]]) -> ValidateLinesResult:
    """4×4 격자의 10선(R1~R4·C1~C4·D1·D2) 합을 검증한다.

    Returns:
        status: pass | fail | incomplete
        failed_lines: 불합격·미검증 선 ID (예: ["D1"], [])
    """
    ...
