#!/usr/bin/env python3
"""
caption-hempcrete-images.py — Generate .txt captions for hempcrete LoRA training images.

Captions teach Kohya what each image contains. Good hempcrete captions describe:
  - The material (hempcrete, hemp lime, lime render, natural plaster)
  - The state (fresh mix, packed in formwork, cured, stripped, plastered)
  - The visual detail (texture, color, fiber visibility, surface quality)
  - The context (construction site, interior, exterior, close-up)
  - Lighting

Trigger word strategy:
  EBHEMPCRETE — used as a Flux activation trigger for the trained LoRA.
  Include in captions if you want a switchable LoRA (activate with the trigger word).
  Omit if you want a category LoRA (improves Flux's default hempcrete rendering).

  Recommendation: include EBHEMPCRETE. The base Flux model's hempcrete knowledge
  is weak enough that a trigger word is useful for reliable activation.

Usage:
  python caption-hempcrete-images.py              # template mode, with trigger word
  python caption-hempcrete-images.py --no-trigger # template mode, no trigger word
  python caption-hempcrete-images.py --review     # open image while captioning
  python caption-hempcrete-images.py --overwrite  # redo all existing captions
  python caption-hempcrete-images.py --check      # list images missing captions
"""

import os
import sys
import argparse
import random
import subprocess
import platform
from pathlib import Path

CURATED_DIR = Path("dataset-hempcrete/curated")

# Trigger word — prepended to all captions when --trigger mode is on
TRIGGER = "EBHEMPCRETE"

# ─── Caption components ────────────────────────────────────────────────────────

MATERIAL_DESCRIPTORS = [
    "hempcrete wall",
    "hemp lime wall",
    "hempcrete construction",
    "hemp hurds and lime mixture",
    "natural hempcrete surface",
    "hempcrete insulation block",
    "hemp lime render",
    "hemp and lime binder wall",
]

STATES = [
    "freshly mixed hempcrete in formwork",
    "hempcrete being tamped into timber formwork",
    "cured hempcrete wall, formwork stripped",
    "rough hempcrete surface, hemp fibers visible in lime matrix",
    "lime-washed hempcrete exterior",
    "cross-section showing hemp hurds suspended in pale lime matrix",
    "hempcrete construction in progress",
    "finished hempcrete wall interior",
    "lime plaster over hempcrete, smooth finish",
    "close-up of hempcrete texture, porous pale grey-green surface",
    "mixing hempcrete — hemp hurd, lime powder, water in barrel mixer",
    "packing hempcrete around timber frame members",
    # Loose hurd
    "loose hemp hurd pile, golden-tan fibrous hemp shiv, raw material before mixing",
    "hemp hurd in bulk bags, raw hemp shiv ready for mixing with lime binder",
    # Pumpable / spray
    "pump-applied hempcrete being sprayed onto wall framing via hose nozzle",
    "pumpable hemp lime mix, fluid slurry consistency for pneumatic application",
    "spray-applied hempcrete wall, continuous uniform coverage from nozzle",
    # Blocks
    "hemp masonry blocks stacked, pre-formed hempcrete units with visible hemp fiber texture",
    "hemp blocks being laid with lime mortar, masonry construction with natural blocks",
]

CONTEXTS = [
    "natural building construction site",
    "interior of a natural building under construction",
    "exterior wall of an earthen home",
    "workshop setting",
    "close-up macro detail",
    "rural construction site",
    "sustainable building project",
    "timber frame with hempcrete infill",
]

LIGHTING = [
    "natural light",
    "soft diffuse daylight",
    "afternoon sunlight, sidelight",
    "overcast daylight",
    "raking sidelight revealing texture",
    "interior window light",
    "warm morning light",
    "even outdoor light",
]

# ─── Filename → caption heuristics ────────────────────────────────────────────
# Source-specific hints to pick better components for known sources

