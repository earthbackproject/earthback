# Earthback — LoRA Training Pipeline
*Master reference · All prompts, all batches, training config*
*Updated: Feb 2026*

---

## Overview

12 character LoRAs, one per cast member. Each LoRA trained on 15–20 images
covering portrait, action, and environmental shot types. Trigger word format: `[NAME]_EB`

**Model:** flux1-dev-fp8.safetensors
**Generation settings:** Steps 25 · CFG 1.0 · Sampler euler · Scheduler simple · 896×1152 · Denoise 1.0
**Trainer:** Kohya SS (Flux LoRA mode)
**Hardware:** RTX 3060 12GB · PyTorch 2.10.0+cu130

---

## Characters & Trigger Words

| Character | Trigger Word | Age | Location | Role |
|---|---|---|---|---|
| James Osei | `JAMES_OSEI_EB` | 34 | Ghana | Earthback trainer |
| Lena Hartmann | `LENA_HARTMANN_EB` | 31 | Morocco | Cob builder |
| Tom Westhall | `TOM_WESTHALL_EB` | 47 | Oregon | Hemp farmer |
| Rosa Mendez | `ROSA_MENDEZ_EB` | 38 | Costa Rica | Bamboo architect |
| Mei Lin | `MEI_LIN_EB` | 29 | Philippines | Community developer |
| Elena Vasquez | `ELENA_VASQUEZ_EB` | 52 | New Mexico | Housing coordinator |
| Amara Diallo | `AMARA_DIALLO_EB` | 41 | Senegal | Master builder |
| Marcus Webb | `MARCUS_WEBB_EB` | 61 | Kentucky | Retired engineer |
| Kenji Nakamura | `KENJI_NAKAMURA_EB` | 35 | Delft NL | Mycelium researcher |
| Priya Sharma | `PRIYA_SHARMA_EB` | 44 | Queensland | Solar specialist |
| Dara Okonkwo | `DARA_OKONKWO_EB` | 33 | Detroit | Land trust organizer |
| Sam Torres | `SAM_TORRES_EB` | 26 | Phoenix | 3D printer tech |

---

## Generation Batches

### Batch 1 — T1 · Portrait shots
*Prefix format: `EB-fp-01-social media-T1-chars-[Name]-01`*
*Status: ✅ Complete (1 image per character)*

| Character | Notes |
|---|---|
| James Osei | Shipping container classroom background |
| Lena Hartmann | Cob wall, Tafraoute Morocco |
| Tom Westhall | Hemp field, Willamette Valley |
| Rosa Mendez | Bamboo structure, Osa Peninsula |
| Mei Lin | Community meeting, rural Mindanao |
| Elena Vasquez | Mesa landscape, Pueblo of Acoma |
| Amara Diallo | Rammed earth structure, Thiès |
| Marcus Webb | Hempcrete wall, Eastern Kentucky |
| Kenji Nakamura | Materials lab, Delft |
| Priya Sharma | Standing seam roof, Queensland |
| Dara Okonkwo | Vacant lot, Detroit |
| Sam Torres | 3D printer, Phoenix |

---

### Batch 2 — T2 · Action shots
*Prefix format: `EB-fp-01-social media-T2-chars-[Name]-01`*
*Status: ✅ Complete (1 image per character)*

```
JAMES_OSEI_EB — hempcrete mixing demo to trainees, hands in mix, shipping container bg, West African midday
LENA_HARTMANN_EB — foot-mixing cob on tarp, dry Moroccan earth, Anti-Atlas bg, golden hour
TOM_WESTHALL_EB — kneeling in hemp field examining stalks, checking fiber, overcast Oregon light
ROSA_MENDEZ_EB — sketching bamboo joint details at outdoor table, bamboo culms nearby, Osa Peninsula morning
MEI_LIN_EB — conversation with community members over hand-drawn land map, bamboo hall, rural Mindanao
ELENA_VASQUEZ_EB — running hand along rammed earth wall, construction site, older Pueblo woman beside her
AMARA_DIALLO_EB — soil ribbon test close-up, hands and concentration, Thiès afternoon
MARCUS_WEBB_EB — rebound hammer testing hempcrete wall, reading glasses, skeptic-proved-right expression
KENJI_NAKAMURA_EB — placing mycelium sample in compression tester, TU Delft lab, labeled containers
PRIYA_SHARMA_EB — clipping solar panel mount to standing seam roof, Queensland blue sky
DARA_OKONKWO_EB — showing site plan to Detroit residents, straw bale frames in background
SAM_TORRES_EB — close inspection of 3D-printed hempcrete wall surface, Phoenix workshop
```

---

### Batch 3 — T3 · Environmental / wide shots
*Prefix format: `EB-fp-01-social media-T3-chars-[Name]-01`*
*Status: ✅ Complete (1 image per character)*

```
JAMES_OSEI_EB — wide shot, watching trainees build hempcrete wall, arms crossed, quietly proud, WA afternoon
LENA_HARTMANN_EB — crouching examining cob wall surface, wall fills right frame, Tafraoute pink granite, late afternoon
TOM_WESTHALL_EB — walking hemp row, small figure in large field, 3–4m tall plants, overcast Pacific Northwest
ROSA_MENDEZ_EB — inside completed bamboo structure looking up at roof geometry, small figure, dappled tropical light
MEI_LIN_EB — outside half-built bamboo community hall, clipboard, talking with community group, wide landscape shot
ELENA_VASQUEZ_EB — edge of construction site, three foundations on mesa, small figure in large Acoma landscape, golden hour
AMARA_DIALLO_EB — directing two builders at rammed earth site, gesturing at formwork, Thiès compound, late afternoon dust
MARCUS_WEBB_EB — standing back from completed house, hempcrete walls + metal roof + solar, arms crossed, Kentucky farmland
KENJI_NAKAMURA_EB — bench covered with mycelium samples in stages of growth, writing notes, TU Delft large windows
PRIYA_SHARMA_EB — ground level, reviewing solar spec sheet, completed hempcrete home + full solar array bg, Queensland
DARA_OKONKWO_EB — looking at three adjacent vacant lots in different stages, Detroit street, wide urban landscape
SAM_TORRES_EB — standing back from large 3D printer, arms crossed, completed wall section, desert workshop, Arizona light
```

