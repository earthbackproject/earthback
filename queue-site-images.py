"""
Earthback — Site image generator (no browser required)
======================================================
Generates all non-character visual assets for the Earthback platform.
Sends jobs directly to the ComfyUI API. ComfyUI must be running.

Output lands in: C:\\users\\adrxi\\Earthback\\comfyui-output\\site\\
(copy to site/assets/img/ when happy with results)

Usage:
  python queue-site-images.py                     # queue everything
  python queue-site-images.py --group circles     # circle card images only
  python queue-site-images.py --group posts       # post feed images only
  python queue-site-images.py --group hero        # hero + og images only
  python queue-site-images.py --group textures    # material macro shots
  python queue-site-images.py --group game        # game concept art
  python queue-site-images.py --dry-run           # preview without sending
  python queue-site-images.py --status            # show queue depth
  python queue-site-images.py --loops 3           # generate 3 variants each

Resolution guide (all divisible by 64):
  hero:     1536 × 640  (2.4:1 wide landscape)
  og:       1232 × 640  (≈1.93:1 social card)
  circle:   1344 × 768  (1.75:1 card banner)
  post:     1024 × 768  (4:3 feed thumbnail)
  texture:   896 × 896  (1:1 macro detail)
  game:     1536 × 640  (wide cinematic)
"""

import json
import random
import time
import argparse
import urllib.request
from copy import deepcopy

COMFY_URL   = "http://127.0.0.1:8188"
STAGGER_MS  = 200
OUTPUT_PFX  = "site"   # all site images prefix with "site-"

# Style anchors
STYLE_DOC   = "Documentary photograph, 35mm film, natural light only, no people visible."
STYLE_MACRO = "35mm macro photograph, natural light, sharp focus on texture and material detail."
STYLE_WIDE  = "Cinematic wide photograph, documentary style, 35mm film, golden hour."
STYLE_GAME  = "Photorealistic wide shot, cinematic documentary style, no text, no HUD, hyper-real."

# Palette note (included in relevant prompts)
PALETTE     = "Color palette: deep forest green, clay gold, warm parchment, muted earth tones. No neon, no oversaturation."

