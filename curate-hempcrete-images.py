#!/usr/bin/env python3
"""
curate-hempcrete-images.py — Crop, resize, and filter hempcrete images for LoRA training.

What this does:
  1. Scans dataset-hempcrete/raw/ for all images
  2. Smart-crops to 1024x1024 (center crop, preserves aspect ratio)
  3. Saves to dataset-hempcrete/curated/
  4. Optional: opens each image for manual accept/reject review

Manual review is STRONGLY recommended for hempcrete — the supporting-term images
from Pexels/Pixabay will include some that are too abstract or off-target. You want
the final training set to be dense with images that show: hempcrete/lime-rich wall
surfaces, construction processes with formwork, natural building textures, and
plaster/render finishes. Images of random walls or unrelated construction should be
rejected during --review.

Usage:
  python curate-hempcrete-images.py            # Auto-crop all, no review
  python curate-hempcrete-images.py --review   # Show each image, y/n/q to skip/quit
  python curate-hempcrete-images.py --stats    # Count images without processing
  python curate-hempcrete-images.py --source wikimedia  # Only process one source
"""

import os
import sys
import argparse
import subprocess
import platform
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required:  pip install Pillow")
    sys.exit(1)

RAW_DIR     = Path("dataset-hempcrete/raw")
CURATED_DIR = Path("dataset-hempcrete/curated")
TARGET_SIZE = 1024
MIN_SHORT_SIDE = 600

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

def is_probably_good(img, path):
    """Rough automated quality checks — manual review catches the rest."""
    w, h = img.size
    if w < MIN_SHORT_SIDE or h < MIN_SHORT_SIDE:
        return False, f"too small ({w}x{h})"
    aspect = max(w, h) / min(w, h)
    if aspect > 3.5:
        return False, f"extreme aspect ratio {aspect:.1f}:1"
    return True, "ok"

def smart_crop(img, target=TARGET_SIZE):
    """Scale so shorter side = target, then center crop to target×target."""
    w, h = img.size
    scale = target / min(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - target) // 2
    top  = (new_h - target) // 2
    return img.crop((left, top, left + target, top + target))

def open_image_viewer(path):
    """Open image for review in platform default viewer."""
    if platform.system() == "Windows":
        os.startfile(str(path))
    elif platform.system() == "Darwin":
        subprocess.run(["open", str(path)])
    else:
        subprocess.run(["xdg-open", str(path)])

def main():
    parser = argparse.ArgumentParser(description="Curate hempcrete LoRA training images")
    parser.add_argument("--review",  action="store_true", help="Manual yes/no for each image")
    parser.add_argument("--stats",   action="store_true", help="Count images, no processing")
    parser.add_argument("--source",  default="all",
                        help="Only process: wikimedia | pexels | pixabay | all")
    parser.add_argument("--input",   default="dataset-hempcrete/raw")
    parser.add_argument("--output",  default="dataset-hempcrete/curated")
    args = parser.parse_args()

    raw_dir     = Path(args.input)
    curated_dir = Path(args.output)

    if not raw_dir.exists():
        print(f"Raw directory not found: {raw_dir}")
        print("Run collect-hempcrete-images.py first.")
        sys.exit(1)

    # Collect all source images
    all_images = []
    for subdir in raw_dir.iterdir():
        if not subdir.is_dir():
            continue
        if args.source != "all" and subdir.name != args.source:
            continue
        for f in subdir.iterdir():
            if f.suffix.lower() in IMAGE_EXTS:
                all_images.append(f)

    print(f"Found {len(all_images)} raw images")

    if args.stats:
        by_source = {}
        for p in all_images:
            src = p.parent.name
            by_source[src] = by_source.get(src, 0) + 1
        print("\nBy source:")
        for src, count in sorted(by_source.items()):
            print(f"  {src}: {count}")
        if curated_dir.exists():
            curated = list(curated_dir.glob("curated_*.jpg"))
            print(f"\nCurated: {len(curated)} images ready for training")
        return

    curated_dir.mkdir(parents=True, exist_ok=True)

    accepted = 0
    rejected = 0
    skipped  = 0

    for i, src_path in enumerate(sorted(all_images)):
        try:
            img = Image.open(src_path).convert("RGB")
        except Exception as e:
            print(f"  [skip] {src_path.name}: {e}")
            skipped += 1
            continue

        ok, reason = is_probably_good(img, src_path)
        if not ok:
            print(f"  [auto-reject] {src_path.name}: {reason}")
            rejected += 1
            continue

        dest_name = f"curated_{accepted:04d}_{src_path.stem[:60]}.jpg"
        dest_path = curated_dir / dest_name

        if dest_path.exists() and not args.review:
            accepted += 1
            continue

        if args.review:
            open_image_viewer(src_path)
            print(f"\n[{i+1}/{len(all_images)}] {src_path.parent.name}/{src_path.name}")
            print(f"  Source: {src_path.parent.name}")
            print(f"  Size: {img.size}")
            response = input("  Keep? [y/n/q]: ").strip().lower()
            if response == "q":
                print("Review stopped.")
                break
            if response != "y":
                print("  Rejected.")
                rejected += 1
                continue

        cropped = smart_crop(img)
        cropped.save(dest_path, "JPEG", quality=95)
        accepted += 1
        print(f"  [ok] {dest_name}")

    print(f"\n{'─'*50}")
    print(f"Accepted: {accepted}")
    print(f"Rejected: {rejected}")
    print(f"Skipped:  {skipped}")
    print(f"\nCurated images saved to: {curated_dir}")
    print(f"\nNext step:")
    print(f"  python caption-hempcrete-images.py")

if __name__ == "__main__":
    main()
