"""
Earthback — PuLID face batch queuer
=====================================
Generates face-angle variants for each character using a reference face image.
The reference image locks the face identity; PuLID applies it across all angles.

SETUP REQUIRED FIRST:
  1. Install ComfyUI-PuLID-Flux via Manager → Custom Nodes
  2. python setup-pulid.py          (downloads model files)
  3. Restart ComfyUI
  4. Pick one best face image per character from comfyui-output,
     rename them as:  faces-reference/[CharName].png
     e.g.  faces-reference/Rosa Mendez.png
           faces-reference/Elena Vasquez.png
           etc.

Usage:
  python queue-pulid-faces.py --dry-run        # preview jobs, don't send
  python queue-pulid-faces.py                  # queue all characters
  python queue-pulid-faces.py --char "Rosa Mendez"
  python queue-pulid-faces.py --loops 3        # 3 variants per angle
  python queue-pulid-faces.py --strength 0.9   # face strength (0.0-1.0, default 0.85)
  python queue-pulid-faces.py --status         # queue depth and exit

Reference images live in:
  Earthback/faces-reference/[CharName].png

Output prefix:  T4-chars-[Name]-pulid-[angle]
  → T4-chars-Rosa Mendez-pulid-front_00001_.png, etc.
"""

import json
import random
import time
import argparse
import urllib.request
import urllib.error
import os
from copy import deepcopy
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
COMFY_URL        = "http://127.0.0.1:8188"
STAGGER_MS       = 200
REFERENCE_DIR    = Path(__file__).parent / "faces-reference"

# Node IDs in the PuLID workflow — different from the base workflow.
# These are the node IDs from the ComfyUI-PuLID-Flux example workflow.
# If you get errors, open the workflow in ComfyUI and check node IDs.
#
# Workflow structure:
#   30  = CheckpointLoaderSimple (Flux model)
#   31  = KSampler
#   27  = EmptySD3LatentImage (resolution)
#   6   = CLIPTextEncode (positive)
#   33  = CLIPTextEncode (negative)
#   35  = FluxGuidance
#   8   = VAEDecode
#   9   = SaveImage
#   40  = LoadImage (reference face)
#   41  = PulidModelLoader
#   42  = ApplyPulid (the face injection node)
#   43  = InsightFaceLoader

