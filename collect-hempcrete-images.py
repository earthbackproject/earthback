#!/usr/bin/env python3
"""
collect-hempcrete-images.py — Download hempcrete & natural building photos for LoRA training.

Sources:
  Wikimedia Commons — CC-licensed, has real hempcrete-tagged images (no key needed)
  Pexels           — CC0, used for broader natural building visual vocabulary
  Pixabay          — CC0, used for broader natural building visual vocabulary

Note on Pexels/Pixabay: "hempcrete" returns almost nothing on stock sites.
These sources are used for RELATED visual terms that help the LoRA learn the
correct aesthetic neighborhood: lime plaster, earthen walls, natural building
textures, construction process shots.

Wikimedia is where the actual hempcrete images live.

Usage:
  python collect-hempcrete-images.py --pexels-key KEY1 --pixabay-key KEY2
  python collect-hempcrete-images.py --source wikimedia        # no keys needed
  python collect-hempcrete-images.py --list-terms
  python collect-hempcrete-images.py --dry-run --source wikimedia

Output:
  dataset-hempcrete/raw/wikimedia/
  dataset-hempcrete/raw/pexels/
  dataset-hempcrete/raw/pixabay/
  dataset-hempcrete/raw/metadata.json
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from urllib.parse import quote

OUTPUT_DIR = Path("dataset-hempcrete/raw")
MIN_WIDTH  = 800
MIN_HEIGHT = 800

# ─── Search terms ──────────────────────────────────────────────────────────────

# CORE — actual hempcrete terms (Wikimedia has these; stock sites mostly don't)
TERMS_CORE = [
    "hempcrete",
    "hemp lime",
    "hemp lime construction",
    "hempcrete wall",
    "hemp building",
    "hemp hurds lime",
]

# SUPPORTING — related natural building terms for stock sites
# These teach the model the correct visual vocabulary even if not hempcrete-specific
TERMS_SUPPORTING = [
    "lime plaster wall",
    "natural lime render",
    "earthen wall construction",
    "cob wall building",
    "straw bale construction",
    "rammed earth wall",
    "natural building construction",
    "lime wash wall texture",
    "insulated wall formwork",
    "natural insulation building",
    "hemp fiber material",
    "lime mortar masonry",
]

# Wikimedia Commons category searches (in addition to text search)
WIKIMEDIA_CATEGORIES = [
    "Hempcrete",
    "Hemp_construction",
    "Natural_building",
    "Lime_plaster",
    "Straw_bale_construction",
    "Cob_(material)",
    "Rammed_earth",
]

# ─── Wikimedia Commons ─────────────────────────────────────────────────────────

WIKI_API = "https://commons.wikimedia.org/w/api.php"

def wikimedia_search_text(query, limit=50):
    """Full-text search of Wikimedia Commons file namespace."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",   # File namespace
        "srlimit": min(limit, 50),
        "format": "json",
    }
    r = requests.get(WIKI_API, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    return [hit["title"] for hit in data.get("query", {}).get("search", [])]

def wikimedia_category_members(category, limit=100):
    """Get file members of a Wikimedia Commons category."""
    titles = []
    cmcontinue = None
    while len(titles) < limit:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmtype": "file",
            "cmlimit": min(50, limit - len(titles)),
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        r = requests.get(WIKI_API, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        members = data.get("query", {}).get("categorymembers", [])
        titles.extend(m["title"] for m in members)
        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
    return titles

def wikimedia_get_image_info(titles):
    """Get download URLs and metadata for a list of File: titles (max 50 at once)."""
    results = []
    # Process in batches of 50
    for i in range(0, len(titles), 50):
        batch = titles[i:i+50]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "imageinfo",
            "iiprop": "url|size|extmetadata|mime",
            "iiurlwidth": 1024,
            "format": "json",
        }
        r = requests.get(WIKI_API, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            if page_id == "-1":
                continue
            infos = page.get("imageinfo", [])
            if not infos:
                continue
            info = infos[0]
            mime = info.get("mime", "")
            if not mime.startswith("image/"):
                continue
            if mime in ("image/svg+xml", "image/gif"):
                continue  # skip vectors and animated
            w = info.get("width", 0)
            h = info.get("height", 0)
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                continue
            url = info.get("thumburl") or info.get("url")
            if not url:
                continue
            meta = info.get("extmetadata", {})
            license_short = meta.get("LicenseShortName", {}).get("value", "")
            results.append({
                "title": page.get("title", ""),
                "url": url,
                "width": w,
                "height": h,
                "mime": mime,
                "license": license_short,
                "page_url": f"https://commons.wikimedia.org/wiki/{quote(page.get('title',''))}",
            })
    return results

def collect_wikimedia(output_dir, max_images, dry_run=False):
    print("\n=== WIKIMEDIA COMMONS ===")
    dest_dir = output_dir / "wikimedia"
    dest_dir.mkdir(parents=True, exist_ok=True)
    meta = []
    seen_titles = set()

    all_titles = []

    # Text search for core terms
    print("\n  Text searches...")
    for term in TERMS_CORE:
        print(f"    Searching: '{term}'")
        try:
            titles = wikimedia_search_text(term, limit=50)
            print(f"      → {len(titles)} results")
            all_titles.extend(titles)
        except Exception as e:
            print(f"    Error: {e}")
        time.sleep(0.3)

    # Category browsing
    print("\n  Category searches...")
    for cat in WIKIMEDIA_CATEGORIES:
        print(f"    Category: {cat}")
        try:
            titles = wikimedia_category_members(cat, limit=50)
            print(f"      → {len(titles)} files")
            all_titles.extend(titles)
        except Exception as e:
            print(f"    Error: {e}")
        time.sleep(0.3)

    # Deduplicate
    unique_titles = list(dict.fromkeys(all_titles))
    print(f"\n  {len(unique_titles)} unique files found. Fetching image info...")

    # Get image info in batches
    image_infos = wikimedia_get_image_info(unique_titles)
    print(f"  {len(image_infos)} valid images after size/format filter")

    downloaded = 0
    for info in image_infos:
        if downloaded >= max_images:
            break
        title = info["title"]
        if title in seen_titles:
            continue
        seen_titles.add(title)

        # Derive filename from title
        stem = title.replace("File:", "").replace(" ", "_").replace("/", "_")
        ext = ".jpg"
        filename = f"wikimedia_{stem}"[:180] + ext
        dest = dest_dir / filename

        entry = {
            "file": str(dest),
            "source": "wikimedia",
            "title": title,
            "page_url": info["page_url"],
            "license": info["license"],
            "width": info["width"],
            "height": info["height"],
            "download_url": info["url"],
        }

        if dest.exists():
            print(f"    [skip] {filename}")
            downloaded += 1
            meta.append(entry)
            continue

        if dry_run:
            print(f"    [dry] {filename} ({info['width']}x{info['height']}) [{info['license']}]")
            downloaded += 1
            meta.append(entry)
            continue

        print(f"    [{downloaded+1}] {filename} ({info['width']}x{info['height']}) [{info['license']}]")
        try:
            r = requests.get(info["url"], timeout=30, stream=True)
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            downloaded += 1
            meta.append(entry)
        except Exception as e:
            print(f"      Download failed: {e}")

        time.sleep(0.2)

    print(f"\n  Wikimedia total: {downloaded} images")
    return meta

# ─── Pexels ────────────────────────────────────────────────────────────────────

def search_pexels(key, query, per_page=80, page=1):
    r = requests.get(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": key},
        params={"query": query, "per_page": min(per_page, 80), "page": page},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def collect_pexels(key, output_dir, max_images, dry_run=False):
    print("\n=== PEXELS (supporting terms) ===")
    dest_dir = output_dir / "pexels"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_ids = set()
    downloaded = 0
    meta = []

    all_terms = TERMS_CORE + TERMS_SUPPORTING
    for term in all_terms:
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
                w, h = photo["width"], photo["height"]
                if w < MIN_WIDTH or h < MIN_HEIGHT:
                    continue
                src = photo["src"]
                url = src.get("large2x") or src.get("large") or src.get("original")
                filename = f"pexels_{img_id}.jpg"
                dest = dest_dir / filename
                entry = {"file": str(dest), "source": "pexels", "id": img_id,
                         "term": term, "photographer": photo.get("photographer", ""),
                         "width": w, "height": h, "download_url": url,
                         "page_url": photo.get("url", "")}
                if dest.exists():
                    downloaded += 1; meta.append(entry); continue
                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h})")
                    downloaded += 1; meta.append(entry); continue
                print(f"    [{downloaded+1}] {filename} ({w}x{h}) — {term}")
                try:
                    r = requests.get(url, timeout=30, stream=True)
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
                    downloaded += 1; meta.append(entry)
                except Exception as e:
                    print(f"      Failed: {e}")
                time.sleep(0.15)
            if not data.get("next_page"):
                break
            page += 1

    print(f"\n  Pexels total: {downloaded} images")
    return meta

# ─── Pixabay ───────────────────────────────────────────────────────────────────

def search_pixabay(key, query, per_page=200, page=1):
    r = requests.get(
        "https://pixabay.com/api/",
        params={"key": key, "q": query, "image_type": "photo",
                "per_page": min(per_page, 200), "page": page,
                "min_width": MIN_WIDTH, "min_height": MIN_HEIGHT,
                "safesearch": "true", "order": "popular"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def collect_pixabay(key, output_dir, max_images, dry_run=False):
    print("\n=== PIXABAY (supporting terms) ===")
    dest_dir = output_dir / "pixabay"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_ids = set()
    downloaded = 0
    meta = []

    all_terms = TERMS_CORE + TERMS_SUPPORTING
    for term in all_terms:
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
                w, h = hit["imageWidth"], hit["imageHeight"]
                url = hit.get("largeImageURL") or hit.get("webformatURL")
                filename = f"pixabay_{img_id}.jpg"
                dest = dest_dir / filename
                entry = {"file": str(dest), "source": "pixabay", "id": img_id,
                         "term": term, "width": w, "height": h, "download_url": url,
                         "page_url": hit.get("pageURL", "")}
                if dest.exists():
                    downloaded += 1; meta.append(entry); continue
                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h})")
                    downloaded += 1; meta.append(entry); continue
                print(f"    [{downloaded+1}] {filename} ({w}x{h}) — {term}")
                try:
                    r = requests.get(url, timeout=30, stream=True)
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
                    downloaded += 1; meta.append(entry)
                except Exception as e:
                    print(f"      Failed: {e}")
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
        description="Collect hempcrete + natural building images for LoRA training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sources:
  wikimedia  — CC-licensed, has actual hempcrete images. No key needed.
  pexels     — CC0 stock, used for supporting natural building terms.
  pixabay    — CC0 stock, used for supporting natural building terms.
  all        — All three (default)

API keys (both free):
  Pexels:  https://www.pexels.com/api/
  Pixabay: https://pixabay.com/api/docs/

Examples:
  python collect-hempcrete-images.py --source wikimedia
  python collect-hempcrete-images.py --pexels-key KEY1 --pixabay-key KEY2
  python collect-hempcrete-images.py --dry-run --source wikimedia
        """
    )
    parser.add_argument("--pexels-key",  default=os.environ.get("PEXELS_API_KEY",  ""))
    parser.add_argument("--pixabay-key", default=os.environ.get("PIXABAY_API_KEY", ""))
    parser.add_argument("--source", choices=["wikimedia", "pexels", "pixabay", "all"], default="all")
    parser.add_argument("--max",    type=int, default=150, help="Max images per source (default 150)")
    parser.add_argument("--output", default="dataset-hempcrete/raw")
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--list-terms", action="store_true")
    args = parser.parse_args()

    if args.list_terms:
        print("Core terms (hempcrete-specific):")
        for t in TERMS_CORE: print(f"  • {t}")
        print("\nSupporting terms (natural building visual vocabulary):")
        for t in TERMS_SUPPORTING: print(f"  • {t}")
        print("\nWikimedia categories:")
        for c in WIKIMEDIA_CATEGORIES: print(f"  • {c}")
        return

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("DRY RUN — no files will be downloaded")

    all_meta = []

    if args.source in ("wikimedia", "all"):
        all_meta.extend(collect_wikimedia(output_dir, args.max, args.dry_run))

    if args.source in ("pexels", "all"):
        if not args.pexels_key:
            print("⚠  No Pexels key. Get free at: https://www.pexels.com/api/")
            if args.source == "pexels": sys.exit(1)
        else:
            all_meta.extend(collect_pexels(args.pexels_key, output_dir, args.max, args.dry_run))

    if args.source in ("pixabay", "all"):
        if not args.pixabay_key:
            print("⚠  No Pixabay key. Get free at: https://pixabay.com/api/docs/")
            if args.source == "pixabay": sys.exit(1)
        else:
            all_meta.extend(collect_pixabay(args.pixabay_key, output_dir, args.max, args.dry_run))

    meta_path = output_dir / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(all_meta, f, indent=2)

    print(f"\n{'─'*50}")
    print(f"Total collected: {len(all_meta)} images")
    print(f"Metadata saved:  {meta_path}")
    if not args.dry_run:
        print(f"\nNext steps:")
        print(f"  python curate-hempcrete-images.py --review")
        print(f"  python caption-hempcrete-images.py")
        print(f"  train-hempcrete-lora.bat")

if __name__ == "__main__":
    main()
