from __future__ import annotations

from PIL import ImageDraw


def draw_finder(draw: ImageDraw.ImageDraw, x: float, y: float, s: float, fill: int) -> None:
    r = s * 0.22
    draw.rounded_rectangle((x, y, x + s, y + s), radius=r, fill=fill)
    inset1 = s * 0.18
    draw.rounded_rectangle((x + inset1, y + inset1, x + s - inset1, y + s - inset1), radius=r * 0.65, fill=0)
    inset2 = s * 0.34
    draw.rounded_rectangle((x + inset2, y + inset2, x + s - inset2, y + s - inset2), radius=r * 0.45, fill=fill)


def draw_alignment(draw: ImageDraw.ImageDraw, x: float, y: float, s: float, fill: int) -> None:
    r = s * 0.2
    draw.rounded_rectangle((x, y, x + s, y + s), radius=r, fill=fill)
    draw.rounded_rectangle((x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75), radius=r * 0.6, fill=0)
    draw.rounded_rectangle((x + s * 0.4, y + s * 0.4, x + s * 0.6, y + s * 0.6), radius=r * 0.4, fill=fill)
