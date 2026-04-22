from __future__ import annotations

from .models import PrettyQRConfig


PRESETS = {
    "telegram_like": {
        "cell_fill_ratio": 0.84,
        "rounding_ratio": 0.43,
        "logo_scale": 0.13,
        "gradient_start": "#C15AC4",
        "gradient_end": "#5298F2",
        "gradient_mode": "diagonal",
        "scan_safe_mode": True,
    },
    "soft_minimal": {
        "cell_fill_ratio": 0.78,
        "rounding_ratio": 0.36,
        "scan_safe_mode": True,
    },
}


def apply_preset(config: PrettyQRConfig) -> PrettyQRConfig:
    if not config.preset:
        return config
    preset = PRESETS.get(config.preset)
    if not preset:
        return config
    for key, value in preset.items():
        setattr(config, key, value)
    return config
