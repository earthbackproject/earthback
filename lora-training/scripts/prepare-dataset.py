"""
Earthback LoRA Dataset Preparation Script
==========================================
Scans comfyui-output, copies images for each character into their
lora-training/datasets/<char>/images/ folder, and writes matching .txt
caption files in Kohya SS format.

Run from: C:\users\adrxi\Earthback\lora-training\scripts\
Usage:    python prepare-dataset.py [--dry-run] [--char james-osei]

Options:
  --dry-run     Print actions without copying anything
  --char NAME   Only process one character (use slug, e.g. james-osei)
  --min 10      Only copy characters with >= N images (default: 10)

Caption format: TRIGGER_WORD, [scene description without character identity]
Kohya SS reads the .txt file that matches each image filename.
"""

import os
import shutil
import argparse
import re
from pathlib import Path

# ─── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(r"C:\users\adrxi\Earthback")
COMFY_OUTPUT  = BASE_DIR / "comfyui-output"
DATASET_ROOT  = BASE_DIR / "lora-training" / "datasets"

# ─── CHARACTER DATA ───────────────────────────────────────────────────────────
# Keys match the ComfyUI prefix pattern: "T[N]-chars-[Name]-[sub]"
# Captions: trigger_word + scene (no character identity description —
#   that's what the trigger word learns to encode)

