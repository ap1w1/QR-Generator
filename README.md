# pretty_qr

Python-модуль для генерации стилизованных QR-кодов со скругленной геометрией, градиентом и опциональным логотипом.

## Установка

```bash
pip install -e .
```

## Быстрый старт

```python
from pretty_qr import generate_pretty_qr

img = generate_pretty_qr(
    data="https://t.me/test",
    output_path="examples/telegram_like.png",
    size=1400,
    preset="telegram_like",
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

- Скругленный рендер модулей с визуальным объединением через oversampling + blur/threshold.
- Кастомные finder/alignment patterns.
- Диагональный, горизонтальный, вертикальный градиент.
- Центральный логотип в белом круглом бейдже.
- Экспорт в PNG (через Pillow), возврат изображения в памяти.

## Тесты

```bash
pytest -q
```
