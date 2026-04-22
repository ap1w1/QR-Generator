# pretty_qr

Python-модуль для генерации стилизованных QR-кодов со скругленной геометрией, градиентом и опциональным логотипом.

## Установка

```bash
pip install -e .
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

## Тесты

```bash
pytest -q
```
