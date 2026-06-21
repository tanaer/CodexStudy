#!/usr/bin/env python3
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "docs" / "images"
WATERMARK = "CodexStudy"
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]


def font_path() -> str:
    for path in FONT_PATHS:
        if Path(path).exists():
            return path
    raise RuntimeError("No usable font found")


def load_font(width: int, height: int) -> ImageFont.FreeTypeFont:
    size = max(11, min(28, round(min(width, height) * 0.035)))
    return ImageFont.truetype(font_path(), size=size)


def text_size(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), WATERMARK, font=font)
    return box[2] - box[0], box[3] - box[1]


def edit_bitmap(path: Path) -> None:
    with Image.open(path) as original:
        fmt = original.format
        mode = original.mode
        has_alpha = mode in {"RGBA", "LA"} or (
            mode == "P" and "transparency" in original.info
        )
        image = original.convert("RGBA")

    width, height = image.size
    font = load_font(width, height)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    tw, th = text_size(draw, font)

    pad_x = max(8, round(tw * 0.22))
    pad_y = max(5, round(th * 0.45))
    margin = max(8, round(min(width, height) * 0.018))
    box_w = tw + pad_x * 2
    box_h = th + pad_y * 2
    x1 = max(0, width - margin - box_w)
    y1 = max(0, height - margin - box_h)
    x2 = min(width, width - margin)
    y2 = min(height, height - margin)
    radius = max(5, round(box_h * 0.35))

    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=radius,
        fill=(255, 255, 255, 235),
        outline=(20, 20, 20, 48),
        width=1,
    )
    text_x = x1 + (x2 - x1 - tw) / 2
    text_y = y1 + (y2 - y1 - th) / 2 - max(1, round(th * 0.06))
    draw.text((text_x, text_y), WATERMARK, font=font, fill=(17, 24, 39, 230))

    image = Image.alpha_composite(image, overlay)

    save_kwargs = {}
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        output = image.convert("RGB")
        save_kwargs.update(quality=92, optimize=True)
    elif suffix == ".webp":
        output = image if has_alpha else image.convert("RGB")
        save_kwargs.update(quality=92, method=6)
    else:
        output = image if has_alpha else image.convert("RGB")
        save_kwargs.update(optimize=True)

    output.save(path, format=fmt, **save_kwargs)


def edit_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n</svg>\s*$", "", text)
    watermark = f"""
  <g class="font" opacity="0.86">
    <rect x="1044" y="714" width="112" height="28" rx="14" fill="#ffffff" stroke="#d4d4d4" />
    <text x="1100" y="733" text-anchor="middle" font-size="13" font-weight="700" fill="#111827">CodexStudy</text>
  </g>
</svg>
"""
    path.write_text(text + watermark, encoding="utf-8")


def main() -> None:
    changed = 0
    for path in sorted(IMAGE_DIR.iterdir()):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            edit_bitmap(path)
            changed += 1
        elif suffix == ".svg":
            edit_svg(path)
            changed += 1
    print(f"updated {changed} image files")


if __name__ == "__main__":
    main()
