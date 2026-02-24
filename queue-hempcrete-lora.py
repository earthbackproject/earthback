"""
Earthback — Hempcrete LoRA training image queuer
==================================================
Generates training images for a hempcrete (hemp-lime) LoRA.

IMPORTANT — WHY THIS SCRIPT EXISTS:
  Flux defaults to generating hempcrete as grey concrete slurry.
  This is completely wrong. Real hempcrete is:
    - Warm golden-honey / buff-tan / cream — NEVER grey
    - Chunky, crumbly, granular — like damp oatmeal — NEVER poured slurry
    - Visibly fibrous — individual golden-amber hemp shiv pieces throughout
    - Matte and porous — NEVER glossy or smooth like wet concrete
  Every prompt in this file fights that default with explicit color and
  texture descriptions.

Character: Nadia Benali (NADIA_BENALI_EB)
  43-year-old French-Moroccan woman, medium olive skin, dark brown eyes,
  short dark hair with early grey at the temples, compact build, strong forearms,
  lime-stained hands and forearms

Image groups:
  character  — Nadia working with hempcrete, 10 scenes
  material   — Material-only detail shots, 12 images (no people)
  process    — Full process documentation, 10 images (no people)
  cured      — Finished and cured hempcrete walls, 8 images (no people)

Usage:
  python queue-hempcrete-lora.py                     # all groups
  python queue-hempcrete-lora.py --group material    # one group
  python queue-hempcrete-lora.py --batch-size 3      # 3 per job
  python queue-hempcrete-lora.py --dry-run
  python queue-hempcrete-lora.py --status
"""

import json, random, time, argparse, urllib.request
from copy import deepcopy

# ── Config ─────────────────────────────────────────────────────────────────────
COMFY_URL  = "http://127.0.0.1:8188"
STAGGER_MS = 150

CHAR_TRIGGER = "NADIA_BENALI_EB"
CHAR_DESC    = ("43-year-old French-Moroccan woman, medium olive skin, dark brown eyes, "
                "short dark hair with early grey at the temples, compact build, strong forearms, "
                "lime-dusted hands and forearms")
CHAR_SEED    = 440001

