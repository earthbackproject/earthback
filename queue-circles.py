"""
Earthback — Explore circle image queuer
========================================
Generates 3 images per circle category for the explore.html grid.
No faces. Documentary aesthetic. Earthback palette.

Usage:
  python queue-circles.py                          # queue all categories
  python queue-circles.py --category earth-building
  python queue-circles.py --group building         # queue a theme group
  python queue-circles.py --loops 2                # 2 passes per image
  python queue-circles.py --batch-size 3           # 3 images per job
  python queue-circles.py --dry-run
  python queue-circles.py --status
  python queue-circles.py --list                   # print all category slugs

Output prefix:  circle-[category]-[N]
  → circle-earth-building-1_00001_.png  etc.
"""

import json, random, time, argparse, urllib.request
from copy import deepcopy

# ── Config ─────────────────────────────────────────────────────────────────────
COMFY_URL  = "http://127.0.0.1:8188"
STAGGER_MS = 150

WORKFLOW = {
    "6":  {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "8":  {"inputs": {"samples": ["31", 0], "vae": ["30", 2]},
           "class_type": "VAEDecode"},
    "9":  {"inputs": {"filename_prefix": "", "images": ["8", 0]},
           "class_type": "SaveImage"},
    "27": {"inputs": {"width": 1344, "height": 768, "batch_size": 1},
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
    "33": {"inputs": {"text": "people, faces, text, watermark, blurry, oversaturated", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
}

STYLE = ("Documentary photograph, natural light, shallow depth of field, "
         "no people, no faces, rich material texture. "
         "Warm earth tones, terracotta, ochre, sage green, undyed linen.")

def p(desc):
    """Wrap a description with the shared style anchor."""
    return f"{STYLE} {desc}"

# ── Circle categories ─────────────────────────────────────────────────────────
# Structure: { slug: { "group": str, "label": str, "prompts": [str, str, str] } }

CIRCLES = {

    # ── BUILDING & SHELTER ───────────────────────────────────────────────────

    "earth-building": {
        "group": "building",
        "label": "Earth Building",
        "prompts": [
            p("Close-up of a hand-pressed compressed earth block, rough edges and fine grain texture, warm terracotta in raking sidelight."),
            p("A stack of drying adobe bricks in rows in a bare yard, long afternoon shadow crossing them, ochre and red tones."),
            p("A freshly troweled earthen wall section mid-plaster, texture changing from rough to smooth across the frame, warm dusty light."),
        ],
    },

    "cob": {
        "group": "building",
        "label": "Cob",
        "prompts": [
            p("A cross-section of cob wall under construction, straw fibers and clay visible in the cut face, warm natural light."),
            p("Bare feet treading a dark clay and straw mix on a tarp, the material worked into rough circular patterns, outdoor light."),
            p("A finished rounded cob wall corner, smooth lime-washed surface, soft overcast light, herbs growing at the base."),
        ],
    },

    "rammed-earth": {
        "group": "building",
        "label": "Rammed Earth",
        "prompts": [
            p("A rammed earth wall face showing distinct horizontal strata in terracotta, sand, and grey tones, flat raking light."),
            p("Close-up of wooden formwork being stripped from a newly rammed section, raw compressed earth revealed, sharp shadow."),
            p("A rammed earth home exterior in late afternoon sun, the wall glowing ochre and burnt sienna, deep window reveals."),
        ],
    },

    "straw-bale": {
        "group": "building",
        "label": "Straw Bale",
        "prompts": [
            p("A cut straw bale cross-section showing the dense golden interior, straw ends catching direct sunlight, rich texture."),
            p("Straw bales stacked in an unfinished wall, baling twine still visible, wide blue sky above, long light."),
            p("A finished straw bale wall corner with thick lime plaster, windowsill deep enough to sit in, warm interior light."),
        ],
    },

    "stone-masonry": {
        "group": "building",
        "label": "Stone Masonry",
        "prompts": [
            p("Close-up of a dry-stack stone wall corner, flat stones fitted without mortar, lichen on the older faces, cool diffuse light."),
            p("A fieldstone wall running across a hillside, grey and ochre tones, wild grass at its base, overcast morning."),
            p("A mason's tools laid on a flat stone surface — wooden mallet, wide chisel, spirit level — warm natural light."),
        ],
    },

    "timber-framing": {
        "group": "building",
        "label": "Timber Framing",
        "prompts": [
            p("A mortise-and-tenon joint freshly cut in oak, wood shavings around it, sharp shadow in raking light showing the depth."),
            p("A timber frame skeleton rising against an overcast sky, pegged joints at each intersection, clean geometric lines."),
            p("Close-up of an aged timber frame wall, the wood darkened to silver-grey, white lime plaster between the members."),
        ],
    },

    "bamboo": {
        "group": "building",
        "label": "Bamboo",
        "prompts": [
            p("Cross-section cuts of bamboo culms in several sizes, nodes and hollow interiors visible, warm side light."),
            p("A bamboo structure frame under construction, lashed joints at angles, tropical light filtering through the poles."),
            p("Close-up of a traditional bamboo lashing joint, cane binding wrapped tight in a precise crossing pattern."),
        ],
    },

    "living-roofs": {
        "group": "building",
        "label": "Living Roofs",
        "prompts": [
            p("A living roof covered in sedum in autumn rust and green tones, moss at the edges, soft overcast light from above."),
            p("Close-up of sedum rosettes on a green roof, dew on the leaves, warm morning light at a low angle, rich texture."),
            p("A traditional Scandinavian sod roof, deep grass growing from thick earth layers, wooden fascia below."),
        ],
    },

    "natural-plasters": {
        "group": "building",
        "label": "Natural Plasters",
        "prompts": [
            p("Close-up of a layered natural plaster wall showing scratch, brown, and finish coats at the cut edge, warm raking light."),
            p("A bucket of fresh lime putty, brilliant white and glossy, a wide wooden float resting across the rim."),
            p("Clay plaster surface transitioning from wet dark brown to dried pale buff, a trowel mark mid-pass."),
        ],
    },

    "passive-solar": {
        "group": "building",
        "label": "Passive Solar",
        "prompts": [
            p("Warm winter sunlight falling in a long diagonal rectangle across a tiled thermal mass floor, tiles absorbing heat."),
            p("A trombe wall — dark-painted masonry behind glass — condensation beading on the glazing interior, warm light beyond."),
            p("A deep south-facing window reveal in adobe, afternoon sun cutting a precise rectangle across the earthen sill."),
        ],
    },

    # ── ENERGY ───────────────────────────────────────────────────────────────

    "solar-electric": {
        "group": "energy",
        "label": "Solar Electric",
        "prompts": [
            p("Close-up of crystalline silicon solar cells, blue metallic grid lines sharp, direct sun catching the anti-reflective coating."),
            p("A small off-grid solar array on a simple pole mount, panels angled south, dry grass and open sky behind."),
            p("A weathered battery bank and charge controller on a wooden shelf, indicator lights glowing amber, shed interior."),
        ],
    },

    "wind-power": {
        "group": "energy",
        "label": "Wind Power",
        "prompts": [
            p("A small three-blade wind turbine against a wide grey sky, blades caught in slight motion blur."),
            p("Close-up of a wind turbine hub and blade root, painted steel and bolt detail, overcast industrial light."),
            p("A homemade wind turbine on a pipe mast above a farmstead, welded frame, open landscape behind."),
        ],
    },

    "micro-hydro": {
        "group": "energy",
        "label": "Micro Hydro",
        "prompts": [
            p("A small intake weir on a clear rocky stream, water sheeting evenly over the lip, morning mountain light."),
            p("Close-up of a pelton wheel turbine, wet brass buckets catching the light, water spray mid-impact, copper and silver tones."),
            p("Penstock pipe running down a steep wooded hillside, condensation on the outside, dappled forest light."),
        ],
    },

    "biogas": {
        "group": "energy",
        "label": "Biogas",
        "prompts": [
            p("A small fixed-dome biogas digester, weathered concrete, a copper gas outlet pipe emerging from the top, outdoor light."),
            p("Close-up of a biogas flame on a small burner, clean blue cone of flame, warm kitchen interior, low light."),
            p("A simple biogas balloon storage system, translucent plastic filled, held down with a bamboo frame, morning light."),
        ],
    },

    "rocket-stove": {
        "group": "energy",
        "label": "Rocket Stove",
        "prompts": [
            p("Close-up of a rocket stove combustion unit — the L-shaped brick feed and burn tunnel, glowing orange inside."),
            p("A sculpted cob rocket mass heater bench in a finished room, smooth earthen curves, warm indirect light."),
            p("A small outdoor rocket stove cooking fire, efficient small-diameter wood burning cleanly with minimal smoke."),
        ],
    },

    "biochar": {
        "group": "energy",
        "label": "Biochar",
        "prompts": [
            p("Freshly made biochar poured from a kiln onto soil, the black porous carbon catching light on each fractured cell wall."),
            p("Close-up of biochar granules next to rich dark soil, the contrast of matte black carbon and brown earth."),
            p("A simple TLUD biochar kiln made from nested metal drums, clean white smoke rising in a still morning sky."),
        ],
    },

    # ── FOOD & GROWING ────────────────────────────────────────────────────────

    "permaculture": {
        "group": "growing",
        "label": "Permaculture",
        "prompts": [
            p("A densely planted permaculture bed with multiple layers — herbs, shrubs, and a young fruit tree — morning light."),
            p("A hand-drawn permaculture zone map on paper, pencil circles and annotations, laid on a rough wooden table."),
            p("A mature food forest understory, dappled light through the canopy, ground cover and mulched paths below."),
        ],
    },

    "food-forest": {
        "group": "growing",
        "label": "Food Forest",
        "prompts": [
            p("A food forest canopy break with light filtering through fruit trees to shrubs and ground cover below, layered green."),
            p("Close-up of a loaded apple bough, fruit clustered and heavy, soft diffuse autumn light, leaves turning."),
            p("A newly planted food forest — small trees with mulch rings, sheet mulch at the edges, open sky above."),
        ],
    },

    "market-gardening": {
        "group": "growing",
        "label": "Market Gardening",
        "prompts": [
            p("Long permanent beds of mixed salad greens in precise rows, morning light angled across the leaf texture."),
            p("Close-up of freshly harvested radishes, roots still damp with earth, bundled and rubber-banded on a harvest crate."),
            p("A market garden overview at dawn, raised beds in geometric rows, irrigation tape along the length, mist low."),
        ],
    },

    "microgreens": {
        "group": "growing",
        "label": "Microgreens",
        "prompts": [
            p("Dense microgreen trays at the cotyledon stage, sunflower shoots arching upward, grow light warm overhead."),
            p("Close-up of radish microgreens, vivid red stems and bright green paired leaves, tightly packed, backlit."),
            p("A home microgreen setup — stacked trays, a spray bottle, scissors, natural window light, clean and minimal."),
        ],
    },

    "mushroom-growing": {
        "group": "growing",
        "label": "Mushroom Growing",
        "prompts": [
            p("Oyster mushrooms erupting from a straw block fruiting bag, white fans clustered at the opening, cool humid light."),
            p("Close-up of shiitake pinning on a soaked oak log, small mushroom caps pushing through the bark surface."),
            p("A mushroom fruiting chamber interior, damp and humid, clusters at various stages of growth, cool diffuse light."),
        ],
    },

    "aquaponics": {
        "group": "growing",
        "label": "Aquaponics",
        "prompts": [
            p("Close-up of a raft aquaponics channel, lettuce roots hanging into clear circulating water, green and white tones."),
            p("Tilapia circling in a round tank, water surface catching light in rings, bubbles rising from the aerator."),
            p("A small backyard aquaponics system — IBC tote fish tank with grow beds above, damp green morning light."),
        ],
    },

    "seed-saving": {
        "group": "growing",
        "label": "Seed Saving",
        "prompts": [
            p("Dried seed heads of several varieties on a white cloth, labeled with handwritten paper tags, flat even light."),
            p("Close-up of heirloom tomato seeds being ferment-washed in a jar of water, seeds and gel floating."),
            p("A seed library — small paper envelopes in a wooden card catalog, labeled in various handwriting styles."),
        ],
    },

    "beekeeping": {
        "group": "growing",
        "label": "Beekeeping",
        "prompts": [
            p("A frame of honeycomb pulled from a hive, cells capped in beeswax, golden and amber tones, warm afternoon light."),
            p("Close-up of honeybees clustered at a hive entrance, wings and bodies catching sidelight, warm afternoon."),
            p("A natural log hive in a garden, weathered bark and wood, bees at the entrance notch, soft overcast light."),
        ],
    },

    "composting": {
        "group": "growing",
        "label": "Composting",
        "prompts": [
            p("A compost pile cross-section showing rich dark decomposed center against fresh green material at the edge."),
            p("Close-up of finished compost, dark and crumbly, an earthworm visible at the surface, low warm raking light."),
            p("A three-bay compost system, wooden slat sides, each bay at a different stage — raw, turning, finished."),
        ],
    },

    "fermentation": {
        "group": "growing",
        "label": "Fermentation",
        "prompts": [
            p("A row of glass fermentation jars with airlocks, vegetable brines at different stages, window backlight."),
            p("Close-up of kimchi in a wide jar, red chili paste and cabbage leaves, a glass weight pressing it down."),
            p("A sourdough starter in a glass jar, active and domed, flour and water recently added, warm kitchen light."),
        ],
    },

    # ── WATER ─────────────────────────────────────────────────────────────────

    "rainwater-harvesting": {
        "group": "water",
        "label": "Rainwater Harvesting",
        "prompts": [
            p("A corrugated iron roof gutter and downpipe leading to a large concrete cistern, rain-stained and mossy."),
            p("Close-up of a first-flush diverter on a downpipe, simple PVC mechanism, algae at the fitting base."),
            p("An underground rainwater tank being installed, concrete ring at the opening, dark earth around it."),
        ],
    },

    "greywater": {
        "group": "water",
        "label": "Greywater",
        "prompts": [
            p("A branched drain greywater outlet in a mulched garden basin, clear water spreading through wood chips."),
            p("Close-up of a greywater wetland edge, plant roots in clear water, sedge and iris growing from the margin."),
            p("A laundry-to-landscape pipe running through a wall to a mulched fruit tree basin, simple and functional."),
        ],
    },

    "water-harvesting": {
        "group": "water",
        "label": "Water Harvesting",
        "prompts": [
            p("A newly dug swale on a hillside contour, dark wet soil at the base, water sitting level after rain."),
            p("A farm pond reflecting sky and treeline, a simple earthen berm along one side, calm morning water."),
            p("Close-up of a swale base, soil darkening as moisture spreads sideways through it, grass at the lip."),
        ],
    },

    # ── FIBER & CRAFT ─────────────────────────────────────────────────────────

    "natural-dyeing": {
        "group": "craft",
        "label": "Natural Dyeing",
        "prompts": [
            p("A skein of freshly dyed wool hanging to dry, deep indigo blue, still damp, light catching the twist."),
            p("Close-up of a dye vat — a copper pot of dark liquid with plant material floating at the surface."),
            p("A line of naturally dyed fabric swatches in rust, mustard, sage, and umber, hung in order on a cord."),
        ],
    },

    "weaving": {
        "group": "craft",
        "label": "Weaving",
        "prompts": [
            p("Close-up of a warp on a floor loom, threads in alternating natural and earthy-dyed colors, parallel and taut."),
            p("A shuttle mid-pass through a shed of warp threads, the weft building a pattern of warm earth tones."),
            p("A backstrap loom outdoors, the warp anchored to a post, finished cloth growing from the frame, dappled light."),
        ],
    },

    "basketry": {
        "group": "craft",
        "label": "Basketry",
        "prompts": [
            p("Close-up of a coiled basket base in two-tone rush, the spiral tightening to a center point, warm light."),
            p("Willow withies woven over and under upright stakes in a traditional basket, the form emerging."),
            p("A collection of finished baskets in natural and dyed rush, stacked and hung in a workshop, interior light."),
        ],
    },

    "pottery-ceramics": {
        "group": "craft",
        "label": "Pottery & Ceramics",
        "prompts": [
            p("A freshly thrown bowl still on the wheel, wet clay walls thin and even, fingermarks visible in the surface."),
            p("Close-up of a wood-fired anagama kiln exterior, the bricked arch and dark ash marks from past firings."),
            p("A line of bisque-fired pots before glazing, pale and porous, arranged by size on a shelf, flat light."),
        ],
    },

    "blacksmithing": {
        "group": "craft",
        "label": "Blacksmithing",
        "prompts": [
            p("A piece of hot steel on an anvil, glowing orange at the working end, hammer marks spreading the metal."),
            p("Close-up of a gas forge interior, the refractory glowing white-hot, a steel bar in the chamber."),
            p("Finished hand-forged tools on a pegboard — hooks, chisels, tongs — dark iron, warm workshop light."),
        ],
    },

    "woodworking": {
        "group": "craft",
        "label": "Woodworking",
        "prompts": [
            p("A hand plane making a long pass across a pine board, a continuous shaving curling away, morning light."),
            p("Close-up of a hand-cut dovetail joint, the interlocking tails and pins precise, fresh wood smell implied."),
            p("A woodworking bench with tools arranged — marking gauge, chisels, mallet — shavings on the floor below."),
        ],
    },

    # ── LAND & COMMUNITY ─────────────────────────────────────────────────────

    "rewilding": {
        "group": "land",
        "label": "Rewilding",
        "prompts": [
            p("A restored prairie strip in late summer, tall grasses and native wildflowers dense and unmowed, golden light."),
            p("Close-up of native seedlings in biodegradable tubes on a reforested hillside, early spring morning light."),
            p("A restored wetland edge, sedge and cattail at the water margin, open sky reflecting on still water."),
        ],
    },

    "agroforestry": {
        "group": "land",
        "label": "Agroforestry",
        "prompts": [
            p("Rows of young nut trees in a silvopasture system, grass growing between the rows, open morning light."),
            p("Close-up of an alley cropping strip, vegetables growing in the light gap between two rows of fruit trees."),
            p("Mature pollarded trees in open pasture, branches spreading wide, dappled shade on the grass below."),
        ],
    },

    "holistic-grazing": {
        "group": "land",
        "label": "Holistic Grazing",
        "prompts": [
            p("A dense mob of sheep grazing tall-grass, the grass pressed flat behind them as they move through."),
            p("Close-up of a cattle hoof print in recently grazed soil, roots and organic matter visible in the disturbance."),
            p("A paddock move in progress — temporary electric fence being rewound, grazed side short, manure scattered."),
        ],
    },

    "urban-farming": {
        "group": "land",
        "label": "Urban Farming",
        "prompts": [
            p("A rooftop vegetable garden, raised beds productive with greens, city skyline softly out of focus behind."),
            p("A vacant lot converted to community garden, raised beds on rubble and fill, a painted chainlink fence."),
            p("Close-up of a city balcony food garden — pots of herbs, a small tomato plant trained to a wall trellis."),
        ],
    },

    "repair-culture": {
        "group": "community",
        "label": "Repair Culture",
        "prompts": [
            p("Close-up of a soldering iron tip on a circuit board repair, small smoke curl, warm focused task light."),
            p("A worn pair of boots being resoled at a cobbler's bench, awl and thread and fresh leather visible."),
            p("A communal repair table with a bicycle wheel in a stand, tools spread around it, workshop light."),
        ],
    },

    "tool-library": {
        "group": "community",
        "label": "Tool Library",
        "prompts": [
            p("A wall of labeled hand tools on pegboard — levels, squares, planes, chisels — organized by type and size."),
            p("Close-up of a well-used wooden hand plane, the sole polished bright from long use, shavings around it."),
            p("A shared workshop interior, workbenches and tools in order, natural light from high clerestory windows."),
        ],
    },

    # ── HEALTH & ECOLOGY ─────────────────────────────────────────────────────

    "herbalism": {
        "group": "ecology",
        "label": "Herbalism",
        "prompts": [
            p("Dried herb bundles hanging from a wooden rod — lavender, chamomile, yarrow — warm backlight through them."),
            p("Close-up of fresh herb sprigs on a wooden cutting board, sorted by variety — rosemary, thyme, sage."),
            p("Labeled tincture bottles in amber glass on a shelf, morning light through the window backlighting the liquid."),
        ],
    },

    "forest-bathing": {
        "group": "ecology",
        "label": "Forest Bathing",
        "prompts": [
            p("Light filtering through old-growth forest canopy, rays catching dust and spores in still air, cool and green."),
            p("Close-up of deep moss on a log, brilliant green and damp, light diffuse and cool, texture rich."),
            p("A forest floor in autumn — oak leaves, acorn caps, a log covered in lichen and shelf fungus, soft light."),
        ],
    },

    "appropriate-tech": {
        "group": "ecology",
        "label": "Appropriate Technology",
        "prompts": [
            p("A hand-cranked grain mill clamped to a wooden counter, whole wheat berries in the hopper, warm morning light."),
            p("Close-up of a bicycle-powered generator, the drive belt and flywheel visible, workshop light."),
            p("A simple solar food dryer — screen trays in a plywood box with a glazed lid, herbs drying inside."),
        ],
    },

    "natural-swimming": {
        "group": "ecology",
        "label": "Natural Swimming",
        "prompts": [
            p("A natural swimming pond with a planted regeneration zone, clear water and water lilies at the edge."),
            p("Close-up of the water-plant margin in a natural pool, submerged aquatic plants visible below the surface."),
            p("A simple timber deck over a natural pond, low and minimal, sky and willow reflected in the water."),
        ],
    },

    "hempcrete": {
        "group": "building",
        "label": "Hempcrete",
        "prompts": [
            p("Close-up of freshly mixed hempcrete in a bucket — warm golden-honey buff-tan chunky crumbly material, "
              "visible golden-amber hemp shiv pieces throughout a cream lime binder, "
              "NOT grey NOT concrete, like damp oatmeal with golden grain pieces, matte not glossy. "
              "Natural light, shallow depth of field."),
            p("A freshly stripped hempcrete wall face — warm honey-tan color NOT grey, "
              "visible hemp shiv fiber pieces locked in pale lime matrix, "
              "porous matte organic texture, bumpy and fibrous, clearly not concrete. "
              "Raking afternoon sidelight showing the relief texture."),
            p("Raw hemp shiv pile beside white lime binder bags on a job site — "
              "golden-amber loose woody fiber pieces, warm tan and gold tones, "
              "lightweight and airy-looking, beside off-white chalky lime sacks. "
              "Outdoor morning light, organic and agricultural."),
        ],
    },

    "off-grid-systems": {
        "group": "ecology",
        "label": "Off-Grid Systems",
        "prompts": [
            p("A hand-crank emergency radio and a small solar lantern on a windowsill, afternoon light through them."),
            p("Close-up of an off-grid DC power panel — breakers, battery monitor, labeled wiring, amber indicator light."),
            p("A simple mesh network node on a wooden post, weatherproofed enclosure and small antenna, rural backdrop."),
        ],
    },
}

# Group metadata for filtering
GROUPS = {
    "building":  "Building & Shelter",
    "energy":    "Energy",
    "growing":   "Food & Growing",
    "water":     "Water",
    "craft":     "Fiber & Craft",
    "land":      "Land & Ecology",
    "community": "Community",
    "ecology":   "Health & Ecology",
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

def build_prompt(text, prefix, seed, batch_size, width, height):
    from copy import deepcopy
    p = deepcopy(WORKFLOW)
    p["6"]["inputs"]["text"]            = text
    p["9"]["inputs"]["filename_prefix"] = prefix
    p["27"]["inputs"]["width"]          = width
    p["27"]["inputs"]["height"]         = height
    p["27"]["inputs"]["batch_size"]     = batch_size
    p["31"]["inputs"]["seed"]           = seed
    return p

def send_job(text, prefix, seed, batch_size=1, width=1344, height=768, dry_run=False):
    if dry_run:
        print(f"    [DRY] {prefix}  seed={seed}  {width}x{height}  bs={batch_size}")
        print(f"          {text[:90]}...")
        return True
    prompt = build_prompt(text, prefix, seed, batch_size, width, height)
    result = api_post("/prompt", {"prompt": prompt})
    return bool(result.get("prompt_id"))

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue Earthback circle images")
    parser.add_argument("--category",   default=None,
                        help="Single category slug (e.g. earth-building, cob, fermentation)")
    parser.add_argument("--group",      default=None,
                        help=f"Theme group: {', '.join(GROUPS.keys())}")
    parser.add_argument("--loops",      type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Images per job (3 recommended for curation)")
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--status",     action="store_true")
    parser.add_argument("--list",       action="store_true",
                        help="Print all available category slugs and exit")
    args = parser.parse_args()

    if args.list:
        for group_key, group_label in GROUPS.items():
            cats = {k: v for k, v in CIRCLES.items() if v["group"] == group_key}
            if cats:
                print(f"\n{group_label}:")
                for slug, data in cats.items():
                    print(f"  {slug:30s}  {data['label']}")
        return

    try:
        running, pending = queue_depth()
    except Exception as e:
        print(f"ERROR: Cannot reach ComfyUI at {COMFY_URL} ({e})")
        return

    if args.status:
        print(f"ComfyUI queue — running: {running}  pending: {pending}")
        return

    print(f"ComfyUI connected — running: {running}  pending: {pending}\n")

    # Resolve categories to run
    if args.category:
        slug = args.category.lower()
        if slug not in CIRCLES:
            print(f"Unknown category '{slug}'. Run --list to see all.")
            return
        cats = {slug: CIRCLES[slug]}
    elif args.group:
        cats = {k: v for k, v in CIRCLES.items() if v["group"] == args.group.lower()}
        if not cats:
            print(f"Unknown group '{args.group}'. Options: {', '.join(GROUPS)}")
            return
    else:
        cats = CIRCLES

    total = ok = 0
    base_seed = 500000

    for loop in range(args.loops):
        if args.loops > 1:
            print(f"=== Loop {loop + 1} of {args.loops} ===")

        for slug, data in cats.items():
            print(f"\n  [{data['group']}]  {data['label']}  ({slug})")
            for i, prompt_text in enumerate(data["prompts"]):
                prefix = f"circle-{slug}-{i+1}"
                seed   = base_seed + abs(hash(slug)) % 100000 + (i * 7) + (loop * 1000)
                success = send_job(
                    prompt_text, prefix, seed,
                    batch_size=args.batch_size,
                    dry_run=args.dry_run,
                )
                status_str = "✓" if success else "✗ FAILED"
                print(f"    {status_str}  prompt {i+1}")
                if success: ok += 1
                total += 1
                if not args.dry_run:
                    time.sleep(STAGGER_MS / 1000)

    tag = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{tag}Done — {ok}/{total} jobs queued")
    if not args.dry_run:
        running, pending = queue_depth()
        print(f"Queue now: running={running}  pending={pending}")
        print(f"\nImages saved as:  circle-[category]-[1|2|3]_NNNNN_.png")
        print(f"Deploy to:        site/assets/img/circles/")

if __name__ == "__main__":
    main()
