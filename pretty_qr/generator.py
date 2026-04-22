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

    @property
    def version(self) -> int:
        return version_from_size(self.size)


def version_from_size(size: int) -> int:
    return (size - 21) // 4 + 1


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
    return (y == 6 and 8 <= x < n - 8) or (x == 6 and 8 <= y < n - 8)


def alignment_centers(version: int) -> list[int]:
    if version == 1:
        return []
    return qrcode.util.pattern_position(version)


def is_in_alignment(x: int, y: int, version: int, n: int) -> bool:
    centers = alignment_centers(version)
    for cy in centers:
        for cx in centers:
            if (cx < 9 and cy < 9) or (cx > n - 10 and cy < 9) or (cx < 9 and cy > n - 10):
                continue
            if cx - 2 <= x <= cx + 2 and cy - 2 <= y <= cy + 2:
                return True
    return False


def function_module_mask(matrix: list[list[bool]]) -> list[list[bool]]:
    n = len(matrix)
    version = version_from_size(n)
    mask = [[False] * n for _ in range(n)]

    for y in range(n):
        for x in range(n):
            if is_in_finder(x, y, n) or is_timing(x, y, n) or is_in_alignment(x, y, version, n):
                mask[y][x] = True

    # separators around finders
    for i in range(8):
        mask[7][i] = True
        mask[i][7] = True
        mask[7][n - 1 - i] = True
        mask[i][n - 8] = True
        mask[n - 8][i] = True
        mask[n - 1 - i][7] = True

    # format information
    for i in range(9):
        if i != 6:
            mask[8][i] = True
            mask[i][8] = True
            mask[8][n - 1 - i] = True
            mask[n - 1 - i][8] = True

    # dark module
    if n > 8:
        mask[n - 8][8] = True

    # version information (v7+)
    if version >= 7:
        for dy in range(6):
            for dx in range(3):
                mask[dy][n - 11 + dx] = True
                mask[n - 11 + dx][dy] = True

    return mask
