from __future__ import annotations

from .models import PrettyQRConfig


PRESETS = {
    "telegram_like": {

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
