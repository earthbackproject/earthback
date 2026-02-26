"""
Earthback — Reference Image Scraper
Scrapes hempcrete and 3D-printed concrete images from curated sources.
Downloads images >= MIN_SIZE into organized folders for LoRA training review.

Usage:
  pip install requests beautifulsoup4

  # Run with built-in URLs:
  python scrape-reference-images.py

  # Run with a URL file (one URL per line, blank lines and #comments ignored):
  python scrape-reference-images.py urls.txt

  # Run with a URL file into a specific category folder:
  python scrape-reference-images.py urls.txt --category earthships

URL file format:
  # This is a comment
  https://example.com/page1
  https://example.com/page2

Output folders:
  lora-reference/hempcrete/
  lora-reference/3d-concrete/
  lora-reference/<custom-category>/
"""

import os, re, sys, time, hashlib, argparse
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# ── CONFIG ──────────────────────────────────────────────────
MIN_WIDTH  = 600      # skip images smaller than this (when detectable)
MIN_BYTES  = 40_000   # skip files smaller than 40 KB
MAX_BYTES  = 25_000_000  # skip files larger than 25 MB
TIMEOUT    = 15
DELAY      = 1.0      # seconds between page fetches (be polite)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lora-reference")

# ── SOURCES ─────────────────────────────────────────────────
SOURCES = {
    "hempcrete": [
        "https://www.ukhempcrete.com/gallery/",
        "https://hempbuilding.au/hempcrete-buildings-structures/",
        "https://hempstone.net/goshenhemphouse",
        "https://hempstone.net/catalyst-for-change/hempcrete-wall-system-the-hempshed",
        "https://hempcretewalls.com/info/",
        "https://natural-building-alliance.org/hempcrete/",
        "https://balancedarchitecture.com/hempcrete-homeowners-guide/",
        "https://www.hempbuildmag.com/home/3-hemp-houses",
        "https://www.lunchboxarchitect.com/featured/hempcrete-house-ecolibrium-designs-sustainable-country-home-sunshine-coast-queensland",
        "https://www.designsindetail.com/articles/what-is-hempcrete-everything-you-need-to-know",
        "https://hempco.net.au/different-methods-of-building-with-hempcrete/blog",
    ],
    "3d-concrete": [
        "https://builtin.com/articles/3d-printed-house",
        "https://www.architecturelab.net/3d-printed-houses-shaping-the-future-of-sustainable-living/",
        "https://foyr.com/learn/best-examples-of-3d-printed-houses-around-the-world",
        "https://parametric-architecture.com/top-10-pioneers-of-3d-printing-in-construction/",
        "https://parametric-architecture.com/3d-printed-homes-a-guide-to-time-cost-and-ownership/",
        "https://www.3dwasp.com/en/3d-printing-architecture/",
        "https://cobod.com/",
        "https://www.apis-cor.com/",
        "https://www.arch2o.com/3d-printed-house-apis-cor/",
        "https://3dprintingindustry.com/news/wasp-finishes-3d-printing-sustainable-biomaterial-based-tecla-eco-habitat-182940/",
        "https://www.greenbuildermedia.com/blog/step-by-step-manual-details-construction-of-hempcrete-structures",
        "https://dmv.realestate/3d-printed-homes-in-the-us/",
        "https://shuntool.com/article/how-to-build-hempcrete-concrete-house-step-by-step",
    ],
}

# ── SKIP PATTERNS (logos, icons, avatars, tracking pixels) ──
SKIP_PATTERNS = re.compile(
    r'(logo|favicon|icon|avatar|badge|sprite|pixel|tracking|banner-ad|advert|'
    r'widget|button|arrow|spinner|loading|placeholder|gravatar|wp-emoji|'
    r'data:image|\.gif$|\.svg$|/ads/|/ad-|doubleclick|googlesyndication)',
    re.IGNORECASE
)

# ── HELPERS ──────────────────────────────────────────────────
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

seen_hashes = set()


def safe_filename(url, idx):
    """Generate a filesystem-safe filename from a URL."""
    parsed = urlparse(url)
    base = os.path.basename(parsed.path)
    # Clean up the filename
    base = re.sub(r'[^\w.\-]', '_', base)
    if not base or len(base) < 5:
        base = f"img_{idx}.jpg"
    # Ensure it has an image extension
    if not re.search(r'\.(jpe?g|png|webp|bmp|tiff?)$', base, re.IGNORECASE):
        base += ".jpg"
    return base


def is_likely_photo(tag, src):
    """Heuristic: skip tiny UI elements, keep real photos."""
    if SKIP_PATTERNS.search(src):
        return False
    # Check width/height attributes
    w = tag.get('width', '')
    h = tag.get('height', '')
    try:
        if w and int(w) < MIN_WIDTH:
            return False
        if h and int(h) < 100:
            return False
    except (ValueError, TypeError):
        pass
    # Skip known tiny classes
    cls = ' '.join(tag.get('class', []))
    if any(x in cls.lower() for x in ['icon', 'logo', 'avatar', 'emoji']):
        return False
    return True


