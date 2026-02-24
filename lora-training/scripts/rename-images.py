"""
Earthback — Rename comfyui-output images to character-first naming.

Old: EB-fp-01-social media-T4-chars-James Osei-02_00001_.png
New: chars-James Osei-T4-02_00001_.png

Run with --dry-run first to preview, then run without to apply.

Usage:
  python rename-images.py --dry-run
  python rename-images.py
"""

import os
import re
import argparse
from pathlib import Path

OUTPUT_DIR = Path(r"C:\users\adrxi\Earthback\comfyui-output")

# Known character names exactly as they appear in filenames
CHARACTERS = [
    "James Osei",
    "Lena Hartmann",
    "Tom Westhall",
    "Rosa Mendez",
    "Mei Lin",
    "Elena Vasquez",
    "Amara Diallo",
    "Marcus Webb",
    "Kenji Nakamura",
    "Priya Sharma",
    "Dara Okonkwo",
    "Sam Torres",
]

def new_name(filename: str) -> str | None:
    """
    Map an old-style filename to the new character-first scheme.
    Returns None if this file should be skipped (not a character image).
    """
    stem = Path(filename).stem   # strip .png
    # Extract the trailing _NNNNN_ counter — keep it exactly as-is
    counter_match = re.search(r'(_\d+_)$', stem)
    counter = counter_match.group(1) if counter_match else ""
    base    = stem[: -len(counter)] if counter else stem

    # Find which character this file belongs to
    char_name = None
    for name in CHARACTERS:
        if name in filename:
            char_name = name
            break
    if not char_name:
        return None  # skip — not a character image (e.g. test file)

    # --- T1 / T2 / T3 ---
    for t in ("T1", "T2", "T3"):
        if f"-{t}-chars-" in filename:
            return f"chars-{char_name}-{t}{counter}.png"

    # --- T4-XX (sub-batch number at end, before counter) ---
    # Pattern: -T4-chars-[Name]-NN_counter
    m = re.search(r'-T4-chars-[^-]+-(\d+)$', base)
    if m:
        sub = m.group(1).zfill(2)   # zero-pad: 1 → 01
        return f"chars-{char_name}-T4-{sub}{counter}.png"

    # --- Face batches (new naming, already correct style) ---
    # Pattern: -face-front / -face-left / -face-right / -face-down / -face-talk
    m = re.search(r'-(face-(?:front|left|right|down|talk))$', base)
    if m:
        face = m.group(1)
        return f"chars-{char_name}-{face}{counter}.png"

    return None  # unknown pattern — skip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview renames without changing any files")
    args = parser.parse_args()

    if not OUTPUT_DIR.exists():
        print(f"ERROR: {OUTPUT_DIR} not found")
        return

    files = sorted(OUTPUT_DIR.glob("*.png"))
    renamed = 0
    skipped = 0
    conflicts = 0

    print(f"Scanning {len(files)} .png files in {OUTPUT_DIR}\n")

    for f in files:
        target_name = new_name(f.name)
        if target_name is None:
            print(f"  SKIP  {f.name}")
            skipped += 1
            continue

        target = OUTPUT_DIR / target_name

        if target == f:
            print(f"  OK    {f.name}  (already correct)")
            continue

        if target.exists():
            print(f"  CONFLICT  {f.name}  →  {target_name}  (target exists!)")
            conflicts += 1
            continue

        if args.dry_run:
            print(f"  RENAME  {f.name}")
            print(f"       →  {target_name}")
        else:
            f.rename(target)
            print(f"  ✓  {target_name}")
        renamed += 1

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done.")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")
    if conflicts:
        print(f"  CONFLICTS (not renamed): {conflicts}")


if __name__ == "__main__":
    main()
