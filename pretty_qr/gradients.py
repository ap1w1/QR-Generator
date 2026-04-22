from __future__ import annotations

from PIL import ImageColor


def to_rgb(color: str | tuple[int, int, int] | tuple[int, int, int, int]) -> tuple[int, int, int]:
    if isinstance(color, str):
        return ImageColor.getrgb(color)
    return color[:3]


def lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def gradient_t(x: int, y: int, w: int, h: int, mode: str = "diagonal") -> float:
    if mode == "horizontal":
        return x / max(1, w - 1)
    if mode == "vertical":
        return y / max(1, h - 1)
    return (x / max(1, w - 1) + y / max(1, h - 1)) * 0.5
