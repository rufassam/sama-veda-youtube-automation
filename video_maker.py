# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 23:53:11 2025

@author: Rufas
"""

#!/usr/bin/env python3

import os
import datetime
import subprocess
from PIL import Image, ImageDraw, ImageFont

AUDIO_DIR = "audio"
IMAGES_DIR = "images"
OUTPUT_DIR = "output"

AUTHOR = "Rufas Sam"
SERIES_NAME = "Sama Veda Healing Series"

# pick a safe cross-platform font
def get_font(size):
    candidates = [
        r"C:\Windows\Fonts\Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for f in candidates:
        if os.path.exists(f):
            from PIL import ImageFont
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def create_background(base_image_path, output_path, title):
    img = Image.open(base_image_path).convert("RGB").resize((1920, 1080))

    draw = ImageDraw.Draw(img)

    title_font = get_font(72)
    subtitle_font = get_font(42)

    # Title text
    w = draw.textlength(title, font=title_font)
    draw.text(((1920 - w) / 2, 120), title, fill="white", font=title_font)

    subtitle = f"{SERIES_NAME}"
    w2 = draw.textlength(subtitle, font=subtitle_font)
    draw.text(((1920 - w2) / 2, 220), subtitle, fill=(210, 220, 255), font=subtitle_font)

    # Watermark
    wm = f"{AUTHOR}"
    w3 = draw.textlength(wm, font=subtitle_font)
    draw.text(((1920 - w3) / 2, 980), wm, fill="white", font=subtitle_font)

    img.save(output_path, quality=95)


def build_video(audio_file, image_file, label, output_video):
    temp_image = "temp_bg.jpg"
    create_background(image_file, temp_image, label)

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", temp_image,
        "-i", audio_file,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_video,
    ]

    subprocess.run(cmd, check=True)
    os.remove(temp_image)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tracks = sorted([
        f for f in os.listdir(AUDIO_DIR)
        if f.lower().endswith((".mp3", ".wav", ".m4a"))
    ])

    if not tracks:
        raise RuntimeError("No audio tracks found")

    today_index = len([
        f for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".mp4")
    ])

    track = tracks[today_index % len(tracks)]
    audio_path = os.path.join(AUDIO_DIR, track)

    background = sorted(os.listdir(IMAGES_DIR))[0]
    bg_path = os.path.join(IMAGES_DIR, background)

    day = today_index + 1
    label = f"Sama Veda Healing — Day {day}"

    out = os.path.join(OUTPUT_DIR, f"sama_veda_day_{day}.mp4")

    build_video(audio_path, bg_path, label, out)

    print("Created:", out)


if __name__ == "__main__":
    main()