def guess_state_from_filename(filename):
    """Rough guess at image content from filename keywords."""
    fn = filename.lower()

    # Loose hemp hurd (the raw material before mixing)
    if any(k in fn for k in ["hurd", "chanvre", "shiv", "shive", "beton_de", "raw_hemp"]):
        return "loose hemp hurd, golden-tan fibrous material, hemp shiv before mixing"

    # Pumpable / spray-applied hempcrete
    if any(k in fn for k in ["pump", "spray", "projet", "projeté", "pura", "pneumatic"]):
        return "spray-applied hempcrete, pump-mix hemp lime being applied via hose nozzle"

    # Hemp blocks / pre-formed blocks
    if any(k in fn for k in ["block", "bloc", "coexist", "preformed", "pre-formed", "masonry"]):
        return "hemp blocks, pre-formed hempcrete masonry units being laid with lime mortar"

    # Mixing / wet mix
    if any(k in fn for k in ["mix", "mixing", "barrel", "wet", "mixed"]):
        return "mixing hempcrete — hemp hurd, lime binder, water combined into pale grey slurry"

    # Formwork / casting
    if any(k in fn for k in ["form", "formwork", "tamp", "pack", "cast"]):
        return "hempcrete being tamped and packed into timber formwork, construction in progress"

    # Stripped / cured surface
    if any(k in fn for k in ["strip", "stripped", "bare", "raw", "exposed"]):
        return "cured hempcrete wall, formwork stripped, rough pale grey-green surface exposed"

    # Plaster / render finish
    if any(k in fn for k in ["plaster", "render", "finish", "trowel"]):
        return "lime plaster render applied over hempcrete wall, smooth pale finish"

    # Lime + hemp (combined material shot)
    if any(k in fn for k in ["lime-and", "lime_and", "hemp-lime", "hemp_lime"]):
        return "hemp hurds and lime binder, natural building materials side by side"

    # Texture / close-up
    if any(k in fn for k in ["texture", "close", "detail", "macro", "surface"]):
        return "close-up of hempcrete wall texture, pale grey-green surface with visible hemp fibers"

    # Exterior
    if any(k in fn for k in ["exterior", "outside", "facade", "wall-house", "wall_house"]):
        return "hempcrete building exterior wall, natural pale surface, sustainable construction"

    # Interior
    if any(k in fn for k in ["interior", "inside", "room"]):
        return "hempcrete wall interior, cured pale grey surface, natural building finish"

    # Natural building adjacents
    if any(k in fn for k in ["straw", "bale"]):
        return "natural building construction, straw bale wall with lime plaster finish"
    if any(k in fn for k in ["cob", "adobe", "earth", "rammed"]):
        return "earthen wall construction, natural building process"

    # Default
    return random.choice(STATES)

def build_caption(filename, use_trigger=True):
    """Build a structured caption for a hempcrete training image."""
    state   = guess_state_from_filename(filename)
    context = random.choice(CONTEXTS)
    light   = random.choice(LIGHTING)

    caption = f"{state}, {context}, {light}"

    if use_trigger:
        caption = f"{TRIGGER}, {caption}"

    return caption

# ─── Main ──────────────────────────────────────────────────────────────────────

def open_image_viewer(path):
    if platform.system() == "Windows":
        os.startfile(str(path))
    elif platform.system() == "Darwin":
        subprocess.run(["open", str(path)])
    else:
        subprocess.run(["xdg-open", str(path)])

def main():
    parser = argparse.ArgumentParser(description="Caption hempcrete LoRA training images")
    parser.add_argument("--no-trigger", action="store_true",
                        help="Omit trigger word (category LoRA mode)")
    parser.add_argument("--review",     action="store_true",
                        help="Open each image for review while generating caption")
    parser.add_argument("--overwrite",  action="store_true",
                        help="Regenerate captions even if .txt already exists")
    parser.add_argument("--check",      action="store_true",
                        help="List images missing captions, then exit")
    parser.add_argument("--input",      default="dataset-hempcrete/curated")
    args = parser.parse_args()

    curated_dir = Path(args.input)
    if not curated_dir.exists():
        print(f"Curated directory not found: {curated_dir}")
        print("Run curate-hempcrete-images.py first.")
        sys.exit(1)

    images = sorted(curated_dir.glob("curated_*.jpg"))
    if not images:
        print(f"No curated images found in {curated_dir}")
        sys.exit(1)

    use_trigger = not args.no_trigger

    if args.check:
        missing = [img for img in images if not img.with_suffix(".txt").exists()]
        if missing:
            print(f"{len(missing)} images missing captions:")
            for p in missing: print(f"  {p.name}")
        else:
            print(f"All {len(images)} images have captions.")
        return

    print(f"{'─'*50}")
    print(f"Captioning {len(images)} images")
    print(f"Trigger word: {'ENABLED — ' + TRIGGER if use_trigger else 'DISABLED (category LoRA)'}")
    print(f"{'─'*50}\n")

    written = 0
    skipped = 0

    for i, img_path in enumerate(images):
        txt_path = img_path.with_suffix(".txt")

        if txt_path.exists() and not args.overwrite:
            skipped += 1
            continue

        if args.review:
            open_image_viewer(img_path)
            print(f"[{i+1}/{len(images)}] {img_path.name}")

        caption = build_caption(img_path.name, use_trigger=use_trigger)

        if args.review:
            print(f"  Auto-caption: {caption}")
            edit = input("  Press Enter to accept, or type replacement: ").strip()
            if edit:
                caption = edit
                if use_trigger and not caption.startswith(TRIGGER):
                    caption = f"{TRIGGER}, {caption}"

        txt_path.write_text(caption, encoding="utf-8")
        print(f"  [{i+1}] {img_path.name}")
        print(f"       → {caption}")
        written += 1

    print(f"\n{'─'*50}")
    print(f"Written: {written}  |  Skipped (existing): {skipped}")
    print(f"\nSample captions:")
    for p in list(curated_dir.glob("curated_*.txt"))[:3]:
        print(f"  {p.name}: {p.read_text()}")
    print(f"\nNext step:")
    print(f"  train-hempcrete-lora.bat")

if __name__ == "__main__":
    main()
