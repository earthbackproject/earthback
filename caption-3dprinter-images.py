#!/usr/bin/env python3
"""
caption-3dprinter-images.py — Generate .txt captions for 3D printer LoRA training images.

Two modes:

  --mode template  (default, fast)
    Generates structured captions from filename + visual keywords.
    Format: "a [type] 3D FDM printer, [state], [lighting], [environment]"
    You then review and hand-edit any that are wrong.

  --mode blip2  (slow, GPU recommended)
    Runs BLIP-2 to auto-caption, then overlays the 3D printer template prefix.
    Requires: pip install transformers accelerate Pillow torch
    Requires: ~15GB VRAM (or will run slowly on CPU)

Usage:
  python caption-3dprinter-images.py                    # template mode
  python caption-3dprinter-images.py --mode blip2       # BLIP-2 mode
  python caption-3dprinter-images.py --review           # open each image while writing
  python caption-3dprinter-images.py --overwrite        # redo existing captions
  python caption-3dprinter-images.py --check            # list images missing captions

Output:
  For each curated_NNNN_foo.jpg → curated_NNNN_foo.txt
  (Kohya expects image and caption in same folder with same stem)
"""

import os
import sys
import json
import argparse
import subprocess
import platform
import random
from pathlib import Path

CURATED_DIR = Path("dataset-3dprinter/curated")

# ─── Caption templates ─────────────────────────────────────────────────────────
# These are filled in during template mode.
# The trigger word EB3DPRINTER can be added or omitted depending on training goal.
# For a category LoRA (teach Flux what a printer looks like) — no trigger needed.
# For a switchable LoRA (activate with a word) — include EB3DPRINTER.

TRIGGER = ""  # Set to "EB3DPRINTER" to enable trigger word

PRINTER_TYPES = [
    "desktop FDM",
    "desktop FDM CoreXY",
    "desktop FDM Cartesian",
    "desktop FDM",
    "desktop FDM",
]

STATES = [
    "idle",
    "actively printing",
    "mid-print with partial object visible on build plate",
    "idle with spool of filament loaded",
    "printing in progress, first layer",
    "idle",
    "print removal in progress",
    "filament loading",
    "idle with completed print on build plate",
]

LIGHTING = [
    "warm workshop lighting",
    "natural window light",
    "cool overhead LED lighting",
    "warm diffuse studio lighting",
    "side-lit from a window",
    "mixed natural and artificial light",
    "clean studio lighting",
    "warm ambient light",
]

ENVIRONMENTS = [
    "on a wooden workbench",
    "in a home office",
    "in a maker space",
    "on a desk with tools nearby",
    "in a workshop",
    "on a clean white surface",
    "in a studio setting",
    "in a garage workshop",
    "in a well-lit maker space",
]

ANGLES = [
    "",                            # no angle specified
    ", front view",
    ", three-quarter view",
    ", side view",
    ", close-up of the nozzle and extruder",
    ", close-up of the build plate and print",
    ", full shot showing the complete printer",
    "",
]

NEGATIVES_REMINDER = """
# NEGATIVES for training (add to Kohya config or use queue-3dprinter-lora.py):
# "cartoon, illustration, render, CGI, 3D render, anime, drawing, sketch,
#  painting, person, human, hands, watermark, logo, text, blurry, low quality"
"""

def build_template_caption(filename):
    """Build a structured caption from the filename and randomized components."""
    stem = filename.stem

    # Detect model hints from filename
    type_str = random.choice(PRINTER_TYPES)
    if "bambu" in stem.lower() or "x1c" in stem.lower():
        type_str = "desktop FDM CoreXY enclosed"
    elif "prusa" in stem.lower() or "mk4" in stem.lower():
        type_str = "desktop FDM Cartesian"
    elif "ender" in stem.lower() or "creality" in stem.lower():
        type_str = "desktop FDM Cartesian"

    state   = random.choice(STATES)
    light   = random.choice(LIGHTING)
    env     = random.choice(ENVIRONMENTS)
    angle   = random.choice(ANGLES)

    trigger_str = f"{TRIGGER} " if TRIGGER else ""

    caption = f"{trigger_str}a {type_str} 3D FDM printer{angle}, {state}, {light}, {env}"
    return caption

def open_image(path):
    try:
        if platform.system() == "Windows":
            os.startfile(str(path))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception:
        pass

# ─── BLIP-2 mode ───────────────────────────────────────────────────────────────

def load_blip2():
    try:
        from transformers import Blip2Processor, Blip2ForConditionalGeneration
        import torch
        from PIL import Image

        print("Loading BLIP-2 model (this takes a minute first time)...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"  Device: {device}")

        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        )
        model.to(device)
        return processor, model, device, Image
    except ImportError as e:
        print(f"BLIP-2 dependencies missing: {e}")
        print("Install with:")
        print("  pip install transformers accelerate torch Pillow")
        sys.exit(1)

def blip2_caption(path, processor, model, device, Image):
    """Run BLIP-2 on a single image, return raw caption string."""
    img = Image.open(path).convert("RGB")
    import torch
    inputs = processor(img, return_tensors="pt").to(device, torch.float16 if device == "cuda" else torch.float32)
    out = model.generate(**inputs, max_new_tokens=50)
    raw = processor.decode(out[0], skip_special_tokens=True).strip()
    return raw