WORKFLOW_PULID = {
    "6":  {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "8":  {"inputs": {"samples": ["31", 0], "vae": ["30", 2]},
           "class_type": "VAEDecode"},
    "9":  {"inputs": {"filename_prefix": "", "images": ["8", 0]},
           "class_type": "SaveImage"},
    "27": {"inputs": {"width": 896, "height": 1152, "batch_size": 1},
           "class_type": "EmptySD3LatentImage"},
    "30": {"inputs": {"ckpt_name": "flux1-dev-fp8.safetensors"},
           "class_type": "CheckpointLoaderSimple"},
    "31": {"inputs": {
               "seed": 0, "steps": 20, "cfg": 1,
               "sampler_name": "euler", "scheduler": "simple",
               "denoise": 1,
               "model":        ["42", 0],   # model comes FROM ApplyPulid now
               "positive":     ["35", 0],
               "negative":     ["33", 0],
               "latent_image": ["27", 0],
           },
           "class_type": "KSampler"},
    "33": {"inputs": {"text": "bad quality, blurry, deformed face, ugly", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
    # PuLID-specific nodes:
    "40": {"inputs": {"image": "", "upload": "image"},
           "class_type": "LoadImage"},
    "41": {"inputs": {"pulid_file": "pulid_flux_v0.9.1.safetensors"},
           "class_type": "PulidModelLoader"},
    "42": {"inputs": {
               "weight":       0.85,   # face strength, filled per job
               "start_at":     0.0,
               "end_at":       1.0,
               "model":        ["30", 0],
               "pulid":        ["41", 0],
               "eva_clip":     ["41", 1],
               "face_analysis": ["43", 0],
               "image":        ["40", 0],
           },
           "class_type": "ApplyPulid"},
    "43": {"inputs": {"provider": "CPU"},
           "class_type": "InsightFaceLoader"},
}

# ── Character data ─────────────────────────────────────────────────────────────
# Same as queue-batches.py but face-specific prompts tuned for PuLID.
# PuLID handles identity; prompts just need to describe angle and lighting.

CHARS = [
    {"name": "James Osei",    "trigger": "JAMES_OSEI_EB",
     "desc": "a 34-year-old Ghanaian man, lean build, slight stubble, "
             "warm dark brown skin, high cheekbones, strong jaw, close-cropped hair, deep-set dark brown eyes",
     "seed": 100001},
    {"name": "Lena Hartmann", "trigger": "LENA_HARTMANN_EB",
     "desc": "a 31-year-old German woman, reddish-brown shoulder-length hair, "
             "light freckled skin, blue-gray eyes, oval face, fine features, narrow nose",
     "seed": 200001},
    {"name": "Tom Westhall",  "trigger": "TOM_WESTHALL_EB",
     "desc": "a 47-year-old white American man, deeply weathered tan face, "
             "salt-and-pepper close-cropped stubble, square jaw, blue eyes, crow's feet wrinkles, broad forehead",
     "seed": 300001},
    {"name": "Rosa Mendez",   "trigger": "ROSA_MENDEZ_EB",
     "desc": "a 38-year-old Costa Rican woman, medium warm brown skin, "
             "dark hair pulled back tightly, dark brown eyes, full lips, round soft face, slight cheek fullness",
     "seed": 400001},
    {"name": "Mei Lin",       "trigger": "MEI_LIN_EB",
     "desc": "a 29-year-old Filipino woman, short practical dark black hair, "
             "warm tan skin, dark almond-shaped eyes, round face, broad nose, wide cheekbones",
     "seed": 500001},
    {"name": "Elena Vasquez", "trigger": "ELENA_VASQUEZ_EB",
     "desc": "a 52-year-old Native American woman, Pueblo descent, "
             "deep copper-brown skin, strong angular face, very prominent cheekbones, "
             "dark brown eyes, silver-streaked black hair, strong nose",
     "seed": 600001},
    {"name": "Amara Diallo",  "trigger": "AMARA_DIALLO_EB",
     "desc": "a 41-year-old Senegalese West African man, master builder, "
             "very dark brown skin, broad face, strong heavy brow, close-cropped hair, prominent forehead, wide nose",
     "seed": 700001},
    {"name": "Marcus Webb",   "trigger": "MARCUS_WEBB_EB",
     "desc": "a 61-year-old white American man, deeply lined weathered face, "
             "short gray hair, pale blue eyes, heavyset build, broad nose, prominent jaw, age spots",
     "seed": 800001},
    {"name": "Kenji Nakamura","trigger": "KENJI_NAKAMURA_EB",
     "desc": "a 35-year-old Japanese man, researcher, slim build, "
             "dark brown eyes, straight black hair, clean-shaven, narrow oval face, wire-rimmed glasses, smooth skin",
     "seed": 900001},
    {"name": "Priya Sharma",  "trigger": "PRIYA_SHARMA_EB",
     "desc": "a 44-year-old Australian woman of South Indian descent, "
             "dark brown skin, black hair with early gray streaks, dark eyes, strong defined brow, oval face",
     "seed": 110001},
    {"name": "Dara Okonkwo",  "trigger": "DARA_OKONKWO_EB",
     "desc": "a 33-year-old Black American woman, deep rich brown skin, "
             "natural hair, warm round face, bright expressive dark eyes, full lips, high cheekbones",
     "seed": 220001},
    {"name": "Sam Torres",    "trigger": "SAM_TORRES_EB",
     "desc": "a 26-year-old Mexican-American man, warm tan skin, "
             "thick dark hair, dark brown eyes, square face, light stubble, broad shoulders, strong jaw",
     "seed": 330001},
]

# ── Face angle prompts ─────────────────────────────────────────────────────────
# PuLID handles WHO; prompts just steer angle, lighting, expression.
# Keep trigger word in so LoRA training captions still align.

FACE_ANGLES = [
    ("face-front",
     "Documentary photograph, 35mm film. {trigger}, {desc}. "
     "Straight-on face portrait, looking directly into camera, neutral relaxed expression. "
     "Tight crop from collarbones up, face fills the frame. Soft even frontal daylight."),

    ("face-left",
     "Documentary photograph, 35mm film. {trigger}, {desc}. "
     "Three-quarter portrait, head turned slightly left, eyes toward camera. "
     "Tight crop, face fills the frame. Soft sidelight from the left, gentle shadow on right cheek."),

    ("face-right",
     "Documentary photograph, 35mm film. {trigger}, {desc}. "
     "Three-quarter portrait, head turned slightly right, eyes toward camera. "
     "Tight crop, face fills the frame. Soft sidelight from the right, gentle shadow on left cheek."),

    ("face-down",
     "Documentary photograph, 35mm film. {trigger}, {desc}. "
     "Close portrait, head tilted slightly down, eyes looking downward as if reading or thinking, "
     "brow slightly furrowed in concentration. Tight crop. Soft overhead daylight."),

    ("face-talk",
     "Documentary photograph, 35mm film. {trigger}, {desc}. "
     "Close candid portrait, mid-sentence, mouth slightly open, eyes alive and engaged. "
     "Natural animated expression. Tight crop from collarbones up. Soft natural daylight."),
]

FACE_ANGLE_SEED_OFFSET = {
    "face-front": 0,
    "face-left":  1,
    "face-right": 2,
    "face-down":  3,
    "face-talk":  4,
}

# ── API helpers ─────────────────────────────────────────────────────────────────

def api_get(path):
    url = COMFY_URL + path
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())

def api_post(path, data):
    url     = COMFY_URL + path
    payload = json.dumps(data).encode()
    req     = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def queue_depth():
    q = api_get("/queue")
    return len(q["queue_running"]), len(q["queue_pending"])

def upload_image(image_path: Path) -> str:
    """Upload a reference image to ComfyUI and return its server filename."""
    url = COMFY_URL + "/upload/image"
    with open(image_path, "rb") as f:
        data = f.read()
    boundary = "----FormBoundary" + str(random.randint(100000, 999999))
    body  = f"--{boundary}\r\n"
    body += f'Content-Disposition: form-data; name="image"; filename="{image_path.name}"\r\n'
    body += "Content-Type: image/png\r\n\r\n"
    body  = body.encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body,
                                  headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    return result["name"]   # server-side filename ComfyUI will use

def build_prompt(text, prefix, ref_image_name, weight, seed):
    p = deepcopy(WORKFLOW_PULID)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = prefix
    p["31"]["inputs"]["seed"]           = seed
    p["40"]["inputs"]["image"]          = ref_image_name
    p["42"]["inputs"]["weight"]         = weight
    return p

def send_job(text, prefix, ref_image_name, weight, seed, dry_run=False):
    if dry_run:
        print(f"    [DRY] prefix={prefix}  seed={seed}  weight={weight}")
        print(f"          ref={ref_image_name}")
        print(f"          prompt={text[:90]}...")
        return True
    prompt = build_prompt(text, prefix, ref_image_name, weight, seed)
    result = api_post("/prompt", {"prompt": prompt})
    return bool(result.get("prompt_id"))

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue PuLID face batches for Earthback characters")
    parser.add_argument("--char",     default=None,
                        help="Only queue one character by name (e.g. 'Rosa Mendez')")
    parser.add_argument("--loops",    type=int, default=1,
                        help="Variants per angle per character (default 1)")
    parser.add_argument("--strength", type=float, default=0.85,
                        help="PuLID face strength 0.0-1.0 (default 0.85). "
                             "Higher = more faithful to reference, less prompt flexibility. "
                             "Try 0.75-0.90 range.")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Print jobs without sending")
    parser.add_argument("--status",   action="store_true",
                        help="Show queue depth and exit")
    parser.add_argument("--ref-dir",  default=str(REFERENCE_DIR),
                        help="Folder containing reference face images (one per character)")
    args = parser.parse_args()

    ref_dir = Path(args.ref_dir)

    # Status check
    try:
        running, pending = queue_depth()
    except Exception as e:
        print(f"ERROR: Cannot reach ComfyUI at {COMFY_URL}")
        print(f"  Make sure ComfyUI is running. ({e})")
        return

    if args.status:
        print(f"ComfyUI queue — running: {running}  pending: {pending}")
        return

    print(f"ComfyUI connected — running: {running}  pending: {pending}")
    print(f"PuLID strength: {args.strength}  |  loops: {args.loops}")
    print()

    # Resolve characters
    chars_to_run = CHARS
    if args.char:
        chars_to_run = [c for c in CHARS if c["name"].lower() == args.char.lower()]
        if not chars_to_run:
            print(f"Character '{args.char}' not found.")
            print("Available:", ", ".join(c["name"] for c in CHARS))
            return

    # Check reference images exist
    missing = []
    for char in chars_to_run:
        ref_path = ref_dir / f"{char['name']}.png"
        if not ref_path.exists():
            # also try jpg
            ref_jpg = ref_dir / f"{char['name']}.jpg"
            if not ref_jpg.exists():
                missing.append(char["name"])

    if missing:
        print(f"⚠  Missing reference images for:")
        for name in missing:
            print(f"     {ref_dir / name}.png")
        print()
        print("Pick the best face image from comfyui-output for each character,")
        print("copy it to faces-reference/ and rename it to [CharName].png")
        if not args.dry_run:
            remaining = [c for c in chars_to_run if c["name"] not in missing]
            if remaining:
                ans = input(f"Continue with the {len(remaining)} characters that DO have references? (y/n): ").strip().lower()
                if ans != "y":
                    return
                chars_to_run = remaining
            else:
                return

    # Upload reference images (skip in dry-run)
    ref_map = {}   # char name → server filename
    if not args.dry_run:
        print("Uploading reference images to ComfyUI...")
        for char in chars_to_run:
            ref_path = ref_dir / f"{char['name']}.png"
            if not ref_path.exists():
                ref_path = ref_dir / f"{char['name']}.jpg"
            print(f"  Uploading: {ref_path.name} ...", end=" ", flush=True)
            server_name = upload_image(ref_path)
            ref_map[char["name"]] = server_name
            print(f"✓  ({server_name})")
        print()

    # Queue jobs
    total = 0
    ok    = 0

    for loop in range(args.loops):
        if args.loops > 1:
            print(f"=== Loop {loop + 1} of {args.loops} ===")

        for char in chars_to_run:
            ref_image_name = ref_map.get(char["name"], f"{char['name']}.png")
            print(f"\n  Character: {char['name']}")

            for angle_key, prompt_tmpl in FACE_ANGLES:
                text   = prompt_tmpl.format(trigger=char["trigger"], desc=char["desc"])
                prefix = f"T4-chars-{char['name']}-pulid-{angle_key.replace('face-','')}"
                angle_offset = FACE_ANGLE_SEED_OFFSET[angle_key]
                seed   = char["seed"] + angle_offset + (loop * 100)

                success = send_job(
                    text, prefix,
                    ref_image_name=ref_image_name,
                    weight=args.strength,
                    seed=seed,
                    dry_run=args.dry_run,
                )
                status_str = "✓" if success else "✗ FAILED"
                print(f"    {status_str}  {angle_key}")
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
        print()
        print("Output files will be named:  T4-chars-[Name]-pulid-[angle]_NNNNN_.png")
        print("Add them to lora-training/datasets/[char]/images/ for training.")


if __name__ == "__main__":
    main()
