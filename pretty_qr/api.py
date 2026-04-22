from __future__ import annotations

from pathlib import Path

from PIL import Image

from .logo import add_center_logo
from .models import PrettyQRConfig
from .presets import apply_preset
from .renderer import PrettyQRRenderer


def generate_pretty_qr(
    data: str,
    output_path: str | Path | None = None,
    *,
    size: int = 1400,
    logo_path: str | Path | None = None,
    gradient_start: str = "#C15AC4",
    gradient_end: str = "#5298F2",
    background_color: str = "#FFFFFF",
    error_correction: str = "H",
    margin_modules: int = 4,
    cell_fill_ratio: float = 0.78,
    rounding_ratio: float = 0.46,
    logo_scale: float = 0.15,
    oversample: int = 3,
    preset: str | None = "telegram_like",
) -> Image.Image:
    config = PrettyQRConfig(
        data=data,
        output_path=output_path,
        size=size,
        logo_path=logo_path,
        gradient_start=gradient_start,
        gradient_end=gradient_end,
        background_color=background_color,
        error_correction=error_correction,
        margin_modules=margin_modules,
        cell_fill_ratio=cell_fill_ratio,
        rounding_ratio=rounding_ratio,
        logo_scale=logo_scale,
        oversample=oversample,
        preset=preset,
    )
    config = apply_preset(config)
    image = PrettyQRRenderer().render(config)
    if logo_path:
        image = add_center_logo(image, logo_path, config.logo_scale)
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
    return image