def blend_with_template(blip_caption, filename):
    """Combine BLIP-2 auto-caption with our structured template prefix."""
    trigger_str = f"{TRIGGER} " if TRIGGER else ""
    # BLIP tends to say "a 3d printer" or "a printer on a desk" — use it as the environment/state
    caption = f"{trigger_str}a desktop FDM 3D FDM printer, {blip_caption.lower()}"
    return caption

# ─── Main processing ───────────────────────────────────────────────────────────

def caption_images(curated_dir, mode="template", review=False, overwrite=False):
    image_files = sorted(curated_dir.glob("curated_*.jpg"))

    if not image_files:
        print(f"No curated images found in {curated_dir}")
        print("Run curate-3dprinter-images.py first.")
        sys.exit(1)

    print(f"Found {len(image_files)} curated images")
    print(f"Mode: {mode}")
    if TRIGGER:
        print(f"Trigger word: {TRIGGER}")
    print()

    blip2_stuff = None
    if mode == "blip2":
        blip2_stuff = load_blip2()

    written   = 0
    skipped   = 0
    captions  = {}

    for i, img_path in enumerate(image_files):
        txt_path = img_path.with_suffix(".txt")

        if txt_path.exists() and not overwrite:
            skipped += 1
            continue

        if review:
            open_image(img_path)

        if mode == "blip2":
            processor, model, device, Image = blip2_stuff
            try:
                raw = blip2_caption(img_path, processor, model, device, Image)
                caption = blend_with_template(raw, img_path)
                print(f"  [{i+1}] {img_path.name}")
                print(f"        BLIP-2: {raw}")
                print(f"        Final:  {caption}")
            except Exception as e:
                print(f"  BLIP-2 error on {img_path.name}: {e}")
                caption = build_template_caption(img_path)
        else:
            caption = build_template_caption(img_path)
            print(f"  [{i+1:03d}] {img_path.name}")
            print(f"         {caption}")

        if review:
            ans = input("  Edit? (enter to keep, or type new caption): ").strip()
            if ans:
                caption = ans

        txt_path.write_text(caption, encoding="utf-8")
        captions[img_path.name] = caption
        written += 1

    # Save all captions to one review file for easy editing
    review_path = curated_dir / "captions-review.json"
    existing = {}
    if review_path.exists():
        try:
            existing = json.loads(review_path.read_text())
        except Exception:
            pass

    for img_path in image_files:
        txt_path = img_path.with_suffix(".txt")
        if txt_path.exists():
            existing[img_path.name] = txt_path.read_text().strip()

    with open(review_path, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"\n{'─'*50}")
    print(f"✓ Written: {written} captions")
    print(f"→ Skipped: {skipped} (already captioned)")
    print(f"\nReview all captions: {review_path}")
    print(f"  Edit the JSON and run:")
    print(f"  python caption-3dprinter-images.py --apply-edits")
    print(f"\nNext step:")
    print(f"  train-3dprinter-lora.bat")

def apply_edits(curated_dir):
    """Apply edits from captions-review.json back to individual .txt files."""
    review_path = curated_dir / "captions-review.json"
    if not review_path.exists():
        print(f"No review file found at {review_path}")
        sys.exit(1)

    captions = json.loads(review_path.read_text())
    updated = 0
    for img_name, caption in captions.items():
        img_path = curated_dir / img_name
        if img_path.exists():
            txt_path = img_path.with_suffix(".txt")
            old = txt_path.read_text().strip() if txt_path.exists() else ""
            if old != caption:
                txt_path.write_text(caption, encoding="utf-8")
                updated += 1
                print(f"  Updated: {img_name}")

    print(f"\n✓ Updated {updated} captions from review file")

def check_missing(curated_dir):
    """List images without caption files."""
    image_files = sorted(curated_dir.glob("curated_*.jpg"))
    missing = [p for p in image_files if not p.with_suffix(".txt").exists()]

    if not missing:
        print(f"✓ All {len(image_files)} images have captions")
    else:
        print(f"⚠  {len(missing)} images missing captions:")
        for p in missing:
            print(f"   {p.name}")

def main():
    parser = argparse.ArgumentParser(description="Caption 3D printer images for LoRA training")
    parser.add_argument("--mode",    choices=["template", "blip2"], default="template")
    parser.add_argument("--review",  action="store_true",  help="Open each image during captioning")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .txt files")
    parser.add_argument("--apply-edits", action="store_true", help="Apply edits from captions-review.json")
    parser.add_argument("--check",   action="store_true",  help="List images missing captions")
    parser.add_argument("--trigger", default="",           help="Trigger word to prepend (default: none)")
    parser.add_argument("--input",   default="dataset-3dprinter/curated")
    args = parser.parse_args()

    global TRIGGER
    if args.trigger:
        TRIGGER = args.trigger

    curated_dir = Path(args.input)

    if not curated_dir.exists():
        print(f"Curated directory not found: {curated_dir}")
        print("Run curate-3dprinter-images.py first.")
        sys.exit(1)

    if args.check:
        check_missing(curated_dir)
    elif args.apply_edits:
        apply_edits(curated_dir)
    else:
        caption_images(curated_dir, mode=args.mode, review=args.review, overwrite=args.overwrite)

    # Remind about negative captions
    if not args.check and not args.apply_edits:
        print(NEGATIVES_REMINDER)

if __name__ == "__main__":
    main()
