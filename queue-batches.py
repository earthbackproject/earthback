"""
Earthback — ComfyUI batch queuer (no browser required)
=======================================================
Sends jobs directly to the ComfyUI API. ComfyUI must be running.

Usage:
  python queue-batches.py                  # queue everything not yet done
  python queue-batches.py --batch face     # face batches only
  python queue-batches.py --batch t4       # scenario batches only
  python queue-batches.py --char "James Osei"  # one character only
  python queue-batches.py --dry-run        # print jobs, don't send
  python queue-batches.py --status         # show queue depth and exit

ComfyUI API: http://127.0.0.1:8188
Output dir:  C:\\users\\adrxi\\Earthback\\comfyui-output  (set in start-comfy-claude.bat)
"""

import json
import random
import time
import argparse
import urllib.request
import urllib.error
from copy import deepcopy

# ── Config ────────────────────────────────────────────────────────────────────
COMFY_URL  = "http://127.0.0.1:8188"
STAGGER_MS = 150   # ms between API calls (be polite to the server)

# Workflow skeleton extracted directly from running ComfyUI instance.
# Node IDs confirmed: 6=prompt, 9=SaveImage, 27=latent, 30=model, 31=KSampler
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
               "model":         ["30", 0],
               "positive":      ["35", 0],
               "negative":      ["33", 0],
               "latent_image":  ["27", 0]
           },
           "class_type": "KSampler"},
    "33": {"inputs": {"text": "", "clip": ["30", 1]},
           "class_type": "CLIPTextEncode"},
    "35": {"inputs": {"guidance": 3.5, "conditioning": ["6", 0]},
           "class_type": "FluxGuidance"},
}

# ── Character data ─────────────────────────────────────────────────────────────
# prefix naming: chars-[Name]-[type]
# ComfyUI auto-appends _00001_, _00002_... when same prefix is reused
#
# seed: locked per character so face batches generate the same underlying person.
#   Face angles all use char seed + small offset (0-4) — same noise base, different pose.
#   Scenario batches use char seed + 1000+ offsets for variety while staying in the same
#   "character neighborhood". Use --reseed to generate fresh random seeds.
#
# desc: intentionally detailed facial specifics so Flux has enough to lock onto a face.