WORKFLOW = {
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
               "model":        ["30", 0],
               "positive":     ["35", 0],
               "negative":     ["33", 0],
               "latent_image": ["27", 0],
           },
           "class_type": "KSampler"},
    "33": {"inputs": {
               "text": ("grey concrete, grey slurry, wet concrete, smooth liquid mix, "
                        "portland cement, industrial construction, bad quality, blurry"),
               "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
}

# ── Shared style constants ─────────────────────────────────────────────────────
# Repeated in every prompt to override Flux's concrete defaults.
HC_MATERIAL = (
    "hempcrete hemp-lime building material, warm golden-honey buff-tan color, "
    "NOT grey NOT concrete, visible golden-amber hemp shiv pieces throughout, "
    "chunky crumbly granular texture like damp oatmeal, "
    "lime binder coating each hemp piece, matte not glossy"
)

HC_CURED = (
    "cured hempcrete wall, warm honey-tan buff color NOT grey, "
    "visible hemp shiv fiber texture locked in pale lime matrix, "
    "porous matte surface, organic fibrous appearance"
)

HC_STYLE = "documentary photograph, natural light, shallow depth of field"
HC_STYLE_WIDE = "documentary photograph, natural light"

def p_char(scene, light="soft Dordogne afternoon light"):
    """Character scene prompt."""
    return (f"{CHAR_TRIGGER}, {CHAR_DESC}. "
            f"{scene} {light}. Photograph.")

def p_mat(scene, style=None):
    """Material-only prompt (no people)."""
    s = style or HC_STYLE
    return f"{s}, no people. {scene}"

# ── Image definitions ──────────────────────────────────────────────────────────

GROUPS = {

    # ── CHARACTER SCENES ───────────────────────────────────────────────────────
    # Nadia working — face and hands visible, hempcrete clearly shown

    "character": [

        ("hc-nadia-01-squeeze",
         p_char(
            "Holding a handful of freshly mixed hempcrete — warm golden-buff chunky mix, "
            "NOT grey slurry, crumbling apart between her fingers as she releases it, "
            "testing the consistency. White-cream lime dust on her forearms and shirt. "
            "Wooden formwork visible behind her."
         )),

        ("hc-nadia-02-tamping",
         p_char(
            "Using both hands to press and tamp a layer of warm golden hempcrete into wooden "
            "formwork, the buff-tan chunky mix compressing under her palms. "
            "The material is clearly granular and crumbly, NOT concrete. "
            "Lime dust on her forearms, sleeves rolled up."
         )),

        ("hc-nadia-03-mixer",
         p_char(
            "Watching golden-amber hempcrete tumble from a paddle mixer drum into a bucket — "
            "the mix visibly chunky and warm-toned, NOT grey slurry, "
            "individual hemp shiv pieces catching the light. "
            "Lime dust in the air, outdoor morning light."
         )),

        ("hc-nadia-04-shiv",
         p_char(
            "Picking up a handful of raw hemp shiv from a pile — "
            "loose golden-brown woody fiber pieces, light and airy, "
            "like dry animal bedding or coarse sawdust, visibly fibrous and warm-toned. "
            "Examining it close before mixing. Morning light."
         )),

        ("hc-nadia-05-bucket",
         p_char(
            "Carrying a full bucket of freshly mixed hempcrete — "
            "the top of the bucket showing warm buff-tan chunky material, "
            "visibly granular not liquid, hemp pieces visible in the mix. "
            "Moving purposefully across a job site. Outdoor light."
         )),

        ("hc-nadia-06-formwork",
         p_char(
            "Standing back and assessing a section of wooden formwork "
            "partially filled with hempcrete — the buff-golden chunky material "
            "visible between the timber boards, matte and textured. "
            "Late afternoon light, job site."
         )),

        ("hc-nadia-07-workshop",
         p_char(
            "Teaching — holding a small sample of cured hempcrete wall section "
            "in both hands, showing participants the warm honey-tan surface "
            "with visible hemp fiber texture. "
            "Workshop interior, even natural light."
         )),

        ("hc-nadia-08-strips",
         p_char(
            "Stripping wooden formwork from a freshly cured hempcrete wall — "
            "the board pulling away to reveal a warm honey-buff surface "
            "with textured hemp fiber impressions, NOT grey, NOT concrete. "
            "Afternoon light, Dordogne farmhouse."
         )),

        ("hc-nadia-09-plaster",
         p_char(
            "Applying a lime plaster finish coat over a cured hempcrete wall "
            "with a wide steel trowel — the cream-white plaster going over "
            "the warm buff hempcrete base. Compact focus, interior natural light."
         )),

        ("hc-nadia-10-notebook",
         p_char(
            "Crouching at the base of a freshly stripped hempcrete wall, "
            "making notes in a small notebook while running one finger "
            "along the warm honey-tan surface texture. "
            "Lime dust on her knees and forearms. Soft afternoon light."
         )),
    ],

    # ── MATERIAL DETAIL ────────────────────────────────────────────────────────
    # Close-up and mid-range shots of the material itself. No people.

    "material": [

        ("hc-mat-01-shiv-pile",
         p_mat(
            f"Close-up of a pile of raw hemp shiv — loose golden-amber woody fiber pieces, "
            f"10-20mm long, splintered and irregular, warm tan-gold color, "
            f"airy and lightweight-looking, resembling coarse dry animal bedding. "
            f"Raking sidelight, warm and clear. {HC_MATERIAL}"
         )),

        ("hc-mat-02-shiv-macro",
         p_mat(
            f"Extreme close-up macro of individual hemp shiv pieces — "
            f"golden-brown woody fragments showing fibrous internal structure, "
            f"splintered ragged edges, porous surface, warm amber and tan tones. "
            f"Raking natural light, very shallow depth of field. {HC_MATERIAL}"
         )),

        ("hc-mat-03-mix-fresh",
         p_mat(
            f"A fresh batch of hempcrete in a mixer drum or bucket — "
            f"warm golden-buff chunky crumbly mass, "
            f"individual golden hemp shiv pieces visible throughout a cream-tan lime binder, "
            f"damp but NOT wet, NOT grey, NOT slurry. "
            f"Like damp oatmeal with golden grain pieces. Outdoor natural light. {HC_MATERIAL}"
         )),

        ("hc-mat-04-squeeze-test",
         p_mat(
            f"A handful of hempcrete mix being squeezed and released — "
            f"the warm buff-tan crumbly mass breaking apart as fingers open, "
            f"hemp pieces visible, damp but holding loosely together, "
            f"NOT liquid, NOT grey, showing correct consistency. "
            f"Close crop, warm sidelight. {HC_MATERIAL}"
         )),

        ("hc-mat-05-lime-shiv",
         p_mat(
            f"Hemp shiv pieces next to a pile of white NHL lime powder — "
            f"golden-amber hemp shiv versus off-white chalky lime, "
            f"the two raw ingredients before mixing, "
            f"showing the warm tones of the final material's components. "
            f"Flat even light on a wooden surface. {HC_STYLE}"
         )),

        ("hc-mat-06-bales",
         p_mat(
            f"Hemp shiv bales in plastic wrapping on a job site — "
            f"golden-tan compressed hemp shiv visible through clear plastic, "
            f"rectangular bales stacked, lightweight-looking, warm agricultural appearance. "
            f"Outdoor morning light. {HC_STYLE_WIDE}"
         )),

        ("hc-mat-07-lime-bags",
         p_mat(
            f"Stacked white paper sacks of NHL natural hydraulic lime on a wooden pallet — "
            f"off-white cream colored bags, printed labels, "
            f"chalky lime dust around the base, "
            f"beside golden hemp shiv bales, job site setting. "
            f"Outdoor light. {HC_STYLE_WIDE}"
         )),

        ("hc-mat-08-mix-in-formwork",
         p_mat(
            f"Hempcrete freshly tamped inside open wooden formwork — "
            f"warm buff-golden chunky material between the timber boards, "
            f"matte and textured surface, individual hemp pieces visible, "
            f"NOT grey, NOT concrete, clearly granular and organic. "
            f"Outdoor light, construction site. {HC_MATERIAL}"
         )),

        ("hc-mat-09-layer",
         p_mat(
            f"A cross-section view of hempcrete layers inside formwork — "
            f"warm golden-tan material showing the distinct tamped layers, "
            f"individual hemp shiv pieces throughout the buff-cream lime matrix, "
            f"wooden shuttering on either side. Raking light. {HC_MATERIAL}"
         )),

        ("hc-mat-10-dust-air",
         p_mat(
            f"White-cream lime dust suspended in sunlight over a hempcrete mixing area — "
            f"the dust haze warm and soft, golden hemp shiv pieces scattered on the ground, "
            f"a bucket of buff-tan mixed hempcrete visible. "
            f"Outdoor morning light, dust catching in shafts of sun. {HC_STYLE_WIDE}"
         )),

        ("hc-mat-11-clothes",
         p_mat(
            f"Close-up of a builder's forearms and hands covered in "
            f"white-cream lime dust and warm tan hempcrete material — "
            f"the two colors distinct, lime white and hemp-lime buff, "
            f"knuckles stained, dried material on skin. "
            f"Natural outdoor light, no face. {HC_STYLE}"
         )),

        ("hc-mat-12-bucket",
         p_mat(
            f"A large plastic bucket filled with freshly mixed hempcrete — "
            f"the top surface showing warm golden-buff chunky granular material, "
            f"visibly crumbly not liquid, hemp pieces catching the light, "
            f"matte surface. Outdoor light, job site ground. {HC_MATERIAL}"
         )),
    ],

    # ── PROCESS ───────────────────────────────────────────────────────────────
    # Full process documentation without character.

    "process": [

        ("hc-proc-01-paddle-mixer",
         p_mat(
            f"A paddle mixer drum tumbling a batch of hempcrete — "
            f"warm golden-buff chunky mix visible inside the rotating drum, "
            f"NOT grey slurry, clearly granular and fibrous. "
            f"Electric motor, outdoor job site, morning light. {HC_MATERIAL}"
         )),

        ("hc-proc-02-cascade",
         p_mat(
            f"Hempcrete pouring from a mixer chute into a bucket — "
            f"the golden-tan chunky material cascading, NOT liquid, "
            f"individual hemp shiv pieces visible in the tumbling mass, "
            f"lime dust rising, warm buff color throughout. "
            f"Outdoor light, action shot. {HC_MATERIAL}"
         )),

        ("hc-proc-03-formwork-setup",
         p_mat(
            f"Wooden formwork set up against a timber frame wall structure — "
            f"plywood sheets and timber boards forming the void, "
            f"metal props bracing the sides, construction tape marking levels, "
            f"ready to receive hempcrete. Outdoor light. {HC_STYLE_WIDE}"
         )),

        ("hc-proc-04-tamping",
         p_mat(
            f"Hands tamping a layer of hempcrete into wooden formwork "
            f"from above — warm golden-buff chunky mix being pressed down, "
            f"the granular crumbly material consolidating under pressure, "
            f"hemp pieces visible, matte not glossy. "
            f"Top-down view, outdoor light. {HC_MATERIAL}"
         )),

        ("hc-proc-05-layer-depth",
         p_mat(
            f"Wooden depth markers and a rule measuring a hempcrete layer "
            f"inside formwork — the warm buff material packed to a consistent depth, "
            f"hemp texture visible at the surface, "
            f"ruler and marker stick showing 150mm layer. "
            f"Close crop, natural light. {HC_MATERIAL}"
         )),

        ("hc-proc-06-stripping",
         p_mat(
            f"Wooden formwork board being pulled away from newly cured hempcrete — "
            f"the board peeling off to reveal a warm honey-tan wall surface "
            f"with imprinted hemp fiber texture, "
            f"NOT grey, NOT concrete, clearly organic and warm. "
            f"Afternoon light, reveal moment. {HC_CURED}"
         )),

        ("hc-proc-07-curing",
         p_mat(
            f"A hempcrete wall section mid-cure with formwork partially removed — "
            f"the revealed section warm buff-golden with visible hemp texture, "
            f"the covered section still in timber shuttering beside it. "
            f"Outdoor light, Dordogne farmhouse. {HC_CURED}"
         )),

        ("hc-proc-08-scratch-coat",
         p_mat(
            f"A scratch coat of lime plaster being applied over a cured hempcrete wall — "
            f"the cream-white plaster going over warm tan hempcrete, "
            f"the hemp texture still partially visible where not yet covered, "
            f"a trowel mark in the plaster. "
            f"Interior natural light. {HC_STYLE}"
         )),

        ("hc-proc-09-workspace",
         p_mat(
            f"A hempcrete job site overview — wooden formwork rising against a stone building, "
            f"golden hemp shiv bales stacked, white lime sacks on pallets, "
            f"buckets of buff-tan mixed hempcrete around the base, "
            f"lime dust haze in the air. Warm morning light. {HC_STYLE_WIDE}"
         )),

        ("hc-proc-10-ground",
         p_mat(
            f"Hempcrete job site ground level — "
            f"spilled golden hemp shiv and warm buff hempcrete mix on the earth, "
            f"white lime dust settling on everything, "
            f"buckets, tools, wooden scraps, the organized mess of a working site. "
            f"Warm morning light. {HC_STYLE_WIDE}"
         )),
    ],

    # ── CURED WALLS ───────────────────────────────────────────────────────────
    # Finished hempcrete in various states.

    "cured": [

        ("hc-cured-01-raw-face",
         p_mat(
            f"A freshly stripped hempcrete wall face — "
            f"warm honey-tan golden color, NOT grey, "
            f"visible hemp shiv fiber pieces locked in the pale lime matrix, "
            f"porous matte texture, bumpy and organic, clearly not concrete. "
            f"Raking afternoon light showing the relief texture. {HC_CURED}"
         )),

        ("hc-cured-02-macro",
         p_mat(
            f"Extreme close-up of cured hempcrete surface — "
            f"golden-amber hemp shiv pieces visible in a pale cream-buff lime matrix, "
            f"porous open texture, fibrous and organic, matte not glossy, "
            f"warm honey tones, NOT grey, NOT concrete. "
            f"Macro lens, raking sidelight. {HC_CURED}"
         )),

        ("hc-cured-03-wall-interior",
         p_mat(
            f"Interior hempcrete wall in a finished room — "
            f"warm honey-buff color with visible hemp texture, "
            f"where the wall meets a timber window frame, "
            f"soft interior natural light showing the warmth of the material. "
            f"The wall glows warmly, organic and breathable-looking. {HC_CURED}"
         )),

        ("hc-cured-04-exterior",
         p_mat(
            f"Exterior hempcrete wall section on an old French farmhouse renovation — "
            f"warm buff-tan color, visible hemp fiber texture, "
            f"where new hempcrete meets old stone masonry, "
            f"afternoon sun on the wall face. NOT grey, NOT concrete. {HC_CURED}"
         )),

        ("hc-cured-05-corner",
         p_mat(
            f"A hempcrete wall corner, the hemp-lime material wrapping around "
            f"a timber structural post — warm honey-buff texture, "
            f"hemp fibers visible in the surface, "
            f"the organic texture contrasting with the smooth post. "
            f"Soft interior light. {HC_CURED}"
         )),

        ("hc-cured-06-stratigraphy",
         p_mat(
            f"A hempcrete wall cross-section where a section has been cut or broken — "
            f"showing the interior stratigraphy, "
            f"tamped layers visible, golden hemp shiv pieces throughout, "
            f"pale lime matrix, warm and airy-looking. "
            f"Even light, architectural documentation style. {HC_CURED}"
         )),

        ("hc-cured-07-rendered",
         p_mat(
            f"A hempcrete wall with a traditional lime render finish — "
            f"smooth cream-white exterior plaster over the buff hempcrete structure, "
            f"the warmth of the material visible where the render is thin, "
            f"an old French farmhouse exterior, afternoon sun. {HC_STYLE_WIDE}"
         )),

        ("hc-cured-08-window",
         p_mat(
            f"A deep hempcrete window reveal — "
            f"the wall thickness showing 400mm of warm honey-buff material, "
            f"hemp fiber texture on the splayed reveal sides, "
            f"warm afternoon light cutting into the deep opening. {HC_CURED}"
         )),
    ],
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

def build_prompt(text, prefix, seed, batch_size, width=896, height=1152):
    p = deepcopy(WORKFLOW)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = prefix
    p["27"]["inputs"]["width"]          = width
    p["27"]["inputs"]["height"]         = height
    p["27"]["inputs"]["batch_size"]     = batch_size
    p["31"]["inputs"]["seed"]           = seed
    return p

def send_job(text, prefix, seed, batch_size=1, dry_run=False):
    if dry_run:
        print(f"    [DRY] {prefix}  seed={seed}  bs={batch_size}")
        print(f"          {text[:100]}...")
        return True
    prompt = build_prompt(text, prefix, seed, batch_size)
    result = api_post("/prompt", {"prompt": prompt})
    return bool(result.get("prompt_id"))

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue hempcrete LoRA training images")
    parser.add_argument("--group",      default=None,
                        help=f"Image group: {', '.join(GROUPS.keys())}. Omit for all.")
    parser.add_argument("--loops",      type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Images per job. 3 recommended for curation.")
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--status",     action="store_true")
    args = parser.parse_args()

    try:
        running, pending = queue_depth()
    except Exception as e:
        print(f"ERROR: Cannot reach ComfyUI at {COMFY_URL} ({e})")
        return

    if args.status:
        print(f"ComfyUI queue — running: {running}  pending: {pending}")
        return

    print(f"ComfyUI connected — running: {running}  pending: {pending}\n")
    print("Hempcrete LoRA — prompts are written to override Flux's grey-slurry default.")
    print("All images target: warm golden-honey buff, chunky crumbly, visible hemp fiber.\n")

    groups_to_run = GROUPS
    if args.group:
        if args.group not in GROUPS:
            print(f"Unknown group '{args.group}'. Options: {', '.join(GROUPS.keys())}")
            return
        groups_to_run = {args.group: GROUPS[args.group]}

    total = ok = 0

    for loop in range(args.loops):
        if args.loops > 1:
            print(f"=== Loop {loop + 1} of {args.loops} ===")

        for group_name, images in groups_to_run.items():
            print(f"\n  Group: {group_name}  ({len(images)} images)")

            for i, (prefix, prompt_text) in enumerate(images):
                # Character group uses char seed base; others use material seed base
                if group_name == "character":
                    seed = CHAR_SEED + (i * 10) + (loop * 200)
                else:
                    seed = 550000 + (i * 37) + (abs(hash(group_name)) % 10000) + (loop * 500)

                success = send_job(
                    prompt_text, prefix, seed,
                    batch_size=args.batch_size,
                    dry_run=args.dry_run,
                )
                status_str = "✓" if success else "✗ FAILED"
                print(f"    {status_str}  {prefix}")
                if success: ok += 1
                total += 1
                if not args.dry_run:
                    time.sleep(STAGGER_MS / 1000)

    tag = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{tag}Done — {ok}/{total} jobs queued")
    if not args.dry_run:
        running, pending = queue_depth()
        print(f"Queue now: running={running}  pending={pending}")
        n_images = ok * args.batch_size
        print(f"Generating approximately {n_images} images total.")
        print(f"\nOutput files prefix:  hc-[group]-[NN]-[slug]_NNNNN_.png")
        print(f"Add all to:           lora-training/datasets/hempcrete/images/")

if __name__ == "__main__":
    main()