CHARACTERS = {
    "james-osei": {
        "trigger":      "JAMES_OSEI_EB",
        "prefix_match": "James Osei",
        "captions": {
            "T1": "JAMES_OSEI_EB, full-length documentary portrait, Kumasi Ghana hempcrete construction site, Accra region, afternoon West African light, practical work clothes, confident direct gaze, red laterite earth, 35mm documentary photography",
            "T2": "JAMES_OSEI_EB, mixing hempcrete in a large drum with a paddle, physical work, West African midday sun, shipping container workshop visible behind, red earth, work clothes, 35mm photojournalism",
            "T3": "JAMES_OSEI_EB, standing inside a partially completed hempcrete structure, inspecting the walls, warm West African afternoon light filtering through the formwork gaps, earthy interior, 35mm documentary",
            "T4-01": "JAMES_OSEI_EB, close-up of hands pressing into hempcrete mix, texture of hemp hurd and lime binder, warm West African foreground light, shallow depth of field, detail shot",
            "T4-02": "JAMES_OSEI_EB, standing in front of a shipping container converted into a workshop classroom, Accra region Ghana, bright West African midday light, dark t-shirt, cargo pants, red earth, tools visible, medium shot",
            "T4-03": "JAMES_OSEI_EB, demonstrating hempcrete mixing technique to a group of young Ghanaian trainees outdoors, hands deep in the mix, explaining, red laterite earth, West African midday light, energetic, 35mm photojournalism",
            "T4-04": "JAMES_OSEI_EB, standing at a distance watching trainees build a hempcrete wall, arms crossed, quietly proud, wide shot, shipping container classroom, red earth, five or six trainees working, West African afternoon light",
            "T4-05": "JAMES_OSEI_EB, writing on a whiteboard inside the shipping container classroom, mid-sentence, marker in hand, trainee visible at edge of frame, West African afternoon light, energetic teaching moment",
        }
    },
    "lena-hartmann": {
        "trigger":      "LENA_HARTMANN_EB",
        "prefix_match": "Lena Hartmann",
        "captions": {
            "T1": "LENA_HARTMANN_EB, full-length documentary portrait, Tafraoute Morocco, Anti-Atlas mountains, pink granite, cob wall beside her, reddish-brown hair tied back, practical clothes, earth on hands, afternoon light, 35mm documentary",
            "T2": "LENA_HARTMANN_EB, placing a course of damp cob onto a wall, tamping with hands, physical effort, golden hour Morocco, Anti-Atlas mountains background, practical clothes, earth on arms, 35mm photojournalism",
            "T3": "LENA_HARTMANN_EB, sitting on a low wall outside a completed cob home at dusk, Tafraoute Morocco, pink granite village, warm lantern light, peaceful, reflective, 35mm documentary",
            "T4-01": "LENA_HARTMANN_EB, close-up of one hand pressed against finished cob wall surface, Tafraoute Morocco, afternoon light raking across the wall texture, earth tones, shallow depth of field, detail shot",
            "T4-02": "LENA_HARTMANN_EB, standing next to her first cob wall in Tafraoute Morocco, Anti-Atlas mountains behind, pink granite, blue sky, practical clothes, hands showing dried earth, earned confidence, documentary portrait, natural light",
            "T4-03": "LENA_HARTMANN_EB, foot-mixing cob on a tarp on dry Moroccan earth, hemp fiber, clay soil, water, full physical effort, Anti-Atlas mountains visible, worn practical clothes, earth on arms and legs, golden hour Morocco",
            "T4-04": "LENA_HARTMANN_EB, crouching and examining the surface of a cob wall, running hand along it, Tafraoute Morocco, pink granite rock formations, late afternoon light, wall fills right frame, wide to show full wall height",
            "T4-05": "LENA_HARTMANN_EB, tamping a new course of cob onto a wall with a wooden tamping tool, visible physical effort, both hands on the tool, Tafraoute Morocco, golden morning light on the wall surface, earth and hemp fiber visible",
        }
    },
    "tom-westhall": {
        "trigger":      "TOM_WESTHALL_EB",
        "prefix_match": "Tom Westhall",
        "captions": {
            "T1": "TOM_WESTHALL_EB, three-quarter portrait, standing in a hemp field, Willamette Valley Oregon, overcast Pacific Northwest sky, worn canvas jacket, flannel shirt, salt-and-pepper stubble, weathered face, direct expression, 35mm documentary",
            "T2": "TOM_WESTHALL_EB, operating a hemp decortication machine in an Oregon barn, overcast light through barn doors, hay dust in the air, canvas jacket off, flannel shirt, focused and skilled, 35mm photojournalism",
            "T3": "TOM_WESTHALL_EB, leaning against a wooden fence at the edge of his hemp field, overcast Oregon evening, canvas jacket, hands in pockets, large field stretching behind him, quiet and patient, 35mm documentary",
            "T4-01": "TOM_WESTHALL_EB, close portrait, squinting slightly in overcast Oregon light, one hand holding a hemp stalk, half-smile, salt-and-pepper stubble, tight head-and-shoulders, shallow depth of field",
            "T4-02": "TOM_WESTHALL_EB, standing in a hemp field in late summer, Willamette Valley Oregon, overcast Pacific Northwest light, worn canvas jacket, flannel underneath, calm direct expression, tall hemp stalks slightly blurred background, shallow depth of field",
            "T4-03": "TOM_WESTHALL_EB, kneeling in a hemp field examining harvested stalks, checking fiber quality, hands working through the material, Willamette Valley Oregon, overcast light, late summer, canvas jacket, flannel, close working shot",
            "T4-04": "TOM_WESTHALL_EB, walking a row between tall hemp plants 3-4 meters high, seen from the side, small figure in a large field, Willamette Valley Oregon, overcast Pacific Northwest sky, wide shot showing scale of hemp crop",
            "T4-05": "TOM_WESTHALL_EB, sitting on the back of a pickup truck at the edge of his hemp field, both hands on knees, looking at the crop, Oregon overcast morning light, canvas jacket, boots, the expression of someone who has been doing this for twenty years",
        }
    },
    "rosa-mendez": {
        "trigger":      "ROSA_MENDEZ_EB",
        "prefix_match": "Rosa Mendez",
        "captions": {
            "T1": "ROSA_MENDEZ_EB, medium documentary portrait, Osa Peninsula Costa Rica, inside a bamboo structure under construction, dark hair pulled back, practical clothes, measuring tape on belt, tropical dappled light, bamboo frame visible, 35mm documentary",
            "T2": "ROSA_MENDEZ_EB, lashing a bamboo joint with cord at height, on scaffolding, focused upward, Osa Peninsula Costa Rica, tropical morning light through bamboo, practical clothes, skilled and sure, 35mm photojournalism",
            "T3": "ROSA_MENDEZ_EB, standing in front of a completed bamboo community structure at sunset, Osa Peninsula Costa Rica, tropical forest behind, full building visible, proud and calm, 35mm documentary",
            "T4-01": "ROSA_MENDEZ_EB, close-up of hands holding a bamboo joint model, pencil marks and measurements visible on the bamboo, tropical morning light, shallow depth of field",
            "T4-02": "ROSA_MENDEZ_EB, standing in partial shade of a bamboo structure under construction, Osa Peninsula Costa Rica, tropical humid light, dappled, practical clothes, measuring tape on belt, bamboo frame in process behind her",
            "T4-03": "ROSA_MENDEZ_EB, sketching structural bamboo joint details at a rough outdoor table, bamboo culms stacked nearby, tropical forest edge, Osa Peninsula Costa Rica, morning light, papers on table, measuring tape visible, focused and skilled",
            "T4-04": "ROSA_MENDEZ_EB, standing inside a completed bamboo structure looking up at the roof geometry, culms and joints visible against tropical sky, small figure inside large bamboo frame, dappled tropical light, green forest visible, wide architectural shot",
            "T4-05": "ROSA_MENDEZ_EB, on a ladder inside a bamboo structure connecting a joint with lashing cord, focused upward, dappled tropical light from above, Osa Peninsula Costa Rica, working at height, skilled and sure",
        }
    },
    "mei-lin": {
        "trigger":      "MEI_LIN_EB",
        "prefix_match": "Mei Lin",
        "captions": {
            "T1": "MEI_LIN_EB, medium documentary portrait, rural Mindanao Philippines, bamboo community hall interior, short dark hair, practical clothes, warm light, thoughtful expression, hand-drawn land map visible on wall behind her, 35mm documentary",
            "T2": "MEI_LIN_EB, presenting at a community meeting, hand-drawn maps pinned to bamboo wall, standing, pointing to the map, engaged and clear, eight community members listening, rural Mindanao, warm interior light, 35mm photojournalism",
            "T3": "MEI_LIN_EB, walking a newly cleared site with two elders, rural Mindanao Philippines, tropical late afternoon light, clipboard in hand, serious conversation, community members alongside, 35mm documentary",
            "T4-01": "MEI_LIN_EB, mid-conversation close portrait, speaking, engaged expression, warm interior light from bamboo hall, rural Mindanao, tight head-and-shoulders, candid, purposeful",
            "T4-02": "MEI_LIN_EB, standing at a community meeting in rural Mindanao Philippines, hand-drawn land map on large sheet behind her, natural light, practical clothes, the kind of person who runs the meeting, documentary portrait",
            "T4-03": "MEI_LIN_EB, in conversation with two community members seated around a hand-drawn land map on a table, pointing to something on the map, bamboo hall interior, warm light, engaged, clear, purposeful, rural Mindanao Philippines",
            "T4-04": "MEI_LIN_EB, standing outside a half-built bamboo community hall, clipboard in hand, talking with a small group of community members, rural Mindanao, bamboo scaffold visible, late afternoon tropical light, wide shot showing community hall and landscape",
            "T4-05": "MEI_LIN_EB, facilitating an outdoor community meeting, eight or ten people in a circle, standing, holding a marker and large paper, rural Mindanao Philippines, evening light, engaged and in command, wide photojournalism style",
        }
    },
    "elena-vasquez": {
        "trigger":      "ELENA_VASQUEZ_EB",
        "prefix_match": "Elena Vasquez",
        "captions": {
            "T1": "ELENA_VASQUEZ_EB, full-length documentary portrait, Pueblo of Acoma New Mexico, high desert landscape, adobe structures visible, plain dark jacket, strong direct gaze, patient authoritative presence, late afternoon golden hour light, 35mm documentary",
            "T2": "ELENA_VASQUEZ_EB, supervising rammed earth wall construction, standing beside timber formwork, directing two younger workers, Pueblo of Acoma New Mexico, high desert afternoon light, plain dark jacket, 35mm photojournalism",
            "T3": "ELENA_VASQUEZ_EB, standing at the edge of the mesa at dusk, overlooking completed rammed earth foundations, Acoma Pueblo New Mexico, high desert sky, adobe structures, deep blue evening, plain dark jacket, 35mm documentary",
            "T4-01": "ELENA_VASQUEZ_EB, close-up of hand on a rammed earth wall surface, strong hand against red-brown earth, high desert afternoon light, dust in air, macro detail, shallow depth of field",
            "T4-02": "ELENA_VASQUEZ_EB, standing outside at Acoma Pueblo New Mexico, mesa landscape, adobe structures, high desert light, simple practical clothing, direct gaze, patient, authoritative, late afternoon golden hour, deep blue sky with clouds",
            "T4-03": "ELENA_VASQUEZ_EB, running hand along a freshly poured rammed earth wall, assessing the surface, construction site Pueblo of Acoma New Mexico, plain dark jacket, an older Pueblo woman beside her, both examining the wall, high desert afternoon light",
            "T4-04": "ELENA_VASQUEZ_EB, standing at the edge of a construction site overlooking three building foundations on the mesa, Pueblo of Acoma New Mexico, adobe structures and high desert landscape visible, plain dark jacket, wide shot, small figure in large landscape, golden hour",
            "T4-05": "ELENA_VASQUEZ_EB, reviewing construction drawings unrolled on a truck hood, holding one corner down in wind, Acoma Pueblo site, high desert light, plain dark jacket, another person's hands visible at far edge, working, practical",
        }
    },
    "amara-diallo": {
        "trigger":      "AMARA_DIALLO_EB",
        "prefix_match": "Amara Diallo",
        "captions": {
            "T1": "AMARA_DIALLO_EB, medium documentary portrait, Thiès Senegal rammed earth construction site, strong hands, calm mastery in expression, work clothes, West African afternoon light, red earth and formwork visible, 35mm documentary",
            "T2": "AMARA_DIALLO_EB, tamping earth into timber formwork with a hand tamper, arms raised, physical effort visible, rammed earth construction, Thiès Senegal, West African afternoon light on red earth, assistants working beside him, 35mm photojournalism",
            "T3": "AMARA_DIALLO_EB, standing outside a completed rammed earth compound, Thiès Senegal, West African late afternoon light, long shadows, hands at sides, quiet satisfaction, 35mm documentary",
            "T4-01": "AMARA_DIALLO_EB, extreme close-up of hands performing the soil ribbon test, rolling damp earth between thumb and fingers, the ribbon forming, Senegal afternoon light, detail shot",
            "T4-02": "AMARA_DIALLO_EB, standing in front of a rammed earth structure in Thiès Senegal, strong hands, calm mastery in expression, bright West African afternoon light, slight dust, work clothes, documentary photography, warm tones",
            "T4-03": "AMARA_DIALLO_EB, performing the soil ribbon test, rolling damp earth between fingers to test clay content, close-up on hands and concentration, Thiès Senegal, afternoon light, detail-focused photojournalism",
            "T4-04": "AMARA_DIALLO_EB, directing two younger builders at a rammed earth construction site, gesturing at the formwork, wide shot showing the compound under construction, Thiès Senegal, West African landscape, late afternoon dust and light",
            "T4-05": "AMARA_DIALLO_EB, packing earth into timber formwork with a hand tamper, arms raised, physical effort visible, rammed earth construction, Thiès Senegal, West African afternoon light on red earth, two assistants working beside him",
        }
    },
    "marcus-webb": {
        "trigger":      "MARCUS_WEBB_EB",
        "prefix_match": "Marcus Webb",
        "captions": {
            "T1": "MARCUS_WEBB_EB, medium documentary portrait, Eastern Kentucky farmland, hempcrete wall he built himself visible beside him, gray hair, reading glasses pushed up, flannel shirt, work boots, morning light, overcast, quiet pride, 35mm documentary",
            "T2": "MARCUS_WEBB_EB, installing hempcrete block into a wall cavity, kneeling, focused, Eastern Kentucky, overcast morning, flannel sleeves rolled up, the careful precision of an engineer, 35mm photojournalism",
            "T3": "MARCUS_WEBB_EB, sitting on the porch of his completed hempcrete home, Eastern Kentucky farmland, overcast afternoon, flannel shirt, coffee mug in hand, looking out at the land, quiet and satisfied, 35mm documentary",
            "T4-01": "MARCUS_WEBB_EB, close portrait reading a technical spec sheet, concentration, slight skepticism, reading glasses on, Eastern Kentucky morning light, tight head-and-shoulders, candid",
            "T4-02": "MARCUS_WEBB_EB, standing beside a hempcrete wall he built himself, Eastern Kentucky farmland, morning light, overcast, flannel shirt, work boots, gray hair, reading glasses pushed up, quiet pride without posing, documentary photography",
            "T4-03": "MARCUS_WEBB_EB, using a rebound hammer to test the hardness of a hempcrete wall, Eastern Kentucky, overcast morning, flannel shirt, gray hair, reading glasses on, the expression of a skeptic being proved right by data, slightly wry",
            "T4-04": "MARCUS_WEBB_EB, standing back from his nearly completed house — hempcrete walls, standing seam metal roof, solar panels — arms crossed, looking at it, Eastern Kentucky farmland, overcast sky, wide shot showing full house, quiet pride",
            "T4-05": "MARCUS_WEBB_EB, mixing hempcrete in a large trough, wooden paddle in both hands, forearms showing effort, Eastern Kentucky morning light, flannel sleeves rolled up, the expression of someone surprised to find themselves enjoying this",
        }
    },
    "kenji-nakamura": {
        "trigger":      "KENJI_NAKAMURA_EB",
        "prefix_match": "Kenji Nakamura",
        "captions": {
            "T1": "KENJI_NAKAMURA_EB, medium documentary portrait, TU Delft materials lab, holding a mycelium composite panel sample, off-white fibrous organic surface, northern European lab light, clean large windows, curious and careful expression, 35mm documentary",
            "T2": "KENJI_NAKAMURA_EB, inoculating a mycelium substrate tray in the lab, precise and methodical, gloves on, TU Delft, north window light, lab bench with multiple substrate samples, 35mm photojournalism",
            "T3": "KENJI_NAKAMURA_EB, presenting research findings to a small audience in a TU Delft seminar room, standing beside a projected slide showing mycelium composite test results, engaged and clear, 35mm documentary",
            "T4-01": "KENJI_NAKAMURA_EB, close-up of hands holding a finished mycelium composite sample, pale, fibrous, slightly rough surface, lab light from large north windows, TU Delft, shallow depth of field",
            "T4-02": "KENJI_NAKAMURA_EB, in a materials lab in Delft Netherlands, holding a mycelium composite panel sample, off-white, slightly textured, organic, northern European lab light, clean but not sterile, precise and slightly reserved, small smile",
            "T4-03": "KENJI_NAKAMURA_EB, carefully placing a mycelium composite sample into a compression testing apparatus in a materials lab, Delft Netherlands, focused, methodical, lab bench with multiple labeled sample containers, north window light",
            "T4-04": "KENJI_NAKAMURA_EB, at a bench covered with mycelium substrate samples in various stages of growth, some dark and growing, some finished and pale, writing notes, surrounded by research, TU Delft lab, large north-facing windows, afternoon light",
            "T4-05": "KENJI_NAKAMURA_EB, presenting a mycelium composite sample to two colleagues in the lab, holding it up in the light for them to see, TU Delft, north-facing windows, engaged collegial conversation, afternoon",
        }
    },
    "priya-sharma": {
        "trigger":      "PRIYA_SHARMA_EB",
        "prefix_match": "Priya Sharma",
        "captions": {
            "T1": "PRIYA_SHARMA_EB, medium documentary portrait, Queensland Australia, standing on the ground beside a hempcrete home, standing seam metal roof with solar panels visible above, bright Australian sun, work clothes, tool belt, direct practical expression, 35mm documentary",
            "T2": "PRIYA_SHARMA_EB, on a roof installing a solar panel rail bracket with a power driver, crouching, focused, Queensland strong sun, blue sky, work clothes, tool belt, completely at ease at height, 35mm photojournalism",
            "T3": "PRIYA_SHARMA_EB, reviewing a completed solar installation from ground level at dusk, Queensland, the hempcrete home behind her with full solar array lit by setting sun, arms crossed, satisfied, 35mm documentary",
            "T4-01": "PRIYA_SHARMA_EB, close-up of hands connecting a solar panel clip to a standing seam metal roof, tool in hand, seam detail visible, Queensland strong light, detail shot",
            "T4-02": "PRIYA_SHARMA_EB, standing on a standing seam metal roof of a hempcrete home in Queensland Australia, solar panels behind her, clip-mounted, bright Australian sun, harsh and clear, work clothes, completely at ease at height, intense Queensland blue sky",
            "T4-03": "PRIYA_SHARMA_EB, crouching on a standing seam metal roof clipping a solar panel mount to the seam, zero penetrations, clip-only connection, hands working on the detail, focused, Queensland blue sky above, work clothes, tool belt",
            "T4-04": "PRIYA_SHARMA_EB, standing at ground level reviewing a solar system spec sheet, the completed off-grid hempcrete home behind her, standing seam roof with full solar array visible, Queensland landscape, wide shot, afternoon light",
            "T4-05": "PRIYA_SHARMA_EB, on the roof laying out solar panel grid layout with chalk lines on standing seam, kneeling, planning the installation, Queensland strong sun, tool belt, practical precision",
        }
    },
    "dara-okonkwo": {
        "trigger":      "DARA_OKONKWO_EB",
        "prefix_match": "Dara Okonkwo",
        "captions": {
            "T1": "DARA_OKONKWO_EB, medium documentary portrait, Detroit vacant lot, straw bale wall frame under construction visible behind, overcast Midwest sky, practical clothing, clipboard in hand, sharp and warm expression, 35mm documentary",
            "T2": "DARA_OKONKWO_EB, leading a community meeting on a vacant lot, standing, animated, eight residents seated in a circle on folding chairs, Detroit, brick buildings behind, overcast sky, site plan on the ground, 35mm photojournalism",
            "T3": "DARA_OKONKWO_EB, standing inside a completed straw bale home, Detroit, looking around at the finished plaster walls, afternoon light through large windows, quiet satisfaction, 35mm documentary",
            "T4-01": "DARA_OKONKWO_EB, close-up of hands holding a site plan on a clipboard, pencil markings visible, Detroit overcast light, one finger pointing to something on the plan",
            "T4-02": "DARA_OKONKWO_EB, standing on a vacant lot in Detroit mid-transformation, straw bale wall frames visible, foundation poured nearby, Detroit urban landscape — brick buildings, empty lots, overcast Midwest sky, practical clothing, direct, purposeful",
            "T4-03": "DARA_OKONKWO_EB, showing a hand-drawn site plan to two Detroit residents on a vacant lot, straw bale wall frames under construction visible behind them, overcast Midwest sky, pointing at something on the plan, animated and clear",
            "T4-04": "DARA_OKONKWO_EB, standing at a distance looking at three adjacent vacant lots in different stages of construction, one framed, one foundation, one still cleared earth, Detroit street, brick buildings, overcast sky, wide shot, small figure in urban landscape",
            "T4-05": "DARA_OKONKWO_EB, standing on a completed straw bale wall foundation, talking to a group of eight people below, slightly elevated, holding papers, Detroit vacant lot, brick buildings behind, overcast sky, leadership and momentum",
        }
    },
    "sam-torres": {
        "trigger":      "SAM_TORRES_EB",
        "prefix_match": "Sam Torres",
        "captions": {
            "T1": "SAM_TORRES_EB, medium documentary portrait, Phoenix Arizona, outside a large construction 3D printer, desert workshop, dark hair, work clothes with dried hempcrete, harsh Arizona light, critical and engaged expression, 35mm documentary",
            "T2": "SAM_TORRES_EB, calibrating the extrusion head of a large construction 3D printer, crouching, tablet in hand showing the print path, Phoenix Arizona workshop, harsh desert light, focused and technical, 35mm photojournalism",
            "T3": "SAM_TORRES_EB, standing back looking at a completed section of 3D-printed hempcrete wall, arms crossed, Arizona desert workshop, late afternoon sun catching the extruded layers, satisfied assessment, 35mm documentary",
            "T4-01": "SAM_TORRES_EB, close portrait examining a 3D printer nozzle detail, critical expression, focused, Arizona workshop harsh light, tight head-and-shoulders, candid",
            "T4-02": "SAM_TORRES_EB, crouching beside the extrusion head of a large 3D construction printer in a desert workshop, Phoenix Arizona, printer mid-print, hempcrete in visible layers, harsh Arizona sunlight, work clothes with dried hempcrete, excited but professional",
            "T4-03": "SAM_TORRES_EB, leaning in close inspecting the surface of a freshly 3D-printed hempcrete wall, visible extruded layers, slightly rough texture, Phoenix Arizona workshop, harsh light, hands on wall surface, expression of critical assessment",
            "T4-04": "SAM_TORRES_EB, standing back from the large industrial construction 3D printer, arms crossed, looking at a completed wall section it has printed, desert workshop, sand floor, Arizona sunlight, wide shot showing full printer scale and printed wall",
            "T4-05": "SAM_TORRES_EB, loading hempcrete material into the printer hopper, effort visible, one foot on the machine for leverage, Phoenix Arizona workshop, strong Arizona light, practical work, no glamour",
        }
    },
}