CHARS = [
    {
        "name": "James Osei",
        "trigger": "JAMES_OSEI_EB",
        "desc": "a 34-year-old Ghanaian man, lean build, slight stubble, "
                "warm dark brown skin, high cheekbones, strong jaw, close-cropped hair, "
                "deep-set dark brown eyes",
        "location": "Accra region Ghana",
        "light": "bright West African midday light",
        "seed": 100001,
    },
    {
        "name": "Lena Hartmann",
        "trigger": "LENA_HARTMANN_EB",
        "desc": "a 31-year-old German woman, reddish-brown shoulder-length hair, "
                "light freckled skin, blue-gray eyes, oval face, fine features, "
                "narrow nose",
        "location": "Tafraoute Morocco",
        "light": "Anti-Atlas afternoon light",
        "seed": 200001,
    },
    {
        "name": "Tom Westhall",
        "trigger": "TOM_WESTHALL_EB",
        "desc": "a 47-year-old white American man, deeply weathered tan face, "
                "salt-and-pepper close-cropped stubble, square jaw, blue eyes, "
                "crow's feet wrinkles, broad forehead",
        "location": "Willamette Valley Oregon",
        "light": "overcast Pacific Northwest light",
        "seed": 300001,
    },
    {
        "name": "Rosa Mendez",
        "trigger": "ROSA_MENDEZ_EB",
        "desc": "a 38-year-old Costa Rican woman, medium warm brown skin, "
                "dark hair pulled back tightly, dark brown eyes, full lips, "
                "round soft face, slight cheek fullness",
        "location": "Osa Peninsula Costa Rica",
        "light": "dappled tropical morning light",
        "seed": 400001,
    },
    {
        "name": "Mei Lin",
        "trigger": "MEI_LIN_EB",
        "desc": "a 29-year-old Filipino woman, short practical dark black hair, "
                "warm tan skin, dark almond-shaped eyes, round face, broad nose, "
                "wide cheekbones",
        "location": "rural Mindanao Philippines",
        "light": "warm tropical interior light",
        "seed": 500001,
    },
    {
        "name": "Elena Vasquez",
        "trigger": "ELENA_VASQUEZ_EB",
        "desc": "a 52-year-old Native American woman, Pueblo descent, "
                "deep copper-brown skin, strong angular face, very prominent cheekbones, "
                "dark brown eyes, silver-streaked black hair, strong nose",
        "location": "Pueblo of Acoma New Mexico",
        "light": "high desert afternoon light",
        "seed": 600001,
    },
    {
        "name": "Amara Diallo",
        "trigger": "AMARA_DIALLO_EB",
        "desc": "a 41-year-old Senegalese West African man, master builder, "
                "very dark brown skin, broad face, strong heavy brow, "
                "close-cropped hair, prominent forehead, wide nose",
        "location": "Thiès Senegal",
        "light": "bright West African afternoon light, slight dust",
        "seed": 700001,
    },
    {
        "name": "Marcus Webb",
        "trigger": "MARCUS_WEBB_EB",
        "desc": "a 61-year-old white American man, deeply lined weathered face, "
                "short gray hair, pale blue eyes, heavyset build, broad nose, "
                "prominent jaw, age spots",
        "location": "Eastern Kentucky farmland",
        "light": "soft overcast morning light",
        "seed": 800001,
    },
    {
        "name": "Kenji Nakamura",
        "trigger": "KENJI_NAKAMURA_EB",
        "desc": "a 35-year-old Japanese man, researcher, slim build, "
                "dark brown eyes, straight black hair, clean-shaven, "
                "narrow oval face, wire-rimmed glasses, smooth skin",
        "location": "TU Delft materials lab",
        "light": "soft northern European lab light",
        "seed": 900001,
    },
    {
        "name": "Priya Sharma",
        "trigger": "PRIYA_SHARMA_EB",
        "desc": "a 44-year-old Australian woman of South Indian descent, "
                "dark brown skin, black hair with early gray streaks, dark eyes, "
                "strong defined brow, oval face, medium build",
        "location": "Queensland Australia",
        "light": "harsh clear Australian sun",
        "seed": 110001,
    },
    {
        "name": "Dara Okonkwo",
        "trigger": "DARA_OKONKWO_EB",
        "desc": "a 33-year-old Black American woman, deep rich brown skin, "
                "natural hair, warm round face, bright expressive dark eyes, "
                "full lips, high cheekbones",
        "location": "Detroit Michigan",
        "light": "overcast Midwest sky",
        "seed": 220001,
    },
    {
        "name": "Sam Torres",
        "trigger": "SAM_TORRES_EB",
        "desc": "a 26-year-old Mexican-American man, warm tan skin, "
                "thick dark hair, dark brown eyes, square face, light stubble, "
                "broad shoulders, strong jaw",
        "location": "Phoenix Arizona workshop",
        "light": "harsh Arizona sunlight",
        "seed": 330001,
    },
]

# Offset added to char seed per face angle — keeps same noise base, varies pose
FACE_ANGLE_SEED_OFFSET = {
    "face-front": 0,
    "face-left":  1,
    "face-right":  2,
    "face-down":  3,
    "face-talk":  4,
}

# ── Batch definitions ──────────────────────────────────────────────────────────
# Each batch is a list of (prefix_suffix, prompt_template) pairs.
# {trigger}, {desc}, {location}, {light} are filled per character.

SCENARIO_BATCHES = {
    "t4-01": {
        "label": "T4 detail/close shots",
        "suffix": "T4-01",
        "prompts": [
            ("chars-{name}-T4-01",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Close-up detail shot, hands working with material, texture and craft visible, "
             "{light}, shallow depth of field. Photojournalism style."),
        ]
    },
    "t4-02": {
        "label": "T4 fresh portrait seeds",
        "suffix": "T4-02",
        "prompts": [
            ("chars-{name}-T4-02",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Medium documentary portrait, standing in their primary work environment, {location}, "
             "{light}, practical clothes, confident presence. Photojournalism style."),
        ]
    },
    "t4-03": {
        "label": "T4 action seeds",
        "suffix": "T4-03",
        "prompts": [
            ("chars-{name}-T4-03",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Working shot — active, mid-task, hands engaged with their craft, {location}, "
             "{light}, full physical involvement in the work. Photojournalism style."),
        ]
    },
    "t4-04": {
        "label": "T4 environmental seeds",
        "suffix": "T4-04",
        "prompts": [
            ("chars-{name}-T4-04",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Wide environmental shot, small figure in large setting, {location}, "
             "{light}, showing scale and context of their work. Wide photojournalism frame."),
        ]
    },
    "t4-05": {
        "label": "T4 scenario seeds",
        "suffix": "T4-05",
        "prompts": [
            ("chars-{name}-T4-05",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Candid working moment — teaching, explaining, or assessing, {location}, "
             "{light}, animated and purposeful expression. Photojournalism style."),
        ]
    },
}