---

### Batches 4–6 — Additional seeds (PENDING)
*Re-run T1, T2, T3 with fresh random seeds × 4 each*
*Target: 5 images per prompt type per character = 15 total per character*
*Prefix: same as original but `-02`, `-03`, `-04`, `-05`*

To queue in ComfyUI: load `window._batch1/2/3` arrays, run with `Math.random()` seeds, increment suffix.

---

### Batch 7 — T4 · Close detail shots (PLANNED)
*New prompt type: hands, tools, faces mid-conversation, material textures*
*Will push each character to 18–20 images*

```
JAMES_OSEI_EB — close-up hands mixing hempcrete, texture of material visible, forearms, West African light
LENA_HARTMANN_EB — close-up of cob wall surface she built, one hand on it, Morocco
TOM_WESTHALL_EB — close-up face, squinting in Oregon overcast, half-smile, hemp stalk in one hand
ROSA_MENDEZ_EB — close-up of her hands holding a bamboo joint model, pencil marks visible
MEI_LIN_EB — mid-conversation face, speaking, engaged, Mindanao interior warm light
ELENA_VASQUEZ_EB — close-up of hand on rammed earth wall surface, high desert dust
AMARA_DIALLO_EB — close-up of soil ribbon test, earth between fingers, Senegal afternoon light
MARCUS_WEBB_EB — face reading a spec sheet, glasses on, concentration, slight skepticism
KENJI_NAKAMURA_EB — close-up of mycelium sample in hands, pale fibrous material, lab light
PRIYA_SHARMA_EB — close-up hands connecting solar clip to seam, tool in hand, roof surface detail
DARA_OKONKWO_EB — close-up of site plan in hands, pencil markings, Detroit, overcast
SAM_TORRES_EB — close-up face looking at printer nozzle detail, critical expression, Arizona light
```

---

## Dataset Folder Structure

```
D:\AI\lora-datasets\
  james-osei\
    images\
      JAMES_OSEI_EB_01.png
      JAMES_OSEI_EB_02.png
      ... (15–20 images)
    captions\
      JAMES_OSEI_EB_01.txt
      JAMES_OSEI_EB_02.txt
      ... (one .txt per image, same filename)
  lena-hartmann\
    images\
    captions\
  ... (repeat for all 12)
```

---

## Caption Format

Each `.txt` file contains one line. Start with trigger word, then natural description.
Keep captions 20–40 words. Vary the description — don't repeat identical captions.

**Examples:**
```
JAMES_OSEI_EB, a Ghanaian man in his thirties, demonstrating hempcrete mixing to trainees outdoors, hands in material, West African midday light, shipping container visible in background
```
```
JAMES_OSEI_EB, lean Ghanaian man, standing at a distance watching trainees build a hempcrete wall, arms crossed, quietly proud, wide construction site shot
```
```
JAMES_OSEI_EB, 34-year-old Ghanaian man with slight stubble, portrait, standing in front of shipping container classroom, warm natural light
```

---

## Kohya SS — Installation (Windows)

```powershell
# 1. Clone Kohya
git clone https://github.com/bmaltais/kohya_ss.git D:\AI\kohya_ss
cd D:\AI\kohya_ss

# 2. Run setup (creates its own venv)
.\setup.bat

# 3. Launch GUI
.\run_gui.bat
```

Open browser at `http://127.0.0.1:7860`

---

## Kohya SS — Flux LoRA Training Config (per character)

Use these settings in the GUI under **Flux LoRA** tab:

| Setting | Value |
|---|---|
| Pretrained model | `D:\AI\ComfyUI\models\diffusion_models\flux1-dev-fp8.safetensors` |
| Train data dir | `D:\AI\lora-datasets\[character]\` |
| Output dir | `D:\AI\ComfyUI\models\loras\earthback-chars\` |
| Output name | `[trigger-word]` (e.g. `JAMES_OSEI_EB`) |
| Resolution | `896,1152` |
| Batch size | `1` |
| Max train epochs | `20` |
| Learning rate | `1e-4` |
| Network rank (dim) | `16` |
| Network alpha | `16` |
| Optimizer | `AdamW8bit` |
| Mixed precision | `bf16` |
| Gradient checkpointing | `ON` |
| Cache latents | `ON` |

**Estimated time per character:** 15–25 min on RTX 3060 12GB

---

## Training Priority Order

1. James Osei — most active in platform narrative, main game NPC
2. Lena Hartmann — bridge character (game + real world)
3. Amara Diallo — highest craft post frequency
4. Tom Westhall
5. Rosa Mendez
6. Remaining 7 in any order

---

## Output Locations

- **Generated images (comfyui-output):** `C:\users\adrxi\Earthback\comfyui-output\`
- **LoRA weights:** `D:\AI\ComfyUI\models\loras\earthback-chars\`
- **Training datasets:** `D:\AI\lora-datasets\`

---

*See also: flux-image-prompts.md (original T1 portrait prompts)*
*See also: flux-lora-batch2-prompts.md (T2 action + T3 environmental full text)*