# ─── PREFIX → CAPTION KEY MAPPING ─────────────────────────────────────────────
def get_caption_key(filename: str) -> str | None:
    """
    Map a ComfyUI output filename to a caption key.
    Examples:
      EB-fp-01-social media-T1-chars-James Osei-01_00001_.png  → T1
      EB-fp-01-social media-T4-chars-James Osei-03_00002_.png  → T4-03
    """
    # Match T1/T2/T3
    m = re.search(r'-T([123])-chars-', filename)
    if m:
        return f"T{m.group(1)}"
    # Match T4-XX
    m = re.search(r'-T4-chars-[^-]+-(\d+)_', filename)
    if m:
        return f"T4-{m.group(1).zfill(2)}"
    return None


def get_char_slug(filename: str) -> str | None:
    """Map a filename to a character slug."""
    for slug, data in CHARACTERS.items():
        if data["prefix_match"] in filename:
            return slug
    return None


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Prepare Earthback LoRA dataset")
    parser.add_argument("--dry-run", action="store_true", help="Print only, no file operations")
    parser.add_argument("--char", default=None, help="Only process one character slug")
    parser.add_argument("--min", type=int, default=10, help="Min images to include a character (default 10)")
    args = parser.parse_args()

    if not COMFY_OUTPUT.exists():
        print(f"ERROR: comfyui-output not found at {COMFY_OUTPUT}")
        return

    # Collect images per character
    char_images: dict[str, list[Path]] = {slug: [] for slug in CHARACTERS}

    for img in COMFY_OUTPUT.glob("*.png"):
        slug = get_char_slug(img.name)
        if slug and (args.char is None or args.char == slug):
            char_images[slug].append(img)

    print("\n=== IMAGE COUNTS ===")
    for slug, imgs in char_images.items():
        status = "✓" if len(imgs) >= args.min else "✗ (below min)"
        print(f"  {slug:<20} {len(imgs):>3} images  {status}")

    print("\n=== PROCESSING ===")
    total_copied = 0
    total_captions = 0
    missing_captions = []

    for slug, imgs in char_images.items():
        if args.char and args.char != slug:
            continue
        if len(imgs) < args.min:
            print(f"  SKIP {slug} — only {len(imgs)} images (need {args.min})")
            continue

        dest_dir = DATASET_ROOT / slug / "images"
        if not args.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        char_data = CHARACTERS[slug]
        print(f"\n  {slug} ({len(imgs)} images → {dest_dir})")

        for img in sorted(imgs):
            caption_key = get_caption_key(img.name)
            caption = char_data["captions"].get(caption_key)

            if not caption:
                missing_captions.append((slug, img.name, caption_key))
                print(f"    ⚠ NO CAPTION for {img.name} (key={caption_key})")
                continue

            dest_img  = dest_dir / img.name
            dest_txt  = dest_dir / (img.stem + ".txt")

            if args.dry_run:
                print(f"    [DRY] {img.name} → caption key: {caption_key}")
            else:
                shutil.copy2(img, dest_img)
                dest_txt.write_text(caption, encoding="utf-8")
                print(f"    ✓ {img.name} [{caption_key}]")
                total_copied += 1
                total_captions += 1

    print(f"\n=== DONE ===")
    print(f"  Copied: {total_copied} images")
    print(f"  Captions written: {total_captions}")
    if missing_captions:
        print(f"\n  ⚠ Missing captions for {len(missing_captions)} files:")
        for slug, fname, key in missing_captions:
            print(f"    {slug}: {fname} (key={key})")

    print(f"\nDataset ready at: {DATASET_ROOT}")
    print("Next step: run flux-lora-train.bat for each character in Kohya SS")


if __name__ == "__main__":
    main()
