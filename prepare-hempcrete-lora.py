"""
Earthback — Hempcrete LoRA Dataset Preparation
================================================
Consolidates hempcrete reference photos from multiple sources into a single
Kohya SS-ready training dataset.

Sources:
  1. lora-reference/hempcrete/         (152 scraped photos)
  2. lora-training/hempcrete pics/     (25 manually collected)
  3. dataset-hempcrete/curated/        (15 already curated + captioned)

Pipeline:
  Step 1: --consolidate  → Copy all images to dataset-hempcrete/consolidated/
  Step 2: (manual)       → Delete bad images from consolidated/
  Step 3: --caption      → Generate captions for uncaptioned images
  Step 4: --build        → Build Kohya training structure (repeats folder)

Usage:
  python prepare-hempcrete-lora.py --consolidate       # gather all images
  python prepare-hempcrete-lora.py --stats              # show dataset stats
  python prepare-hempcrete-lora.py --caption             # auto-caption uncaptioned
  python prepare-hempcrete-lora.py --build               # build training folder
  python prepare-hempcrete-lora.py --build --repeats 15  # custom repeat count
"""

import os
import sys
import shutil
import hashlib
import argparse
from pathlib import Path
from PIL import Image

# ── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

SOURCES = [
    ("lora-reference/hempcrete",     "scraped"),
    ("lora-training/hempcrete pics", "manual"),
]

ALREADY_CURATED = BASE_DIR / "dataset-hempcrete" / "curated"
CONSOLIDATED    = BASE_DIR / "dataset-hempcrete" / "consolidated"
TRAIN_READY     = BASE_DIR / "dataset-hempcrete" / "train_ready"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

# ── TRIGGER WORD ─────────────────────────────────────────────────────────────
TRIGGER = "EBHEMPCRETE"

# ── TARGET RESOLUTION ────────────────────────────────────────────────────────
TARGET_SIZE = 1024  # Kohya trains at this resolution

# ── CAPTION TEMPLATES ────────────────────────────────────────────────────────
# Used for auto-captioning. The script picks the best match based on filename
# keywords and image aspect ratio. These can be hand-edited after generation.

CAPTION_TEMPLATES = {
    "wall_exterior": f"{TRIGGER}, cured hempcrete wall exterior, warm honey-buff surface with visible hemp fiber texture, natural light",
    "wall_interior": f"{TRIGGER}, hempcrete wall interior, warm golden-tan surface, visible hemp shiv in lime matrix, soft interior light",
    "construction": f"{TRIGGER}, hempcrete construction in progress, timber formwork, building site, natural daylight",
    "mixing": f"{TRIGGER}, hempcrete being mixed, golden hemp hurd with lime binder, chunky granular texture, construction site",
    "formwork": f"{TRIGGER}, hempcrete packed in timber formwork, warm buff-tan material between boards, construction site, natural light",
    "close_up": f"{TRIGGER}, close-up of hempcrete texture, visible hemp shiv fibers in pale lime matrix, shallow depth of field",
    "raw_material": f"{TRIGGER}, raw hemp hurd, loose golden-tan fibrous material, natural building material",
    "blocks": f"{TRIGGER}, hempcrete blocks, pre-formed hemp-lime masonry units, natural building material",
    "finished": f"{TRIGGER}, finished hempcrete building exterior, lime-rendered or exposed hemp-lime walls, architectural photography",
    "process": f"{TRIGGER}, hempcrete building process, workers tamping hemp-lime into formwork, construction documentary",
    "generic": f"{TRIGGER}, hempcrete hemp-lime building material, natural building, documentary photograph",
}

# Filename keyword → template mapping
KEYWORD_MAP = {
    "block": "blocks",
    "brick": "blocks",
    "masonry": "blocks",
    "mix": "mixing",
    "hurd": "raw_material",
    "hurd": "raw_material",
    "shiv": "raw_material",
    "raw": "raw_material",
    "loose": "raw_material",
    "form": "formwork",
    "tamp": "process",
    "pack": "process",
    "cast": "process",
    "pour": "process",
    "build": "construction",
    "construct": "construction",
    "progress": "construction",
    "site": "construction",
    "wall": "wall_exterior",
    "exterior": "wall_exterior",
    "facade": "wall_exterior",
    "interior": "wall_interior",
    "inside": "wall_interior",
    "room": "wall_interior",
    "close": "close_up",
    "macro": "close_up",
    "texture": "close_up",
    "detail": "close_up",
    "finish": "finished",
    "complete": "finished",
    "house": "finished",
    "home": "finished",
    "render": "finished",
    "plaster": "finished",
}


