from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def add_center_logo(image: Image.Image, logo_path: str | Path, scale: float = 0.15) -> Image.Image:
    img = image.convert("RGBA")
    w, h = img.size
    badge_d = int(min(w, h) * scale * 1.15)
    cx, cy = w // 2, h // 2

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((cx - badge_d // 2, cy - badge_d // 2, cx + badge_d // 2, cy + badge_d // 2), fill=(255, 255, 255, 255))

    logo = Image.open(logo_path).convert("RGBA")
    max_logo = int(badge_d * 0.68)
    logo.thumbnail((max_logo, max_logo), Image.Resampling.LANCZOS)
    lx = cx - logo.width // 2
    ly = cy - logo.height // 2
    overlay.alpha_composite(logo, (lx, ly))

    return Image.alpha_composite(img, overlay)
