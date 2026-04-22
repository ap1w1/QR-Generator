from __future__ import annotations

from PIL import Image, ImageDraw

from .generator import build_qr_matrix, function_module_mask
from .gradients import gradient_t, lerp_color, to_rgb
from .models import PrettyQRConfig


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

        data_inset = (cell * (1 - config.cell_fill_ratio)) / 2
        data_radius = (cell * config.cell_fill_ratio) * config.rounding_ratio

        fn_fill_ratio = 0.95 if config.scan_safe_mode else max(config.cell_fill_ratio, 0.88)
        fn_rounding = 0.1 if config.scan_safe_mode else min(config.rounding_ratio, 0.25)
        fn_inset = (cell * (1 - fn_fill_ratio)) / 2
        fn_radius = (cell * fn_fill_ratio) * fn_rounding

        for y in range(n):
            for x in range(n):
                if not matrix[y][x]:
                    continue
                cx = offset + x * cell
                cy = offset + y * cell
                if function_mask[y][x]:
                    inset, radius = fn_inset, fn_radius
                else:
                    inset, radius = data_inset, data_radius
                draw.rounded_rectangle(
                    (cx + inset, cy + inset, cx + cell - inset, cy + cell - inset),
                    radius=radius,
                    fill=255,
                )

        # Add organic bridges only for data modules to avoid damaging functional zones.
        bridge_w = cell * (config.cell_fill_ratio * 0.56)
        for y in range(n):
            for x in range(n):
                if not matrix[y][x] or function_mask[y][x]:
                    continue
                cx = offset + x * cell + cell / 2
                cy = offset + y * cell + cell / 2

                if x + 1 < n and matrix[y][x + 1] and not function_mask[y][x + 1]:
                    ncx = offset + (x + 1) * cell + cell / 2
                    draw.rounded_rectangle(
                        (cx, cy - bridge_w / 2, ncx, cy + bridge_w / 2),
                        radius=bridge_w / 2,
                        fill=255,
                    )
                if y + 1 < n and matrix[y + 1][x] and not function_mask[y + 1][x]:
                    ncy = offset + (y + 1) * cell + cell / 2
                    draw.rounded_rectangle(
                        (cx - bridge_w / 2, cy, cx + bridge_w / 2, ncy),
                        radius=bridge_w / 2,
                        fill=255,
                    )

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

        return bg.resize((config.size, config.size), Image.Resampling.LANCZOS)