FACE_BATCHES = {
    "face-front": {
        "label": "Face: straight-on neutral",
        "prompts": [
            ("chars-{name}-face-front",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Straight-on face portrait, looking directly into camera, neutral expression, relaxed. "
             "Tight crop from collarbones up, face fills most of the frame. "
             "Soft even frontal daylight, no harsh shadows. Shallow depth of field."),
        ]
    },
    "face-left": {
        "label": "Face: 3/4 left",
        "prompts": [
            ("chars-{name}-face-left",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Three-quarter face portrait, head turned slightly left, eyes still toward camera. "
             "Tight crop, face fills most of the frame. "
             "Soft sidelight from the left, gentle shadow on right cheek showing facial structure. "
             "Shallow depth of field."),
        ]
    },
    "face-right": {
        "label": "Face: 3/4 right",
        "prompts": [
            ("chars-{name}-face-right",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Three-quarter face portrait, head turned slightly right, eyes toward camera. "
             "Tight crop, face fills most of the frame. "
             "Soft sidelight from the right, gentle shadow on left cheek showing facial structure. "
             "Shallow depth of field."),
        ]
    },
    "face-down": {
        "label": "Face: downward look / thinking",
        "prompts": [
            ("chars-{name}-face-down",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Close portrait, head tilted slightly down, eyes looking downward as if reading or thinking, "
             "brow slightly furrowed in concentration. "
             "Tight crop, face fills most of the frame. Soft overhead daylight, natural. Shallow depth of field."),
        ]
    },
    "face-talk": {
        "label": "Face: mid-sentence / animated",
        "prompts": [
            ("chars-{name}-face-talk",
             "Documentary photograph, 35mm film, real person. {trigger}, {desc}. "
             "Close candid portrait, mid-sentence, mouth slightly open, eyes alive and engaged, "
             "speaking to someone just off frame. Natural animated expression. "
             "Tight crop from collarbones up. Soft natural daylight. Shallow depth of field."),
        ]
    },
}

ALL_BATCHES = {**SCENARIO_BATCHES, **FACE_BATCHES}

# ── T5 per-character scenes ─────────────────────────────────────────────────────
# T5 is a different structure: each character has their own specific scenes
# drawn from their actual biography and work. No generic templates.
# Prompts are literal — no documentary/photojournalism framing.
# Format per scene: (prefix, prompt_text)
# {trigger} and {light} are still substituted at queue time.