def download_image(url, folder, idx):
    """Download a single image if it meets size thresholds."""
    try:
        resp = session.get(url, timeout=TIMEOUT, stream=True)
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '')
        if 'image' not in content_type and 'octet-stream' not in content_type:
            return False

        data = resp.content
        if len(data) < MIN_BYTES or len(data) > MAX_BYTES:
            return False

        # Deduplicate by content hash
        h = hashlib.md5(data).hexdigest()
        if h in seen_hashes:
            return False
        seen_hashes.add(h)

        fname = safe_filename(url, idx)
        path = os.path.join(folder, fname)
        # Avoid overwrites
        if os.path.exists(path):
            name, ext = os.path.splitext(fname)
            path = os.path.join(folder, f"{name}_{h[:6]}{ext}")

        with open(path, 'wb') as f:
            f.write(data)
        return True

    except Exception as e:
        return False


def scrape_page(url, folder):
    """Fetch a page and download all qualifying images."""
    print(f"  Fetching: {url}")
    try:
        resp = session.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"    SKIP (fetch failed): {e}")
        return 0

    soup = BeautifulSoup(resp.text, 'html.parser')
    imgs = soup.find_all('img')
    count = 0

    for i, img in enumerate(imgs):
        # Try srcset first (often has higher-res version)
        src = None
        srcset = img.get('srcset', '')
        if srcset:
            # Pick the largest from srcset
            parts = [s.strip() for s in srcset.split(',') if s.strip()]
            best_w = 0
            for part in parts:
                tokens = part.split()
                if len(tokens) >= 2 and tokens[-1].endswith('w'):
                    try:
                        w = int(tokens[-1][:-1])
                        if w > best_w:
                            best_w = w
                            src = tokens[0]
                    except ValueError:
                        pass
            if not src and parts:
                src = parts[-1].split()[0]

        if not src:
            src = img.get('data-src') or img.get('data-lazy-src') or img.get('src', '')

        if not src or src.startswith('data:'):
            continue

        src = urljoin(url, src)

        if not is_likely_photo(img, src):
            continue

        if download_image(src, folder, i):
            count += 1
            print(f"    ✓ {os.path.basename(src)[:60]}")

    # Also check <a> tags linking directly to images (common in galleries)
    for a in soup.find_all('a', href=True):
        href = a['href']
        if re.search(r'\.(jpe?g|png|webp)(\?|$)', href, re.IGNORECASE):
            full_url = urljoin(url, href)
            if not SKIP_PATTERNS.search(full_url):
                if download_image(full_url, folder, count):
                    count += 1
                    print(f"    ✓ (linked) {os.path.basename(href)[:60]}")

    return count


# ── URL FILE LOADER ──────────────────────────────────────────
def load_urls_from_file(filepath):
    """Read URLs from a text file (one per line, # comments, blank lines ok)."""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            urls.append(line)
    return urls


# ── MAIN ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Earthback — Reference Image Scraper",
        epilog="Examples:\n"
               "  python scrape-reference-images.py\n"
               "  python scrape-reference-images.py my-urls.txt\n"
               "  python scrape-reference-images.py my-urls.txt --category earthships\n"
               "  python scrape-reference-images.py my-urls.txt -c cob-houses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('url_file', nargs='?', default=None,
                        help='Text file with URLs (one per line). If omitted, uses built-in list.')
    parser.add_argument('-c', '--category', default='custom',
                        help='Category/folder name for URLs from file (default: "custom")')
    parser.add_argument('--only-file', action='store_true',
                        help='Skip built-in URLs, only scrape from the URL file')
    args = parser.parse_args()

    # Build the sources dict
    sources = {}
    if not args.only_file:
        sources.update(SOURCES)

    if args.url_file:
        if not os.path.isfile(args.url_file):
            print(f"ERROR: File not found: {args.url_file}")
            sys.exit(1)
        file_urls = load_urls_from_file(args.url_file)
        if file_urls:
            cat = args.category
            if cat in sources:
                sources[cat] = sources[cat] + file_urls
            else:
                sources[cat] = file_urls
            print(f"Loaded {len(file_urls)} URLs from {args.url_file} → category '{cat}'")
        else:
            print(f"WARNING: No URLs found in {args.url_file}")

    if not sources:
        print("Nothing to scrape. Provide a URL file or remove --only-file.")
        sys.exit(0)

    print("=" * 60)
    print("Earthback — Reference Image Scraper")
    print("=" * 60)

    total = 0
    for category, urls in sources.items():
        folder = os.path.join(BASE_DIR, category)
        os.makedirs(folder, exist_ok=True)
        print(f"\n{'─' * 50}")
        print(f"Category: {category} ({len(urls)} sources)")
        print(f"Output:   {folder}")
        print(f"{'─' * 50}")

        cat_count = 0
        for url in urls:
            n = scrape_page(url, folder)
            cat_count += n
            time.sleep(DELAY)

        print(f"\n  → {cat_count} images saved for '{category}'")
        total += cat_count

    print(f"\n{'=' * 60}")
    print(f"DONE — {total} total images saved to {BASE_DIR}")
    print(f"{'=' * 60}")
    print("\nReview the folders and delete anything that's not useful.")
    print("Good candidates: construction process shots, finished exteriors,")
    print("wall textures, formwork, tools in action, close-ups of material.")


if __name__ == "__main__":
    main()
