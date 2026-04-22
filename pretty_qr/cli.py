from __future__ import annotations

import argparse

from .api import generate_pretty_qr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate stylized pretty QR")
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--size", type=int, default=1400)
    parser.add_argument("--logo", default=None)
    parser.add_argument("--start", default="#C15AC4")
    parser.add_argument("--end", default="#5298F2")
    parser.add_argument("--bg", default="#FFFFFF")
    parser.add_argument("--preset", default="telegram_like")
    parser.add_argument("--cell-fill-ratio", type=float, default=0.78)
    parser.add_argument("--rounding-ratio", type=float, default=0.46)
    parser.add_argument("--logo-scale", type=float, default=0.15)
    parser.add_argument("--margin-modules", type=int, default=4)
    parser.add_argument("--error-correction", choices=["L", "M", "Q", "H"], default="H")
    parser.add_argument("--oversample", type=int, default=3)
    parser.add_argument("--no-logo", action="store_true")
    parser.add_argument("--no-gradient", action="store_true")
    parser.add_argument("--unsafe-style", action="store_true", help="allow more aggressive style at the cost of scan reliability")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start = args.start
    end = args.end
    if args.no_gradient:
        end = start
    logo = None if args.no_logo else args.logo
    generate_pretty_qr(
        data=args.data,
        output_path=args.out,
        size=args.size,
        logo_path=logo,
        gradient_start=start,
        gradient_end=end,
        background_color=args.bg,
        error_correction=args.error_correction,
        margin_modules=args.margin_modules,
        cell_fill_ratio=args.cell_fill_ratio,
        rounding_ratio=args.rounding_ratio,
        logo_scale=args.logo_scale,
        oversample=args.oversample,
        preset=args.preset,
        scan_safe_mode=not args.unsafe_style,
    )


if __name__ == "__main__":
    main()
