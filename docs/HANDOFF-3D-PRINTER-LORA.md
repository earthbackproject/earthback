# 3D Printer LoRA — Handoff Notes

## The Core Problem
Flux has no meaningful training data for 3D printer hardware. It generates generic "machine" shapes that would immediately put off anyone who actually works with printers. A LoRA is the right fix, but unlike hempcrete or characters, we **cannot bootstrap training images from Flux itself** — it's a chicken-and-egg. We need real photographs.

---

## Scope Decision: One LoRA or Several?

**Decision: Start with one general FDM LoRA, split later if needed.**

Rationale:
- A combined FDM dataset (50-80 images, mixed types) teaches Flux "what a 3D printer looks like" — which is the primary gap
- Model-specific prompting (`Bambu X1C style`, `Prusa i3 style`) can steer the output once the base is learned
- Split only if the combined LoRA can't differentiate CoreXY from Cartesian well enough for our use case

**Resin is always separate** — completely different visual grammar (enclosed box, LCD screen, FEP film, UV light) with essentially no visual overlap with FDM.

### FDM sub-types (for captioning — not separate LoRAs yet)
| Type | Examples | Visual distinguishers |
|------|----------|-----------------------|
| CoreXY enclosed | Bambu X1C, P2S, Bambu A1 (enclosed) | Box shape, camera visible, touchscreen, AMS on side |
| CoreXY open | Voron, some Bambu | Open frame, fast moving toolhead |
| Cartesian i3 | Prusa MK4, Ender 3, most budget | Rectangular frame, bed slides Y, toolhead moves XZ |
| Delta | Anycubic Kossel | Triangular towers, circular build plate |

---

## Pipeline Scripts (ready to run)

```
collect-3dprinter-images.py    — Download CC0 images from Pexels + Pixabay APIs
curate-3dprinter-images.py     — Crop/resize to 1024x1024, optional manual review
caption-3dprinter-images.py    — Generate .txt captions (template or BLIP-2)
train-3dprinter-lora.bat       — Kohya SS Flux LoRA training command
```

---

## Data Collection Strategy

### Step 1 — Get free API keys (5 minutes each)
- **Pexels**: https://www.pexels.com/api/ — free, 200 requests/hour, CC0
- **Pixabay**: https://pixabay.com/api/docs/ — free, 100 requests/minute, CC0

### Step 2 — Run collection
```
python collect-3dprinter-images.py --pexels-key KEY1 --pixabay-key KEY2
```
Target: 150 from Pexels + 150 from Pixabay → curate down to 60-80 usable

### Tier 2 — Press kits (worth pursuing after initial dataset)
- Bambu Lab, Prusa, Creality, Elegoo all have media/press pages
- Most grant editorial use if asked
- **Note**: Bambu Lab's legal team is aggressive — check their TOS carefully before using
- Prusa is the most open-source-friendly and likely easiest to get permission from

### Tier 3 — Skip
- Reddit, YouTube thumbnails, product listings — copyright exposure not worth it

---

## Priority Printer Models to Cover
For a "realistic desktop FDM printer" result, these 5 cover ~70% of the market:

1. **Bambu Lab X1C** — CoreXY, enclosed, camera visible, market leader
2. **Bambu Lab P2S** — newer flagship, larger build volume
3. **Prusa MK4** — Cartesian, open-source community standard
4. **Creality Ender 3 V3 SE** — budget Cartesian, massive install base
5. **Bambu Lab A1 Mini** — compact entry CoreXY

Secondary if dataset allows:
- Anycubic Photon Mono X (resin — completely different visual grammar)
- Creality K1 (high-speed Cartesian)

---

## What Flux Gets Wrong (Visual Problems to Fix)
- Gantry geometry — CoreXY vs Cartesian look completely different, Flux doesn't know either
- Extruder/nozzle assembly — usually wrong size, wrong position
- Filament path — spool to extruder routing is distinctive and Flux ignores it
- Build plate surface — texture, clips, adhesion
- Screens/interfaces — modern printers have touchscreens, cameras (Bambu), LEDs
- Print-in-progress — partial prints, layer lines, first layer squish

---

## Dataset Specs
- **Target**: 50-80 images total after curation
- **Distribution**: 5-10 per printer model, varied angles
- **Angles needed per model**: front, side, 3/4, top-down, nozzle close-up, full shot with context
- **States**: idle, printing in progress, print removal, filament loading
- **Environments**: workshop bench, home office, maker space, studio/white bg
- **Resolution**: 1024x1024 (scripts handle the crop)

---

## Captioning Strategy
Format: `a [type] 3D FDM printer, [state], [lighting], [environment]`

Examples:
- `a desktop FDM CoreXY enclosed 3D FDM printer, actively printing, warm workshop lighting, on wooden bench`
- `a desktop FDM Cartesian 3D FDM printer, idle, professional studio lighting, white background`
- `a desktop FDM 3D FDM printer, mid-print with partial object visible on build plate, natural window light, in a maker space`

**Trigger word**: `EB3DPRINTER` — optional. Add with `--trigger EB3DPRINTER` flag to caption script.
For a category LoRA (just make Flux know what printers look like), skip the trigger.

Tool options: BLIP-2 (free, HuggingFace), `caption-3dprinter-images.py --mode blip2`

---

## Training Parameters
```
Steps:     1500  (evaluate checkpoints at 500, 1000, 1500)
Rank:      16
Alpha:     16
LR:        1e-4
Optimizer: AdamW8bit
Precision: bf16
Scheduler: cosine_with_restarts, 100 warmup steps
```

Same Kohya SS Flux setup as hempcrete LoRA. See `train-3dprinter-lora.bat`.

---

## Evaluation Prompts (run after training each checkpoint)
Load LoRA in ComfyUI at 0.8 strength, test with:

```
a desktop FDM 3D printer actively printing, warm workshop lighting, on a wooden bench
a Prusa-style Cartesian 3D printer, idle, studio lighting, white background
a Bambu-style enclosed CoreXY 3D printer, printing in progress, home office setting
close-up of a 3D printer nozzle and extruder, filament loaded, macro photography
a 3D printer with a completed print on the build plate, maker space, natural light
```

Look for:
- [ ] Correct gantry type visible (not generic "machine")
- [ ] Extruder/nozzle in right place and right scale
- [ ] Filament spool visible and routed correctly
- [ ] Build plate texture recognizable
- [ ] No extra arms/robots/industrial machinery

---

## Next Steps When We Pick This Up
1. [ ] Get Pexels API key at https://www.pexels.com/api/
2. [ ] Get Pixabay API key at https://pixabay.com/api/docs/
3. [ ] Run `python collect-3dprinter-images.py --pexels-key KEY1 --pixabay-key KEY2`
4. [ ] Run `python curate-3dprinter-images.py --review` — accept/reject, target 60-80
5. [ ] Run `python caption-3dprinter-images.py` — generates .txt files
6. [ ] Edit `dataset-3dprinter/curated/captions-review.json` for any wrong captions
7. [ ] Run `python caption-3dprinter-images.py --apply-edits`
8. [ ] Run `train-3dprinter-lora.bat`
9. [ ] Evaluate at 500/1000/1500 step checkpoints

---

## Notes
- Resin printers are a different enough visual world they may warrant a separate LoRA later
- Once the printer LoRA is working, can combine with character LoRAs for "maker working at printer" shots
- The Earthback context: 3D printing fits under appropriate-tech / distributed manufacturing / spare parts — good circle category candidate too
- Dataset lives at: `C:\users\adrxi\Earthback\dataset-3dprinter\`
- LoRA output: `C:\users\adrxi\Earthback\lora-output\3dprinter\`
