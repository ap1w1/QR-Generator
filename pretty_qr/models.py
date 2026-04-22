from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

ColorType = str | tuple[int, int, int] | tuple[int, int, int, int]
GradientMode = Literal["diagonal", "horizontal", "vertical"]


@dataclass(slots=True)
class PrettyQRConfig:
    data: str
    output_path: str | Path | None = None
    size: int = 1400
    logo_path: str | Path | None = None
    gradient_start: ColorType = "#C15AC4"
    gradient_end: ColorType = "#5298F2"
    background_color: ColorType = "#FFFFFF"
    error_correction: Literal["L", "M", "Q", "H"] = "H"
    margin_modules: int = 4
    cell_fill_ratio: float = 0.82
    rounding_ratio: float = 0.42
    logo_scale: float = 0.13
    oversample: int = 3
    preset: str | None = "telegram_like"
    gradient_mode: GradientMode = "diagonal"
    gradient_fn: Callable[[float], float] | None = None
    scan_safe_mode: bool = True

    def validate(self) -> None:
        if not self.data:
            raise ValueError("data must be non-empty")
        if self.size < 128:
            raise ValueError("size must be >= 128")
        if self.margin_modules < 4:
            raise ValueError("margin_modules must be >= 4 for scan safety")
        if not (0.55 <= self.cell_fill_ratio <= 1.0):
            raise ValueError("cell_fill_ratio must be in [0.55, 1.0]")
        if not (0.0 <= self.rounding_ratio <= 0.5):
            raise ValueError("rounding_ratio must be in [0.0, 0.5]")
        if not (0.05 <= self.logo_scale <= 0.18):
            raise ValueError("logo_scale must be in [0.05, 0.18]")
        if self.oversample < 1:
            raise ValueError("oversample must be >= 1")