T5_SCENES = {
    "James Osei": [
        ("{trigger}, warm dark brown skin, high cheekbones, slight stubble, lean build. "
         "Both hands on the lever of a hand-operated compressed earth block press, "
         "mid-stroke, blocks stacking in rows behind him in the red laterite yard. "
         "Bright West African midday light. Photograph."),

        ("{trigger}, warm dark brown skin, high cheekbones, slight stubble. "
         "Holding a freshly split compressed earth block in both hands, "
         "examining the cross-section close, checking grain and density. "
         "Outdoor shade, soft diffuse light. Photograph."),

        ("{trigger}, warm dark brown skin, lean build. "
         "Crouching beside a newly formed earth wall, pressing one thumb hard into the surface "
         "to test cure, concentrating. Bright Ghana afternoon light, long shadow. Photograph."),

        ("{trigger}, warm dark brown skin, close-cropped hair. "
         "Standing at a postal scale, spooning dry laterite soil into a bowl, "
         "adjusting a stabilizer mix. Outdoor workshop, West African morning light. Photograph."),

        ("{trigger}, warm dark brown skin, lean build, slight stubble. "
         "Walking a building site with a client, gesturing at a half-risen compressed earth block wall, "
         "explaining something. Bright midday sun, both squinting slightly. Photograph."),
    ],

    "Lena Hartmann": [
        ("{trigger}, reddish-brown shoulder-length hair, light freckled skin, blue-gray eyes. "
         "Crouching at the base of an old pisé wall, photographing the texture close "
         "with a macro lens, field notebook open on the ground beside her. "
         "Anti-Atlas afternoon light, warm and flat. Photograph."),

        ("{trigger}, reddish-brown hair, freckled, oval face. "
         "Scraping a mortar sample from an ancient earthen wall with a palette knife, "
         "collecting it carefully in a small glass jar she holds in the other hand. "
         "Narrow alley shade, cool indirect light. Photograph."),

        ("{trigger}, reddish-brown hair, blue-gray eyes, fine features. "
         "Sitting cross-legged on a rooftop at dusk with her laptop open, "
         "drawing over a photograph of a floor plan, the Anti-Atlas ridgeline behind her. "
         "Golden evening light. Photograph."),

        ("{trigger}, reddish-brown shoulder-length hair, light freckled skin. "
         "Standing at the top of a rammed earth formwork, watching workers tamp a layer below, "
         "one hand shading her eyes, the other holding a folded drawing. "
         "Bright afternoon sun, Moroccan sky. Photograph."),

        ("{trigger}, reddish-brown hair, oval face, narrow nose. "
         "Walking a narrow village alley with a local Amazigh woman, "
         "both looking up at a cracked earthen parapet overhead. "
         "Dappled alley shade, warm light. Photograph."),
    ],

    "Tom Westhall": [
        ("{trigger}, deeply weathered tan face, salt-and-pepper stubble, square jaw. "
         "Treading cob barefoot on a tarp, both feet working straw deep into a clay-rich mix, "
         "arms loose at his sides, rhythmic. Overcast Oregon sky behind him. Photograph."),

        ("{trigger}, weathered face, salt-and-pepper stubble, blue eyes. "
         "On his knees applying a thin clay slip coat to a cob wall section, "
         "both hands flat against the surface, pressing it smooth. "
         "Soft overcast Pacific Northwest morning light. Photograph."),

        ("{trigger}, weathered tan face, square jaw, broad forehead, crow's feet. "
         "Leaning against a finished cob wall, running his palm slowly along the lime plaster, "
         "assessing it. Willamette Valley afternoon, soft diffuse light. Photograph."),

        ("{trigger}, deeply weathered face, salt-and-pepper stubble. "
         "Cutting a straw bale with an electric chainsaw to fit a curved wall section, "
         "sawdust and chaff in the air. Barn interior, open door light. Photograph."),

        ("{trigger}, weathered tan face, broad forehead, blue eyes. "
         "Sitting on an overturned bucket in a half-built cob workshop at dusk, "
         "writing in a dog-eared notebook by headlamp. Soft evening light. Photograph."),
    ],

    "Rosa Mendez": [
        ("{trigger}, medium warm brown skin, dark hair pulled back tightly, full lips, round face. "
         "Weaving thin bamboo splits between structural bamboo poles with both hands, "
         "building up a wattle panel. Dappled tropical morning light through a palm canopy. Photograph."),

        ("{trigger}, medium warm brown skin, dark brown eyes, round soft face. "
         "Pressing a handful of wet clay daub into a wattle panel with both palms, "
         "smoothing it flat and even. Outdoor morning light, humid air. Photograph."),

        ("{trigger}, medium warm brown skin, dark hair pulled back, full lips. "
         "Standing in front of a circle of women, rolling a ball of clay between her palms "
         "to demonstrate a soil test, looking at the group. "
         "Open-air shade, soft tropical morning light. Photograph."),

        ("{trigger}, medium warm brown skin, round face, dark brown eyes. "
         "Kneeling at a riverbank, machete set aside, testing the clay content of exposed soil "
         "by pressing and rolling it between her fingers, examining it closely. "
         "Low tropical morning sun, river glare. Photograph."),

        ("{trigger}, medium warm brown skin, dark hair, slight cheek fullness. "
         "Standing back from a newly plastered exterior wall, wiping red clay from both forearms "
         "with a cloth, looking at the wall surface. Osa Peninsula afternoon light. Photograph."),
    ],

    "Mei Lin": [
        ("{trigger}, short practical dark black hair, warm tan skin, round face, broad nose. "
         "Measuring wall thickness with a steel tape, pencil in her mouth, "
         "marking a number on a clipboard sketch. Warm tropical interior light. Photograph."),

        ("{trigger}, short dark hair, warm tan skin, dark almond-shaped eyes. "
         "Pulling a soil auger core from the ground, holding the tube up to read the layers "
         "in the sunlight, squinting slightly. Rural Mindanao noon light. Photograph."),

        ("{trigger}, short practical dark hair, round face, wide cheekbones. "
         "Mixing clay and rice hull ash in a large bucket with a wooden paddle, "
         "leaning into the work. Interior light through an open wall. Photograph."),

        ("{trigger}, short dark hair, warm tan skin, dark almond eyes. "
         "Explaining something to an older village woman with careful hand gestures, "
         "both standing in front of an unfinished earthen block wall. "
         "Soft overcast tropical light. Photograph."),

        ("{trigger}, short practical dark hair, round face. "
         "Walking a finished earthen structure alone, running one hand slowly along the interior "
         "plaster wall as she goes, assessing it. Warm interior light. Photograph."),
    ],

    "Elena Vasquez": [
        ("{trigger}, deep copper-brown skin, very prominent cheekbones, silver-streaked black hair, strong nose. "
         "On her knees applying mica-flecked mud plaster to an interior adobe wall with bare hands "
         "and a sheepskin pad, face close to the surface. "
         "High desert afternoon light through a small window. Photograph."),

        ("{trigger}, deep copper-brown skin, strong angular face, prominent cheekbones. "
         "Mixing a small batch of traditional adobe mud in a bucket, adding water slowly "
         "from a cup, watching the consistency change. Outdoor morning shade, cool desert air. Photograph."),

        ("{trigger}, deep copper-brown skin, silver-streaked black hair, dark brown eyes. "
         "Standing outside a pale adobe wall in harsh noon sun, looking up at a hairline crack "
         "that needs repair, one hand resting flat against the warm wall. "
         "High desert noon, full overhead sun. Photograph."),

        ("{trigger}, deep copper-brown skin, prominent cheekbones, strong nose. "
         "Teaching a teenage girl how to burnish dried plaster with a smooth river stone, "
         "guiding her hands from behind, both focused on the wall. "
         "Warm interior light. Photograph."),

        ("{trigger}, deep copper-brown skin, strong angular face, silver-streaked hair. "
         "Sitting at a low wooden table with an elder, both looking at old photographs "
         "of the village spread between them. Quiet interior light. Photograph."),
    ],

    "Amara Diallo": [
        ("{trigger}, very dark brown skin, broad face, strong heavy brow, prominent forehead. "
         "Standing on scaffold beside a rising banco wall, one arm raised directing workers below, "
         "looking down. Bright West African afternoon light, slight dust haze. Photograph."),

        ("{trigger}, very dark brown skin, broad face, wide nose, close-cropped hair. "
         "Pressing both thumbs deep into a fresh banco surface to test plasticity, "
         "frowning slightly in concentration. Outdoor midday light. Photograph."),

        ("{trigger}, very dark brown skin, strong heavy brow, broad face. "
         "Tamping a foundation trench with a heavy wooden tamper, both hands on the handle, "
         "focused and rhythmic, dust rising at each strike. "
         "West African morning light, long shadow. Photograph."),

        ("{trigger}, very dark brown skin, prominent forehead, close-cropped hair. "
         "Squatting beside a pile of fresh banco balls, rolling one between his large palms, "
         "testing moisture and consistency. Outdoor shade, warm diffuse light. Photograph."),

        ("{trigger}, very dark brown skin, broad face, strong brow. "
         "In the shade of a neem tree, reviewing hand-drawn building plans with two younger men, "
         "tracing a line on the paper with one finger. "
         "Thiès afternoon, filtered tree shade. Photograph."),
    ],

    "Marcus Webb": [
        ("{trigger}, deeply lined weathered face, short gray hair, pale blue eyes, prominent jaw. "
         "Splitting fieldstones with a cold chisel and hammer, working methodically through a pile, "
         "chips flying. Soft overcast Kentucky morning light. Photograph."),

        ("{trigger}, deeply lined face, short gray hair, heavyset build, age spots on his hands. "
         "Mixing mortar in a wheelbarrow with a flat-bladed hoe, alone in the farmyard, "
         "moving it in long slow arcs. Overcast morning light. Photograph."),

        ("{trigger}, deeply lined weathered face, pale blue eyes, prominent jaw. "
         "On one knee inspecting the base of an old stone foundation, scraping away soil "
         "with his fingers, looking closely at the mortar joint. "
         "Soft morning light, damp ground. Photograph."),

        ("{trigger}, short gray hair, deeply lined face, heavyset build. "
         "Leaning against a split-rail fence at the edge of the farm, "
         "looking at a half-built stone structure in the mid-distance, arms crossed. "
         "Overcast Kentucky morning, flat light. Photograph."),

        ("{trigger}, deeply lined face, pale blue eyes, age spots, broad nose. "
         "Sitting on the tailgate of an old pickup truck, wrapping baling twine "
         "around a bundle of tools, slow and methodical. "
         "Farmyard morning, soft grey sky. Photograph."),
    ],

    "Kenji Nakamura": [
        ("{trigger}, dark brown eyes, straight black hair, clean-shaven, narrow oval face, wire-rimmed glasses. "
         "Examining a compressed earth cylinder in a load-testing machine, "
         "pen on his lab notebook, watching the pressure reading. "
         "Soft northern European lab light, fluorescent. Photograph."),

        ("{trigger}, wire-rimmed glasses, narrow face, straight black hair, smooth skin. "
         "Slicing a dried earth sample with a scalpel to examine its cross-section, "
         "face very close, desk lamp angled in from the side. "
         "Lab interior, focused task light. Photograph."),

        ("{trigger}, dark brown eyes, wire-rimmed glasses, clean-shaven, narrow face. "
         "Pipetting water into a graduated cylinder, right hand steady, "
         "left hand steadying the cylinder, eyes on the meniscus. "
         "Lab bench, even overhead light. Photograph."),

        ("{trigger}, straight black hair, wire-rimmed glasses, slim build, smooth skin. "
         "Peering through a microscope eyepiece, one hand on the focus knob, "
         "the other on his notebook. Lab, northern light through a window. Photograph."),

        ("{trigger}, wire-rimmed glasses, narrow oval face, straight black hair. "
         "Standing at a whiteboard covered in material property graphs and equations, "
         "marker in one hand, reading what he's written. "
         "TU Delft lab, soft natural light. Photograph."),
    ],

    "Priya Sharma": [
        ("{trigger}, dark brown skin, black hair with early gray streaks, dark eyes, strong defined brow. "
         "Inside rammed earth formwork, shoveling a measured layer of damp earth "
         "before tamping, working steadily. Harsh Queensland sun overhead. Photograph."),

        ("{trigger}, dark brown skin, strong brow, oval face, black hair with gray. "
         "Holding a paint chip against a freshly stripped rammed earth wall face, "
         "comparing color, squinting. Bright outdoor light, Queensland blue sky. Photograph."),

        ("{trigger}, dark brown skin, dark eyes with strong defined brow, medium build. "
         "Sitting across from an Aboriginal elder under a tree, listening, "
         "notepad open in her lap, pen down. Soft outdoor shade. Photograph."),

        ("{trigger}, dark brown skin, black hair with gray, strong brow, oval face. "
         "Walking a suburban rammed earth building site in hard hat and hi-vis vest, "
         "reviewing something on a clipboard. Harsh clear Queensland sun, long shadow. Photograph."),

        ("{trigger}, dark brown skin, strong brow, black hair with early gray. "
         "Pouring a soil sample through a set of nested sieves, tapping the side "
         "to move material through, watching each layer. "
         "Lab table, even natural light. Photograph."),
    ],

    "Dara Okonkwo": [
        ("{trigger}, deep rich brown skin, natural hair, warm round face, full lips, high cheekbones. "
         "Turning soil in a vacant urban lot with a garden fork, exposing dark fill underneath, "
         "sleeves rolled up. Overcast Detroit morning light. Photograph."),

        ("{trigger}, deep rich brown skin, natural hair, bright expressive dark eyes. "
         "At the front of a small community center room, presenting to a neighborhood group, "
         "earthen brick samples on the table beside her, hands open. "
         "Interior fluorescent light, late afternoon. Photograph."),

        ("{trigger}, deep rich brown skin, natural hair, high cheekbones, full lips. "
         "On her phone at a construction site, one hand gesturing at something in the distance "
         "while she talks, half-turned from the camera. "
         "Overcast Detroit sky, flat grey light. Photograph."),

        ("{trigger}, deep rich brown skin, warm round face, natural hair. "
         "Lifting a fresh earthen brick from a wooden mold, lining it up on a drying pallet, "
         "concentrated and efficient. Outdoor Detroit morning, overcast. Photograph."),

        ("{trigger}, deep rich brown skin, bright eyes, high cheekbones, full lips. "
         "Sitting on the front stoop of a half-finished earthen building with two teenagers, "
         "all three looking at something on her phone, relaxed. "
         "Overcast afternoon light. Photograph."),
    ],

    "Sam Torres": [
        ("{trigger}, warm tan skin, thick dark hair, dark brown eyes, square face, light stubble. "
         "Pressing an adobe brick mix into a wooden mold with both fists, "
         "leaning into it, face concentrated. Harsh Arizona morning sun. Photograph."),

        ("{trigger}, warm tan skin, square face, broad shoulders, light stubble. "
         "Lifting a cured adobe block from a drying row with both hands, "
         "testing its weight and hardness, checking the edges. "
         "Phoenix midday sun, bare yard. Photograph."),

        ("{trigger}, warm tan skin, thick dark hair, dark brown eyes. "
         "Laying adobe blocks in a rising wall, trowel in one hand, "
         "mud mortar bucket beside him. Harsh Arizona sunlight, long morning shadow. Photograph."),

        ("{trigger}, warm tan skin, square face, light stubble. "
         "On the phone, face turned away from the sun, one hand shading his eyes, "
         "looking at a half-built adobe wall while he talks. "
         "Phoenix morning, hard clear light. Photograph."),

        ("{trigger}, warm tan skin, thick dark hair, broad shoulders. "
         "Sitting with an older Mexican man in the shade of a mesquite tree, "
         "both looking at a hand-drawn diagram on paper between them. "
         "Barrio afternoon shade, warm filtered light. Photograph."),
    ],
}

