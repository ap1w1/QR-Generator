# pretty_qr

Python-модуль для генерации стилизованных QR-кодов со скругленной геометрией, градиентом и опциональным логотипом.

## Установка

```bash
pip install -e .
```

## Важно для сканируемости

По умолчанию включен `scan_safe_mode=True`:

- функциональные зоны QR (finder/timing/format/alignment/version/dark module) рисуются более консервативно;
- quiet zone сохраняется минимум 4 модуля;
- стиль сглаживания не размывает служебные паттерны.

Если нужен более агрессивный визуальный стиль, можно отключить защиту (`scan_safe_mode=False` или `--unsafe-style`), но это может снизить читаемость.

## Быстрый старт

```python
from pretty_qr import generate_pretty_qr

img = generate_pretty_qr(
    data="https://t.me/test",
    output_path="examples/telegram_like.png",
    size=1400,
    preset="telegram_like",
    scan_safe_mode=True,
)
```

## CLI

```bash
python -m pretty_qr.cli \
  --data "https://t.me/test" \
  --out examples/qr.png \
  --size 1400 \
  --logo examples/logo.png \
  --start "#C15AC4" \
  --end "#5298F2" \
  --bg "#FFFFFF" \
  --preset telegram_like
```

## Основные возможности

- Скругленный рендер модулей с мягкими соединениями соседних data-модулей.
- Защищенный рендер функциональных зон для сохранения сканируемости.
- Диагональный, горизонтальный, вертикальный градиент.
- Центральный логотип в белом круглом бейдже.
- Экспорт в PNG (через Pillow), возврат изображения в памяти.

## Тесты

```bash
pytest -q
```
