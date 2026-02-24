"""
Earthback — Site asset batch generator
=======================================
Queues atmospheric, environmental, and thematic images for site use.
No specific characters — places, materials, work, community, ecology.
All images use documentary/photojournalism style matching the character imagery.

~80 prompts × batch_size=2 = ~160 images overnight.

Usage:
  python queue-site-assets.py                      # queue all
  python queue-site-assets.py --batch hempcrete    # one theme
  python queue-site-assets.py --batch texture,food # multiple themes
  python queue-site-assets.py --list               # show all batch keys
  python queue-site-assets.py --dry-run
  python queue-site-assets.py --status
  python queue-site-assets.py --batch-size 3       # 3 images per job
"""

import json, random, time, argparse, urllib.request, urllib.error
from copy import deepcopy

COMFY_URL  = "http://127.0.0.1:8188"
STAGGER_MS = 150

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

# Wide landscape variant for establishing/hero shots
WORKFLOW_WIDE = deepcopy(WORKFLOW)
WORKFLOW_WIDE["27"]["inputs"]["width"]  = 1344
WORKFLOW_WIDE["27"]["inputs"]["height"] = 896

STYLE = "Documentary photograph, 35mm film, natural light. "

# ── Asset batches ───────────────────────────────────────────────────────────────
# Format: batch_key → {"label": str, "wide": bool, "prompts": [str, ...]}
# wide=True uses landscape dimensions (1344×896) — good for hero/banner images