# ── Workflow skeleton (from live ComfyUI instance) ────────────────────────────
BASE_WORKFLOW = {
    "6":  {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "8":  {"inputs": {"samples": ["31", 0], "vae": ["30", 2]},
           "class_type": "VAEDecode"},
    "9":  {"inputs": {"filename_prefix": "", "images": ["8", 0]},
           "class_type": "SaveImage"},
    "27": {"inputs": {"width": 1024, "height": 768, "batch_size": 1},
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
               "latent_image": ["27", 0]
           },
           "class_type": "KSampler"},
    "33": {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
}

# ── Site image definitions ────────────────────────────────────────────────────
# Each entry: (slug, width, height, prompt)
# slug becomes the filename_prefix → site-[slug]_00001_.png

SITE_IMAGES = {

    # ── HERO / LANDING ────────────────────────────────────────────────────────
    "hero": [
        (
            "hero-home-01",
            1536, 640,
            f"{STYLE_WIDE} A newly completed hempcrete home at golden hour, "
            "standing seam metal roof with solar panels flush to the surface, "
            "earthen walls warm in the late light, set in a semi-arid transitional landscape — "
            "could be American Southwest, West Africa, or Mediterranean (geographically ambiguous). "
            "Community members visible as small figures outside, showing human scale. "
            "The home is beautiful, clean-lined, rooted in its landscape. "
            "No text overlays. Wide 16:9 cinematic crop. "
            f"{PALETTE}"
        ),
        (
            "hero-home-02",
            1536, 640,
            f"{STYLE_WIDE} Late afternoon light on a hempcrete and bamboo structure under construction "
            "in a tropical landscape — Osa Peninsula Costa Rica or similar. "
            "The building is half-done: one wall solid and finished, another just timber formwork. "
            "Tools and materials visible. Two anonymous small figures working at distance. "
            "Humid green foliage behind. Golden directional light. No faces visible. "
            "Wide cinematic crop, hopeful energy. "
            f"{PALETTE}"
        ),
        (
            "hero-community-01",
            1536, 640,
            f"{STYLE_WIDE} Overhead or wide view of multiple anonymous pairs of hands around a "
            "rough wooden table — different skin tones, hempcrete block in the center, "
            "tools, notebooks, material samples at edges of frame. Flat-lay documentary. "
            "Natural diffuse light. No faces. About work and knowledge sharing. "
            "Wide crop. Earth tones, warm. "
            f"{PALETTE}"
        ),
        (
            "og-social-card",
            1232, 640,
            f"{STYLE_DOC} Wide establishing shot: a hempcrete home with solar panels "
            "on standing seam metal roof, warm golden hour light, "
            "semi-arid landscape — could be Oregon, West Africa, or Morocco. "
            "Clean, simple, no clutter. One or two anonymous small figures at distance. "
            "Space in the sky for text overlay at top. "
            "Deep greens, clay gold, warm parchment walls. Cinematic, real, not stock. "
            f"{PALETTE}"
        ),
    ],

    # ── CIRCLE CARD IMAGES ────────────────────────────────────────────────────
    # Used as card header/background on explore.html
    # Format: 1344×768 wide card, cropped to card aspect in CSS
    "circles": [
        (
            "circle-natural-building",
            1344, 768,
            f"{STYLE_DOC} Close-up of hempcrete being packed into timber formwork by strong hands, "
            "late afternoon directional light raking across the wall surface, "
            "texture of hemp hurd and lime binder clearly visible, warm golden tones. "
            "No face visible — hands and material are the subject. "
            "Wide banner crop. Earth tones, tactile. "
            f"{PALETTE}"
        ),
        (
            "circle-solar-offgrid",
            1344, 768,
            f"{STYLE_DOC} Row of solar panels mounted on a standing seam metal roof, "
            "clip-mounted with zero roof penetrations, "
            "bright clear blue sky behind, Queensland or desert Southwest US. "
            "The seam and clip detail visible in foreground, panels receding to horizon. "
            "No people. Wide banner. Clean, precise, powerful. "
            f"{PALETTE}"
        ),
        (
            "circle-water-systems",
            1344, 768,
            f"{STYLE_DOC} Large rainwater collection cistern beside a hempcrete home, "
            "pipe running from roof gutter to tank, "
            "green vegetation beside the tank benefiting from overflow, "
            "dry landscape behind — American Southwest or West Africa. "
            "Late afternoon light. No people. Wide banner. "
            "Earthy, practical, essential. "
            f"{PALETTE}"
        ),
        (
            "circle-permaculture-food",
            1344, 768,
            f"{STYLE_DOC} Dense food forest garden — multiple canopy layers visible, "
            "fruit trees above, berry bushes mid-layer, ground cover below, "
            "morning light filtering through the canopy in long rays. "
            "Lush, productive, intentional. Temperate climate, Pacific Northwest or UK. "
            "No people. Wide banner. Green and gold. "
            f"{PALETTE}"
        ),
        (
            "circle-mutual-aid",
            1344, 768,
            f"{STYLE_DOC} Anonymous hands passing tools and materials between people — "
            "a stack of salvaged lumber being lifted, or a crate of seeds being handed across. "
            "Outdoor community gathering, overcast natural light. "
            "Multiple skin tones visible. No faces. The act of giving and receiving. "
            "Wide banner. Warm tones. "
            f"{PALETTE}"
        ),
        (
            "circle-community-housing",
            1344, 768,
            f"{STYLE_DOC} Small cluster of three hempcrete homes arranged around a shared courtyard, "
            "late afternoon golden hour light, solar panels on each roof, "
            "a shared garden space in the center with raised beds and a simple bench. "
            "No people visible. Aerial or elevated wide shot. "
            "Shows community at human scale. Warm earthy palette. "
            f"{PALETTE}"
        ),
        (
            "circle-skills-workshops",
            1344, 768,
            f"{STYLE_DOC} A tool wall inside a workshop — hand tools hung neatly on a pegboard, "
            "levels, chisels, hand saws, trowels, a hammer, a soil testing kit. "
            "Morning light from a high window casting long shadows. "
            "Background: workbench with a project underway. No people. "
            "Wide banner. Ochre and grey tones. Honest and practical. "
            f"{PALETTE}"
        ),
        (
            "circle-land-soil",
            1344, 768,
            f"{STYLE_DOC} Close-up of two anonymous hands holding rich dark living soil, "
            "fingers slightly parted letting it fall, visible earthworms, "
            "a planted field in soft focus behind. Morning or overcast light. "
            "The soil is the subject — alive and dense. Wide banner. "
            "Deep brown, moss green. "
            f"{PALETTE}"
        ),
        (
            "circle-alternative-dwellings",
            1344, 768,
            f"{STYLE_DOC} A hand-built off-grid cabin in a forest clearing, "
            "small and precise — timber frame or straw bale, metal roof, "
            "wood smoke coming from a small chimney, late afternoon forest light. "
            "No people. The cabin is lived-in and real. "
            "Wide banner, slightly elevated angle. Green and gold. "
            f"{PALETTE}"
        ),
        (
            "circle-materials-salvage",
            1344, 768,
            f"{STYLE_DOC} A salvage yard or deconstruction site — "
            "stacks of old-growth reclaimed fir beams, vintage brick pallets, "
            "salvaged window frames leaning against a wall, "
            "afternoon light raking across the textures. "
            "No people. Documentary. The materials are beautiful and worth saving. "
            "Wide banner. Warm timber tones, weathered grey. "
            f"{PALETTE}"
        ),
        (
            "circle-community-energy",
            1344, 768,
            f"{STYLE_DOC} A neighborhood microgrid installation — "
            "three or four rooftops in a row, each with solar panels, "
            "visible conduit and meter connections between them at street level. "
            "Overcast sky, urban or semi-urban US neighborhood. "
            "No people. Wide banner. Shows shared infrastructure, not individual. "
            "Muted blues, greens, grey. "
            f"{PALETTE}"
        ),
        (
            "circle-community-tech",
            1344, 768,
            f"{STYLE_DOC} A LoRa mesh network antenna mounted on a rooftop — "
            "small solar-powered, simple fabricated enclosure, "
            "overlooking a neighborhood below, overcast Pacific Northwest or urban sky. "
            "No people. Wide banner. Shows appropriate tech at human scale. "
            "Grey, green, minimal. "
            f"{PALETTE}"
        ),
    ],

    # ── POST FEED IMAGES ──────────────────────────────────────────────────────
    # Drop-in replacements for assets/img/posts/ — 1024×768 (4:3)
    "posts": [
        (
            "post-hempcrete-mix",
            1024, 768,
            f"{STYLE_DOC} Close-up of hempcrete being mixed in a large drum or trough — "
            "visible hemp hurd fibers, lime binder, water combining. "
            "A wooden paddle mid-stir, afternoon workshop light. "
            "The texture is rough, organic, and warm golden-grey. "
            "No face. Hands only at edge of frame. "
            f"{PALETTE}"
        ),
        (
            "post-utah-hemp-wall",
            1024, 768,
            f"{STYLE_DOC} A finished hempcrete wall, exterior view, "
            "lime-rendered surface with slight texture variation, "
            "warm afternoon light raking across the surface revealing the organic texture. "
            "Standing seam metal roof line visible at top. High desert landscape behind. "
            "Beautiful, solid, real. No people. "
            f"{PALETTE}"
        ),
        (
            "post-food-forest",
            1024, 768,
            f"{STYLE_DOC} A food forest garden in peak summer abundance — "
            "multiple layers: a pear tree loaded with fruit above, "
            "currant bushes and comfrey mid-layer, "
            "ground cover of strawberries and clover below. "
            "Morning light, dew still on the leaves. Temperate climate. "
            "No people. Lush, complex, alive. "
            f"{PALETTE}"
        ),
        (
            "post-greywater-system",
            1024, 768,
            f"{STYLE_DOC} A residential greywater recycling system — "
            "pipes running from a sink or shower drain through a constructed wetland "
            "planted with cattails and irises in a raised gravel bed, "
            "beside a hempcrete home exterior. "
            "Afternoon light. No people. Elegant and functional. "
            f"{PALETTE}"
        ),
        (
            "post-lora-mesh",
            1024, 768,
            f"{STYLE_DOC} A LoRa community radio node — "
            "small weatherproof enclosure mounted on a wood post, "
            "simple yagi antenna pointing skyward, "
            "solar panel on a bracket beside it, "
            "rural or peri-urban landscape behind. Overcast morning light. "
            "No people. Modest scale, serious purpose. "
            f"{PALETTE}"
        ),
        (
            "post-salvage-fir",
            1024, 768,
            f"{STYLE_DOC} A stack of reclaimed old-growth fir beams "
            "in a salvage yard or workshop, "
            "deep red-brown grain visible on fresh cut ends, "
            "original nail holes and weathered surfaces on faces, "
            "afternoon light catching the grain. "
            "No people. The wood is the subject — old, beautiful, worth saving. "
            f"{PALETTE}"
        ),
        (
            "post-solar-coop",
            1024, 768,
            f"{STYLE_DOC} Four or five adjacent rooftops in a neighborhood, "
            "each with solar panels, conduit running between meters at ground level, "
            "a small handwritten sign visible on a fence: 'Community Solar Co-op'. "
            "Overcast morning light. No faces. Wide enough to show the shared nature. "
            f"{PALETTE}"
        ),
        (
            "post-tiny-cabin",
            1024, 768,
            f"{STYLE_DOC} A small hand-built off-grid cabin in a clearing — "
            "timber frame or straw bale construction, metal standing seam roof, "
            "a small porch with a single chair, wood pile stacked neatly beside. "
            "Late afternoon forest light, golden and directional. "
            "No people. Lived-in, precise, intentional. "
            f"{PALETTE}"
        ),
    ],

    # ── MATERIAL TEXTURES (for section backgrounds, dividers) ─────────────────
    # Square macro shots — can be used as CSS background textures
    "textures": [
        (
            "texture-hempcrete-surface",
            896, 896,
            f"{STYLE_MACRO} Extreme close-up of a finished hempcrete wall surface, "
            "lime render with slight organic variation, "
            "hemp hurd fragments just visible beneath the surface, "
            "late afternoon raking light revealing texture. "
            "No people. Fill the frame entirely with wall. Warm ochre-grey. "
            f"{PALETTE}"
        ),
        (
            "texture-rammed-earth",
            896, 896,
            f"{STYLE_MACRO} Close-up of a rammed earth wall showing the compressed "
            "layer lines — red clay, sand, and aggregate banding, "
            "each layer slightly different in color and mineral content. "
            "Strong directional sidelight. Fill the frame. "
            "Red, ochre, cream bands. Geological and beautiful. "
            f"{PALETTE}"
        ),
        (
            "texture-bamboo-culm",
            896, 896,
            f"{STYLE_MACRO} Cross-section view of cut bamboo culms, "
            "circular forms and hollow centers visible, "
            "natural nodes visible on culm surfaces, "
            "morning light in a workshop. Fill the frame. "
            "Golden green and warm tan tones. Organic geometry. "
            f"{PALETTE}"
        ),
        (
            "texture-hemp-fiber",
            896, 896,
            f"{STYLE_MACRO} Raw hemp bast fiber close-up — "
            "long parallel strands, slightly golden, "
            "loose and fibrous, caught in late afternoon light. "
            "Fill the frame entirely. No context — pure material. "
            "Warm gold and cream. "
            f"{PALETTE}"
        ),
        (
            "texture-cob-wall",
            896, 896,
            f"{STYLE_MACRO} Close-up of an exterior cob wall surface — "
            "hand-built, showing finger marks and straw fiber in the earth mix, "
            "natural plaster skin with minor cracks typical of earthen walls. "
            "Morning sidelight. Fill the frame. "
            "Warm ochre, brown, straw gold. "
            f"{PALETTE}"
        ),
        (
            "texture-standing-seam",
            896, 896,
            f"{STYLE_MACRO} Close-up of standing seam metal roofing — "
            "the parallel raised seams receding, Corten or galvalume finish, "
            "a clip-mounted solar rail visible crossing perpendicular to the seams. "
            "Overcast diffuse light, no harsh shadows. "
            "Fill the frame. Grey, silver, industrial-natural. "
            f"{PALETTE}"
        ),
    ],

    # ── GAME CONCEPT ART ──────────────────────────────────────────────────────
    "game": [
        (
            "game-world-overview",
            1536, 640,
            f"{STYLE_GAME} Post-collapse landscape at golden hour — "
            "an overgrown highway visible in the middle distance, reclaimed by vegetation. "
            "In the foreground: a small but solid hempcrete community, "
            "solar panels on standing seam roofs, hemp fields at the edge. "
            "The contrast: collapse behind, rebuilding in front. "
            "Cinematic wide shot, anamorphic quality. Warm, honest, hopeful. "
            "No text or HUD elements. No faces visible. "
            f"{PALETTE}"
        ),
        (
            "game-container-classroom",
            1536, 640,
            f"{STYLE_GAME} A large shipping container repurposed as a mobile fabrication "
            "and training unit, deployed in a West African landscape — "
            "red earth, sparse acacia trees, open sky. "
            "Sides open, revealing tools, material samples, a small 3D printer inside. "
            "A group of anonymous small figures gathered outside. "
            "Late afternoon light, dust in the air. "
            "Real-feeling, not fantasy. Wide cinematic. "
            f"{PALETTE}"
        ),
        (
            "game-structure-build",
            1536, 640,
            f"{STYLE_GAME} A partially completed hempcrete structure being built "
            "in a post-collapse world — rough terrain, improvised scaffolding, "
            "one wall complete and solid, another just timber formwork. "
            "Anonymous small figures working at distance. "
            "Golden hour, cinematic wide. The vibe: this matters, people are invested. "
            "No text. Hyper-real. "
            f"{PALETTE}"
        ),
        (
            "game-player-horizon",
            1536, 640,
            f"{STYLE_GAME} A lone figure standing at the edge of a clearing, "
            "back to camera, looking toward a half-built community in the distance — "
            "hempcrete walls, bamboo structures, solar panels, small fires. "
            "Sunset behind the community, silhouette of figure in foreground. "
            "The figure is the player: no defined face or ethnicity, "
            "carrying tools and a materials pack. "
            "Wide cinematic. Hope as a visual. "
            f"{PALETTE}"
        ),
        (
            "game-night-community",
            1536, 640,
            f"{STYLE_GAME} A small hempcrete community at night — "
            "warm interior lights glowing through windows, "
            "solar-charged LED string lights on a shared courtyard, "
            "a communal fire with anonymous gathered figures at distance, "
            "stars visible above. "
            "The contrast: the dark world outside, warmth within. "
            "Cinematic, hopeful, specific. No faces. "
            f"{PALETTE}"
        ),
    ],
}

# All groups
ALL_GROUPS = list(SITE_IMAGES.keys())

# ── API helpers ────────────────────────────────────────────────────────────────

def api_get(path):
    with urllib.request.urlopen(COMFY_URL + path, timeout=10) as r:
        return json.loads(r.read())

def api_post(path, data):
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        COMFY_URL + path, data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def queue_depth():
    q = api_get("/queue")
    return len(q["queue_running"]), len(q["queue_pending"])

def build_prompt(text, prefix, width, height):
    p = deepcopy(BASE_WORKFLOW)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = f"site-{prefix}"
    p["27"]["inputs"]["width"]          = width
    p["27"]["inputs"]["height"]         = height
    p["31"]["inputs"]["seed"]           = random.randint(0, 9_999_999_999)
    return p

def send_job(text, prefix, width, height, dry_run=False):
    if dry_run:
        print(f"    [DRY] site-{prefix}  {width}×{height}")
        print(f"          {text[:90]}...")
        return True
    prompt = build_prompt(text, prefix, width, height)
    result = api_post("/prompt", {"prompt": prompt})
    return bool(result.get("prompt_id"))

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue Earthback site images")
    parser.add_argument("--group",   default=None,
                        help=f"Image group(s) to queue, comma-separated. "
                             f"Options: {', '.join(ALL_GROUPS)}. "
                             f"Omit to queue all.")
    parser.add_argument("--loops",   type=int, default=1,
                        help="Variants per image (default 1). "
                             "Each loop stacks _00002_, _00003_... for curation.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status",  action="store_true")
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

    # Resolve groups
    if args.group is None:
        groups = ALL_GROUPS
    else:
        requested = [g.strip().lower() for g in args.group.split(",")]
        groups = [g for g in ALL_GROUPS if g in requested]
        if not groups:
            print(f"Unknown group(s): {args.group}. Options: {', '.join(ALL_GROUPS)}")
            return

    total = ok = 0

    for loop in range(args.loops):
        if args.loops > 1:
            print(f"=== Variant {loop + 1} of {args.loops} ===")

        for group in groups:
            images = SITE_IMAGES[group]
            print(f"\n  Group: {group} ({len(images)} images)")

            for (slug, w, h, prompt) in images:
                success = send_job(prompt, slug, w, h, dry_run=args.dry_run)
                status  = "✓" if success else "✗ FAILED"
                print(f"    {status}  site-{slug}  [{w}×{h}]")
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
        print(f"\nImages land in: C:\\users\\adrxi\\Earthback\\comfyui-output\\")
        print(f"Filenames:      site-[slug]_00001_.png")
        print(f"Copy keepers to: site/assets/img/ and rename to match HTML references")

if __name__ == "__main__":
    main()
