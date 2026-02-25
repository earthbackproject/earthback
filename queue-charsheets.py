"""
Earthback — Character reference sheet generator
================================================
Generates wide triptych images (3 panels per image) to establish consistent
face identity per character before PuLID. One seed locks the face across all
three panels of a single image. Two seed sets per character (char_seed and
char_seed+7) give subtle variation while staying in the same face neighborhood.

Result: 12 chars × 3 sheets × 2 seeds = 72 images
Output: charsheet-NAME-A_00001_.png, charsheet-NAME-A_00002_.png, etc.

Usage:
  python queue-charsheets.py              # all characters, all sheets
  python queue-charsheets.py --char "James Osei"
  python queue-charsheets.py --sheet A    # Sheet A only
  python queue-charsheets.py --dry-run
  python queue-charsheets.py --status
"""

import json, random, time, argparse, urllib.request, urllib.error
from copy import deepcopy

COMFY_URL  = "http://127.0.0.1:8188"
STAGGER_MS = 150

# Wide landscape: 1536×640 — fits 3 portrait panels at ~512×640 each
# Stays close to 1MP (Flux's comfort zone)
WORKFLOW = {
    "6":  {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "8":  {"inputs": {"samples": ["31", 0], "vae": ["30", 2]},
           "class_type": "VAEDecode"},
    "9":  {"inputs": {"filename_prefix": "", "images": ["8", 0]},
           "class_type": "SaveImage"},
    "27": {"inputs": {"width": 1536, "height": 640, "batch_size": 1},
           "class_type": "EmptySD3LatentImage"},
    "30": {"inputs": {"ckpt_name": "flux1-dev-fp8.safetensors"},
           "class_type": "CheckpointLoaderSimple"},
    "31": {"inputs": {
               "seed": 0, "steps": 20, "cfg": 1,
               "sampler_name": "euler", "scheduler": "simple", "denoise": 1,
               "model": ["30", 0], "positive": ["35", 0],
               "negative": ["33", 0], "latent_image": ["27", 0],
           },
           "class_type": "KSampler"},
    "33": {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
}

# Condensed char list (desc only — no trigger/location needed for identity sheets)
CHARS = [
    {"name": "James Osei",
     "desc": "a 34-year-old Ghanaian man, lean build, slight stubble, "
             "warm dark brown skin, high cheekbones, strong jaw, close-cropped hair, deep-set dark brown eyes",
     "seed": 100001},
    {"name": "Lena Hartmann",
     "desc": "a 31-year-old German woman, reddish-brown shoulder-length hair, "
             "light freckled skin, blue-gray eyes, oval face, fine features, narrow nose",
     "seed": 200001},
    {"name": "Tom Westhall",
     "desc": "a 47-year-old white American man, deeply weathered tan face, "
             "salt-and-pepper close-cropped stubble, square jaw, blue eyes, crow's feet, broad forehead",
     "seed": 300001},
    {"name": "Rosa Mendez",
     "desc": "a 38-year-old Costa Rican woman, medium warm brown skin, "
             "dark hair pulled back tightly, dark brown eyes, full lips, round soft face",
     "seed": 400001},
    {"name": "Mei Lin",
     "desc": "a 29-year-old Filipino woman, short practical dark black hair, "
             "warm tan skin, dark almond-shaped eyes, round face, broad nose, wide cheekbones",
     "seed": 500001},
    {"name": "Elena Vasquez",
     "desc": "a 52-year-old Native American woman, Pueblo descent, deep copper-brown skin, "
             "strong angular face, very prominent cheekbones, dark brown eyes, silver-streaked black hair",
     "seed": 600001},
    {"name": "Amara Diallo",
     "desc": "a 41-year-old Senegalese man, very dark brown skin, broad face, "
             "strong heavy brow, close-cropped hair, prominent forehead, wide nose",
     "seed": 700001},
    {"name": "Marcus Webb",
     "desc": "a 61-year-old white American man, deeply lined weathered face, "
             "short gray hair, pale blue eyes, heavyset build, broad nose, prominent jaw, age spots",
     "seed": 800001},
    {"name": "Kenji Nakamura",
     "desc": "a 35-year-old Japanese man, dark brown eyes, straight black hair, "
             "clean-shaven, narrow oval face, wire-rimmed glasses, smooth skin",
     "seed": 900001},
    {"name": "Priya Sharma",
     "desc": "a 44-year-old Australian woman of South Indian descent, dark brown skin, "
             "black hair with early gray streaks, dark eyes, strong defined brow, oval face",
     "seed": 110001},
    {"name": "Dara Okonkwo",
     "desc": "a 33-year-old Black American woman, deep rich brown skin, natural hair, "
             "warm round face, bright expressive dark eyes, full lips, high cheekbones",
     "seed": 220001},
    {"name": "Sam Torres",
     "desc": "a 26-year-old Mexican-American man, warm tan skin, thick dark hair, "
             "dark brown eyes, square face, light stubble, broad shoulders, strong jaw",
     "seed": 330001},
    {"name": "Britta Svensson",
     "desc": "a 27-year-old Swedish woman, long straight pale golden blonde hair, "
             "very fair skin, clear blue eyes, angular Nordic face, tall and lean, clean-featured",
     "seed": 440001},
    {"name": "Sofia Marini",
     "desc": "a 31-year-old Italian woman, dark brown wavy medium-length hair, "
             "warm olive-tan skin, dark brown eyes, oval face, defined jaw, expressive dark brows",
     "seed": 550001},
    {"name": "Owen Marsh",
     "desc": "a 23-year-old white American man, short dark brown hair, light skin with freckles, "
             "lean build, hazel eyes, clean-shaven, sharp jaw, youthful face",
     "seed": 660001},
    {"name": "Callum Reed",
     "desc": "a 25-year-old white Welsh man, medium brown wavy hair, fair skin, "
             "blue-green eyes, slender build, light stubble, angular face, narrow jaw",
     "seed": 770001},
    {"name": "Joseph Runningwater",
     "desc": "a 67-year-old Coast Salish man, Lummi Nation, deep copper-brown heavily weathered skin, "
             "thick silver-white hair worn long, strong broad face, prominent cheekbones, "
             "dark deep-set eyes, heavy brow, heavyset commanding build",
     "seed": 880001},
    {"name": "Tariq Hassan",
     "desc": "a 29-year-old Yemeni man, warm medium-brown skin, short black hair, "
             "close-trimmed dark beard, angular lean face, deep dark eyes, tall and lean build",
     "seed": 990001},
    {"name": "Devon Clarke",
     "desc": "a 25-year-old Black American man, deep brown skin, close-cropped natural hair, "
             "wide bright expressive eyes, lean athletic build, clean-shaven, warm open face",
     "seed": 111001},
]

# ── Three triptych sheet types ─────────────────────────────────────────────────
# Each generates a single wide image with 3 portrait panels side by side.
# The single seed forces Flux to render the same face across all 3 panels.

SHEETS = {
    "A": {
        "label": "Sheet A — neutral angles (front / 3/4-left / 3/4-right)",
        "prompt": (
            "Photographic reference sheet, horizontal triptych. {desc}. "
            "Three documentary portraits of the same individual arranged side by side: "
            "left panel — straight-on neutral expression, facing directly toward camera, relaxed; "
            "center panel — three-quarter view, head turned slightly left, eyes still toward camera; "
            "right panel — three-quarter view, head turned slightly right, eyes toward camera. "
            "Same person consistently rendered in all three panels. "
            "Tight portrait crop in each panel, face fills most of each frame. "
            "Soft even natural daylight. 35mm documentary film, shallow depth of field."
        ),
    },
    "B": {
        "label": "Sheet B — expressions (thinking / speaking / warm)",
        "prompt": (
            "Photographic reference sheet, horizontal triptych. {desc}. "
            "Three documentary portraits of the same individual arranged side by side: "
            "left panel — looking slightly downward, brow gently furrowed in concentration or thought; "
            "center panel — mid-sentence, mouth slightly open, eyes alive and engaged, speaking to someone off-frame; "
            "right panel — warm genuine expression, slight relaxed smile, fully at ease. "
            "Same person consistently rendered in all three panels. "
            "Tight portrait crop in each panel, face fills most of each frame. "
            "Soft natural daylight. 35mm documentary film, shallow depth of field."
        ),
    },
    "C": {
        "label": "Sheet C — crop variations (eyes / face / shoulders)",
        "prompt": (
            "Photographic reference sheet, horizontal triptych. {desc}. "
            "Three documentary portraits of the same individual at different crop levels: "
            "left panel — very tight close-up, eyes and bridge of nose filling the frame, high detail; "
            "center panel — standard portrait crop, chin to crown, face centered and neutral; "
            "right panel — wider crop showing full face, neck, and upper chest and shoulders. "
            "Same person consistently rendered in all three panels. "
            "Even soft natural daylight across all panels. 35mm documentary film, shallow depth of field."
        ),
    },
}

# Two seed offsets — small delta stays in the same face neighborhood, avoids near-duplicates
SEED_SETS = [0, 7]


# ── API helpers ────────────────────────────────────────────────────────────────

def api_get(path):
    with urllib.request.urlopen(COMFY_URL + path, timeout=10) as r:
        return json.loads(r.read())

def api_post(path, data):
    payload = json.dumps(data).encode()
    req = urllib.request.Request(COMFY_URL + path, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def queue_depth():
    q = api_get("/queue")
    return len(q["queue_running"]), len(q["queue_pending"])

def send_job(text, prefix, seed, dry_run=False):
    if dry_run:
        print(f"    [DRY] prefix={prefix}  seed={seed}")
        print(f"          {text[:90]}...")
        return True
    p = deepcopy(WORKFLOW)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = prefix
    p["31"]["inputs"]["seed"]           = seed
    result = api_post("/prompt", {"prompt": p})
    return bool(result.get("prompt_id"))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue Earthback character reference sheets")
    parser.add_argument("--char",    default=None,
                        help="One character by name (e.g. 'James Osei')")
    parser.add_argument("--sheet",   default=None,
                        help="Which sheet(s): A, B, C or comma-separated (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print jobs without sending")
    parser.add_argument("--status",  action="store_true",
                        help="Show queue depth and exit")
    args = parser.parse_args()

    try:
        running, pending = queue_depth()
    except Exception as e:
        print(f"ERROR: Cannot reach ComfyUI at {COMFY_URL}\n  ({e})")
        return

    if args.status:
        print(f"ComfyUI queue — running: {running}  pending: {pending}")
        return

    print(f"ComfyUI connected — running: {running}  pending: {pending}\n")

    # Resolve characters
    chars = CHARS
    if args.char:
        chars = [c for c in CHARS if c["name"].lower() == args.char.lower()]
        if not chars:
            print(f"Character '{args.char}' not found.")
            print("Available:", ", ".join(c["name"] for c in CHARS))
            return

    # Resolve sheets
    if args.sheet:
        keys = [k.strip().upper() for k in args.sheet.split(",")]
        invalid = [k for k in keys if k not in SHEETS]
        if invalid:
            print(f"Unknown sheet(s): {invalid}. Use A, B, C.")
            return
        sheets = {k: SHEETS[k] for k in keys}
    else:
        sheets = SHEETS

    total, ok = 0, 0

    for sheet_key, sheet in sheets.items():
        print(f"\n  {sheet['label']}")
        for char in chars:
            for seed_offset in SEED_SETS:
                seed   = char["seed"] + seed_offset
                prefix = f"charsheet-{char['name']}-{sheet_key}"
                text   = sheet["prompt"].format(desc=char["desc"])
                success = send_job(text, prefix, seed=seed, dry_run=args.dry_run)
                status  = "✓" if success else "✗ FAILED"
                print(f"    {status}  {char['name']}  [Sheet {sheet_key}  seed={seed}]")
                if success:
                    ok += 1
                total += 1
                if not args.dry_run:
                    time.sleep(STAGGER_MS / 1000)

    tag = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{tag}Done — {ok}/{total} jobs queued")
    if not args.dry_run:
        running, pending = queue_depth()
        print(f"Queue now: running={running}  pending={pending}")


if __name__ == "__main__":
    main()