ASSET_BATCHES = {

    # ── Establishing / Hero ───────────────────────────────────────────────────
    "establishing": {
        "label": "Wide establishing shots — green building sites",
        "wide": True,
        "prompts": [
            STYLE + "Wide view of a natural building work party — a dozen people working together on rising earthen walls, scaffolding, barrels of hempcrete mix, bright morning light on a rural site.",
            STYLE + "Aerial perspective of a small permaculture homestead — food forest, garden beds, rainwater tanks, solar panels, earthen outbuilding. Lush green, overcast soft light.",
            STYLE + "Community work day on a straw bale house — volunteers packing bales into a timber frame, a finished wall section visible, golden afternoon light.",
            STYLE + "Wide shot of an off-grid community in a desert landscape — adobe buildings, solar panels, garden, dry creek bed. Long morning shadows, clear sky.",
            STYLE + "A small cluster of earthen homes at the edge of a field — different colors of lime plaster, low profile, integrated with the landscape. Soft overcast daylight.",
            STYLE + "Rural timber frame raising — six people lifting a heavy beam into position with ropes, sawdust in the air. Pacific Northwest forest backdrop, overcast light.",
        ],
    },

    # ── Hempcrete ─────────────────────────────────────────────────────────────
    "hempcrete": {
        "label": "Hempcrete — construction, material, process",
        "wide": False,
        "prompts": [
            STYLE + "Close-up of a barrel mixer turning hempcrete — hemp hurd, lime, and water tumbling together, dusty pale mix. Outdoor afternoon light.",
            STYLE + "Hands pressing freshly mixed hempcrete into timber formwork, packing it tightly around a post. Cross-section of layers visible. Soft daylight.",
            STYLE + "A newly stripped hempcrete wall — pale gray-green surface, slightly rough texture, timber uprights visible at intervals. Diffuse natural light.",
            STYLE + "Cross-section of a hempcrete block showing internal texture — hemp hurds suspended in lime matrix, air pockets, layered compression. Close-up.",
            STYLE + "A hempcrete building under construction — timber frame standing, formwork panels attached to one bay, hempcrete being tamped from above. Wide shot, afternoon sun.",
            STYLE + "Dry hemp hurd piled on a tarp beside bags of hydraulic lime — raw materials before mixing. Outdoor morning light, slight dew on the hemp.",
        ],
    },

    # ── Adobe & Earthen ───────────────────────────────────────────────────────
    "earthen": {
        "label": "Adobe, cob, rammed earth — construction and material",
        "wide": False,
        "prompts": [
            STYLE + "Long rows of adobe bricks drying in the sun on flat ground — hundreds of pale tan bricks in neat rows, long afternoon shadows, desert landscape.",
            STYLE + "Rammed earth formwork — wooden panels clamped to a rising wall, a tamper rod visible, distinct horizontal strata of compressed earth in different tones.",
            STYLE + "A finished rammed earth wall face — beautiful horizontal layers of ochre, rust, and cream, compressed and smooth. Close-up, even daylight.",
            STYLE + "Cob being trodden on a tarp — straw twisted deep into red clay mud underfoot, bare feet visible. Overcast daylight, outdoor scene.",
            STYLE + "Applying clay slip to an exterior cob wall — both hands flat, pressing a thin coat smooth, surface glistening. Afternoon light, drying wall behind.",
            STYLE + "Earthen floor being poured — dark clay-sand mix leveled with a straight edge across a room, wet surface catching window light. Interior, soft daylight.",
            STYLE + "Adobe wall corner detail — mud mortar joints, slightly uneven brick faces, weathered plaster at the base. Close-up, raking sidelight.",
        ],
    },

    # ── Straw Bale ────────────────────────────────────────────────────────────
    "strawbale": {
        "label": "Straw bale — bales, construction, finish",
        "wide": False,
        "prompts": [
            STYLE + "Stack of golden straw bales beside a building site — tight rectangular bales, straw ends catching the light, blue sky behind.",
            STYLE + "Straw bale end cross-section close-up — dense golden straw compressed into a tight rectangle, cut clean. Sidelight picks up the texture.",
            STYLE + "Interior of a straw bale wall section during construction — bales stacked between timber posts, string ties visible, unplastered. Soft interior light.",
            STYLE + "Applying lime plaster to a straw bale wall exterior — a wide float pressing cream-colored plaster into the straw surface. Outdoor afternoon sun.",
        ],
    },

    # ── Timber Frame & Wood ───────────────────────────────────────────────────
    "timber": {
        "label": "Timber frame — joinery, raising, wood detail",
        "wide": False,
        "prompts": [
            STYLE + "Mortise and tenon joint close-up — hand-cut oak, tight fit, wooden peg driven through. Sidelight showing tool marks and grain.",
            STYLE + "A timber frame structure mid-raising — bent frames standing, knee braces pinned, sky visible through the open frame. Morning light.",
            STYLE + "Salvaged old-growth fir beam end showing growth rings — decades of rings visible, rough-hewn surface, warm brown. Close-up.",
            STYLE + "Hand-planing a beam — wood shaving curling up, grain revealed beneath, sawdust on the floor. Workshop interior, window light.",
        ],
    },

    # ── Solar & Energy ────────────────────────────────────────────────────────
    "solar": {
        "label": "Solar, wind, off-grid energy systems",
        "wide": False,
        "prompts": [
            STYLE + "Solar panel array on the roof of a community building — rows of dark panels catching afternoon sun, surrounding green landscape.",
            STYLE + "Off-grid battery bank and inverter — wall of deep-cycle batteries, cables, a charge controller with blinking lights. Utility room, fluorescent light.",
            STYLE + "Single solar panel on a small cabin roof — simple 200W panel, wire running down the side, pine trees behind. Morning sun.",
            STYLE + "Community solar garden — a field of solar panels on a cooperative property, gravel paths between rows, overcast sky.",
            STYLE + "A wind turbine on a small tower at a rural homestead — spinning blades, guy wires, an outbuilding and garden below. Wide sky, afternoon.",
            STYLE + "Off-grid kitchen powered by solar — a simple counter with a 12V fan, LED light strip, a small solar charge controller mounted on the wall. Interior.",
        ],
    },

    # ── Water Systems ─────────────────────────────────────────────────────────
    "water": {
        "label": "Water systems — greywater, rainwater, streams",
        "wide": False,
        "prompts": [
            STYLE + "Rainwater catchment — large corrugated metal cistern beside an earthen building, downspout from the roof, first-flush diverter. Soft cloudy light.",
            STYLE + "Greywater mulch basin — a planted bed receiving water from a pipe, lush plants thriving around it. Afternoon light, casual garden setting.",
            STYLE + "Constructed wetland water treatment — shallow cells with cattails and bulrushes, water flowing between them, sky reflected. Natural light.",
            STYLE + "Swale system on a hillside — long level earthworks following the contour, overflow spillways, new plantings on the berm. Aerial-ish perspective, soft light.",
            STYLE + "Hand pump at a shallow well — simple iron pump, concrete pad, a bucket and rope beside it. Rural, late afternoon light.",
            STYLE + "Stream restoration work — a cleared bank with newly planted native sedges and willows, rocks placed for deflection, clear water moving. Overcast.",
        ],
    },

    # ── Food Systems ──────────────────────────────────────────────────────────
    "food": {
        "label": "Food systems — forest gardens, harvests, community food",
        "wide": False,
        "prompts": [
            STYLE + "A food forest in summer — layered canopy of fruit trees, berries, herbs, and groundcover. Dappled light, lush and wild but intentional.",
            STYLE + "Market garden in morning light — long rows of mixed vegetables, irrigation lines, a barn in the background. Low sun, long shadows, dew.",
            STYLE + "Seed saving — dozens of seed varieties spread on paper to dry, labeled in handwriting. Close-up, table in natural light.",
            STYLE + "Community kitchen in action — a large pot on a wood stove, people working around a long table, jars of preserved food on shelves. Interior warm light.",
            STYLE + "Earthen wood-fired bread oven — domed cob oven with fire glowing inside, bread loaves on a wooden peel, outdoor setting. Evening light.",
            STYLE + "Community orchard in spring — rows of young fruit trees in bloom, white flowers, green grass, a distant house. Soft overcast light.",
            STYLE + "Fermentation shelf — rows of mason jars with fermenting vegetables, cloth lids, labels, bubbling. Pantry interior, window light.",
            STYLE + "Community fridge on a sidewalk — painted free-standing fridge open, fresh vegetables inside, neighborhood street. Overcast day.",
        ],
    },

    # ── Community & Mutual Aid ────────────────────────────────────────────────
    "community": {
        "label": "Community gatherings, mutual aid, skill sharing",
        "wide": False,
        "prompts": [
            STYLE + "Community gathering in a circle outdoors — people of different ages sitting on benches and ground, listening, afternoon shade.",
            STYLE + "Tool library interior — pegboard wall with hand tools hanging in outlines, shelves of labeled tool bins, a check-out counter. Interior.",
            STYLE + "Repair cafe — a long table with people fixing things — a sewing machine, a lamp, electronics — alongside tools and parts. Community center, interior.",
            STYLE + "Skill-share workshop — someone demonstrating technique to a small group watching closely. Hands on materials, absorbed attention. Natural light.",
            STYLE + "Community meal outdoors — long tables end to end, people sharing food, plates passed, conversation. Late afternoon sun, dappled shade.",
            STYLE + "Work party on a community project — a mix of ages and backgrounds working together, laughing, midday, outdoor construction site.",
            STYLE + "Cooperative workspace interior — shared tools, workbenches, people at different projects. Natural light through large windows.",
            STYLE + "Community bulletin board — hand-lettered flyers, event posters, skill-trade cards, resource listings pinned densely. Close-up.",
        ],
    },

    # ── Land & Ecology ────────────────────────────────────────────────────────
    "ecology": {
        "label": "Ecology — rewilding, native plants, restoration",
        "wide": False,
        "prompts": [
            STYLE + "Native plant restoration planting — rows of small native plants in a cleared area, volunteers with buckets and spades. Overcast morning light.",
            STYLE + "Rewilded field edge — a fence line where managed land meets wildflower meadow, grasses, insects, blurred background. Afternoon light.",
            STYLE + "Community forest — tall mixed trees, a narrow footpath, dappled light through the canopy. Lush, quiet, no people.",
            STYLE + "Biochar production — an open-air kiln smoking, charcoal being quenched with water, black char pile beside it. Outdoor afternoon.",
            STYLE + "Composting system — three-bay wooden compost bins at different stages, garden fork resting on one, a wheelbarrow alongside. Morning.",
            STYLE + "Living roof on a small outbuilding — a thick mat of sedums and grasses in bloom, dragonfly, blue sky. Low angle looking up.",
            STYLE + "Mycelium inoculated logs stacked in a shaded area — white mycelium threading through end grain, dark and damp environment.",
        ],
    },

    # ── Alternative Shelter ───────────────────────────────────────────────────
    "shelter": {
        "label": "Shelter — tiny homes, earthships, mobile, alternative",
        "wide": False,
        "prompts": [
            STYLE + "A small earthen home in a high desert landscape — thick adobe walls, vigas protruding, a portal, garden, blue sky. Morning light.",
            STYLE + "Earthship under construction — tire walls being rammed with a sledgehammer, rebar grid, bottles in the wall face. Desert afternoon.",
            STYLE + "Tiny home in a forested setting — simple clad structure on a trailer, small porch, raised garden beds. Soft Pacific Northwest light.",
            STYLE + "Interior of a small cob home — curved walls, plastered in cream, a wood stove, earthen floor, low window with plants. Warm interior light.",
            STYLE + "Converted school bus as a mobile home — painted bus in a field, small solar panel on the roof, a simple awning extended, morning light.",
            STYLE + "Yurt in a meadow — round white yurt, door open, a solar panel and water barrel beside it, mountains behind. Clear afternoon.",
        ],
    },

    # ── Material Textures (site backgrounds) ──────────────────────────────────
    "texture": {
        "label": "Material textures — close-ups for site backgrounds",
        "wide": False,
        "prompts": [
            STYLE + "Hempcrete wall surface close-up — rough pale texture, hemp fibers visible, small air pockets. Even raking sidelight, abstract.",
            STYLE + "Rammed earth wall face detail — horizontal strata in ochre, rust, and cream. Very close, fills frame, no sky or context.",
            STYLE + "Natural lime plaster — slightly undulating surface, soft off-white, trowel marks barely visible. Diffuse sidelight.",
            STYLE + "Straw bale end — compressed golden straw tightly packed, dense and regular. Close-up, sidelight picking up individual stems.",
            STYLE + "Raw hemp hurd fiber — loose tan-colored woody fiber pieces, close-up macro, fine texture. Soft overhead light.",
            STYLE + "Adobe mud consistency — wet clay being pressed between fingers, showing plasticity and color. Close-up of hands, outdoor light.",
            STYLE + "Hand-hewn timber grain — rough surface of an old beam, tool marks, growth rings, warm brown. Close-up, raking sidelight.",
            STYLE + "Dry-laid stone foundation — flat fieldstones stacked without mortar, lichen patches, moss in joints. Close-up, soft daylight.",
        ],
    },

    # ── Hands at Work ─────────────────────────────────────────────────────────
    "hands": {
        "label": "Hands at work — non-character close-ups",
        "wide": False,
        "prompts": [
            STYLE + "Two hands pressing clay daub into a wattle panel, fingers spreading it even. Outdoor morning light, soil-stained hands.",
            STYLE + "Hands threading bamboo splits between upright poles — deliberate and tight. Warm tropical light from the side.",
            STYLE + "One hand tracing a crack in an adobe wall, fingertip in the gap. Bright noon sun, long shadow.",
            STYLE + "Hands on a wooden tamper handle — mid-downstroke into a foundation trench, motion blur on impact. Afternoon light, dust rising.",
            STYLE + "Hands wrapping electrical wire around a battery terminal in an off-grid system — careful, close work. Utility light, interior.",
            STYLE + "Hands holding a freshly pulled soil auger core — dark layered soil visible in the cylinder. Outdoor midday light.",
            STYLE + "Hands spreading seeds onto a paper tray to dry — a variety of shapes and colors. Indoor window light.",
        ],
    },

    # ── Bioregional Landscapes ────────────────────────────────────────────────
    "landscape": {
        "label": "Bioregional landscapes — Southwest, PNW, Appalachia, etc.",
        "wide": True,
        "prompts": [
            STYLE + "High desert landscape — red rock mesas, sparse juniper, a small earthen building in the distance. Morning light, long shadows.",
            STYLE + "Pacific Northwest homestead — Douglas fir forest edge, a cleared garden, overcast soft light, green and wet.",
            STYLE + "Appalachian farm — rolling hardwood ridges, a stone barn, fields in the valley, late afternoon sun.",
            STYLE + "Great Plains land trust — flat horizon, native prairie grass, a wind turbine and solar array in the distance. Wide sky.",
            STYLE + "Tropical community land — lush green, banana and mango trees, an earthen building with a thatched overhang. Humid midday light.",
            STYLE + "West African village setting — wide laterite road, low earthen buildings, neem trees for shade, afternoon light and dust.",
        ],
    },

    # ── Tech & Fabrication ────────────────────────────────────────────────────
    "fabrication": {
        "label": "Fabrication — digital tools, community workshop",
        "wide": False,
        "prompts": [
            STYLE + "Community workshop interior — CNC router mid-cut, sawdust in the air, sheets of plywood stacked beside it. Industrial light.",
            STYLE + "A 3D printer printing a small architectural component — nozzle depositing filament on a model in progress, warm light from the side.",
            STYLE + "Open-source hardware project on a workbench — circuit board, wires, a multimeter, handwritten notes. Workshop lighting.",
            STYLE + "Laser cutter etching wood — bright line of light on a wooden panel, faint smoke, protective glass. Dark workshop, dramatic light.",
        ],
    },

    # ── Mycology & Soil ───────────────────────────────────────────────────────
    "mycology": {
        "label": "Mycology, soil, and decomposition",
        "wide": False,
        "prompts": [
            STYLE + "Oyster mushrooms fruiting from a straw log in a shaded greenhouse — clusters of pale fan-shaped mushrooms. Cool diffuse light.",
            STYLE + "Soil food web close-up — a handful of dark rich compost with earthworms, white mycelium threads, plant roots. Macro, natural light.",
            STYLE + "Biochar amendment — dark black biochar mixed into garden soil, hands crumbling it in. Outdoor light, healthy dark earth.",
            STYLE + "Worm farm open bin — red wigglers in dark castings, shredded paper bedding, a mist of moisture. Interior, natural light.",
        ],
    },

    # ── Community Housing & Co-ops ────────────────────────────────────────────
    "cohousing": {
        "label": "Community housing, land trusts, co-ops",
        "wide": True,
        "prompts": [
            STYLE + "Cohousing cluster from above — 8-12 small homes around a shared courtyard, communal garden, common house. Soft overcast light.",
            STYLE + "Land trust property sign at a farm entrance — handmade wood sign, overgrown with vines, gravel driveway. Morning light.",
            STYLE + "Cooperative grocery storefront — hand-painted sign, open door, produce bins visible outside, neighborhood street. Overcast day.",
            STYLE + "Community land trust meeting — people around a table with maps and documents, a whiteboard, natural light through windows.",
        ],
    },

}


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

