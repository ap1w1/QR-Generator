from __future__ import annotations

from dataclasses import dataclass

import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

ERROR_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


@dataclass(slots=True)
class QRMatrix:
    matrix: list[list[bool]]

    @property
    def size(self) -> int:
        return len(self.matrix)


def build_qr_matrix(data: str, error_correction: str = "H") -> QRMatrix:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_MAP[error_correction],
        box_size=10,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return QRMatrix(matrix=qr.get_matrix())


def is_in_finder(x: int, y: int, n: int) -> bool:
    zones = [
        (0, 0),
        (n - 7, 0),
        (0, n - 7),
    ]
    return any(zx <= x < zx + 7 and zy <= y < zy + 7 for zx, zy in zones)


def is_timing(x: int, y: int, n: int) -> bool:
    return ((y == 6 and 8 <= x < n - 8) or (x == 6 and 8 <= y < n - 8))


def function_module_mask(matrix: list[list[bool]]) -> list[list[bool]]:
    n = len(matrix)
    mask = [[False] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            if is_in_finder(x, y, n) or is_timing(x, y, n):
                mask[y][x] = True
    # format info around finders
    for i in range(9):
        if i != 6:
            mask[8][i] = True
            mask[i][8] = True
            mask[8][n - 1 - i] = True
            mask[n - 1 - i][8] = True
    # dark module
    if n > 8:
        mask[n - 8][8] = True
    return mask


def alignment_centers(version: int) -> list[int]:
    if version == 1:
        return []
    return qrcode.util.pattern_position(version)
