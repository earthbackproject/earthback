#!/usr/bin/env python3
"""
collect-construction-machine-images.py
Download images for two construction machine LoRAs:

  MACHINE_GANTRY   — Large-format gantry-style 3D printers / portal frame
                     construction robots. Think: overhead beam on rails, nozzle
                     moving in XY, printing concrete/hempcrete/clay layer by layer.
                     NOT desktop FDM printers.

  MACHINE_PUMP     — Concrete pump / crane-arm delivery systems. Think: truck-mounted
                     boom arm, separate mixing + pumping unit, hose-and-nozzle end
                     effector. Also covers shotcrete/gunite rigs which are visually
                     similar and sometimes used in natural building contexts.

These are kept as separate datasets so each LoRA trains cleanly on its own
visual identity. The gantry machine is more unique (Earthback-specific context);
the pump/crane is drawn from abundant stock photography.

Sources:
  Pexels   — CC0, good for pump/crane (abundant); sparse for gantry
  Pixabay  — CC0, same
  Wikimedia — CC-licensed, has some construction robotics / concrete pump images

Usage:
  python collect-construction-machine-images.py --pexels-key KEY --pixabay-key KEY
  python collect-construction-machine-images.py --machine gantry --source wikimedia
  python collect-construction-machine-images.py --machine pump --pexels-key KEY
  python collect-construction-machine-images.py --list-terms
  python collect-construction-machine-images.py --dry-run --machine pump --pexels-key KEY
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from urllib.parse import quote

MIN_WIDTH  = 800
MIN_HEIGHT = 800

# ─── Search terms by machine type ─────────────────────────────────────────────

TERMS = {
    "gantry": {
        # Core — gantry 3D printers and portal construction robots
        "core": [
            "gantry 3D printer",
            "large format 3D printer",
            "construction 3D printer",
            "concrete 3D printer",
            "3D printing construction",
            "additive construction",
            "3D printed building",
            "3D printing house",
            "robotic construction",
            "portal frame robot",
            "automated construction machine",
        ],
        # Supporting — construction machinery visually adjacent
        "supporting": [
            "gantry crane",
            "portal crane",
            "overhead crane workshop",
            "CNC gantry machine",
            "industrial robot arm construction",
            "construction robot",
            "concrete extrusion",
            "layer by layer construction",
        ],
        "wikimedia_categories": [
            "Construction_3D_printing",
            "Additive_manufacturing",
            "3D_printed_buildings",
            "Construction_robotics",
        ],
        "wikimedia_terms": [
            "construction 3D printer",
            "concrete 3D printing",
            "gantry 3D printer building",
            "additive construction robot",
        ],
    },
    "pump": {
        # Core — concrete pump trucks and boom systems
        "core": [
            "concrete pump truck",
            "boom pump concrete",
            "truck mounted concrete pump",
            "concrete boom arm",
            "concrete pumping construction",
            "pump truck construction site",
            "placing boom concrete",
        ],
        # Supporting — crane arms, delivery systems, site machinery
        "supporting": [
            "mobile crane construction",
            "concrete pour construction",
            "concrete delivery site",
            "construction crane arm",
            "shotcrete machine",
            "gunite equipment",
            "concrete hose construction",
            "ready mix concrete truck",
            "concrete placement construction",
            "spider crane",
        ],
        "wikimedia_categories": [
            "Concrete_pump_trucks",
            "Concrete_pumps",
            "Construction_equipment",
            "Concrete_construction",
        ],
        "wikimedia_terms": [
            "concrete pump truck",
            "boom pump construction",
            "concrete pumping",
        ],
    },
}

WIKI_API = "https://commons.wikimedia.org/w/api.php"

# ─── Wikimedia ─────────────────────────────────────────────────────────────────

def wikimedia_search_text(query, limit=50):
    params = {"action": "query", "list": "search", "srsearch": query,
              "srnamespace": "6", "srlimit": min(limit, 50), "format": "json"}
    r = requests.get(WIKI_API, params=params, timeout=15)
    r.raise_for_status()
    return [h["title"] for h in r.json().get("query", {}).get("search", [])]

def wikimedia_category_members(category, limit=80):
    titles = []
    cmcontinue = None
    while len(titles) < limit:
        params = {"action": "query", "list": "categorymembers",
                  "cmtitle": f"Category:{category}", "cmtype": "file",
                  "cmlimit": min(50, limit - len(titles)), "format": "json"}
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        r = requests.get(WIKI_API, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        titles.extend(m["title"] for m in data.get("query", {}).get("categorymembers", []))
        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
    return titles

def wikimedia_get_image_info(titles):
    results = []
    for i in range(0, len(titles), 50):
        batch = titles[i:i+50]
        params = {"action": "query", "titles": "|".join(batch), "prop": "imageinfo",
                  "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1024, "format": "json"}
        r = requests.get(WIKI_API, params=params, timeout=15)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            if page_id == "-1":
                continue
            infos = page.get("imageinfo", [])
            if not infos:
                continue
            info = infos[0]
            mime = info.get("mime", "")
            if not mime.startswith("image/") or mime in ("image/svg+xml", "image/gif"):
                continue
            w, h = info.get("width", 0), info.get("height", 0)
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                continue
            url = info.get("thumburl") or info.get("url")
            if not url:
                continue
            meta = info.get("extmetadata", {})
            results.append({
                "title": page.get("title", ""),
                "url": url, "width": w, "height": h, "mime": mime,
                "license": meta.get("LicenseShortName", {}).get("value", ""),
                "page_url": f"https://commons.wikimedia.org/wiki/{quote(page.get('title',''))}",
            })
    return results

def collect_wikimedia(machine, output_dir, max_images, dry_run=False):
    print(f"\n=== WIKIMEDIA ({machine.upper()}) ===")
    dest_dir = output_dir / "wikimedia"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_titles = set()
    meta = []
    config = TERMS[machine]
    all_titles = []

    for term in config["wikimedia_terms"]:
        print(f"  Searching: '{term}'")
        try:
            all_titles.extend(wikimedia_search_text(term))
        except Exception as e:
            print(f"    Error: {e}")
        time.sleep(0.3)

    for cat in config["wikimedia_categories"]:
        print(f"  Category: {cat}")
        try:
            all_titles.extend(wikimedia_category_members(cat))
        except Exception as e:
            print(f"    Error: {e}")
        time.sleep(0.3)

    unique = list(dict.fromkeys(all_titles))
    print(f"  {len(unique)} unique files. Fetching image info...")
    image_infos = wikimedia_get_image_info(unique)
    print(f"  {len(image_infos)} valid images after filter")

    downloaded = 0
    for info in image_infos:
        if downloaded >= max_images:
            break
        title = info["title"]
        if title in seen_titles:
            continue
        seen_titles.add(title)
        stem = title.replace("File:", "").replace(" ", "_").replace("/", "_")
        filename = f"wikimedia_{stem}"[:180] + ".jpg"
        dest = dest_dir / filename
        entry = {"file": str(dest), "source": "wikimedia", "machine": machine,
                 "title": title, "license": info["license"],
                 "width": info["width"], "height": info["height"],
                 "download_url": info["url"], "page_url": info["page_url"]}
        if dest.exists():
            downloaded += 1; meta.append(entry); continue
        if dry_run:
            print(f"  [dry] {filename} ({info['width']}x{info['height']}) [{info['license']}]")
            downloaded += 1; meta.append(entry); continue
        print(f"  [{downloaded+1}] {filename}")
        try:
            r = requests.get(info["url"], timeout=30, stream=True)
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
            downloaded += 1; meta.append(entry)
        except Exception as e:
            print(f"    Failed: {e}")
        time.sleep(0.2)

    print(f"  Wikimedia total: {downloaded}")
    return meta

# ─── Pexels ────────────────────────────────────────────────────────────────────

def collect_pexels(key, machine, output_dir, max_images, dry_run=False):
    print(f"\n=== PEXELS ({machine.upper()}) ===")
    dest_dir = output_dir / "pexels"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_ids = set()
    downloaded = 0
    meta = []
    config = TERMS[machine]
    all_terms = config["core"] + config["supporting"]

    for term in all_terms:
        if downloaded >= max_images:
            break
        print(f"  '{term}'")
        page = 1
        while downloaded < max_images:
            try:
                r = requests.get("https://api.pexels.com/v1/search",
                    headers={"Authorization": key},
                    params={"query": term, "per_page": 80, "page": page}, timeout=15)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  Error: {e}"); break
            for photo in data.get("photos", []):
                if downloaded >= max_images: break
                img_id = photo["id"]
                if img_id in seen_ids: continue
                seen_ids.add(img_id)
                w, h = photo["width"], photo["height"]
                if w < MIN_WIDTH or h < MIN_HEIGHT: continue
                src = photo["src"]
                url = src.get("large2x") or src.get("large") or src.get("original")
                filename = f"pexels_{img_id}.jpg"
                dest = dest_dir / filename
                entry = {"file": str(dest), "source": "pexels", "machine": machine,
                         "id": img_id, "term": term, "width": w, "height": h,
                         "download_url": url, "page_url": photo.get("url", ""),
                         "photographer": photo.get("photographer", "")}
                if dest.exists():
                    downloaded += 1; meta.append(entry); continue
                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h}) — {term}")
                    downloaded += 1; meta.append(entry); continue
                print(f"    [{downloaded+1}] {filename}")
                try:
                    resp = requests.get(url, timeout=30, stream=True)
                    resp.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192): f.write(chunk)
                    downloaded += 1; meta.append(entry)
                except Exception as e:
                    print(f"      Failed: {e}")
                time.sleep(0.15)
            if not data.get("next_page"): break
            page += 1

    print(f"  Pexels total: {downloaded}")
    return meta

# ─── Pixabay ───────────────────────────────────────────────────────────────────

def collect_pixabay(key, machine, output_dir, max_images, dry_run=False):
    print(f"\n=== PIXABAY ({machine.upper()}) ===")
    dest_dir = output_dir / "pixabay"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_ids = set()
    downloaded = 0
    meta = []
    config = TERMS[machine]
    all_terms = config["core"] + config["supporting"]

    for term in all_terms:
        if downloaded >= max_images: break
        print(f"  '{term}'")
        page = 1
        while downloaded < max_images:
            try:
                r = requests.get("https://pixabay.com/api/",
                    params={"key": key, "q": term, "image_type": "photo",
                            "per_page": 200, "page": page,
                            "min_width": MIN_WIDTH, "min_height": MIN_HEIGHT,
                            "safesearch": "true"}, timeout=15)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  Error: {e}"); break
            for hit in data.get("hits", []):
                if downloaded >= max_images: break
                img_id = hit["id"]
                if img_id in seen_ids: continue
                seen_ids.add(img_id)
                w, h = hit["imageWidth"], hit["imageHeight"]
                url = hit.get("largeImageURL") or hit.get("webformatURL")
                filename = f"pixabay_{img_id}.jpg"
                dest = dest_dir / filename
                entry = {"file": str(dest), "source": "pixabay", "machine": machine,
                         "id": img_id, "term": term, "width": w, "height": h,
                         "download_url": url, "page_url": hit.get("pageURL", "")}
                if dest.exists():
                    downloaded += 1; meta.append(entry); continue
                if dry_run:
                    print(f"    [dry] {filename} ({w}x{h})")
                    downloaded += 1; meta.append(entry); continue
                print(f"    [{downloaded+1}] {filename}")
                try:
                    resp = requests.get(url, timeout=30, stream=True)
                    resp.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192): f.write(chunk)
                    downloaded += 1; meta.append(entry)
                except Exception as e:
                    print(f"      Failed: {e}")
                time.sleep(0.15)
            total = data.get("totalHits", 0)
            if page * 200 >= total: break
            page += 1

    print(f"  Pixabay total: {downloaded}")
    return meta

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Collect construction machine images for LoRA training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Machine types:
  gantry  — Large-format gantry 3D printers, construction robots, portal frames
  pump    — Concrete pump trucks, boom arms, shotcrete rigs
  both    — Collect both (default, separate dataset directories)

Output directories:
  dataset-gantry/raw/   — for gantry machine LoRA
  dataset-pump/raw/     — for pump/crane LoRA

Next steps after collection:
  python curate-hempcrete-images.py  (adapt --input path)
  python caption-hempcrete-images.py (adapt --input path and captions)
  train-gantry-lora.bat / train-pump-lora.bat
        """
    )
    parser.add_argument("--machine", choices=["gantry", "pump", "both"], default="both")
    parser.add_argument("--source",  choices=["wikimedia", "pexels", "pixabay", "all"], default="all")
    parser.add_argument("--pexels-key",  default=os.environ.get("PEXELS_API_KEY",  ""))
    parser.add_argument("--pixabay-key", default=os.environ.get("PIXABAY_API_KEY", ""))
    parser.add_argument("--max",    type=int, default=150)
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--list-terms", action="store_true")
    args = parser.parse_args()

    if args.list_terms:
        for mtype in ["gantry", "pump"]:
            print(f"\n── {mtype.upper()} ──")
            config = TERMS[mtype]
            print("Core:")
            for t in config["core"]: print(f"  • {t}")
            print("Supporting:")
            for t in config["supporting"]: print(f"  • {t}")
            print("Wikimedia categories:")
            for c in config["wikimedia_categories"]: print(f"  • {c}")
        return

    machines = ["gantry", "pump"] if args.machine == "both" else [args.machine]

    for machine in machines:
        output_dir = Path(f"dataset-{machine}/raw")
        output_dir.mkdir(parents=True, exist_ok=True)
        all_meta = []

        if args.source in ("wikimedia", "all"):
            all_meta.extend(collect_wikimedia(machine, output_dir, args.max, args.dry_run))

        if args.source in ("pexels", "all"):
            if not args.pexels_key:
                print(f"⚠  No Pexels key — skipping pexels for {machine}")
            else:
                all_meta.extend(collect_pexels(args.pexels_key, machine, output_dir, args.max, args.dry_run))

        if args.source in ("pixabay", "all"):
            if not args.pixabay_key:
                print(f"⚠  No Pixabay key — skipping pixabay for {machine}")
            else:
                all_meta.extend(collect_pixabay(args.pixabay_key, machine, output_dir, args.max, args.dry_run))

        meta_path = output_dir / "metadata.json"
        with open(meta_path, "w") as f:
            json.dump(all_meta, f, indent=2)

        print(f"\n{'─'*50}")
        print(f"{machine.upper()} — {len(all_meta)} total images")
        print(f"Metadata: {meta_path}")

    print(f"\nNext steps:")
    for machine in machines:
        print(f"  python curate-hempcrete-images.py --input dataset-{machine}/raw --output dataset-{machine}/curated --review")
        print(f"  (then caption and train — see train-{machine}-lora.bat)")

if __name__ == "__main__":
    main()
