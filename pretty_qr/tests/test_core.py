from pathlib import Path

from PIL import Image

from pretty_qr import PrettyQRConfig, generate_pretty_qr
from pretty_qr.generator import alignment_centers, build_qr_matrix, function_module_mask, version_from_size


def test_matrix_generation_non_empty() -> None:
    matrix = build_qr_matrix("https://example.com", "H").matrix
    assert len(matrix) >= 21
    assert len(matrix) == len(matrix[0])


def test_function_mask_marks_finder_and_timing() -> None:
    matrix = build_qr_matrix("hello", "H").matrix
    mask = function_module_mask(matrix)
    n = len(matrix)
    assert mask[0][0]
    assert mask[6][6]
    assert mask[6][10]
    assert mask[10][6]
    assert mask[n - 8][8]


def test_alignment_centers_v2() -> None:
    assert alignment_centers(2) == [6, 18]


def test_version_from_size() -> None:
    assert version_from_size(21) == 1
    assert version_from_size(25) == 2


def test_config_validation() -> None:
    cfg = PrettyQRConfig(data="ok")
    cfg.validate()


def test_generate_and_save(tmp_path: Path) -> None:
    out = tmp_path / "qr.png"
    img = generate_pretty_qr("https://example.com", output_path=out, size=512)
    assert out.exists()
    assert isinstance(img, Image.Image)
    assert img.size == (512, 512)