# ── API helpers ────────────────────────────────────────────────────────────────

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

def build_prompt(text, prefix, seed=None, batch_size=1):
    p = deepcopy(WORKFLOW)
    p["6"]["inputs"]["text"]              = text
    p["9"]["inputs"]["filename_prefix"]   = prefix
    p["27"]["inputs"]["batch_size"]       = batch_size
    p["31"]["inputs"]["seed"]             = seed if seed is not None else random.randint(0, 9_999_999_999)
    return p

def send_job(text, prefix, seed=None, batch_size=1, dry_run=False):
    if dry_run:
        seed_str = str(seed) if seed is not None else "random"
        print(f"    [DRY] prefix={prefix}  seed={seed_str}  batch_size={batch_size}")
        print(f"          prompt={text[:80]}...")
        return True
    prompt = build_prompt(text, prefix, seed=seed, batch_size=batch_size)
    result = api_post("/prompt", {"prompt": prompt})
    return bool(result.get("prompt_id"))

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Queue Earthback ComfyUI batches")
    parser.add_argument("--batch",   default=None,
                        help="Which batch(es) to run, comma-separated: "
                             "t5, face, t4, face-front, face-left, t4-02, etc. "
                             "Omit to run ALL batches.")
    parser.add_argument("--char",    default=None,
                        help="Only queue one character by name (e.g. 'James Osei')")
    parser.add_argument("--loops",   type=int, default=1,
                        help="How many times to repeat each batch (default 1). "
                             "Each loop stacks _00002_, _00003_... automatically.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print jobs without sending")
    parser.add_argument("--status",  action="store_true",
                        help="Show queue depth and exit")
    parser.add_argument("--reseed",  action="store_true",
                        help="Ignore character seeds, use fully random seeds (good for getting "
                             "variant looks / curation candidates)")
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Images per job (default 1). 3 is stable and gives similar "
                             "variants from the same seed in one pass.")
    args = parser.parse_args()

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

    print(f"ComfyUI connected — running: {running}  pending: {pending}\n")

    # Resolve which batches to run
    run_t5 = False
    if args.batch is None:
        batches_to_run = list(ALL_BATCHES.keys())
        run_t5 = True
    else:
        requested = [b.strip().lower() for b in args.batch.split(",")]
        if "t5" in requested:
            run_t5 = True
        batches_to_run = []
        for key in ALL_BATCHES:
            # Match "face" → all face-* batches, "t4" → all t4-* batches
            for req in requested:
                if req == key or key.startswith(req + "-") or key == req:
                    if key not in batches_to_run:
                        batches_to_run.append(key)

    if not batches_to_run and not run_t5:
        print(f"No batches matched '{args.batch}'. Available: t5, {', '.join(ALL_BATCHES)}")
        return

    # Resolve which characters
    chars_to_run = CHARS
    if args.char:
        chars_to_run = [c for c in CHARS if c["name"].lower() == args.char.lower()]
        if not chars_to_run:
            print(f"Character '{args.char}' not found.")
            print("Available:", ", ".join(c["name"] for c in CHARS))
            return

    # Queue everything
    total = 0
    ok    = 0

    for loop in range(args.loops):
        if args.loops > 1:
            print(f"=== Loop {loop + 1} of {args.loops} ===")

        for batch_key in batches_to_run:
            batch    = ALL_BATCHES[batch_key]
            is_face  = batch_key in FACE_ANGLE_SEED_OFFSET
            print(f"\n  Batch: {batch['label']}")

            for char in chars_to_run:
                for prefix_tmpl, prompt_tmpl in batch["prompts"]:
                    prefix = prefix_tmpl.format(name=char["name"])
                    text   = prompt_tmpl.format(
                        trigger  = char["trigger"],
                        desc     = char["desc"],
                        name     = char["name"],
                        location = char["location"],
                        light    = char["light"],
                    )

                    # Seed logic:
                    #   Face batches  → char seed + angle offset + loop shift
                    #                   keeps all angles of the same person in the
                    #                   same noise neighborhood
                    #   Other batches → char seed + large batch offset (still
                    #                   character-anchored but varied)
                    #   --reseed      → fully random (curation / exploration)
                    if args.reseed:
                        seed = None
                    elif is_face:
                        angle_offset = FACE_ANGLE_SEED_OFFSET[batch_key]
                        seed = char["seed"] + angle_offset + (loop * 100)
                    else:
                        # scenario batches: char-anchored but shifted well away from faces
                        batch_idx = list(SCENARIO_BATCHES.keys()).index(batch_key) if batch_key in SCENARIO_BATCHES else 0
                        seed = char["seed"] + 1000 + (batch_idx * 50) + (loop * 100)

                    success = send_job(text, prefix, seed=seed, batch_size=args.batch_size, dry_run=args.dry_run)
                    status  = "✓" if success else "✗ FAILED"
                    print(f"    {status}  {char['name']}  [{batch_key}]")
                    if success:
                        ok += 1
                    total += 1
                    if not args.dry_run:
                        time.sleep(STAGGER_MS / 1000)

    # ── T5 per-character scenes ──
    if run_t5:
        print(f"\n  Batch: T5 — character-specific literal scenes")
        for char in chars_to_run:
            scenes = T5_SCENES.get(char["name"], [])
            if not scenes:
                print(f"    ⚠  No T5 scenes defined for {char['name']}")
                continue
            for loop in range(args.loops):
                for i, scene_prompt in enumerate(scenes):
                    prefix = f"chars-{char['name']}-T5-{i+1:02d}"
                    # T5 prompts are already fully written — just substitute trigger
                    text = scene_prompt.replace("{trigger}", char["trigger"])
                    if args.reseed:
                        seed = None
                    else:
                        seed = char["seed"] + 2000 + (i * 10) + (loop * 100)
                    success = send_job(text, prefix, seed=seed, batch_size=args.batch_size, dry_run=args.dry_run)
                    status_str = "✓" if success else "✗ FAILED"
                    print(f"    {status_str}  {char['name']}  [T5-{i+1:02d}]")
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