def build_prompt(text, prefix, seed, batch_size, wide=False):
    import copy
    base = WORKFLOW_WIDE if wide else WORKFLOW
    p = copy.deepcopy(base)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = prefix
    p["27"]["inputs"]["batch_size"]     = batch_size
    p["31"]["inputs"]["seed"]           = seed
    return p

def send_job(text, prefix, seed, batch_size=1, wide=False, dry_run=False):
    if dry_run:
        dims = "1344×896" if wide else "896×1152"
        print(f"    [DRY] prefix={prefix}  seed={seed}  {dims}  batch_size={batch_size}")
        print(f"          {text[:90]}...")
        return True
    p = build_prompt(text, prefix, seed, batch_size, wide=wide)
    result = api_post("/prompt", {"prompt": p})
    return bool(result.get("prompt_id"))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue Earthback site asset images")
    parser.add_argument("--batch",      default=None,
                        help="Theme(s) to queue, comma-separated. Use --list to see all.")
    parser.add_argument("--list",       action="store_true",
                        help="List all available batch keys and exit")
    parser.add_argument("--batch-size", type=int, default=2,
                        help="Images per job (default 2)")
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--status",     action="store_true")
    args = parser.parse_args()

    if args.list:
        print("Available asset batches:")
        for key, b in ASSET_BATCHES.items():
            print(f"  {key:<16} — {b['label']}  ({len(b['prompts'])} prompts)")
        return

    try:
        running, pending = queue_depth()
    except Exception as e:
        print(f"ERROR: Cannot reach ComfyUI at {COMFY_URL}\n  ({e})")
        return

    if args.status:
        print(f"ComfyUI queue — running: {running}  pending: {pending}")
        return

    print(f"ComfyUI connected — running: {running}  pending: {pending}\n")

    # Resolve batches
    if args.batch:
        keys = [k.strip().lower() for k in args.batch.split(",")]
        invalid = [k for k in keys if k not in ASSET_BATCHES]
        if invalid:
            print(f"Unknown batch(es): {invalid}")
            print("Use --list to see all available keys.")
            return
        batches = {k: ASSET_BATCHES[k] for k in keys}
    else:
        batches = ASSET_BATCHES

    total, ok = 0, 0

    for batch_key, batch in batches.items():
        wide = batch.get("wide", False)
        dims = "1344×896 wide" if wide else "896×1152 portrait"
        print(f"\n  [{batch_key}] {batch['label']}  ({dims})")

        for i, prompt_text in enumerate(batch["prompts"]):
            seed   = random.randint(0, 9_999_999_999)
            prefix = f"site-{batch_key}-{i+1:02d}"

            success = send_job(prompt_text, prefix, seed=seed,
                               batch_size=args.batch_size,
                               wide=wide, dry_run=args.dry_run)
            status = "✓" if success else "✗ FAILED"
            snippet = prompt_text.replace(STYLE, "")[:60]
            print(f"    {status}  [{i+1:02d}] {snippet}...")
            if success:
                ok += 1
            total += 1
            if not args.dry_run:
                time.sleep(STAGGER_MS / 1000)

    tag = "[DRY RUN] " if args.dry_run else ""
    total_images = ok * args.batch_size
    print(f"\n{tag}Done — {ok}/{total} jobs queued (~{total_images} images)")
    if not args.dry_run:
        running, pending = queue_depth()
        print(f"Queue now: running={running}  pending={pending}")


if __name__ == "__main__":
    main()