def file_hash(path):
    """MD5 hash of file contents for deduplication."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_image(path):
    return path.suffix.lower() in IMAGE_EXTS


def smart_crop_resize(img_path, output_path, size=TARGET_SIZE):
    """Center-crop to square, resize to target. Saves as high-quality JPEG."""
    try:
        img = Image.open(img_path)
        img = img.convert("RGB")

        w, h = img.size
        # Center crop to square
        short = min(w, h)
        left = (w - short) // 2
        top = (h - short) // 2
        img = img.crop((left, top, left + short, top + short))
        img = img.resize((size, size), Image.LANCZOS)

        # Save as JPEG (consistent format for training)
        out = output_path.with_suffix(".jpg")
        img.save(out, "JPEG", quality=95)
        return out
    except Exception as e:
        print(f"  SKIP (image error): {img_path.name} — {e}")
        return None


def guess_caption(filename):
    """Guess a caption template based on filename keywords."""
    name_lower = filename.lower()
    for keyword, template_key in KEYWORD_MAP.items():
        if keyword in name_lower:
            return CAPTION_TEMPLATES[template_key]
    return CAPTION_TEMPLATES["generic"]


# ── CONSOLIDATE ──────────────────────────────────────────────────────────────
def consolidate(min_bytes=30000):
    """Gather all hempcrete images into one folder, deduplicated and resized."""
    CONSOLIDATED.mkdir(parents=True, exist_ok=True)

    seen_hashes = set()
    total = 0
    dupes = 0
    small = 0
    errors = 0

    # First, collect already-curated images (they keep their existing captions)
    if ALREADY_CURATED.exists():
        for f in sorted(ALREADY_CURATED.iterdir()):
            if is_image(f):
                h = file_hash(f)
                seen_hashes.add(h)
                dest = CONSOLIDATED / f"curated_{f.stem}.jpg"
                caption_src = f.with_suffix(".txt")

                result = smart_crop_resize(f, dest)
                if result:
                    # Copy matching caption if exists
                    if caption_src.exists():
                        caption_dest = result.with_suffix(".txt")
                        shutil.copy2(caption_src, caption_dest)
                    total += 1
                    print(f"  ✓ [curated] {f.name}")

    # Then pull from other sources
    for rel_path, source_label in SOURCES:
        source_dir = BASE_DIR / rel_path
        if not source_dir.exists():
            print(f"  SKIP source (not found): {source_dir}")
            continue

        print(f"\n  Source: {source_dir} ({source_label})")
        for f in sorted(source_dir.iterdir()):
            if not is_image(f):
                continue

            # Size filter
            if f.stat().st_size < min_bytes:
                small += 1
                continue

            # Dedup
            h = file_hash(f)
            if h in seen_hashes:
                dupes += 1
                continue
            seen_hashes.add(h)

            # Crop and resize
            dest = CONSOLIDATED / f"{source_label}_{f.stem}.jpg"
            result = smart_crop_resize(f, dest)
            if result:
                total += 1
                print(f"  ✓ [{source_label}] {f.name}")
            else:
                errors += 1

    print(f"\n{'='*50}")
    print(f"Consolidated: {total} images")
    print(f"Duplicates skipped: {dupes}")
    print(f"Too small (<{min_bytes}B): {small}")
    print(f"Errors: {errors}")
    print(f"Output: {CONSOLIDATED}")
    print(f"\nNEXT: Open {CONSOLIDATED} in Explorer and delete anything")
    print(f"that's NOT useful hempcrete content (logos, diagrams, unrelated).")
    print(f"Target: keep 50-80 of the best images.")
    print(f"Then run: python prepare-hempcrete-lora.py --caption")


# ── STATS ────────────────────────────────────────────────────────────────────
def stats():
    """Show dataset statistics."""
    if not CONSOLIDATED.exists():
        print("No consolidated folder yet. Run --consolidate first.")
        return

    images = [f for f in CONSOLIDATED.iterdir() if is_image(f)]
    captions = [f for f in CONSOLIDATED.iterdir() if f.suffix == ".txt"]
    captioned = [f for f in images if f.with_suffix(".txt").exists()]

    print(f"{'='*50}")
    print(f"Hempcrete LoRA Dataset Stats")
    print(f"{'='*50}")
    print(f"  Images:      {len(images)}")
    print(f"  Captioned:   {len(captioned)}")
    print(f"  Uncaptioned: {len(images) - len(captioned)}")
    print(f"  Caption files: {len(captions)}")
    print(f"  Location: {CONSOLIDATED}")

    if images:
        sizes = []
        for f in images:
            try:
                img = Image.open(f)
                sizes.append(img.size)
            except:
                pass
        if sizes:
            widths = [s[0] for s in sizes]
            heights = [s[1] for s in sizes]
            print(f"  Resolution range: {min(widths)}x{min(heights)} — {max(widths)}x{max(heights)}")


# ── CAPTION ──────────────────────────────────────────────────────────────────
def caption(overwrite=False):
    """Generate template captions for uncaptioned images."""
    if not CONSOLIDATED.exists():
        print("No consolidated folder yet. Run --consolidate first.")
        return

    images = sorted(f for f in CONSOLIDATED.iterdir() if is_image(f))
    written = 0
    skipped = 0

    for img in images:
        txt = img.with_suffix(".txt")
        if txt.exists() and not overwrite:
            skipped += 1
            continue

        caption_text = guess_caption(img.stem)
        txt.write_text(caption_text, encoding="utf-8")
        written += 1
        print(f"  ✓ {img.name} → {caption_text[:60]}...")

    print(f"\n{'='*50}")
    print(f"Captioned: {written} images")
    print(f"Skipped (already captioned): {skipped}")
    print(f"\nIMPORTANT: Review and edit captions in {CONSOLIDATED}")
    print(f"Each .txt file should describe WHAT IS VISIBLE in that specific image.")
    print(f"Better captions = better LoRA. Generic captions work but specific is better.")
    print(f"\nThen run: python prepare-hempcrete-lora.py --build")


# ── BUILD ────────────────────────────────────────────────────────────────────
def build(repeats=15):
    """Build Kohya SS training directory structure."""
    if not CONSOLIDATED.exists():
        print("No consolidated folder yet. Run --consolidate first.")
        return

    images = sorted(f for f in CONSOLIDATED.iterdir() if is_image(f))
    captioned = [f for f in images if f.with_suffix(".txt").exists()]

    if not captioned:
        print("No captioned images found. Run --caption first.")
        return

    uncaptioned = len(images) - len(captioned)
    if uncaptioned > 0:
        print(f"WARNING: {uncaptioned} images have no captions and will be skipped.")
        print(f"Run --caption first, or delete uncaptioned images.\n")

    # Kohya expects: train_ready/<N>_<concept>/  with images + .txt captions
    concept_dir = TRAIN_READY / f"{repeats}_hempcrete"

    if concept_dir.exists():
        shutil.rmtree(concept_dir)
    concept_dir.mkdir(parents=True)

    copied = 0
    for img in captioned:
        txt = img.with_suffix(".txt")
        shutil.copy2(img, concept_dir / img.name)
        shutil.copy2(txt, concept_dir / txt.name)
        copied += 1

    total_steps_est = copied * repeats  # rough — actual depends on batch size and epochs

    print(f"{'='*50}")
    print(f"Kohya Training Dataset Built")
    print(f"{'='*50}")
    print(f"  Images: {copied}")
    print(f"  Repeats: {repeats}")
    print(f"  Effective samples per epoch: {copied * repeats}")
    print(f"  Location: {concept_dir}")
    print(f"\n  Recommended training steps: {min(copied * repeats * 2, 2000)}")
    print(f"  (Based on {copied} images × {repeats} repeats × ~2 epochs)")
    print(f"\n  Ready to train! Run: train-hempcrete-lora.bat")


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Earthback Hempcrete LoRA Dataset Prep")
    parser.add_argument("--consolidate", action="store_true", help="Gather all images into one folder")
    parser.add_argument("--stats", action="store_true", help="Show dataset statistics")
    parser.add_argument("--caption", action="store_true", help="Auto-caption uncaptioned images")
    parser.add_argument("--caption-overwrite", action="store_true", help="Overwrite existing captions")
    parser.add_argument("--build", action="store_true", help="Build Kohya training folder structure")
    parser.add_argument("--repeats", type=int, default=15, help="Repeats per image (default 15)")
    parser.add_argument("--min-bytes", type=int, default=30000, help="Min file size in bytes (default 30KB)")
    args = parser.parse_args()

    if not any([args.consolidate, args.stats, args.caption, args.caption_overwrite, args.build]):
        parser.print_help()
        return

    if args.consolidate:
        consolidate(min_bytes=args.min_bytes)
    if args.stats:
        stats()
    if args.caption or args.caption_overwrite:
        caption(overwrite=args.caption_overwrite)
    if args.build:
        build(repeats=args.repeats)


if __name__ == "__main__":
    main()
