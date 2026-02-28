#!/usr/bin/env python3
"""
Generate cover.png for AMP catalog tile.
Uses Data Dynamics logo with AI enterprise aesthetic.
"""

import io
import math
import random
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

LOGO_URL = "http://data-dynamics.io/logo-small.png"
OUTPUT_PATH = Path(__file__).parent.parent / "assets" / "cover.png"
WIDTH, HEIGHT = 800, 450


def download_logo() -> Image.Image:
    r = requests.get(LOGO_URL, timeout=10)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def draw_ai_network_bg(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Subtle neural network / data flow pattern."""
    for _ in range(80):
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2 = x1 + random.randint(-80, 80)
        y2 = y1 + random.randint(-40, 40)
        alpha = random.randint(8, 25)
        draw.line([(x1, y1), (x2, y2)], fill=(100, 180, 255, alpha), width=1)
    for _ in range(120):
        x, y = random.randint(0, w), random.randint(0, h)
        r = random.randint(1, 3)
        alpha = random.randint(15, 40)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(120, 200, 255, alpha))


def main():
    # Base: dark gradient (navy -> deep blue)
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(15 + 10 * (1 - t))
        g = int(25 + 15 * (1 - t))
        b = int(45 + 25 * (1 - t))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Overlay: AI network pattern
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_ai_network_bg(ImageDraw.Draw(overlay), WIDTH, HEIGHT)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # Top accent bar (cyan/teal - AI feel)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, WIDTH, 6], fill=(0, 200, 180))
    draw.rectangle([0, HEIGHT - 4, WIDTH, HEIGHT], fill=(0, 180, 160))

    # Download and composite logo
    logo = download_logo()
    logo_w, logo_h = logo.size
    scale = min(120 / logo_w, 80 / logo_h)
    new_w = int(logo_w * scale)
    new_h = int(logo_h * scale)
    logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
    logo_x, logo_y = 40, (HEIGHT - new_h) // 2 - 20
    img.paste(logo, (logo_x, logo_y), logo)

    # Text
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        font_dynamics = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
        font_large_bold = font_large
        try:
            font_large_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        except OSError:
            pass
        font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except OSError:
        font_large = font_dynamics = font_large_bold = font_med = font_small = ImageFont.load_default()

    text_x = logo_x + new_w + 30
    purple = (160, 100, 220)
    draw.text((text_x, 100), "DATA", fill=purple, font=font_large_bold)
    data_bbox = draw.textbbox((0, 0), "DATA", font=font_large_bold)
    dynamics_x = text_x + (data_bbox[2] - data_bbox[0]) + 4
    draw.text((dynamics_x, 108), "DYNAMICS", fill=purple, font=font_dynamics)
    draw.text((text_x, 155), "AMP", fill=(0, 230, 200), font=font_large)
    draw.text((text_x, 220), "Cloudera AI · Applied ML Prototype", fill=(180, 200, 220), font=font_med)
    draw.text((text_x, 255), "Data Dynamics · Level 4", fill=(140, 170, 190), font=font_small)

    # Tags
    tags = ["Python 3.11", "Model API", "Streamlit", "Beginner"]
    tag_x, tag_y = text_x, 300
    for tag in tags:
        bbox = draw.textbbox((0, 0), tag, font=font_small)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.rectangle([tag_x, tag_y, tag_x + tw + 16, tag_y + th + 8],
                       outline=(0, 200, 180), fill=(20, 40, 60))
        draw.text((tag_x + 8, tag_y + 4), tag, fill="white", font=font_small)
        tag_x += tw + 28

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
