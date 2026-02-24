"""
Earthback — PuLID Flux model downloader
========================================
Run this AFTER installing the ComfyUI-PuLID-Flux custom node via Manager.

Downloads:
  - pulid_flux_v0.9.1.safetensors  →  ComfyUI/models/pulid/
  - EVA CLIP model                  →  ComfyUI/models/clip/   (if not present)

InsightFace (buffalo_l) is auto-downloaded by the node on first run.

Usage:
  python setup-pulid.py
  python setup-pulid.py --comfy-path "D:/AI/ComfyUI"   # if not default
"""

import os
import sys
import argparse
import urllib.request
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

MODELS = [
    {
        "name": "PuLID Flux v0.9.1",
        "url":  "https://huggingface.co/guozinan/PuLID/resolve/main/pulid_flux_v0.9.1.safetensors",
        "dest_subdir": "pulid",
        "filename": "pulid_flux_v0.9.1.safetensors",
        "size_mb": 1700,
    },
    {
        "name": "EVA CLIP (L/14@336)",
        "url":  "https://huggingface.co/QuanSun/EVA-CLIP/resolve/main/EVA02_CLIP_L_336_psz14_s6B.pt",
        "dest_subdir": "clip",
        "filename": "EVA02_CLIP_L_336_psz14_s6B.pt",
        "size_mb": 890,
    },
]

DEFAULT_COMFY_PATHS = [
    r"C:\Users\adrxi\ComfyUI",
    r"C:\ComfyUI",
    r"D:\AI\ComfyUI",
    r"D:\ComfyUI",
]

# ── Helpers ─────────────────────────────────────────────────────────────────────

def find_comfy_path():
    for p in DEFAULT_COMFY_PATHS:
        if Path(p).exists():
            return Path(p)
    return None

def download(url, dest_path, name, size_mb):
    if dest_path.exists():
        print(f"  ✓ Already exists: {dest_path.name}  (skipping)")
        return True

    print(f"  Downloading {name} (~{size_mb} MB)...")
    print(f"    → {dest_path}")

    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(downloaded / total_size * 100, 100)
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"\r    [{bar}] {pct:.0f}%", end="", flush=True)

    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest_path, reporthook=progress)
        print()  # newline after progress bar
        print(f"  ✓ Done: {dest_path.name}")
        return True
    except Exception as e:
        print(f"\n  ✗ FAILED: {e}")
        if dest_path.exists():
            dest_path.unlink()  # clean up partial download
        return False

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Download PuLID Flux models for ComfyUI")
    parser.add_argument("--comfy-path", default=None,
                        help=r"Path to ComfyUI root (e.g. D:\AI\ComfyUI)")
    args = parser.parse_args()

    # Find ComfyUI
    if args.comfy_path:
        comfy_root = Path(args.comfy_path)
    else:
        comfy_root = find_comfy_path()

    if not comfy_root or not comfy_root.exists():
        print("ERROR: ComfyUI folder not found.")
        print("Pass your path with:  python setup-pulid.py --comfy-path D:\\AI\\ComfyUI")
        sys.exit(1)

    models_dir = comfy_root / "models"
    print(f"ComfyUI: {comfy_root}")
    print(f"Models:  {models_dir}")
    print()

    # Check custom node is installed
    node_path = comfy_root / "custom_nodes" / "ComfyUI-PuLID-Flux"
    if not node_path.exists():
        print("⚠  ComfyUI-PuLID-Flux custom node not found.")
        print("   Install it first via ComfyUI Manager → Custom Nodes → search 'PuLID Flux'")
        print("   Then restart ComfyUI and re-run this script.")
        print()
        # Still offer to download models
        ans = input("Download models anyway? (y/n): ").strip().lower()
        if ans != "y":
            sys.exit(0)

    ok = 0
    for m in MODELS:
        dest = models_dir / m["dest_subdir"] / m["filename"]
        success = download(m["url"], dest, m["name"], m["size_mb"])
        if success:
            ok += 1

    print()
    if ok == len(MODELS):
        print("✓ All models ready.")
        print()
        print("Next steps:")
        print("  1. Restart ComfyUI (if not done already after installing the node)")
        print("  2. Run:  python queue-pulid-faces.py --help")
        print("     (This script will let you pick a reference face image per character")
        print("      and generate all the angle variants with a locked face.)")
    else:
        print(f"  {ok}/{len(MODELS)} models downloaded — check errors above.")


if __name__ == "__main__":
    main()
