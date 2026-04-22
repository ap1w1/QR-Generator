from __future__ import annotations




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


