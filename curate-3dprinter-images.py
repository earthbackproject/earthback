#!/usr/bin/env python3
"""
curate-3dprinter-images.py — Crop, resize, and filter 3D printer images for LoRA training.

What this does:
  1. Scans dataset-3dprinter/raw/ for all images
  2. Smart-crops to 1024x1024 (center crop, preserves aspect)
  3. Saves to dataset-3dprinter/curated/
  4. Optional: opens each image for manual accept/reject review

Usage:
  python curate-3dprinter-images.py            # Auto-crop all, no review
  python curate-3dprinter-images.py --review   # Show each image, y/n/q
  python curate-3dprinter-images.py --stats    # Count images, no processing
"""

import os
import sys
import json
import argparse
import subprocess
import platform
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required. Install with:")
    print("  pip install Pillow")
    sys.exit(1)

RAW_DIR     = Path("dataset-3dprinter/raw")
CURATED_DIR = Path("dataset-3dprinter/curated")
TARGET_SIZE = 1024
MIN_SHORT_SIDE = 600  # reject images smaller than this in either dimension

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# ─── Image quality heuristics ──────────────────────────────────────────────────
# These are rough filters; manual review catches the rest

def is_probably_good(img, path):
    """Return (ok, reason) — rough automated quality checks."""
    w, h = img.size

    # Too small
    if w < MIN_SHORT_SIDE or h < MIN_SHORT_SIDE:
        return False, f"too small ({w}x{h})"

    # Very tall/thin aspect ratios (probably not a printer photo)
    aspect = max(w, h) / min(w, h)
    if aspect > 3.5:
        return False, f"extreme aspect ratio {aspect:.1f}:1"

    return True, "ok"

# ─── Cropping ──────────────────────────────────────────────────────────────────

def smart_crop(img, target=TARGET_SIZE):
    """Scale so shorter side = target, then center crop to target x target."""
    w, h = img.size

    if w < h:
        new_w = target
        new_h = int(h * target / w)
    else:
        new_h = target
        new_w = int(w * target / h)

    img = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - target) // 2
    top  = (new_h - target) // 2
    return img.crop((left, top, left + target, top + target))

# ─── Image viewer (cross-platform) ─────────────────────────────────────────────

def open_image_for_review(path):
    """Open image in default viewer. Returns when viewer opens (not closes)."""
    try:
        if platform.system() == "Windows":
            os.startfile(str(path))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception:
        pass  # viewer failure is non-fatal

# ─── Main processing ───────────────────────────────────────────────────────────

def collect_raw_files(raw_dir):
    """Collect all image files from raw directory."""
    files = []
    for p in sorted(raw_dir.rglob("*")):
        if p.suffix.lower() in IMAGE_EXTS and p.is_file():
            files.append(p)
    return files

def process(raw_dir, curated_dir, review=False, dry_run=False):
    curated_dir.mkdir(parents=True, exist_ok=True)

    raw_files = collect_raw_files(raw_dir)
    print(f"Found {len(raw_files)} raw images in {raw_dir}")
    print(f"Target: {curated_dir}/")
    print()

    accepted  = 0
    rejected  = 0
    skipped   = 0
    log       = []

    for i, src_path in enumerate(raw_files):
        # Output filename: curated_NNNN_original-stem.jpg
        dest_name = f"curated_{i:04d}_{src_path.stem}.jpg"
        dest_path = curated_dir / dest_name

        if dest_path.exists():
            skipped += 1
            continue

        try:
            img = Image.open(src_path).convert("RGB")
        except Exception as e:
            print(f"  ERROR opening {src_path.name}: {e}")
            rejected += 1
            log.append({"file": src_path.name, "action": "error", "reason": str(e)})
            continue

        ok, reason = is_probably_good(img, src_path)
        if not ok:
            print(f"  SKIP ({reason}): {src_path.name}")
            rejected += 1
            log.append({"file": src_path.name, "action": "auto-reject", "reason": reason})
            continue

        # Auto-pass for now; crop it
        cropped = smart_crop(img)

        if review:
            # Save a temp preview, open it, ask
            preview_path = curated_dir / f"_preview_{dest_name}"
            cropped.save(preview_path, "JPEG", quality=90)
            open_image_for_review(preview_path)

            w, h = img.size
            ans = input(f"[{i+1}/{len(raw_files)}] {src_path.name} ({w}x{h}) — Keep? (y/n/q): ").strip().lower()

            try:
                preview_path.unlink()
            except Exception:
                pass

            if ans == "q":
                print("Quitting review early.")
                break
            if ans != "y":
                print(f"  Rejected by user: {src_path.name}")
                rejected += 1
                log.append({"file": src_path.name, "action": "user-reject"})
                continue

        if dry_run:
            print(f"  [dry] would save: {dest_name}")
            accepted += 1
            continue

        cropped.save(dest_path, "JPEG", quality=95)
        accepted += 1
        log.append({"file": src_path.name, "action": "accepted", "dest": dest_name})
        print(f"  [{accepted:03d}] {dest_name}")

    # Save log
    log_path = curated_dir / "curation-log.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n{'─'*50}")
    print(f"✓ Accepted: {accepted}")
    print(f"✗ Rejected: {rejected}")
    print(f"→ Skipped (already done): {skipped}")
    print(f"Log: {log_path}")

    if accepted < 25:
        print(f"\n⚠  Only {accepted} images — target is 50-80 for a good LoRA.")
        print("   Run collect-3dprinter-images.py with more search terms or higher --max.")
    elif accepted < 50:
        print(f"\n  {accepted} images — usable but more is better. Consider another collection pass.")
    else:
        print(f"\n  {accepted} images — good dataset size. Ready to caption.")

    if not dry_run:
        print(f"\nNext step:")
        print(f"  python caption-3dprinter-images.py")

def stats(raw_dir, curated_dir):
    """Just count files, no processing."""
    raw_files = collect_raw_files(raw_dir) if raw_dir.exists() else []
    curated_files = list(curated_dir.glob("curated_*.jpg")) if curated_dir.exists() else []

    print(f"Raw images:     {len(raw_files)}  ({raw_dir})")
    print(f"Curated images: {len(curated_files)}  ({curated_dir})")

    # Check for captions
    txt_files = list(curated_dir.glob("*.txt")) if curated_dir.exists() else []
    print(f"Caption files:  {len(txt_files)}")

# ─── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Curate 3D printer images for LoRA training")
    parser.add_argument("--review",   action="store_true", help="Manually review each image (y/n/q)")
    parser.add_argument("--dry-run",  action="store_true", help="Show what would happen, don't write files")
    parser.add_argument("--stats",    action="store_true", help="Print counts only, no processing")
    parser.add_argument("--input",    default="dataset-3dprinter/raw",     help="Raw images directory")
    parser.add_argument("--output",   default="dataset-3dprinter/curated", help="Output directory")
    args = parser.parse_args()

    raw_dir     = Path(args.input)
    curated_dir = Path(args.output)

    if args.stats:
        stats(raw_dir, curated_dir)
        return

    if not raw_dir.exists():
        print(f"Raw directory not found: {raw_dir}")
        print("Run collect-3dprinter-images.py first.")
        sys.exit(1)

    process(raw_dir, curated_dir, review=args.review, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
