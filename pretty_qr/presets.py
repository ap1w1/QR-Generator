from __future__ import annotations

from .models import PrettyQRConfig


PRESETS = {
    "telegram_like": {
        "cell_fill_ratio": 0.8,
        "rounding_ratio": 0.48,
        "gradient_start": "#C15AC4",
        "gradient_end": "#5298F2",
        "gradient_mode": "diagonal",
    },
    "soft_minimal": {
        "cell_fill_ratio": 0.72,
        "rounding_ratio": 0.38,
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
