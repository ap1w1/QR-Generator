from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter

from .generator import alignment_centers, build_qr_matrix, function_module_mask
from .gradients import gradient_t, lerp_color, to_rgb
from .models import PrettyQRConfig
from .patterns import draw_alignment, draw_finder


class PrettyQRRenderer:
    def render(self, config: PrettyQRConfig) -> Image.Image:
        config.validate()
        matrix_obj = build_qr_matrix(config.data, config.error_correction)
        matrix = matrix_obj.matrix
        n = len(matrix)

        scale = config.oversample
        size = config.size * scale
        cell = size / (n + 2 * config.margin_modules)
        offset = config.margin_modules * cell

        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        function_mask = function_module_mask(matrix)

        base_r = (cell * config.cell_fill_ratio) * config.rounding_ratio
        for y in range(n):
            for x in range(n):
                if not matrix[y][x] or function_mask[y][x]:
                    continue
                cx = offset + x * cell
                cy = offset + y * cell
                inset = (cell * (1 - config.cell_fill_ratio)) / 2
                draw.rounded_rectangle(
                    (cx + inset, cy + inset, cx + cell - inset, cy + cell - inset),
                    radius=base_r,
                    fill=255,
                )

        finder_size = cell * 7
        draw_finder(draw, offset, offset, finder_size, 255)
        draw_finder(draw, offset + (n - 7) * cell, offset, finder_size, 255)
        draw_finder(draw, offset, offset + (n - 7) * cell, finder_size, 255)

        version = (n - 21) // 4 + 1
        centers = alignment_centers(version)
        for cy in centers:
            for cx in centers:
                # skip overlaps with finders
                if (cx < 9 and cy < 9) or (cx > n - 10 and cy < 9) or (cx < 9 and cy > n - 10):
                    continue
                draw_alignment(draw, offset + (cx - 2) * cell, offset + (cy - 2) * cell, 5 * cell, 255)

        mask = mask.filter(ImageFilter.GaussianBlur(radius=max(0.8, 0.95 * scale)))
        mask = mask.point(lambda p: 255 if p > 90 else 0)

        bg = Image.new("RGB", (size, size), to_rgb(config.background_color))
        px = bg.load()
        c1 = to_rgb(config.gradient_start)
        c2 = to_rgb(config.gradient_end)
        mpx = mask.load()
        for y in range(size):
            for x in range(size):
                if mpx[x, y] == 0:
                    continue
                t = gradient_t(x, y, size, size, config.gradient_mode)
                if config.gradient_fn:
                    t = config.gradient_fn(t)
                px[x, y] = lerp_color(c1, c2, t)

        result = bg.resize((config.size, config.size), Image.Resampling.LANCZOS)
        return result
