#!/usr/bin/env python3
"""
collect-3dprinter-images.py — Download 3D printer photos from stock image APIs
for LoRA training dataset.

Sources (all CC0 / commercial use):
  Pexels   — free API key at https://www.pexels.com/api/
  Pixabay  — free API key at https://pixabay.com/api/docs/

Usage:
  python collect-3dprinter-images.py --pexels-key KEY1 --pixabay-key KEY2
  python collect-3dprinter-images.py --pexels-key KEY1 --source pexels
  python collect-3dprinter-images.py --list-terms
  python collect-3dprinter-images.py --dry-run --pexels-key KEY1

Output:
  dataset-3dprinter/raw/pexels/
  dataset-3dprinter/raw/pixabay/
  dataset-3dprinter/raw/metadata.json
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path

OUTPUT_DIR = Path("dataset-3dprinter/raw")

# ─── Search terms ──────────────────────────────────────────────────────────────
# Ordered by expected relevance — broad terms first, model-specific last

SEARCH_TERMS = [
    "3D printer",
    "FDM 3D printer",
    "filament 3D printer",
    "desktop 3D printer",
    "3D printing machine",
    "3D printer filament",
    "3D printer nozzle",
    "3D printer extruder",
    "3D printer build plate",
    "Bambu Lab printer",
    "Prusa 3D printer",
    "Creality 3D printer",
    "Ender 3 printer",
    "3D printing workshop",
    "maker 3D printer",
]

MIN_WIDTH = 800
MIN_HEIGHT = 800

# ─── Pexels ────────────────────────────────────────────────────────────────────

def search_pexels(key, query, per_page=80, page=1):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": key}
    params = {
        "query": query,
        "per_page": min(per_page, 80),
        "page": page,
    }
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def collect_pexels(key, output_dir, max_images, dry_run=False):
    print("\n=== PEXELS ===")
    seen_ids = set()
    downloaded = 0
    dest_dir = output_dir / "pexels"
    dest_dir.mkdir(parents=True, exist_ok=True)
    meta = []

    for term in SEARCH_TERMS:
        if downloaded >= max_images:
            break
        print(f"\n  Searching: '{term}'")
        page = 1

        while downloaded < max_images:
            try:
                data = search_pexels(key, term, per_page=80, page=page)
            except Exception as e:
                print(f"  API error: {e}")
                break

            photos = data.get("photos", [])
            if not photos:
                break

            for photo in photos:
                if downloaded >= max_images:
                    break

                img_id = photo["id"]
                if img_id in seen_ids:
                    continue
                seen_ids.add(img_id)

                w = photo["width"]
                h = photo["height"]
                if w < MIN_WIDTH or h < MIN_HEIGHT:
                    continue

                src = photo["src"]
                url = src.get("large2x") or src.get("large") or src.get("original")

                filename = f"pexels_{img_id}.jpg"
                dest = dest_dir / filename

                entry = {
                    "file": str(dest),
                    "source": "pexels",
                    "id": img_id,
                    "term": term,
                    "page_url": photo.get("url", ""),
                    "photographer": photo.get("photographer", ""),
                    "width": w,
                    "height": h,
                    "download_url": url,
                }

                if dest.exists():
                    print(f"    [skip] {filename}")
                    downloaded += 1
                    meta.append(entry)
                    continue

                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h}) — {term}")
                    downloaded += 1
                    meta.append(entry)
                    continue

                print(f"    [{downloaded+1}] {filename} ({w}x{h})")
                try:
                    r = requests.get(url, timeout=30, stream=True)
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    downloaded += 1
                    meta.append(entry)
                except Exception as e:
                    print(f"      Download failed: {e}")

                time.sleep(0.15)

            if not data.get("next_page"):
                break
            page += 1

    print(f"\n  Pexels total: {downloaded} images")
    return meta

# ─── Pixabay ───────────────────────────────────────────────────────────────────

def search_pixabay(key, query, per_page=200, page=1):
    url = "https://pixabay.com/api/"
    params = {
        "key": key,
        "q": query,
        "image_type": "photo",
        "per_page": min(per_page, 200),
        "page": page,
        "min_width": MIN_WIDTH,
        "min_height": MIN_HEIGHT,
        "safesearch": "true",
        "order": "popular",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def collect_pixabay(key, output_dir, max_images, dry_run=False):
    print("\n=== PIXABAY ===")
    seen_ids = set()
    downloaded = 0
    dest_dir = output_dir / "pixabay"
    dest_dir.mkdir(parents=True, exist_ok=True)
    meta = []

    for term in SEARCH_TERMS:
        if downloaded >= max_images:
            break
        print(f"\n  Searching: '{term}'")
        page = 1

        while downloaded < max_images:
            try:
                data = search_pixabay(key, term, per_page=200, page=page)
            except Exception as e:
                print(f"  API error: {e}")
                break

            hits = data.get("hits", [])
            if not hits:
                break

            for hit in hits:
                if downloaded >= max_images:
                    break

                img_id = hit["id"]
                if img_id in seen_ids:
                    continue
                seen_ids.add(img_id)

                w = hit["imageWidth"]
                h = hit["imageHeight"]

                url = hit.get("largeImageURL") or hit.get("webformatURL")
                filename = f"pixabay_{img_id}.jpg"
                dest = dest_dir / filename

                entry = {
                    "file": str(dest),
                    "source": "pixabay",
                    "id": img_id,
                    "term": term,
                    "page_url": hit.get("pageURL", ""),
                    "width": w,
                    "height": h,
                    "download_url": url,
                }

                if dest.exists():
                    print(f"    [skip] {filename}")
                    downloaded += 1
                    meta.append(entry)
                    continue

                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h}) — {term}")
                    downloaded += 1
                    meta.append(entry)
                    continue

                print(f"    [{downloaded+1}] {filename} ({w}x{h})")
                try:
                    r = requests.get(url, timeout=30, stream=True)
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    downloaded += 1
                    meta.append(entry)
                except Exception as e:
                    print(f"      Download failed: {e}")

                time.sleep(0.15)

            total = data.get("totalHits", 0)
            if page * 200 >= total:
                break
            page += 1

    print(f"\n  Pixabay total: {downloaded} images")
    return meta

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Collect 3D printer stock photos for LoRA training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
API keys (both free):
  Pexels:  https://www.pexels.com/api/
  Pixabay: https://pixabay.com/api/docs/

Examples:
  python collect-3dprinter-images.py --pexels-key KEY1 --pixabay-key KEY2
  python collect-3dprinter-images.py --pexels-key KEY1 --source pexels --max 100
  python collect-3dprinter-images.py --dry-run --pexels-key KEY1
        """
    )
    parser.add_argument("--pexels-key",  default=os.environ.get("PEXELS_API_KEY", ""),  help="Pexels API key (or set PEXELS_API_KEY env)")
    parser.add_argument("--pixabay-key", default=os.environ.get("PIXABAY_API_KEY", ""), help="Pixabay API key (or set PIXABAY_API_KEY env)")
    parser.add_argument("--source", choices=["pexels", "pixabay", "all"], default="all")
    parser.add_argument("--max",    type=int, default=150, help="Max images per source (default 150)")
    parser.add_argument("--output", default="dataset-3dprinter/raw", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="List what would be downloaded without downloading")
    parser.add_argument("--list-terms", action="store_true", help="Print search terms and exit")
    args = parser.parse_args()

    if args.list_terms:
        print("Search terms:")
        for t in SEARCH_TERMS:
            print(f"  • {t}")
        return

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("DRY RUN — no files will be downloaded")

    all_meta = []

    if args.source in ("pexels", "all"):
        if not args.pexels_key:
            print("⚠  No Pexels key. Get one free at: https://www.pexels.com/api/")
            print("   Pass with: --pexels-key YOUR_KEY  or  set PEXELS_API_KEY env")
            if args.source == "pexels":
                sys.exit(1)
        else:
            all_meta.extend(collect_pexels(args.pexels_key, output_dir, args.max, args.dry_run))

    if args.source in ("pixabay", "all"):
        if not args.pixabay_key:
            print("⚠  No Pixabay key. Get one free at: https://pixabay.com/api/docs/")
            print("   Pass with: --pixabay-key YOUR_KEY  or  set PIXABAY_API_KEY env")
            if args.source == "pixabay":
                sys.exit(1)
        else:
            all_meta.extend(collect_pixabay(args.pixabay_key, output_dir, args.max, args.dry_run))

    # Save metadata
    meta_path = output_dir / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(all_meta, f, indent=2)

    print(f"\n{'─'*50}")
    print(f"Total collected: {len(all_meta)} images")
    print(f"Metadata saved:  {meta_path}")
    if not args.dry_run:
        print(f"\nNext step:")
        print(f"  python curate-3dprinter-images.py")

if __name__ == "__main__":
    main()
