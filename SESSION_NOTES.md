# Earthback — Session Notes & Handoff
*Update this file at the end of every Cowork session. To resume: open Cowork, say "read SESSION_NOTES.md and pick up where we left off."*

---

## Last Updated
2026-04-14 — Session 41/42 with Claude via Cowork (Opus)

---

## What Was Done in Session 42 — Watermarking & Site Meta Tags (2026-04-14)

### og:image deployed + full social meta tags
- New `site/assets/img/og-image.jpg` from `og-image-v2-homestead` variant (1200×630, 247 KB, EXIF/IPTC fully stripped)
- Old `og-image.png` backed up as `site/assets/img/og-image-v1-old.png` (kept, not deleted)
- All 26 site HTML files updated with full social meta block via `local/scripts-tmp/update_meta_tags.py`:
  - `og:image` switched .png → .jpg
  - Added per-page `og:title`, `og:description`, `og:url`, plus `og:site_name`, `og:locale`
  - Added `twitter:card="summary_large_image"`, `twitter:site=@earthbackproj` (placeholder, may need real handle), `twitter:title`, `twitter:description`, `twitter:image`
  - Added `keywords`, `author`, `robots` meta tags
- Idempotent script — safe to re-run

### Watermark module + batch
- **New `local/scripts/watermark.py`** — reusable module exporting `apply_watermark(img)`. Final style: faint diagonal `EARTHBACK` pattern at opacity 60 + bold bottom-left wordmark `the Earthback Project.org` (small "the" top-aligned, big Earthback in cream + Project in amber + small ".org" baseline-aligned, with amber accent bar)
- **New `local/scripts/batch_watermark_all.py`** — one-time pass over `local/web-ready/` → writes to `local/web-ready-watermarked/` (parallel folder, same structure). Originals untouched. Re-runnable, skips existing.
- **Batched 3,232 images in 2 minutes** (0 failures). Output in `local/web-ready-watermarked/`.
- **`optimize-for-web.py` updated** — auto-watermarks future runs into `web-ready-watermarked/`. Use `--no-watermark` to skip. og: variant skipped (already branded).
- **`deploy-site-images.py` updated** — sources from `web-ready-watermarked/` by default (falls back to `web-ready/` if missing). Preview gallery now points at thumb files (faster page load).
- Site staging re-built from watermarked source: 43 hero + 43 thumb in `local/site-staging/` ready for deployment
- og:image NOT watermarked (already has full branding overlay, watermark would be redundant). Unwatermarked backup kept as `og-image-v2-nowatermark.jpg`

### Watermark sample preview kept for reference
- `local/web-ready/_watermark-samples/preview-final.html` — final style
- `local/web-ready/_watermark-samples/preview-combo.html` — 4 combo variants explored
- `local/web-ready/_watermark-samples/preview.html` — original 6 styles explored

### Watermark size fix (after first batch was too big on thumbs)
- First batch used ~6% width font with 36px floor — wordmark fell off the right side of all 400px thumbs
- Tested 4 size variants on hero/card/thumb (`local/scripts-tmp/watermark_size_variants.py`) — picked **v3 (3.0% width, 14px floor)**
- Re-batched all 3,237 images with `--force` in 2 min — thumbs now fit cleanly with ~186px wordmark on a 400px image
- **Built `local/scripts/build-review-gallery.py`** — two-tab gallery (Deploy Candidates + All Watermarked) at `local/web-ready-watermarked/review-gallery.html` — 1,508 unique source images grouped by source/category for spot-checking

### Watermarked images deployed to live site
After review approval, copied watermarked staged images into `site/assets/img/`:
- `hero/` (2 files) — establishing.jpg, hero-home.jpg
- `content/` (15 files) — cohousing, community, earthen, ecology, fabrication, food, hands, hempcrete, landscape, mycology, shelter, solar, strawbale, timber, water
- `textures/` (1 file) — texture.jpg
- `dispatch/` (1 file) — dispatch-support.jpg
- `posts/` (5 replaced) — food-forest, salvage-fir, solar-coop, tiny-cabin, utah-hemp-wall now watermarked. Originals backed up in `posts/_unwatermarked-backup/{name}-v1.jpg`. Three other post images (greywater-system, hempcrete-mix, lora-mesh) untouched — no watermarked replacements were staged.

### Next steps for Nicco
1. **Pick a real Twitter handle** (or remove): currently `@earthbackproj` placeholder in all pages — search-and-replace if you want a real one
2. **Wire HTML to new image paths** — pages need `<img src="assets/img/hero/...">`, `assets/img/content/...`, etc. Audit which pages reference which images.
3. **Push to git** so og:image + meta tags + new watermarked images go live on Netlify
4. **Validate link previews** at developers.facebook.com/tools/debug/, cards-dev.twitter.com/validator, linkedin.com/post-inspector/
5. **Uncategorized staged set** (19 circles/game/textures/og-social-card images) still in `local/site-staging/uncategorized/` — need destination decisions before deploying

---

## What Was Done in Session 41 — Autonomous Run (2026-04-14)

---

## What Was Done in Session 41 — Autonomous Run (2026-04-14)

Nicco left to wire up the new laser cutter. Claude ran solo to advance the hempcrete LoRA pipeline and get images site-ready.

### Hempcrete LoRA Verification & Testing
- **Verified Flux hempcrete LoRA checkpoints**: 3 valid safetensors in `local/lora-output/hempcrete-flux-aitk/hempcrete-flux-v2/`:
  - `hempcrete-flux-v2_000000400.safetensors` (165 MB, trained Apr 4)
  - `hempcrete-flux-v2_000000800.safetensors` (165 MB, trained Apr 4)
  - `hempcrete-flux-v2.safetensors` (165 MB, final 1200 steps, Apr 5)
- **Config confirmed**: rank 16, Adafactor, bf16, layer_offloading, resolution 512-768, trigger EBHEMPCRETE
- **SDXL LoRA also verified**: 4 checkpoints in `hempcrete-sdxl/` (170 MB each), final already in ComfyUI loras folder

**New scripts created:**
- `local/scripts/setup-hempcrete-flux-lora.bat` — copies all 3 Flux LoRA checkpoints to `D:\AI\ComfyUI\models\loras\` with clean names
- `local/scripts/test-hempcrete-lora.py` — queues 9 comparison images (3 prompts × 3 variants: flux-v2-final, flux-v2-800, no-lora). Includes LoraLoader node 50 workflow, adjustable strength (default 0.85), scene prompts with EBHEMPCRETE trigger, auto-strips trigger for no-lora baseline. Run with `--dry-run` to preview.

**Next steps for Nicco:**
1. `setup-hempcrete-flux-lora.bat` (copies LoRA files to ComfyUI)
2. `python local\scripts\test-hempcrete-lora.py` (queues comparison batch)
3. Review output in `comfyui-output/` — files named `lora-test-{scene}-{variant}_NNNNN_.png`

### Full Site Asset Audit
Cataloged all generated images across 3 directories:
- **site-assets/**: 221 images, 43 categories (establishing, hempcrete, community, food, solar, etc.)
- **circles/**: 382 images, 46 categories (39 circle topics × ~9 each)
- **methods/**: 905 images, 30 construction methods × 30 each
- **Already deployed**: 56 files in `site/assets/img/` (SVG icons, brand assets, 8 post images, 12 avatar JPGs)
- **og:image**: existing placeholder at 22KB (text-only on green background)

### Web Image Optimization Pipeline
Built `local/scripts/optimize-for-web.py` — complete pipeline that:
- Strips all ComfyUI tEXt metadata from PNGs
- Converts PNG → JPEG with quality control
- Generates 3 size presets per image: hero (1920×1080, q82), card (800×600, q78), thumb (400×300, q72)
- Preserves variant numbers in filenames (e.g., `site-hempcrete-03-v2-hero.jpg`)
- Creates category subdirectories
- Generates `inventory.json` with full metadata

**Results:**
- 1,508 source PNGs (2.3 GB) → 3,237 web-ready JPGs (~80 MB)
- **~29× compression ratio** with no visible quality loss at web sizes
- Site-assets: 663 JPGs (hero + card + thumb)
- Circles: 764 JPGs (card + thumb — hero not needed)
- Methods: 1,810 JPGs (card + thumb)

### og:image Social Sharing Cards
Created 3 variants of the og:image (1200×630) with photo backgrounds and brand overlay:
- `og-image-v2-build.jpg` (197 KB) — community earth building scene, golden backlight (RECOMMENDED)
- `og-image-v2-homestead.jpg` (248 KB) — aerial permaculture homestead, lush green
- `og-image-v2-timber.jpg` (172 KB) — timber frame raising, dramatic PNW forest

All use the Earthback brand treatment: dark green gradient overlay on left, amber accent bar, EARTHBACK wordmark in cream + amber, tagline, URL, Eb badge. Massive upgrade from the plain green text-only placeholder.

### Site Image Deployment Helper
Built `local/scripts/deploy-site-images.py` — staging pipeline that:
- Picks best image per category (most detailed)
- Creates proper `site/assets/img/` directory structure in staging
- Generates HTML preview gallery (`local/site-staging/preview.html`)
- Stages hero + thumb for each category
- Optional `--og build` flag includes chosen og:image variant

**Staged output**: 43 hero images + 43 thumbnails + og:image in `local/site-staging/`

### Files Created
| File | Purpose |
|------|---------|
| `local/scripts/setup-hempcrete-flux-lora.bat` | Copy Flux LoRA checkpoints to ComfyUI |
| `local/scripts/test-hempcrete-lora.py` | Queue LoRA comparison batch (9 images) |
| `local/scripts/optimize-for-web.py` | PNG → JPEG optimization pipeline |
| `local/scripts/deploy-site-images.py` | Stage best images for site deployment |
| `local/web-ready/` | 3,237 web-optimized JPGs across 3 source dirs |
| `local/web-ready/og/` | 3 og:image social card variants |
| `local/web-ready/inventory.json` | Full metadata inventory |
| `local/site-staging/` | 87 images staged for site deployment |
| `local/site-staging/preview.html` | Visual review gallery |

### charmanager.py Updates (from Part 3)
Also applied remaining patches from Session 40 Part 3:
- Editable Prompt Editor (Step 6) with save-to-project
- Gallery metadata viewer (Meta button, slide-out panel, strip metadata)
- `/api/project/prompts` GET/POST endpoints
- Custom prompts flow into generation endpoints

---

## Immediate Next Steps
1. **Nicco reviews staged images** — open `local/site-staging/preview.html` in browser
2. **Run LoRA setup + test** — `setup-hempcrete-flux-lora.bat` then `python local\scripts\test-hempcrete-lora.py`
3. **Pick og:image** — choose from 3 variants in `local/web-ready/og/`, deploy to `site/assets/img/og-image.png`
4. **Deploy approved images** — copy from `local/site-staging/` to `site/assets/img/`
5. **Test charmanager updates** — restart charmanager, test prompt editor + metadata viewer
6. **Social media setup** — og:image ready, need accounts + Buffer/Publer for scheduling

---

## What Was Done in Session 40 — Part 3 (2026-04-13)

### Editable Prompt Editor (Step 6 overhaul)
Replaced the read-only "Prompt Reference" section with a full **Prompt Editor**. Prompts are now editable textareas that save custom overrides to the project JSON.

**Backend:**
- `GET /api/project/prompts` — returns all prompt data (text triptych + PuLID per-panel) merged with any custom overrides from project JSON
- `POST /api/project/prompts` — saves custom prompt overrides to `custom_prompts` dict in project JSON. Empty string = revert to default.
- Generation endpoints (`queue-triptych`, `queue-pulid-triptych`) now check `active_project["custom_prompts"]` before falling back to hardcoded defaults
- Custom prompts stored per-key: `text_A`, `text_B`, `text_C` for triptych mode; `pulid_A_0_prompt`, `pulid_A_0_negative`, etc. for PuLID per-panel

**UI:**
- Step 6 header changed to "Prompt Editor"
- Two tabs: "Text Prompts" (Sheet A/B/C full prompts) and "PuLID Prompts" (per-panel positive + negative)
- Editable textareas with amber highlight when modified from default
- "Save All" button persists to project JSON; "Reset to Defaults" clears all custom overrides
- `{desc}` placeholder still works — gets replaced with character description at generation time

### Image Metadata Viewer in Gallery
Added a **Meta** button to the full-size gallery viewer that opens a slide-out panel showing the ComfyUI workflow data embedded in each PNG.

**Features:**
- Slide-out panel (right side, 380px) with dark monospace theme
- Shows: positive prompt, negative prompt, sampler settings (seed/steps/cfg/sampler/scheduler), resolution, PuLID weight + ref image, model name
- "Strip Metadata for Web" button — removes ComfyUI tEXt chunks from the PNG in place
- Auto-refreshes when navigating between images with the panel open
- Panel closes automatically when gallery closes

**Backend endpoints (built in Part 2, wired to UI in Part 3):**
- `GET /api/image-meta?path=...` — reads PNG tEXt chunks, returns structured workflow data
- `POST /api/image-strip` — strips all tEXt metadata from PNG

### Files Changed
- `local/scripts/charmanager.py` — editable prompt editor, metadata viewer, custom prompt storage + generation integration

---

## What Was Done in Session 40 — Part 2 (2026-04-13)

### PuLID Face-Locked Triptych Generation
Added the ability to upload a single photo of a real person and generate face-locked charsheet triptychs (1536x640, 3-panel) directly from the Character Manager UI.

**Backend:**
- `PULID_TRIPTYCH_WORKFLOW` — merged PuLID face injection nodes (40-44) with triptych resolution/layout. KSampler takes patched model from ApplyPulidFlux node 42.
- `/api/character/<name>/queue-pulid-triptych` — queues PuLID-locked triptych sheets (A/B/C) with adjustable strength, auto-routes to best GPU, uploads reference to target ComfyUI instance.
- `/api/character/<name>/upload-face-ref` — uploads a face photo, saves to `local/faces-reference/Name.png`, returns thumbnail.
- `/api/character/<name>/face-ref` — checks if a face reference exists for a character, returns thumbnail.
- `upload_ref_to_comfyui()` updated with optional `target_url` parameter for dual-GPU reference uploads.

**UI:**
- "Generate from Photo (PuLID)" section in Step 1 with dashed moss-green border
- Photo preview (60x60), upload button, sheet checkboxes (A/B/C), strength slider (0.30–1.00, default 0.60), generate button
- Auto-loads existing face reference thumbnail on character select (e.g., if `faces-reference/Blu Blubaugh.png` exists)
- Status log shows GPU routing, reference used, sheets queued
- Polls for completion and refreshes sheet grid when done

**Context:** Nicco wanted to use a real photo of his friend Blu Blubaugh to generate face-locked triptychs. Also discussed Rena Begay (childhood friend, inspiration for Earthback). Both characters added to the project via the Character Manager GUI.

### Bug Fixes (continued)
- **Duplicate character prevention** — auto-dedup on project load, atomic JSON saves (write .tmp → verify → rename), JSONDecodeError recovery
- **virtiofs write corruption** — earthback.json must always be written via Python script (not VM Write tool) due to ~4400 char truncation limit

### Files Changed
- `local/scripts/charmanager.py` — PuLID triptych workflow + endpoints + UI + auto-load face ref

---

## What Was Done in Session 40 — Part 1 (2026-04-13)

### Character Manager — Pipeline UI Redesign
Completely restructured the detail panel from flat unlabeled sections into a guided 6-step pipeline:
1. **Triptych Source** — drop zone, browse sheets, upload, + NEW: generate triptychs directly via ComfyUI
2. **Reference Panels** — mix-and-match slot assignment + NEW: full-size panel gallery viewer
3. **Generate Faces (PuLID)** — strength/rounds controls, queue button
4. **Triage New Output** — full-size gallery, select/deselect, sort/discard
5. **Training Library** — curated images, browse full-size, weed rejects
6. **Prompt Reference** — collapsed by default, copy prompts for ComfyUI

**Pipeline status bar** at top — clickable pips with counts (Refs 3/3, Triage 12 new), completed steps auto-collapse.
**Grid card mini-pips** — 5 numbered dots per character card showing pipeline progress at a glance.

### Triptych Generation from Character Manager
New `/api/character/<name>/queue-triptych` endpoint sends charsheet generation jobs directly to ComfyUI using the same workflow as `queue-charsheets.py`. Sheet type checkboxes (A/B/C), optional +variant toggle (seed+7). Auto-polls and refreshes when done.

### Dual-GPU Support
- **GPU 1 (:8188)** — main instance for PuLID and batch work (comfy-run.bat)
- **GPU 0 (:8189)** — second instance for triptychs and light work (NEW: comfy-run-gpu0.bat)
- Character Manager auto-routes triptych jobs to GPU 0 if running, falls back to GPU 1
- Dual GPU status chips in header — green=idle, amber+pulse=busy, gray=offline
- Smart warnings: if GPU 0 is offline and GPU 1 has a big queue (PuLID batch), warns about restart risk

### Panel Gallery (Full-Size Reference Viewing)
"Browse Panels Full Size" button + double-click on any panel thumbnail opens a full-screen gallery with arrow nav and keyboard shortcuts. Same overlay as the output gallery but without select/deselect.

### Bug Fixes
- **Corrupt earthback.json** — file was truncated at Joseph Runningwater's description. Rebuilt from queue-charsheets.py source of truth. All 19 characters validated.
- **Duplicate triptych seed confusion** — default changed to 1 seed per sheet (not 2). "+variant" checkbox adds the seed+7 variant when desired. Clearer logging shows exactly how many images will be generated.
- **Poller resilience** — triptych completion poller now requires seeing jobs actually running before declaring "done" (prevents false triggers on ComfyUI restart). Detects and warns if GPU goes offline (PuLID batch restart).

### New Files
| File | Purpose |
|------|---------|
| `local/scripts/comfy-run-gpu0.bat` | Start second ComfyUI instance on GPU 0 (CUDA 0), port 8189 |

### Files Changed
- `local/scripts/charmanager.py` — pipeline UI redesign, triptych generation, dual-GPU, panel gallery (~2933 lines)
- `local/projects/earthback.json` — rebuilt from source of truth (was truncated/corrupt)

---

## Immediate Next Steps (Session 41)
1. **Test PuLID triptych** — restart Character Manager, select Blu Blubaugh, upload his photo, generate face-locked triptych on GPU 0
2. **Test dual-GPU** — start `comfy-run-gpu0.bat`, verify triptychs route to GPU 0 while PuLID batch runs on GPU 1
3. **Verify PuLID workflow** — check that the merged PULID_TRIPTYCH_WORKFLOW actually generates correct 1536x640 triptychs (not 896x1152 portraits)
4. **Test hempcrete LoRA** — load checkpoint from `local/lora-output/hempcrete-flux-aitk/`, generate with EBHEMPCRETE trigger
5. **RunPod integration** — manual test run first, then build into Character Manager Step 5→6
6. **Call it in the Air project** — populate characters, start blocking out screenplay/bio
7. **Caption PuLID images** → train character LoRAs → test face consistency

---

## What Was Done in Session 39 — Part 2 (2026-04-04)

### PuLID Image Quality — 5 Fixes for Angle Variety

**Problem:** PuLID at strength 0.85 with a single reference image produced near-identical poses across all angles. Left, right, front, down — all looked the same. The reference face pose dominated everything.

**Fix 1 — Taskkill safety bug:**
`kill_comfy()` in `run-pulid-all.py` had `taskkill /f /im python.exe` that would kill ALL Python processes including LoRA training. Replaced with targeted `netstat -ano` lookup to find only the PID on port 8188.

**Fix 2 — Prompt variation (4 templates per angle):**
Each face angle now has 4 different prompt templates (documentary, cinematic, editorial, candid) with varied lighting. `--reseed` picks a random template per job.

**Fix 3 — Lower PuLID strength (0.85 to 0.60):**
Default dropped to 0.60 in both `queue-pulid-faces.py` and `run-pulid-all.py`. Keeps face identity while letting pose/angle prompts actually work. (0.75 was tested mid-session — still too strong for reliable angle control.)

**Fix 4 — Per-angle negative prompts:**
Each angle now has specific negatives. Left/right angles reject "facing forward, straight-on, symmetrical face, looking straight ahead." Down angle rejects "looking up, eyes forward, facing camera, direct eye contact."

**Fix 5 — Multi-reference rotation (3 images per character):**
Charsheet triptychs (1536x640, 3 panels) cropped into individual 512x640 references: `CharName-1.png`, `CharName-2.png`, `CharName-3.png` in `local/faces-reference/`. Orchestrator rotates per round: round 1 uses ref-1, round 2 uses ref-2, round 3 uses ref-3.

**Results at 0.75 strength (mid-session test, Amara Diallo):**
- Front: good, clearly front-facing
- Left: good, ~30 degrees
- Right: still defaulting to forward (reference bias)
- Down: ~20 degrees from above, not perfect but usable
- Talk: good, animated expression

### Unicode Fix
Windows cp1252 console crash on unicode symbols. Replaced `checkmark/cross/warning` with ASCII `OK/FAIL/WARNING:` in both scripts.

### comfyui-output Organized (2,362 files sorted)
Created `sort-comfyui-output.py` — sorts flat output dir into: `charsheets/`, `characters/[Name]/{faces,pulid,scenes-t4,scenes-t5}/`, `circles/`, `site-assets/`, `methods/`, `earthmesh/`, `hempcrete-lora/`, `misc/`. Re-runnable for new files. `--undo` to flatten.

### Character LoRA Training Pipeline (train-character-pipeline.py)
Full drop-folder-to-trained-LoRA pipeline. Drop ref images + desc.txt into `local/lora-pipeline/CharacterName/`, run the script, get a trained LoRA. 4 composition tiers (face, upper body, full body, environmental) × 30 prompts × 3 refs = 90 training images per character. Auto-captions from prompt metadata, generates ai-toolkit config, trains on cuda:0.

### Reference Image Swap Process
When a character's charsheet triptych produces bad angles (e.g. Mei Lin always facing right), swap it:

1. **Find or generate a better triptych** — look for one with a more front-facing center panel. The B variant seed 2 tends to be best.
2. **Place the new triptych** anywhere crop-charsheet-refs.py can find it:
   - `comfyui-output/` (root)
   - `comfyui-output/charsheets/`
   - `comfyui-output/characters/CharName/`
3. **Crop into 3 reference panels:**
   ```
   python local\scripts\crop-charsheet-refs.py --char "Character Name" --force
   ```
   This overwrites the existing CharName-1/2/3.png in `local/faces-reference/`.
4. **Verify** — check the 3 new panels in `local/faces-reference/` to confirm the center panel (CharName-2.png) is front-facing.
5. **Re-run PuLID** — the orchestrator will pick up the new refs automatically.

**Example (Mei Lin):** Original B_00001 triptych had a 3/4 right-facing center panel. Swapped to B_00002 which had a more front-facing center. Cropped with `--force`, confirmed 3 new panels.

### New Scripts
| Script | Purpose |
|--------|---------|
| `crop-charsheet-refs.py` | Crops charsheet triptychs into 3 individual face refs per character |
| `sort-comfyui-output.py` | Sorts comfyui-output into categorized subdirectories |
| `train-character-pipeline.py` | Full drop-folder-to-LoRA pipeline (generate, caption, train) |

### Character-LoRA-Pipeline-Guide.docx
New reference doc in `local/docs/` — covers charsheet prompts, drop folder setup, all 30 prompt templates with resolutions, training settings, reference swap process.

### Character Manager GUI (charmanager.py)
Local Flask web app for managing character references and PuLID generation. Launch with `charmanager.bat` or `python local\scripts\charmanager.py`. Runs on http://127.0.0.1:5111.

Features:
- Card grid of all 19 characters with reference panel thumbnails
- Browse/select charsheet triptychs, preview 3-panel crops before committing
- Drag-and-drop upload of new triptych PNGs
- One-click crop & save to faces-reference/
- Queue PuLID generation per character (configurable strength and rounds)
- ComfyUI queue status monitor (auto-refreshes)
- Sort output button (runs sort-comfyui-output.py)
- Recent output gallery per character
- Lightbox for full-size image viewing

Dependencies: Flask, Pillow (auto-installed by .bat). Runs on system Python.

### Files Changed
- `local/scripts/run-pulid-all.py` — kill_comfy() fix, strength 0.60, multi-ref rotation, ref discovery logging
- `local/scripts/queue-pulid-faces.py` — 4 prompt variants/angle, ANGLE_NEGATIVES, `--ref-image` flag, strength 0.60, unicode fix
- `site/eb-grove.html` — updated What's Next panel with PuLID/LoRA status + v2 run instructions

---

## Immediate Next Steps (Session 40)
1. **Re-run PuLID with v2 fixes** — `python local\scripts\run-pulid-all.py --rounds 3` (uses 0.60 strength + negatives + 3 reference rotation)
2. **Re-sort new PuLID output** — `python local\scripts\sort-comfyui-output.py`
3. **Check hempcrete LoRA output** — verify checkpoints at `local/lora-output/`
4. **Test hempcrete LoRA in ComfyUI** — load checkpoint, generate test images with EBHEMPCRETE trigger
5. **Review PuLID quality** — if angles still flat, try strength 0.50 or `start_at: 0.2` in node 42
6. **Caption PuLID character images** — run quick-caption.py for character LoRA training datasets
7. **Generate character LoRA configs** — make-flux-config.py for each of 8 characters
8. **Train character LoRAs** — 8 characters, ~11hrs each on cuda:0
9. **Social media posts for Earthback** — mentioned but not yet started

---

## What Was Done in Session 39 — Part 1 (2026-04-04)

### Flux LoRA Training — Hempcrete (ai-toolkit)
- Resolved HuggingFace gated model access for FLUX.1-dev (token permissions, direct token file write to bypass old huggingface_hub CLI)
- Fixed `from_single_file` approach failure → switched to diffusers format via `name_or_path: "black-forest-labs/FLUX.1-dev"`
- Fixed `enable_gqa` TypeError by upgrading torch 2.4.1 → 2.5.1+cu121 in ai-toolkit venv
- **Hempcrete Flux LoRA training running** on cuda:0 (Task Manager GPU 1) — 1200 steps @ ~36s/step, checkpoints at 400/800/1200
- Config: `local/scripts/configs/hempcrete-flux-12gb.yaml` — rank 16, Adafactor, bf16, layer_offloading (0% transformer on GPU)

### Voice Captioning Workflow
- Created `local/scripts/quick-caption.py` — WhisperFlow-powered image captioning tool
- Shows existing caption, user dictates replacement/append via mic, can exclude bad images (moves to `_excluded/`)
- All 77 hempcrete training images captioned (44 excluded by user), trailing commas cleaned from 69 caption files

### PuLID Face-Locked Generation — Fixed & Running (4 bugs fixed)
- Prepared 8 PuLID reference face images (512×640 center crops from charsheets) in `local/faces-reference/`
- Characters: Amara Diallo, Britta Svensson, Callum Reed, Joseph Runningwater, Lena Hartmann, Mei Lin, Priya Sharma, Sam Torres

**Bug 1 — HTTP 400 (wrong node class_types in workflow JSON):**
PuLID node class names changed in newer ComfyUI-PuLID-Flux. Fixed in `queue-pulid-faces.py`:
  - `ApplyPulid` → `ApplyPulidFlux` (input `pulid` → `pulid_flux`)
  - `PulidModelLoader` → `PulidFluxModelLoader`
  - `InsightFaceLoader` → `PulidFluxInsightFaceLoader`
  - Added new node 44: `PulidFluxEvaClipLoader` (eva_clip is now a separate loader node)

**Bug 2 — InsightFace AssertionError (missing antelopev2 models):**
PuLID needs InsightFace's antelopev2 face detection models. Downloaded 5 ONNX files to:
`D:\AI\ComfyUI\models\insightface\models\antelopev2\` (1k3d68, 2d106det, genderage, glintr100, scrfd_10g_bnkps)

**Bug 3 — CUDA invalid argument (GPU device conflict):**
`--cuda-device 1` only controls ComfyUI's own device selection, but third-party libs (facexlib, insightface) default to cuda:0. Fixed by using `CUDA_VISIBLE_DEVICES=1` in comfy-run.bat instead — this hides GPU 0 entirely from the ComfyUI process.

**Bug 4 — forward_orig() unexpected keyword argument 'attn_mask':**
ComfyUI 0.11.1 passes `transformer_options` and `attn_mask` to `forward_orig()`, but PuLID's patched version didn't accept them. Patched `D:\AI\ComfyUI\custom_nodes\ComfyUI-PuLID-Flux\pulidflux.py` line 65 — added `transformer_options=None, **kwargs` to function signature.
**WARNING:** This patch may be overwritten if ComfyUI-PuLID-Flux is updated via Manager. Re-apply if PuLID breaks after an update.

- PuLID test generation confirmed working (Lena Hartmann images generating)

### Dual GPU Setup Confirmed
- CUDA device 0 = Task Manager GPU 1 (hempcrete LoRA training)
- CUDA device 1 = Task Manager GPU 0 (ComfyUI / PuLID generation)
- Both running in parallel successfully

### Other Fixes
- Fixed `REFERENCE_DIR` path in queue-pulid-faces.py (was pointing to wrong parent)
- Added Britta Svensson, Callum Reed, Joseph Runningwater to CHARS list in queue-pulid-faces.py

---

## What Was Done in Session 38 (2026-03-26)

### CK-Series Communications Kits — Price Research & Design Brief
Researched real wholesale/retail pricing for GMRS radios, SDR radios, LoRa mesh hardware, and accessories using browser automation (Claude in Chrome) to visit manufacturer sites directly (baofengtech.com, tidradio.com, baofengradio.com, rtl-sdr.com, rokland.com, AliExpress, hi-radio.com). Compiled verified component prices into a 5-kit product line:

| SKU | Name | Retail | COGS | Margin |
|-----|------|--------|------|--------|
| CK-10 | Basic Comms (2-radio) | $89 | $37.75 | 57.6% |
| CK-20 | Family Comms (6-radio) | $249 | $129.75 | 47.9% |
| CK-30 | SDR Starter (hackable) | $169 | $41.75 | 75.3% |
| CK-40 | Cyberdeck (SDR + mesh) | $399 | $106.25 | 73.4% |
| CK-50 | Community Network (18-unit) | $999 | $457.25 | 54.2% |

Every kit includes a QR code linking to the FCC GMRS license application ($35, no exam, covers entire family for 10 years).

**Files produced:**
- `eb_research/offline-emp-restart/CK_Series_Design_Brief_v1.docx` + `.pdf` — 12-page design brief with component price reference tables, BOM per kit, revenue projections
- `/sessions/amazing-gifted-brown/ck-series-brief.js` — DOCX generator script (~350 lines)

### Investor Deck V2b — CK-Series Integration + Utah De-emphasis
Updated the Series A investor deck to integrate CK-series comms kits and dramatically reduce Utah-specific language per Nicco's direction ("just barely mention it — the rest plays itself out in their head automatically").

**Slides changed (10 of 18):**
- Slide 2 (Opportunity): Utah stat → "4.5M active preppers in the US (FEMA est.)"
- Slide 3 (Product Line): Tier 2 price range $550-$6,200 → $89-$999, margins updated
- Slide 4 (Holiday Retail): Complete rewrite — Faraday bundles row + CK-series row, Utah banner removed
- Slide 6 (SKU Table): Old CK rows replaced with 5 new CK-series rows
- Slide 7 (Mesh Radio): CK card updated to CK-50 Network Kit with real specs/pricing
- Slide 9 (Timeline): All Utah references → neutral language
- Slide 10: **Complete rewrite** — "UTAH: THE PERFECT LAUNCH MARKET" → "GO-TO-MARKET" with nationally-focused messaging
- Slide 11 (Revenue): "Utah retail" → "regional retail"
- Slide 12 (Unit Economics): Added all 5 CK-series rows with confirmed COGS/margins
- Output filename: V2a → V2b

**File produced:**
- `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V2b.pptx` — 18 slides, 930KB
- PDF conversion failed (LibreOffice issue in VM) — Nicco can convert on Windows: `libreoffice --convert-to pdf` or just open in PowerPoint and Save As PDF

**Source script:** `/sessions/amazing-gifted-brown/deck-v2b.js`

---

## Immediate Next Steps (Session 39)
1. **Convert V2b to PDF on Windows** — LibreOffice headless or PowerPoint Save As
2. **Visual QA the V2b deck** — open in PowerPoint, check Slide 12 table fits (17 rows, may need font adjustment)
3. **Walkie talkie research document** — still needs formal DOCX write-up (carried over)
4. **Test Docker stack on Windows** — Docker Desktop, pull Kiwix + ProtoMaps + CyberChef (carried over)
5. **HuggingFace login** — test Flux LoRA training (carried over)
6. **Laser arrival logistics** — track fiber laser delivery from LA port (carried over)

---

## What Was Done in Session 37 (2026-03-25)

### Wi-Fi HaLow Research — DOCX + PDF Generated
Converted the Wi-Fi HaLow research from markdown to proper document format (user preference: research docs should be .docx, not .md, because .md opens in VSCode which is too heavy for documentation).
- `eb_research/Earthmesh/WiFi_HaLow_Research.docx` — full formatted doc with tables, headings, hyperlinks, styled callout
- `eb_research/Earthmesh/WiFi_HaLow_Research.pdf` — PDF companion for sharing
- Original `.md` file preserved in same folder

### Project N.O.M.A.D. Analysis — Docker Stack Mirroring
Analyzed Crosstalk Solutions' Project N.O.M.A.D. (Node for Offline Media, Archives, and Data) — an open-source Docker-based offline knowledge server. Mapped their entire stack against our existing Earthback Station software/hardware to identify gaps and integration opportunities.

**Key finding:** The two systems are deeply complementary. Nomad has knowledge-layer polish we lack (Kiwix for offline Wikipedia/medical refs, Kolibri for Khan Academy education, ProtoMaps for offline maps, Qdrant for RAG/semantic search, CyberChef for data analysis). We have hardware integration, mesh communications, image generation, speech interfaces, and power infrastructure they lack entirely.

**Files produced:**
1. `eb_research/offline-emp-restart/Nomad_vs_Earthback_Analysis_v1.docx` + `.pdf` — Full gap analysis with feature-by-feature comparison table, integration recommendations (3 phases), proposed Docker architecture, container inventory by trailer tier, content pre-loading strategy, and immediate next steps
2. `eb_research/offline-emp-restart/docker-compose.yml` — Working Docker Compose file with profiles for all 4 Earthmesh trailer tiers (scout/field/hub/command) plus a dev profile for Windows. 13 containerized services using official images where available.
3. `eb_research/offline-emp-restart/.env.example` — Environment config template
4. `eb_research/offline-emp-restart/containers/mesh-bridge/Dockerfile` + `meshtastic_ai_bridge.py` — Container build context for the Meshtastic AI bridge service

**Integration plan (3 phases):**
- Phase 1 (weeks 1-2): Adopt from Nomad — Kiwix, Kolibri, ProtoMaps, CyberChef, Qdrant
- Phase 2 (weeks 2-4): Containerize our stuff — llama.cpp, mesh-bridge, whisper, piper, ComfyUI, dashboard
- Phase 3 (weeks 4-8): Polish — installer script, offline provisioning, auth, station-to-station sync, Windows dev

**Docker profiles by tier:**
- `scout` — Pi-based: llama-pi, mesh-bridge, kiwix (mini), redis
- `field` — Single GPU: llama-server, mesh-bridge, kiwix (full), kolibri, protomaps, redis
- `hub` — Dual GPU: all field + qdrant, cyberchef, whisper, piper
- `command` — Full: everything + comfyui
- `dev` — Windows: llama-dev (CPU), kiwix, kolibri, protomaps, cyberchef, qdrant, redis

### Convention Established: Research Docs Format
Going forward, all research documents will be produced as `.docx` + `.pdf`, not `.md`. Markdown opens in VSCode which is too heavy for documentation browsing.

---

## Immediate Next Steps (Session 38)
1. **Test Docker stack on Windows** — install Docker Desktop, create `C:\earthback-data\` directories, pull Kiwix + ProtoMaps + CyberChef containers and verify they run
2. **Download Kiwix ZIM files** — start with wikipedia_en_100_mini and wikimed for testing
3. **Download Kolibri content packs** — Khan Academy math/science
4. **Download regional PMTiles** — test one tribal land region
5. **Containerize llama.cpp with CUDA** — test the official ghcr.io/ggerganov/llama.cpp:server-cuda image with Nicco's RTX 3060s
6. **Build Earthback Dashboard prototype** — service health page, links to Kiwix/Kolibri/maps
7. **Review V1g investor deck with Nicco** — ready for investor feedback
8. **Laser arrival logistics** — track fiber laser delivery from LA port to Spengler's shop
9. **HuggingFace login** — see Session 34 BLOCKER section, then test Flux LoRA training

---

## What Was Done in Session 36 (2026-03-25)

### Earthmesh EMF Investor Deck — V1b Built
Created a focused investor deck for the EMF shielding products and LoRa/mesh radio technology side of Earthback, targeting seed funding to purchase radio and metal stock before supply chain disruptions (Taiwan/China risk, tariffs).

**Files produced:**
- `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1b.pptx` — 16-slide deck (620 KB)
- `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1b.pdf` — PDF version alongside

**V1a** (broad Earthback Industries deck) preserved in same folder — not overwritten.

**Deck contents (16 slides):**
1. Title — Earthmesh (tagline: "Building Resilient Communities")
2. Why Now — macro threat landscape (supply chain, grid, comms)
3. Product Overview — Faraday Enclosures, Comms Kits, Solar Trailers
4. Full SKU Matrix — 30 configurations across 3 tiers with pricing
5. Entry Product Deep Dive — 6 SKUs with Standard vs Hardened specs
6. Earthmesh Node — LoRa mesh radio product line (EMM/EMR/EML/EMP)
7. Solar Trailer Fleet — 4 trailer types with BFFT as manufacturer
8. Maker Platform — welded metal cores as customization base for 3D printer community
9. Target Markets — 6 segments with dollar values
10. Supply Chain Urgency — semiconductor lead times, metal tariffs, Taiwan timeline
11. Manufacturing Partners — Spengler Industries + BFFT (Bountiful Food Truck & Trailer)
12. Financial Projections — Q3 2026 through Q4 2027
13. Use of Funds — $250K allocation breakdown
14. Founder — Nicco's bio with "three waves" pattern (telecom → building tech → resilience)
15. The Ask — $250K seed round, what investor gets
16. Contact

**Political notes applied:**
- Jon Fletcher NOT mentioned anywhere — only company name BFFT used (per Nicco's instruction re: political sensitivity)
- Spengler present for credibility but NOT positioned as anchor or lead (per session 35 political note)

**Source script:** `deck-v1b.js` (pptxgenjs, Node.js) saved locally in working dir. Color palette: dk=1A1F25, terra=B85042, sage=6B9080, cream=F5F0EB, gold=D4A574. Georgia + Calibri fonts.

**Source data pulled from:**
- `eb_research/offline-emp-restart/Entry_Products_Design_Brief_v12.docx` — 6 entry SKUs, 3 config levels, maker platform concept
- `eb_research/offline-emp-restart/Spengler_CEO_Proposal_v3.docx` — 30-SKU matrix, pricing, margins
- `eb_research/Earthmesh/Earthmesh_Investor_Deck_v7.pptx` — node specs, trailer types, market segments, financials

### Material Change Locked In: Galvalume → Cold-Rolled Steel (CRS)
Nicco and Erno confirmed: **all EMF/EMP products will use plain cold-rolled steel (CRS), not Galvalume.** Galvalume's aluminum-zinc coating reduces magnetic permeability, which hurts shielding effectiveness — especially for EMP protection at lower frequencies. Plain CRS has 100-1000x higher magnetic permeability at the surface. CRS comes in the same coil formats (24 ga, 20 ga), same suppliers, same logistics chain as their existing metal roofing stock. Corrosion handled by powder coat (Finished tier) and maker shells (Plain tier).

**Three documents updated:**
1. `eb_research/offline-emp-restart/Entry_Products_Design_Brief_v13.docx` — 16 Galvalume → CRS replacements, version bumped from v12
2. `eb_research/offline-emp-restart/Spengler_CEO_Proposal_v4.docx` — 2 Galvalume → CRS replacements, version bumped from v3
3. `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1c.pptx` + `.pdf` — material refs updated, laser status updated to "in port of LA — arriving now"

All previous versions preserved (v12, v3, V1a, V1b all untouched).

### V1d — GSM Credential Made Prominent
Updated investor deck to make the GSM milestone a headline credential:
- **Founder slide (14):** Gold-accented callout box at top: "SIGNATORY ON THE FIRST GSM CELL PHONE CALL IN THE WESTERN HEMISPHERE" with SLC 1996 date. Name/title below it. Three waves section updated with stronger language and decade labels.
- **Earthmesh node slide (6):** Added credential line under subtitle: "Designed by a signatory on the first GSM call in the Western Hemisphere."
- Files: `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1d.pptx` + `.pdf`

### V1e — 30-Year Full Circle Narrative
Wove the 30-year arc (GSM launch Jan 1996 → Earthmesh 2026) through three slides:
- **Slide 2 (Problem):** Gold italic hook: "The cellular network that launched 30 years ago was never designed to survive what's coming."
- **Slide 6 (Nodes):** "30 years ago, our founder signed off on the first GSM cell call. Now he's building what replaces it."
- **Slide 14 (Founder):** "30 years later, building the network that stands when that one falls." Wave 3 updated to "30 years full circle."

### V1f — LoRa Bandwidth Accuracy Pass
Corrected all slides to not overstate LoRa capabilities (text/GPS messaging only, no voice/streaming):
- Tier 3 description: "WiFi + AI" → "LoRa mesh messaging + local WiFi for onboard AI"
- Trailer subtitle: clarified LoRa mesh relay vs local WiFi access point
- Trailer specs: user counts replaced with "LoRa relay only" / "Local WiFi + LoRa"
- Slide 5 comparison table was already accurate ("~1-5 kbps messaging")

### V1g — Wi-Fi HaLow Research + Deck Blurb
Researched Wi-Fi HaLow (802.11ah) as potential complementary technology:
- Created `eb_research/Earthmesh/WiFi_HaLow_Research.md` — full comparison vs LoRa, hardware availability, integration recommendations
- Added roadmap note to slide 5 (Mesh Radio): "Wi-Fi HaLow (802.11ah) as Phase 2 mid-range data layer — 1+ Mbps at 1 km for firmware OTA + sensor backhaul"
- Recommendation: Phase 2 addition after LoRa backbone is deployed. Not a LoRa replacement — complementary mid-range layer.

### Laser Table Status
**Fiber laser due in port of Los Angeles March 26, 2026.** This is the production bottleneck — everything downstream scales with labor once the laser is online. Deck V1c updated to reflect this.

### File Mount Issue Resolved
D:\Earthback mount was empty/broken this session. Switched to C:\Users\adrxi\Earthback mount which worked. LibreOffice headless conversion also working again in this session (was broken in session 35).

---

## Immediate Next Steps (Session 37)
1. **Review V1g deck with Nicco** — current version has: CRS material, GSM credential, 30-year arc, LoRa bandwidth accuracy, HaLow roadmap note. Ready for investor feedback.
2. **Laser arrival logistics** — track delivery from LA port to Spengler's shop
3. **CRS coil stock pre-order** — lock in pricing on 24 ga + 20 ga cold-rolled steel, full truckload buy
4. **HuggingFace login** — see Session 34 BLOCKER section, then test Flux LoRA training
5. **Delete old `maint scripts` folder** (space version)
6. **Update g alias** in PowerShell $PROFILE to point to maint-scripts (hyphen)
7. **Run cache-offline-install.ps1** to build the offline cache
8. **Monitor for GE Vernova response** — no action unless they reach out via CSRE

---

## What Was Done in Session 35 (2026-03-23)

### 130 E 1100 North — Acquisition Proposal Submitted to CSRE Global
Full outreach package sent to Phyllis Millhouse at CSRE Global (Phyllis.millhouse@csre-global.com, 260.373.0850). She will forward to her boss, who decides whether to pass it to GE Vernova. One-shot opportunity — no follow-up mechanism.

**Three documents sent (v3 versions):**
1. **Cover email** — `130_Owner_Outreach_Email.md` (sent from earthbackproject@gmail.com)
2. **Acquisition Proposal** — `130_E_1100N_Acquisition_Proposal_v3.docx` / `.pdf` (4→3 pages after tightening)
3. **Owner Presentation** — `130_E_1100N_Owner_Presentation_v3.pptx` / `.pdf` (10 slides)

**Key revisions this session:**
- Toned down Spengler involvement: "anchored by" → "including," removed "Anchor manufacturing tenant" from tenant table
- Removed hard page break causing blank space on page 3
- Tightened signature block spacing to fit on 3 pages (v5 source, but v3 was what shipped)
- Added earthbackproject@gmail.com to deck slide 9 contact block (v4 source — did not ship)

**Source files:** `130_acquisition_proposal.js` (currently outputs v5), `130_owner_deck.js` (currently outputs v4)

**Status:** Proposal is out. Waiting on GE Vernova response via CSRE. No follow-up path exists — if GE reaches out, they do; otherwise it's in the wind.

**Political note:** Spengler language was deliberately softened. Nicco wants Spengler's 40-year credibility present but does NOT want language that gives Erno (Spengler's owner) leverage to insist on a partnership role. Avoid "anchor" or any language positioning Spengler as the lead.

### CLAUDE.md Updated
Added file versioning rule prominently near top of file — NEVER overwrite generated document files, always increment version numbers. This was already documented but not prominently enough.

### LibreOffice Broken in VM
LibreOffice headless conversion (docx→pdf, pptx→pdf) failed silently in this session — exit code 1 with no output. Could not regenerate PDFs from the VM. Nicco exported PDFs manually from Windows. If this persists, the VM service may need a restart (fix-cowork-vm.ps1).

---

## Immediate Next Steps (Session 36)
1. **HuggingFace login** — see Session 34 BLOCKER section, then test Flux LoRA training
2. **Delete old `maint scripts` folder** (space version)
3. **Update g alias** in PowerShell $PROFILE to point to maint-scripts (hyphen)
4. **Run cache-offline-install.ps1** to build the offline cache
5. **Test GPU reset script** under real failure conditions
6. **Monitor for GE Vernova response** — no action unless they reach out via CSRE

---

## What Was Done in Session 34 (2026-03-10)

### GPU Reset Script — maint-scripts/Reset-GPU.ps1 + .bat
Created interactive GPU reset tool using nvidia-smi (NOT PnP disable/enable — that crashed the machine).
Shows GPU load, VRAM, and running processes. Offers to kill blocking processes before reset.
Double-click Reset-GPU.bat to run (auto-elevates to admin).

### ai-toolkit Installed and Configured
Flux LoRA training via ostris/ai-toolkit is fully set up at D:\AI\ai-toolkit:
- Python 3.11 venv with torch 2.4.1+cu121, diffusers 0.36.0, torchaudio 2.4.1
- LTX2 extension disabled (incompatible with pinned diffusers)
- Install script: local/scripts/install-ai-toolkit.ps1
- Training launcher: local/scripts/train-flux-lora.bat
- Config generator: local/scripts/make-flux-config.py
- Hempcrete config: local/scripts/configs/hempcrete-flux-12gb.yaml

### BLOCKER: Model path format
ai-toolkit uses diffusers to load models, which expects a HuggingFace model ID (like "black-forest-labs/FLUX.1-dev"), NOT a direct path to a .safetensors file. The config currently points to a local safetensors file which doesn't work.

**To fix (5-10 minutes):**
1. Make HuggingFace account if needed (huggingface.co)
2. Accept FLUX.1-dev license at https://huggingface.co/black-forest-labs/FLUX.1-dev
3. Create access token at https://huggingface.co/settings/tokens
4. Run: `D:\AI\ai-toolkit\venv\Scripts\huggingface-cli.exe login`
5. Update config name_or_path to: `"black-forest-labs/FLUX.1-dev"`
6. Update make-flux-config.py template too
7. Run: `local\scripts\train-flux-lora.bat`

### Flux LoRA Training Guide
Created comprehensive guide: local/Flux-LoRA-Training-Guide.docx
Covers full pipeline from photo collection through evaluation, all parameters explained.

### Offline Cache Scripts
- maint-scripts/cache-offline-install.ps1 — builds full offline cache to D:\earthback-cache
- maint-scripts/install-from-cache.ps1 — deploys from cache on new machine
- maint-scripts/INSTALL-INSTRUCTIONS.txt — plain-text quick reference
- maint-scripts/Earthback-Rebuild-Guide.docx — comprehensive 12-section rebuild doc

### Folder Consolidation
Copied eb-git.ps1 from "maint scripts" (space) to "maint-scripts" (hyphen).
Still need to: delete old space folder, update g alias in $PROFILE.

### CLAUDE.md Updated
Added ai-toolkit venv, training commands, torch version warning, fixed maint-scripts paths.

---

## Immediate Next Steps (Session 35)
1. **HuggingFace login** — see BLOCKER section above, then test training
2. **Delete old `maint scripts` folder** (space version)
3. **Update g alias** in PowerShell $PROFILE to point to maint-scripts (hyphen)
4. **Run cache-offline-install.ps1** to build the offline cache
5. **Test GPU reset script** under real failure conditions

---

## What Was Done in Session 33 (2026-03-07)

### Name Fix — All Business Docs
Replaced all instances of "Nicco MacIntyre" with "Adrian Knotts (Nicco)" in:
- `earthmesh-deck.js` — 3 instances (title slide, founders slide, close slide)
- `ge-proposal.js` — 3 instances (cover letter signature, founder bio, contact section)

Rule going forward: legal name in all business/investor documents is **Adrian Knotts (Nicco)**.

### Version Increment Rule — Strictly Enforced
Confirmed MANDATORY rule: never overwrite existing output files. Always bump version
number before every copy to workspace. Reason: Claude.ai canvas caches by filename —
old versions remain in canvas until a new filename is used. Rule documented in CLAUDE.md.

### Earthmesh Investor Deck — Continued Iteration (v2 → v7)

**Mesh vs. Cellular comparison slide (added in v3/v4):**
- Initial version used hub-and-spoke vs. distributed topology diagram — WRONG framing
- Correct framing: mesh nodes are like cell towers (same concept), just low power + portable
- Rebuilt as side-by-side spec table: CARRIES / BANDWIDTH / POWER / RANGE / COST / DEPLOY TIME
- Headline: "Think of a mesh node as a portable cell tower — for text messages and coordinates, not streaming."
- CARRIES row: "Text & GPS messaging — no voice, no video" (explicit for non-technical investors)

**Solar deployment trailers added (v7):**
- New product line: 4 trailer types (EMS Scout / EMF Field / EMH Hub / EMC Command)
- Manufacturer: Jonathan Fletcher (Jon), Co-Founder / Manufacturing Operations
- Every trailer = mesh node + WiFi hotspot + offline media server
- Added slides: trailer lineup + margin breakdown table (56–58% GM)
- Updated: Founder → "The Founders" (Adrian left, Jon right)
- Updated: Business Model (5 revenue streams), Financial Projections, Use of Funds
- Sub-headline: "Manufactured by co-founder Jonathan Fletcher in his existing fabrication shop — no facility buildout required."

**Version history:** v1 (initial) → v2 (name fix) → v3 (mesh comparison) → v4 (force new cache) → v5 (AI queries wording) → v6 (no voice/video explicit) → v7 (trailers + Jon)

**Files in:** `eb_research/Earthmesh/` — v1 through v7 (pptx + pdf for each)

### PDF Generation
Generated PDFs for each version via LibreOffice headless + soffice.py helper.

### Earthmesh Pitch Graphics Script — queue-earthmesh-pitch.py
Created `local/scripts/queue-earthmesh-pitch.py` — ComfyUI/Flux queue script for
generating investor deck and proposal imagery. Same toolchain as queue-site-assets.py.

**8 batch categories, 44 total prompts:**
- `hero` (5) — Wide dramatic establishing shots for cover slide
- `problem` (5) — Grid failure, downed towers, isolation scenes
- `solution` (5) — Fast mesh deployment, node detail shots
- `nodes` (5) — Hardware product shots, ruggedized devices
- `trailers` (8) — All 4 trailer types (2 prompts each) in field settings
- `workshop` (6) — Metal fab, welding, trailer manufacture (Jon credibility shots)
- `deployment` (8) — Use cases: wildfire, disaster, festival, humanitarian aid
- `network` (4) — Nodes in landscape, topographic maps, connectivity concept
- `remediation` (6) — GE proposal: brownfield, bioremediation, environmental monitoring

**Key differences from queue-site-assets.py:**
- Default batch-size = 1 (re-run for variations, as user requested)
- Output prefix: `em-{batch_key}-{NN}` e.g. `em-hero-01`
- Includes `remediation` batch for GE Vernova proposal imagery

**Usage:**
```
python local/scripts/queue-earthmesh-pitch.py              # queue all 44 prompts
python local/scripts/queue-earthmesh-pitch.py --batch hero # just hero shots
python local/scripts/queue-earthmesh-pitch.py --dry-run    # preview
python local/scripts/queue-earthmesh-pitch.py --list       # see all batches
```

### Immediate Next Steps
1. Run `queue-earthmesh-pitch.py` — queue hero/problem/solution batches first for the deck
2. Review generated images, pull best into deck via earthmesh-deck.js
3. **Earthmesh deck:** Fill in equity % and pre-money valuation on Slide 13 (The Ask)
4. **GE proposal:** Fill in Adrian's email and phone; confirm auction company (CSRE?); confirm roger.martella@gevernova.com
5. **GE proposal:** Confirm v3 is the send version (name fixes applied)

---

## What Was Done in Session 32 (2026-03-06)

### GE Vernova Proposal — Locked as V1

Built and finalized a formal binder-ready corporate proposal targeting GE Vernova for partnership on the 130 E 1100 North remediation. File location:
`eb_research/HQ locations/GE_Remediation_Proposal_v1.docx`

**Key findings this session:**
- Davis County confirmed current owner of record is **GE Vernova** — inherited through the April 2, 2024 spinoff from General Electric Company
- Parcel number: **060940076** (Davis County)
- Auction company signage appearing at site is believed to be CSRE (not yet confirmed)
- Target contact identified: **Roger Martella**, Chief Corporate & Sustainability Officer, GE Vernova Inc., 58 Charles Street, Cambridge MA 02141
  - Former EPA General Counsel (Bush administration), former DOJ Natural Resources, co-led Sidley Austin's global environmental practice — the right person for this proposal
  - Likely email: roger.martella@gevernova.com

**Proposal structure (14 pages, 272 paragraphs):**
1. Cover page — addressed to Roger Martella, GE Vernova Inc.
2. Cover letter — acknowledges GE Vernova as current owner (inherited April 2024 spinoff), auction urgency, cooperative path
3. Executive Summary — contamination profile, BFPP status, funding stack, CERCLA callout
4. The Property and Its History — 70-year industrial arc (GM/EMD → Sperry Rand → GE → vacant)
5. The Current Situation — active deterioration, why deals failed, auction window, what it means for GE Vernova
6. The Earthback Project — founder credentials (first GSM call, consumer 3D printing), Spengler/Tech Asset/Earthmesh campus, vision statement
7. The Funding Stack — EPA TBA/cleanup grants, WFBC, Utah DEQ VCP, BFPP/EWA table
8. GE Vernova Partnership Options — 3 paths (charitable contribution, named partnership, records access)
9. Recommended Next Steps — Earthback actions + ask to GE Vernova

**Tone:** Written from position of authority — Earthback already has the plan, already knows the contamination profile, already has the funding mapped. GE Vernova is being offered a defined seat at the table before the auction closes.

**Status:** Locked as V1. Nicco reviewing. Pending: fill in Nicco's email/phone, confirm auction company name (CSRE?), send.

### Immediate Next Steps (HQ / GE Vernova)
1. Nicco reads V1 thoroughly
2. Fill in contact details: `[Nicco MacIntyre]` → real name, `[email]`, `[phone]`
3. Confirm auction company name — update any references if not CSRE
4. Find Roger Martella's direct email (likely roger.martella@gevernova.com — unconfirmed)
5. Send via certified mail + email

---

## What Was Done in Session 31 (2026-03-02)

### Construction Methods Directory — Full Feature Build
Nicco added an `eb_research/construction_methods-01/` directory with a comprehensive HTML guide covering 30 construction methods (23 green/natural + 7 conventional), ~1,273 curated images across 24 category folders, and a vision scan report. Built a complete feature from this research:

**Database (Supabase):**
- `SCHEMA_V10_methods.sql` — `construction_methods` table (30 methods with full details: description, materials, climates, pros, cons, practitioners, image folder refs), `member_skills` table (user↔method with 4-tier experience levels), RLS policies, `method_stats` view (claim counts per method), `claim_skill` and `unclaim_skill` RPC functions
- `SCHEMA_V10_seed.sql` — 30 INSERT statements auto-generated from the HTML guide content, with all JSONB arrays properly formatted

**4-tier skill system:**
- 🌱 Curious — "I'm learning about this method"
- 🔨 Hands-On — "I've built or assisted with this method"
- ⭐ Experienced — "I've completed multiple projects"
- 🎓 Trainer/Mentor — "I can teach or mentor others"

**Public methods page (`site/methods.html`):**
- Responsive card grid with all 30 methods, filter by category/difficulty, text search
- Expandable detail panels: full description, materials, climates, pros/cons, practitioners
- Logged-in users can claim skills with tier selection + optional note
- Community stats (builder counts per method) from `method_stats` view
- Matches Earthback design system (parchment, greens, clay, Cormorant Garamond + Inter)

**Profile integration (`site/profile.html`):**
- New "Building Skills" sidebar panel showing claimed method badges
- Skill badges are color-coded by tier, link to methods page
- Fetches from `member_skills` joined with `construction_methods`

**Navigation updates:**
- `nav.js` — Added "Methods" to primary row + "Building Methods" to More → Learn dropdown
- `app-nav.js` — Same additions for logged-in nav
- `sitemap.html` — Added Building Methods entry

### Immediate Next Steps
1. **Run SQL migrations** in Supabase SQL Editor:
   - `SCHEMA_V9b_ip.sql` (if not already run)
   - `SCHEMA_V9c_device.sql` (visitor device/location tracking from session 30)
   - `SCHEMA_V10_methods.sql` (construction methods + skills tables)
   - `SCHEMA_V10_seed.sql` (seed 30 methods)
2. **Push changes** from PowerShell
3. **Test methods page** — browse, search, filter, claim a skill
4. **USB mic arrives** → voice-caption.py for LoRA dataset
5. **Consider:** LoRA images for method cards (one hero image per method from the curated dataset)
6. **Set up Earthback SMTP** for branded auth emails (still pinned)

---

## What Was Done in Session 30 (2026-02-27)

### SDXL Hempcrete LoRA — Trained Successfully
- Switched from Flux to SDXL after Flux LoRA training proved unviable on 12GB VRAM (multiple sessions of troubleshooting — deadlocks, VRAM exhaustion, 286s/step)
- Created `train-hempcrete-sdxl.bat` using `sdxl_train_network.py` with `networks.lora` module
- Key fixes along the way: added `--network_train_unet_only` (text encoder caching assertion), fixed checkpoint path to `C:\AI\models\checkpoints\sdXL_v10VAEFix.safetensors`
- **Training completed:** 1500 steps, 83 minutes, ~3.3s/step, avg loss 0.134
- 4 checkpoints saved in `local\lora-output\hempcrete-sdxl\` (steps 500, 1000, 1500 + final)
- Copied final LoRA to `D:\AI\ComfyUI\models\loras\` for testing
- Initial results: "not bad but need to play around with it more"
- Discussed dataset improvement strategy: caption quality, image variety, removing weak images

### Signup Flow Fixed
- **Root cause identified:** Magic-link-only auth meant users were never authenticated when they reached `/community` — feed.html bounced them back to join.html (the loop)
- Added email + password signup (`sb.auth.signUp()`) — user is authenticated immediately
- Removed Maya Redhawk placeholder defaults from name fields
- Added "Skip for now — take me in" button on Screen 2 (profile builder)
- Fixed profile.html title/meta (was hardcoded "Maya Redhawk")
- Turned off "Confirm email" in Supabase to eliminate confirmation loop
- **Tested and working:** Tommy and Nicco both signed up successfully

### File Organization — `local/` Directory
- Created `local/` directory for all non-deployed files (scripts, datasets, training output, diagnostics)
- Moved all `.py` scripts, `.bat` files, datasets, lora dirs, logs into `local/`
- Simplified `.gitignore` — one `local/` entry replaces dozens of individual patterns
- Cleaned up mangled UTF-16 lora-output entry in .gitignore

### Voice Captioning Tool
- Built `local/scripts/voice-caption.py` — opens each image, records mic via sounddevice, transcribes with Whisper, writes `.txt` caption with trigger word prepended
- Controls: SPACE to record/stop, ENTER to save, E to edit, R to re-record, S to skip, Q to quit
- Flags: `--trigger EBHEMPCRETE`, `--skip-existing`, `--review`, `--model tiny/small/medium`
- Whisper installed on system Python
- **Blocked on USB microphone** — no audio input device available (Dell BIOS disabled onboard audio; audio runs through NVIDIA HDMI output only). USB mic ordered.

### Other
- Researched ostris/ai-toolkit as alternative to Kohya for Flux LoRA training on 12GB — has built-in `low_vram: true` mode with layer offloading. Community reports success on RTX 3060. Worth installing if Flux-quality LoRAs are needed later.
- Pushed signup fixes and gitignore cleanup to GitHub/Netlify

### Immediate Next Steps
1. **USB mic arrives** → run voice-caption.py to re-caption hempcrete dataset with better descriptions
2. **Re-train hempcrete LoRA** with improved captions
3. **Untrack old file paths from git** — some files may still be tracked under old locations
4. **Test LoRA in actual Earthback prompts** — characters + hempcrete in scene compositions
5. **Set up Earthback SMTP** in Supabase for branded auth emails (pin from this session)
6. **Consider ai-toolkit install** at `D:\AI\ai-toolkit\` for Flux LoRA training
7. **Run SCHEMA_V9b_ip.sql** in Supabase if not already run (IP + user tracking for eb-grove)

---

## What Was Done in Session 29 (2026-02-26)

### App nav — fixed positioning fix
- **`position: sticky` → `position: fixed`** in app-nav.js — nav now stays pinned at top of viewport at all times (matching public nav.js behavior)
- Added `.an-spacer` div (87px) after nav to push page content below the fixed header
- Mobile menu also changed to `position: fixed` so it stays aligned under the fixed nav
- **Root cause of sidebar cutoff**: sticky had no room to operate because `#app-nav` container was only as tall as the nav itself

### Feed sidebar scroll fix
- Sidebar `top: 95px` / `max-height: calc(100vh - 103px)` — fixed values since nav is always at viewport top
- **Removed scroll listener entirely** — no dynamic adjustment needed with fixed nav
- Sidebar card order unchanged: Profile → Updates → Navigate → Streams → Invite

### Reference image scraper (`scrape-reference-images.py`)
- New tool: scrapes images from curated hempcrete + 3D concrete URLs for LoRA training review
- 24 built-in source URLs across 2 categories (11 hempcrete, 13 3D concrete)
- Filters: skips <40KB, >25MB, logos/icons/SVGs; deduplicates by content hash; picks highest-res from srcset
- **URL file support added**: `python scrape-reference-images.py urls.txt -c earthships --only-file`
- `urls.txt` template created with usage instructions as comments
- Output: `lora-reference/hempcrete/` and `lora-reference/3d-concrete/` (or custom category)

### Command center simplification
- **Simplified `command-center.html`** — now a static reference for things that shouldn't go online
- Kept: reboot sequence, credentials/API keys (click-to-copy), services + Supabase deep links, deploy instructions, ComfyUI API, folder map, key files, important paths, Claude prompt copier
- Removed: session count, health bars, "What's Next" panel, "Last Session" box (all duplicated SESSION_NOTES/TRACKER)
- Added: credentials section, important paths section (comfy-env, models, Kohya, PuLID)
- Moved to project root, added to `.gitignore` (contains credentials)

### Git lock file fix — permanent solution
- **Root cause**: Cowork VM accesses repo through virtiofs FUSE mount; `unlink()` fails intermittently on Windows NTFS through the bridge, leaving orphan `.lock` files
- **Fix**: `maint scripts/eb-git.ps1` — wrapper that auto-cleans stale lock files before every git operation
- **Alias**: `g` command in PowerShell profile (e.g., `g add -A`, `g commit -m "msg"`, `g push`)
- **Convention going forward**: Claude edits files, Nicco commits from PowerShell with `g`

### Repo cleanup
- Removed `lora-reference/`, `dataset-hempcrete/`, `faces-reference/`, `graphics-review/`, `lora-training/` from git tracking
- Added all five to `.gitignore` — files stay on disk, just not in the repo
- These are local working directories for AI image generation, not source code

### Social media research
- Evaluated Buffer, Publer, Typefully, Later for social media scheduling
- Buffer and Publer recommended as best fit for Earthback's visual-heavy, multi-platform needs
- Nicco has a collaborator helping with social media launch

### Immediate Next Steps
- **LoRA training** — hempcrete + 3D printer datasets ready, switching to Sonnet for training runs
- **Run scraper** to collect more reference images, curate for LoRA training data
- **Social media setup** — finalize platform (Buffer/Publer), start scheduling launch content
- **PuLID face-locked generation** after LoRAs are trained

---

## What Was Done in Session 28 (2026-02-26)

### App nav (app-nav.js) — full rewrite
- **Self-contained** with embedded `<style>` block scoped to `#app-nav` — pages no longer define their own topbar CSS
- **Facebook-style visible link row**: Home · Circles · Map · Projects · Visualizer · Gallery + **More ▾** grouped dropdown (Tools / Community / Learn / Info)
- Messages icon + avatar on right side, early access banner preserved
- Mobile hamburger at 600px breakpoint
- **Removed orphaned `.topbar*` and `.brand-sub` CSS** from 7 app HTML pages (feed, circles, profile, projects, messages, project, create-project)

### Feed sidebar — nav card improvements
- **Navigate card moved above Streams** (order: Profile → Navigate → Streams → Updates → Invite)
- **AI Visualizer promoted** to visible links (above Map)
- **More ▾ toggle** restored with expanded link set: Gallery, Estimator, Messages, How It Works, About, Training Partners, Use Cases, Safety & Trust, Terms, Privacy
- Visible links: Home, Circles, AI Visualizer, Map, Projects

---

## What Was Done in Session 27 (2026-02-26)

### Public nav (nav.js) — full redesign
- **Iterated twice** to land on the right pattern:
  1. First pass: hamburger left + logo + quick links right + full dropdown panel (all links grouped)
  2. Final: **Facebook-style visible link row** — The Feed · Circles · Map · Visualizer · Estimator · Gallery always visible across the top; **More ▾** button opens a grouped dropdown for the rest
- **More ▾ dropdown** has 3 columns: Community (Feed, Circles, Map, Gallery) / Tools (Visualizer, Estimator) / Learn (How It Works, Use Cases, About, Training Partners) / Info (Safety, Terms, Privacy, Site Map)
- **Estimator** (designer.html) now linked in both top row AND dropdown Tools group
- Links progressively collapse into More at 960px and 720px — nav never overflows
- Dropdown closes on backdrop click, link click, or Escape
- Auth state preserved: Sign Out / My Feed when logged in
- **Removed orphaned CSS** (`.nav-hamburger`, `.mobile-nav-overlay`, `nav ul` rules) from 13 HTML pages — nav styles now live exclusively in nav.js
- **Recurring git lock file issue**: HEAD.lock and index.lock get left behind after each commit; requires manual deletion from Windows at `.git\HEAD.lock` / `.git\index.lock`

### Feed sidebar — improvements + bug fix
- **Sticky overflow bug fixed**: sidebar had `height: fit-content` with `position: sticky` — invite card was inaccessible until page bottom. Fixed with `max-height: calc(100vh - 100px); overflow-y: auto`
- **Navigate card added**: compact sidebar nav with icons — Home, Circles, Map, Projects, Gallery visible; More ▾ toggle reveals AI Visualizer, Estimator, Messages in-place
- **Updates card added**: small flash notifications card with green dot indicator; `#flash-text` span easy to wire to real data later
- **Streams card**: `#stream-items-dynamic` capped at 140px with internal scroll so card stays compact
- **Card order** (top to bottom): Profile card → Streams → Navigate → Updates → Invite
- **flex-shrink fix**: added `flex-shrink: 0` to `.sidebar-card` so the profile card can't be compressed by the flex scroll container
- **Pending push**: last 2 commits (reorder + flex-shrink) need push after lock file cleared

### Site tour — flagged as new feature
- User noted during nav discussion that a **site tour page** is needed — a guided walkthrough explaining causes, tools, and possibilities
- Not yet built; add to backlog

---

## Immediate Next Steps
1. **Push + verify** — push commit `c0db47d`, check app nav + feed sidebar at various resolutions
2. **Site tour page** — new guided walkthrough page; scope before building
3. **LoRA training** — hempcrete LoRA + 3D printer LoRA pipeline (datasets ready)
4. **PuLID face-locked generation** — pick reference faces → `setup-pulid.py` → `queue-pulid-faces.py`
5. **Integrate Flux assets into site** — heroes, sections, textures from `comfyui-output/`
6. **Run V9b (IP capture)** — `SCHEMA_V9b_ip.sql` in Supabase SQL Editor when ready
7. **3 SQL migrations still pending** — PROFILE_MIGRATION, V3, V4

---

## What Was Done in Sessions 25–26 (2026-02-26)

### SVG brand graphics package (30 files)
- Created full SVG brand system in `site/assets/img/` subdirectories:
  - **`brand/`** (6): wordmarks (dark/light/compact) + logomarks (leaf monogram, circle, badge)
  - **`icons/`** (15): leaf, seedling, sun, building, hammer, handshake, people, globe, pin, chat, heart, chart, shield, water, lightning
  - **`badges/`** (3): verified partner, community member, early access
  - **`map-pins/`** (3): project (green), member (moss), supplier (clay)
  - **`patterns/`** (4): leaf grid, topography, hemp weave, leaf vine divider
- All use Georgia font (system font, no import needed), brand colors (#1F3A2E, #C2A56C, #7e9b73, #F2EFE6)
- `<tspan>` technique for seamless "Earthback" color split with zero gap
- Review package in `graphics-review/PREVIEW.html`

### Sitewide emoji → SVG icon replacement
- Replaced ~130+ emoji across 18+ HTML/JS files with proper SVG `<img>` tags
- Added `.ico` CSS utility class for inline icons
- Added `_i()` JS helper function in feed.html for template literal contexts
- Updated favicon with leaf vein texture

### Brand standardization across all navs and footers
- **nav.js** (public nav, 13 pages): added leaf icon to logo
- **app-nav.js** (app nav, 7 pages): replaced 🌿 emoji with SVG leaf, replaced 💬 with SVG chat
- **footer.js**: added leaf icon, switched from Cormorant Garamond to Georgia, removed uppercase
- **Inline logos** on login.html, auth-callback.html, profile.html, project.html: added leaf icon
- **`.nav-logo` CSS on 14 pages**: removed `text-transform: uppercase`, removed `letter-spacing: 0.1em`, switched to Georgia
- **`.footer-logo` CSS on 5 pages** (profile, project, terms, explore, privacy): same fixes
- Brand now renders as mixed-case "the Earthback Project" consistently everywhere

### Early access banner centralization + new CTA copy
- Created `site/assets/js/early-access-banner.js` — single config file controls bottom sticky banner on all 7 app pages
  - `enabled: true/false` toggle to kill it everywhere
  - Dismiss button (session-scoped via sessionStorage)
- Removed 7 inline `<aside>` banners from app pages, replaced with `<script>` tag
- Added sub-header banner to **app-nav.js** (matches public nav sub-header)
- Updated copy everywhere: **"Claim your username and get in early — your voice shapes what gets built. Join free →"**
  - nav.js (public pages sub-header)
  - app-nav.js (app pages sub-header)
  - early-access-banner.js (app pages bottom sticky)
- CTA now links to `join.html` instead of mailto feedback

### Hempcrete LoRA dataset committed
- `dataset-hempcrete/curated/` — 15 curated images + captions pushed to repo
- `lora-training/hempcrete pics/` — raw source images pushed

---

## Immediate Next Steps
1. **LoRA training** — hempcrete LoRA + 3D printer LoRA pipeline (datasets ready)
2. **PuLID face-locked generation** — pick reference faces → `setup-pulid.py` → `queue-pulid-faces.py`
3. **Integrate Flux assets into site** — heroes, sections, textures from `comfyui-output/`
4. **Run V9b (IP capture)** — `SCHEMA_V9b_ip.sql` in Supabase SQL Editor when ready
5. **Site cleanup walkthrough** — go through every page detail

---

## What Was Done in Session 24 (2026-02-26)

### Project Designer → Project Estimator rebrand
- Renamed all user-visible text from "Project Designer" to "Project Estimator" across 4 files
- `designer.html`: title, meta description, h1, hero copy updated
- `footer.js`: nav link text "Designer" → "Estimator" (href stays `designer.html`)
- `sitemap.html`: "Project Designer" → "Project Estimator" with updated description
- `visualizer.html`: hint tip text updated from "For the Designer tool" → "Ready to estimate costs?"
- Filename kept as `designer.html` to avoid breaking bookmarks

### All pending SQL migrations run in Supabase
- V6b (visions UPDATE policy) — ✅ run
- V6c (no self-likes) — ✅ run
- V7 (partner_inquiries) — ✅ run
- V7b (partner URL column) — ✅ run
- V8 (map_pins) — ✅ run
- V8b (unmet_need pin type) — ✅ run
- Only V9b (IP capture) still pending — run when ready

### eb-grove.html — new admin panels
- **Flagged Visions review panel** — shows all flagged visions with reporter reasons, image thumbnails, prompt text. Restore (unflag) or Delete (permanent) buttons. Auto-refreshes every 2 min.
- **Partner Inquiry inbox** — shows all training.html form submissions. Mark as reviewed, reply via email link. Shows org name, contact, focus area, message, website. Auto-refreshes every 5 min.
- **What's Next panel updated** — removed stale items (git push session 22, etc.), added current priorities (LoRA, Flux integration, PuLID, site cleanup, V9b)

### Documentation catch-up
- `db/README.md` updated with all migration entries (V6c–V9b) and run statuses
- `TRACKER.md` — eb-grove.html now has dedicated admin portal section with full checklist, added to pages list and Quick Status
- SESSION_NOTES.md and TRACKER.md updated for session 24

### Confirmed already done (from prior sessions)
- Gallery page (gallery.html) — fully built with cards, likes, lightbox, reporting
- Visualizer share button + credit pickup — working
- Profile visions tab — working with like buttons and credit logic

---

## Immediate Next Steps
1. **Run V9b (IP capture)** — `SCHEMA_V9b_ip.sql` in Supabase SQL Editor when ready
2. **LoRA training** — hempcrete LoRA + 3D printer LoRA pipeline
3. **Integrate Flux assets into site** — heroes, sections, textures from `comfyui-output/`
4. **PuLID face-locked generation** — pick reference faces → `setup-pulid.py` → `queue-pulid-faces.py`
5. **Site cleanup walkthrough** — go through every page detail

---

## What Was Done in Session 23 (2026-02-25)

### Live Traffic Monitor + Analytics (session 22 continuation)

#### SCHEMA_V9_analytics.sql (NEW)
- `page_views` table: id (UUID), page (TEXT), referrer (TEXT), session_id (TEXT), created_at (TIMESTAMPTZ)
- Indexes on created_at DESC, session_id, page
- RLS: anon INSERT + public SELECT (no PII stored — publishable key is safe)
- `ALTER PUBLICATION supabase_realtime ADD TABLE page_views` — required for live feed
- **⚠️ Still needs to be run in Supabase SQL Editor before tracking goes live**

#### nav.js — page-view tracking added
- Fire-and-forget `fetch()` POST to `/rest/v1/page_views` on every page load
- Session ID via `sessionStorage` (`eb_sid`) — resets per browser session, persists across page hops
- Same-site referrer filtering — external referrers stored as null (shows as "direct")
- Fully wrapped in try/catch — tracking never breaks the page

#### eb-grove.html — Live Traffic Monitor section
- 4 stat cards: Active Now (last 10 min), Page Views Today, Sessions Today, All-Time
- Visitor Session Trails — groups by session_id, shows page breadcrumbs, deduplicates consecutive repeats, active/recent/old states
- Live Feed — Supabase Realtime `postgres_changes` subscription, flash animation on new rows
- Top Pages Today — CSS bar chart of page counts
- Auto-refreshes every 3 minutes via `setInterval`

### Banner Bug Fixed — "Data may reset" text

- Root cause found: banner was injected via **nav.js** (not hardcoded in individual HTML files)
- All HTML file edits from earlier in the session were red herrings — nav.js was the source on every page
- Fixed in nav.js: "PRE-LAUNCH / data may reset" → "EARLY ACCESS / building in the open"
- Individual HTML page banners also cleaned up (now use `<aside id="eb-early-access">`)
- Confirmed propagating correctly via Netlify after push

### Git / Push Workflow
- All session 22+23 work committed and pushed (24 files, 4,211 insertions)
- Resolved "up to date" confusion: files need `git add` + `git commit` before `git push`
- `tracker/command-center.html` is gitignored — must use `-f` flag or update .gitignore to include it

### Immediate next
- [x] **Run SCHEMA_V9_analytics.sql** — done ✓ traffic monitor working, data coming in overnight
- [ ] **LoRA work** — hempcrete LoRA (Nadia) + 3D printer LoRA (get Pexels/Pixabay API keys → collect → curate → caption → train)
- [ ] **PuLID reference faces** — pick best charsheet panel per char → faces-reference/CharacterName.png → run queue-pulid-faces.py
- [ ] **IP tracking** — run db/SCHEMA_V9b_ip.sql in Supabase (adds ip_address column + RPC function; nav.js ready)
- [ ] **Run 3 still-pending SQL migrations** — PROFILE_MIGRATION → SCHEMA_V3 (messages) → SCHEMA_V4 (post images)
- [ ] **Mobile cleanup** — site looks good on desktop/all browsers; mobile needs polish
- [ ] **Integrate Flux assets** — rendered images into site heroes/sections
- [ ] **Set up social media accounts** — Twitter + Instagram

---

## What Was Done in Session 22 (2026-02-25)

*Planning session — pin map, content bot, social pipeline, Moonback/Marsback.*

### Pin Map Plan — docs/PINMAP_PLAN.md (UPDATED)
- Map framing: universal tool for any community type (rebuilding, greenhouses, cohousing, etc.) — not Ukraine-specific
- Hotspot system added: 5 curated pin categories (Rebuilding, Resource Hub, Active Build, Partner Org, Opportunity)
- Each category has a distinct color; team places these manually before member density builds
- Initial seed list: Kherson, Mykolaiv, New Orleans, Oaxaca, Marrakech, Appalachia, Tamil Nadu, Accra, Taos
- "Claim your pin" onboarding interstitial — post-signup, 2-tap flow, map visible behind dialog
- Proximity detection: if new member's location matches a Rebuilding hotspot → special "join this effort" onboarding
- Layer defaults: Rebuilding + Projects on by default (map looks alive from day one)
- Build sequence revised: Phase 1 = hotspot seeds, Phase 2 = public map.html (useful before any members pin), then member pins, then onboarding

### Content Bot & Social Pipeline — docs/CONTENT_BOT_PLAN.md (NEW)
- **Earthback Dispatch** — platform-native bot org account, posts daily across all circles
- Content types: technique/knowledge posts, project spotlights, news roundups, resource links, community prompts
- Social pipeline: Dispatch posts → Nicco approves queue → format for Twitter/Instagram → post
- Phase 1: curate 30-50 seed posts manually, load with staggered timestamps — fastest path to live circles
- Phase 2: RSS → summarize → post script (`generate-dispatch.py`)
- Phase 3: Claude API generates original posts per circle on demand
- Data model: `is_bot` + `bot_type` on profiles; `scheduled_for` + `status` + `source_url` on posts
- Social media launch this week: start with Twitter + Instagram, manual posting initially

### Moonback / Marsback
- Nicco is seriously considering registering both domains
- Same platform template, same circles/dispatch system, off-world context
- Natural building ↔ space habitat research overlap is real (basalt fiber, mycelium, 3D-printed earthen)
- Action: register domains now, build later

### Vision notes
- Map is universal — not a cause, not a campaign. Wherever communities need building, Earthback applies.
- Geographic view of membership tells you what services to build for each region
- "If you build it they will come" — the value prop is rare enough and real enough that discoverability will follow quality
- Onboarding goal: new member plugs directly into whole community (right circles, right people, right geography) in first session
- Bot/dispatch keeps platform alive pre-critical-mass; displaces itself as member posting takes over

### Hemp Blocks + Hempwood Research + Platform Updates (Session 22 continued)

#### hotspots-seed.csv — EXPANDED to 89 entries (88 usable pins + header)
- Added 11 new entries covering hemp blocks and hempwood suppliers
- Added 24 unmet-need pins for global south areas of need (see below)
- **Hemp block companies added:** Just BioFiber (Canada), Renewabuild (BC), Lancaster Lime Works (PA), DTE Materials (CA), 8th Fire Innovations/DiVita (Edmonton), Cânhamor (Portugal), HempFlax (Netherlands)
- **Hempwood companies added:** Fibonacci LLC / HempWood® (Murray KY), Plantd Materials (Durham NC), Boardwurks Biocomposites (Florida)
- Re-classified IsoHemp, Hemp and Block, Hemp Block USA, IsoHemp France → `hemp-blocks` slug (were `hempcrete`)
- Category breakdown: hempcrete (33), hemp-blocks (10), hempwood (3), straw-bale (7), cob (5), unmet-need (24), rest distributed
- **Key finding:** Plantd Materials (ex-SpaceX founders) is closest to structural hemp OSB — $22M raised, structural panels in prototype. Fibonacci is the only company selling commercial hemp lumber today (non-structural). Load-rated structural hempwood is ~3-5 years out.
- **Dakota Hemp** (South Dakota): first US interlocking hemp block manufacturer expected mid-2026 — worth connecting with
- CSV rebuilt with Python `csv.QUOTE_ALL` (RFC 4180 compliant — fixes comma-in-location_name column misalignment)

#### designer.html — Hemp Block Masonry added as 6th construction method
- New chip: "Hemp Block Masonry" (`hemp-block` val) in construction method selector
- Calculates block count (~120 blocks/yd³), lime mortar, timber frame needs
- R-value: 2.4/inch (same as cast hempcrete)
- Carbon: slightly less negative than cast hempcrete (-0.34 vs -0.37 tCO₂/yd³) — pre-curing offset
- Cost: $750/yd³ material (vs $800 cast), $16/sqft labor (blocks faster than casting), $2,500 equipment
- Needs list: shows Hemp Blocks count, Lime Mortar + Timber Frame, Hemp Block Mason skill
- Wall annotation: "Hemp Block Wall — R-[n]"

#### DISPATCH_POSTS_V2.md — hemp-blocks and hempwood sections added
- **hemp-blocks circle:** 3 posts + SRC-16 sourcing guide
- **hempwood circle:** 3 posts + SRC-17 sourcing guide
- Image queue updated: 4 new images needed (2 hemp-blocks, 2 hempwood)
- Hempwood images can queue now (different visual from hempcrete, no LoRA needed)
- Hemp-block images: hold for hempcrete LoRA (same pale grey-green aesthetic)
- Total posts now: ~118 across all circles

#### Community Map — map.html (NEW)
- **Leaflet.js + OpenStreetMap** — fully open-source, no API key needed, perfectly aligned with Earthback ethos
- Full-viewport map page at `site/map.html`; nav added via nav.js + inline nav CSS (same pattern as explore.html)
- Dynamic top offset: `requestAnimationFrame` + `getBoundingClientRect()` on `<nav>` → correctly accounts for nav + prelaunch banner (~88-90px)
- **6 pin categories** with distinct colors: Rebuilding (#E8A838), Resource Hub (#2D8A7A), Active Build (#C26B42), Partner Org (#4A6FA5), Opportunity (#4a7c3f), Unmet Need (#9E4A4A)
- SVG drop-pin markers via `L.divIcon`; popups with category badge, title, location, description, "Visit site →" link
- Layer toggle panel with per-category pin counts; click to show/hide each category
- Loads hotspots from Supabase `map_hotspots` table via publishable key — works for all visitors including logged-out
- "Loading pins…" overlay removed after data loads; graceful error state if Supabase fails
- Map link added to nav.js (desktop + mobile overlay) — appears before Visualizer in nav order
- **88 pins loaded and working** — user confirmed "HELL YEAH! I can't wait until this map looks like a mycelium maze"

#### "Unmet Need" pin category — 24 global south pins
- User rejected "Opportunity" as exploitative framing for areas of need/disaster
- Brainstormed alternatives: Solidarity, Calling, Frontline, Unmet — user chose **"Unmet Need"** — honest, specific, no political baggage
- **Color:** Deep terracotta `#9E4A4A` — distinct from Active Build clay, conveys urgency without alarm-red
- **24 pins across:** Malawi, Mozambique, Ethiopia, Haiti, Nepal, Bangladesh, Myanmar, Central African Republic, South Sudan, Yemen, Papua New Guinea, Sierra Leone, Liberia, Madagascar, Burkina Faso, Niger, Mali, Chad, DRC, Zambia, Honduras, Bolivia, Guatemala, Cambodia
- All marked `status = 'planned'` — curated from news/housing-crisis data as areas where green building expertise is most needed
- Added to `SCHEMA_V8b_unmet_need.sql` (new CHECK constraint migration), full seed in `hotspots-seed.sql`, incremental in `SEED_unmet_need_pins.sql`

#### Database — SCHEMA_V8 + V8b run in Supabase ✅
- **SCHEMA_V8_map.sql** — creates `map_hotspots` table with full schema (lat/lng, category, title, description, url, status, RLS, indexes, updated_at trigger)
  - Admin write policy removed — `is_admin` column doesn't exist yet; service role bypasses RLS entirely for Supabase dashboard writes
- **SCHEMA_V8b_unmet_need.sql** — drops old category CHECK constraint (found via `pg_constraint`), recreates it adding `'unmet-need'`
- Both run successfully; **hotspots-seed.sql** run after DELETE FROM → all 88 pins loaded

#### Incremental SQL update pattern established
- `hotspots-seed.sql` = full snapshot → run after `DELETE FROM map_hotspots` for a full rebuild
- `SEED_*.sql` = incremental inserts only → safe to run on live DB without touching existing rows
- Schema changes = `SCHEMA_V*.sql` files → always run schema before seed

### Immediate next
- [ ] **Review overnight image output** — new char charsheets + T4/T5/face batches in comfyui-output/
- [ ] **Pick PuLID reference faces** — best charsheet panel per char → faces-reference/CharacterName.png
- [ ] **Write seed content pack** — 30-50 Earthback Dispatch posts for circle seeding (can do with Claude)
- [ ] **Create Dispatch bot account** — insert into Supabase profiles manually
- [ ] **Register Moonback and Marsback domains** — before someone else does
- [ ] **Set up social media accounts** — Twitter + Instagram this week
- [ ] **Run 3 still-pending SQL migrations** — PROFILE_MIGRATION → SCHEMA_V3 (messages) → SCHEMA_V4 (post images) in Supabase SQL Editor
- [ ] **Map — member pins** — add lat/lng + map_visibility to profiles table, show real member dots on map
- [ ] **Map — project pins** — wire existing project lat/lng to map_hotspots or separate layer
- [ ] **"Claim your pin" onboarding** — post-signup interstitial, 2-tap flow, map visible behind dialog
- [ ] **git add / commit / push** — all session 22 changes (hemp blocks, map.html, schema V8/V8b, dispatch posts, nav.js)

---

## What Was Done in Session 21 (2026-02-24)

*7 new characters added, charsheets + full batches queued overnight.*

### 7 new characters added to queue-batches.py and queue-charsheets.py
- **Britta Svensson** — 27, Swedish, blonde, straw bale + natural plaster, Skåne, seed 440001
- **Sofia Marini** — 31, Italian, brunette, earthen architecture + lime plaster, Tuscany, seed 550001
- **Owen Marsh** — 23, white American, young, off-grid + tiny homes, Vermont, seed 660001
- **Callum Reed** — 25, Welsh, young, cordwood + cob, Brecon Beacons, seed 770001
- **Joseph Runningwater** — 67, Coast Salish/Lummi Nation, elder male, land steward + watershed, Pacific Northwest, seed 880001
- **Tariq Hassan** — 29, Yemeni, traditional earthen tower house preservation, Hadhramaut Valley, seed 990001
- **Devon Clarke** — 25, Black American, urban food systems + mutual aid, New Orleans, seed 111001
- Roster now: **19 characters total**
- Full T5 scenes (5 scenes each) written for all 7 new characters
- All 7 added to CHARS in both queue-batches.py and queue-charsheets.py

### Overnight queue running
- Charsheets for all 7 new characters: 7 × 3 sheets × 2 seeds = **42 images**
- Full T4 + T5 + face batches for all 7: `--reseed --batch-size 3` — **~315 images**
- Both running overnight

### Immediate next (when back)
- [ ] **Review new character charsheets** — check face consistency across panels
- [ ] **Review all overnight output** — new chars T4/T5/face + any remaining from prior batch
- [ ] **Pick PuLID reference faces** — best charsheet panel per character → `faces-reference/CharacterName.png`
- [ ] **Update docs/CHARACTERS.md** — add the 7 new character bibles
- [ ] **Integrate Flux assets into site** — heroes, section backgrounds, textures

---

## What Was Done in Session 20 (2026-02-24)

*Shared gallery, training partners page, sitemap, 3D project designer, shared nav/footer components.*

### Shared Gallery — gallery.html (NEW)
- Public gallery page showing community-shared AI visions from the visualizer
- Vision cards: thumbnail, creator name (linked to profile), prompt snippet, structure/climate/style chips, like count + heart button
- Like system: toggle INSERT/DELETE on `vision_likes` table, increments/decrements `like_count`
- **Self-like prevention**: users cannot like their own visions (button hidden or disabled)
- Report system: flag button opens modal with reason radio + optional details, submits to `vision_flags`
- Auth-gated interactions: "Sign in to like" for unauthenticated users
- Credit award: likes earn credits for the vision creator (max 5 per vision)
- Loads shared, non-flagged visions sorted newest first with creator info via Supabase join

### SCHEMA_V6_gallery.sql — NEW (✅ Run in Supabase)
- Added sharing/engagement columns to `visions`: `is_shared`, `is_circle_only`, `circle_slugs`, `like_count`, `credit_earned`, `is_flagged`
- New `vision_likes` table with unique constraint on `(vision_id, user_id)`
- New `vision_flags` table with reason, details, is_reviewed
- RLS policies: public read on shared+unflagged visions, authenticated like/flag

### Shared Nav & Footer Components
- **nav.js** (`site/assets/js/nav.js`) — shared navigation component injected into `<div id="site-nav">` on all pages
  - Handles: nav links, mobile hamburger menu, auth state (Sign In ↔ Sign Out swap), active page highlighting
  - Brand treatment: "the Earthback Project" typography
  - Scroll effect: background opacity change on scroll
- **footer.js** (`site/assets/js/footer.js`) — shared footer component injected into `<div id="site-footer">`
  - 4-column grid: brand blurb, Platform links, Learn links, Legal links
  - Responsive: stacks on mobile
  - Added Designer + Site Map links

### Training Partners Page — training.html (NEW)
- "Skills & Training" page for certification pathway partners
- Contact form: org name, contact name, email, focus area (dropdown), website URL, message
- Submits to `partner_inquiries` table in Supabase
- Content assurance: "We will never use your media, content, or branding without your explicit approval."
- Added to nav and footer links

### SCHEMA_V7_partner_inquiries.sql — NEW (✅ Run in Supabase)
- New `partner_inquiries` table: org_name, contact_name, email, focus_area, message, status, created_at
- RLS: authenticated INSERT, no public read

### SCHEMA_V7b_partner_url.sql — NEW (✅ Run in Supabase)
- `ALTER TABLE partner_inquiries ADD COLUMN website_url TEXT`

### Sitemap Page — sitemap.html (NEW)
- Full site map organized into 6 sections: Discover, Platform, Creative Tools, Learn, Account, Legal
- Each entry has page name + description
- Matches site design language (parchment background, Cormorant Garamond headings, clay accents)

### 3D Project Designer — designer.html (NEW, MAJOR BUILD)
- **Three.js parametric building configurator** with live 3D preview
- 5-step wizard: Foundation & Type → Interior Layout → Roof & Energy → Materials & Finish → Export
- Three.js scene: PerspectiveCamera, OrbitControls, shadow-casting sunlight, fog, ground plane with grid
- Parametric building model: foundation slab, 4 walls with configurable thickness, windows (auto-spaced), door, gable roof with pitch slider, solar panels, optional porch
- **5 construction methods** with distinct material/cost/carbon profiles:
  - 3D Printed Hempcrete (carbon-negative, ~$85-105/sqft)
  - 3D Printed Concrete (carbon-positive, ~$90-110/sqft)
  - Manual Hempcrete (carbon-negative, ~$75-95/sqft)
  - Conventional Build (carbon-positive, ~$120-160/sqft)
  - Hybrid (mixed, ~$95-125/sqft)
- Live material calculations panel (R-values, carbon impact, cost estimates, BOM)
- Auto-generated needs list based on construction method
- 4 camera presets (3D, Front, Top, Side)
- Working exports: glTF/GLB 3D model, CSV Bill of Materials, JSON config
- Wall colors vary by construction method in 3D view

### Nav CSS Fix for Designer
- designer.html was missing all nav CSS — rendered as unstyled text links
- Added ~80 lines of nav styles matching other pages (nav, .nav-inner, .nav-logo, brand classes, hamburger, mobile overlay, 860px breakpoint)
- User confirmed fix working on both Firefox and Chrome

### Site updates
- Footer: added Designer + Site Map links
- Sitemap: added Project Designer entry under Creative Tools
- Nav: gallery.html and visualizer.html links present in shared nav

### Visualizer Prompt Tips (session 20b)
- Dynamic 5-category tips panel (28 tips total) toggled from "Prompt tips" button next to textarea
- Categories: Basics (6), Materials (6), Systems (5), Composition (6), Style Tips (5)
- Each tip has icon, bolded key takeaway, and most include a "Try this" example prompt
- "Use this prompt" button drops example directly into textarea with visual flash
- "More tips" shuffles 3 tips at a time; randomized order on each open
- Tabbed navigation across categories

### Designer Roof Fix (session 20b)
- Roof planes were inverted (V-shape valley instead of ^-shape peak)
- Root cause: rotation.x signs were swapped between left and right roof planes
- Fixed: left roof rotation.x from negative to positive, right from positive to negative
- Solar panel rotation also corrected to match left roof slope

### Commits this session
1. Training form URL field + V7b schema
2. `6437e8a` — Project Designer with Three.js configurator
3. `d5811c6` — Construction method additions (5 methods)
4. `e28f16a` — Nav CSS fix for designer page
5. `c8863f6` — Visualizer prompt tips + session 20 docs
6. Roof inversion fix + final docs update

### Database migrations run this session
- V5 (visions) — run in prior sub-session
- V6 (gallery — vision_likes, vision_flags, sharing columns) — ✅ run
- V7 (partner_inquiries) — ✅ run
- V7b (partner_inquiries website_url) — ✅ run

### Immediate next (tomorrow)
- [ ] **Review Flux overnight output** — charsheets + site assets + T4 re-run in `comfyui-output/`
- [ ] **Pick PuLID reference faces** — best charsheet panel per character → `faces-reference/CharacterName.png`
- [ ] **Download PuLID models** — `python setup-pulid.py`
- [ ] **Integrate Flux assets into site pages** — use rendered images for heroes, sections, textures
- [ ] **Run pending SQL migrations** — PROFILE_MIGRATION, SCHEMA_V3 (messages), V4 (post images)
- [ ] **Profile nav link** — add link to own profile from every page
- [ ] **og:image** — design the 1200×630 social sharing card

---

## What Was Done in Session 19 (2026-02-24)

*Character reference sheets, big site asset batch, overnight queue.*

### Face consistency approach — triptych reference sheets
- Problem: face seeds wander too much across separate images; characters don't look like the same person across batches
- Solution: wide single-image triptychs (3 panels per image) — Flux locks one face across all 3 panels in one generation
- Built `queue-charsheets.py` — 12 chars × 3 sheet types × 2 seed sets = **72 images**
- Dimensions: 1536×640 wide landscape (~512×640 per panel, stays near 1MP)
- Sheet A: front / 3-quarter-left / 3-quarter-right (neutral angles)
- Sheet B: thinking / mid-sentence / warm smile (expressions)
- Sheet C: tight eye crop / standard face / wider shoulders (crop variations)
- 2 seed sets per char: `char_seed` and `char_seed + 7` — same face neighborhood, subtle variation
- Use sheets to pick best face for PuLID reference images

### Site asset batch — big overnight run
- Built `queue-site-assets.py` — 14 themed categories, ~80 prompts, default batch_size=2
- All documentary/photojournalistic style matching character imagery
- Wide (1344×896) for: establishing, landscape, cohousing — portrait (896×1152) for everything else
- Categories: establishing, hempcrete, earthen, strawbale, timber, solar, water, food, community, ecology, shelter, texture, hands, landscape, fabrication, mycology, cohousing
- Supports `--list`, `--batch theme1,theme2`, `--batch-size N`, `--dry-run`

### Overnight queue running
- **101 jobs queued** — charsheets + site assets running through the night
- PowerShell note: use `;` not `&&` to chain commands (Windows PS 5 doesn't support `&&`)
- Command used: `python queue-charsheets.py; python queue-site-assets.py`

### Site asset strategy discussion
- Flux: great for photographic assets (heroes, sections, textures, community scenes)
- Not Flux: icons, logos, badges, social cards, UI elements — those need design work
- og:image (1200×630 social card) still outstanding — needs design, not Flux
- Visual treatment: consistent documentary/photojournalism across all site imagery

### Immediate next (tomorrow)
- [ ] **Review overnight output** — charsheets in `comfyui-output/` named `charsheet-NAME-A/B/C_*`; site assets named `site-THEME-NN_*`
- [ ] **Pick PuLID reference faces** — best sheet panel per character → `faces-reference/CharacterName.png`
- [ ] **Download PuLID models** — `python setup-pulid.py`
- [ ] **Run PuLID** — `python queue-pulid-faces.py`
- [ ] **Review T4 re-run** — pick best character scenario shots
- [ ] **Run hempcrete LoRA batch** — `python queue-hempcrete-lora.py` (still 0 images)
- [ ] **og:image** — design the 1200×630 social sharing card

---

## What Was Done in Session 18 (2026-02-24)

*Vision persistence, rotating credits, positioning rework, gallery repopulate bug.*

### Vision persistence system (committed + pushed + live)
- New `visions` table via SCHEMA_V5_visions.sql — **migration run in Supabase**
- `visions` storage bucket created in Supabase (public, with user-folder upload policy)
- Save flow: render → click "Save to profile" → fetch image as blob → upload to Supabase Storage → insert DB row → gallery reloads
- Gallery below generator shows saved visions with image, prompt snippet, chips, date
- Click-to-repopulate: clicking a gallery card should refill form + show image (BUG: not firing, investigating)
- Save hint text added below toolbar: "Images aren't kept unless you save them..."

### Rotating credit system (committed + pushed + live)
- Replaced flat 20/day limit with accrual-based credits
- Final values: 1 credit per render, earn 1 every 2 hours (~12/day), cap 25
- First visit starts at full 25. Counter shows "X credits · +1 in 1h 42m"
- localStorage-based under key `earthback_viz_credits`
- formatCountdown() helper for proper hours+minutes display

### Positioning language rework (committed + pushed)
- Replaced "no algorithm, no ads" across CLAUDE.md, SESSION_NOTES.md, ghost profile handoff
- New language: "No algorithm, no data harvesting, no feed manipulation. Revenue comes from connecting members with aligned suppliers and materials partners — not from selling attention."

### Chrome crash warning removed from CLAUDE.md
- VM crashes happen regardless of Chrome tool usage — not caused by Chrome MCP
- Simplified to just recovery instructions

### BUG IN PROGRESS: Gallery card click → repopulate not working
- Cards render, have hover state, but onclick doesn't fire
- `repopulateVision()` is at global scope, should be accessible
- Suspect: double JSON.stringify in onclick attribute may be producing bad escaping
- **Next step:** inspect in Chrome devtools to see the actual rendered onclick attribute

---

## What Was Done in Session 15 (2026-02-23)

*AI image generation infrastructure, character curation, file naming overhaul, 3D printer LoRA pipeline.*

### Chrome MCP crash — identified and documented
- Chrome MCP tools (`tabs_context_mcp`, `computer`, `navigate`, etc.) cause `CoworkVMService` to hang and crash — happened a second time this session when checking a browser tab
- Root cause: Chrome MCP bridge conflicts with the non-WSL VM virtualization stack, especially under ComfyUI load
- Fix script already existed: `maint scripts/fix-cowork-vm.ps1` — run as Administrator in PowerShell
- **Added explicit prohibition to CLAUDE.md** — Claude now knows never to use Chrome tools in this session

### CLAUDE.md — created (auto-read every session)
- New file at `/Earthback/CLAUDE.md`; Cowork reads it automatically at session start (no prompt needed)
- Contains: machine quirks (no WSL, ComfyUI Python path), Chrome crash warning + fix command, ComfyUI REST API endpoints, Flux node ID table, seed strategy, all script reference table, key docs table, working directory convention
- **This is the primary orientation file for future sessions** — update it when anything fundamental changes

### command-center.html — updated
- Added ComfyUI to the reboot sequence (step 6: run `comfy-run.bat`; step 7: open Cowork)
- Added red warning strip for the Cowork crash fix referencing `maint scripts\fix-cowork-vm.ps1`
- Added full AI Image Generation section: batch scripts list, ComfyUI API code block + link, output dir, 3D printer LoRA pipeline
- Updated Key Files to include CLAUDE.md, fix-cowork-vm.ps1, CHARACTERS.md, CIRCLES.md

### Character image review — T1-T4 all rejected
- Built `tracker/char-gallery.html` — gallery grouping all 940 character images by character with subsections (Faces, T4-01 through T4-05, T5 scenes), 180×180px thumbnails, lightbox zoom
- After review: **all 237 T1-T4 character images rejected** — fixed seeds caused near-duplicate output (same underlying noise = same face/pose every run)
- Nicco moved all to `comfyui-output/_rejected/` in Windows Explorer
- T5 and face images (198 files) kept

### File naming overhaul — character-first convention
- **Old naming:** `T4-chars-NAME-face-front_00001_.png` / `T5-chars-NAME-01_00001_.png`
- **New naming:** `chars-NAME-face-front_00001_.png` / `chars-NAME-T5-01_00001_.png`
- Character-first so Windows Explorer sort-by-name groups all shots of one character together (critical for curation workflow)
- **198 existing files renamed** via Python script: 36 face images + 162 T5 scene images
- **All 10 prefix strings updated in `queue-batches.py`** — face-front/left/right/down/talk and T4-01 through T4-05 all now use `chars-{name}-*`; T5 prefix changed to `chars-{name}-T5-{i+1:02d}`

### T4 re-run queued
- Command: `python queue-batches.py --batch t4 --reseed --batch-size 3`
- 12 chars × 5 batches × 3 images = **180 new images** with random seeds (no more duplicates)
- User ran from Windows; was queuing as session ended (had ~40 jobs still pending from prior run)
- `--reseed` flag: bypasses character seeds entirely, uses fully random seeds per job for genuine variety

### 3D Printer LoRA pipeline — built
All scripts created at `/Earthback/`:
- `collect-3dprinter-images.py` — downloads CC0 photos from Pexels + Pixabay APIs; 15 search terms; min 800px; saves metadata JSON
- `curate-3dprinter-images.py` — smart center-crop to 1024×1024; rejects images under 600px short-side or aspect ratio >3.5; optional `--review` mode
- `caption-3dprinter-images.py` — template captions (`a [type] 3D FDM printer, [state], [lighting]...`) or BLIP-2 auto-caption; `--apply-edits` flag; Kohya format `.txt` files
- `train-3dprinter-lora.bat` — Kohya SS `flux_train_network.py` command; 1500 steps, rank 16, alpha 16, lr 1e-4, bf16, AdamW8bit
- `docs/HANDOFF-3D-PRINTER-LORA.md` — updated with scope decision, per-type visual grammar table, full pipeline, dataset specs, evaluation prompts

### Immediate next
- [ ] **Review char-gallery after T4 re-run completes** — pick best 2-3 shots per character
- [ ] **Select PuLID reference images** — best face-front shot per character → drop in `faces-reference/CharacterName.png`
- [ ] **Download PuLID models** — `python setup-pulid.py` (downloads `pulid_flux_v0.9.1.safetensors` + EVA CLIP)
- [ ] **Run PuLID face-locked generation** — `python queue-pulid-faces.py` after reference images placed
- [ ] **Run hempcrete LoRA batch** — `python queue-hempcrete-lora.py` (never ran, 0 images generated)
- [ ] **3D printer LoRA** — get Pexels + Pixabay API keys, run `collect-3dprinter-images.py`, curate, caption, train
- [ ] **Regenerate char-gallery.html** — should reflect new `chars-NAME-*` filenames once images are reviewed
- [ ] **Run 3 pending SQL migrations** — PROFILE_MIGRATION → SCHEMA_V3 → SCHEMA_V4 in Supabase SQL Editor
- [ ] **Git commit + push** — sessions 13-15 changes not yet pushed
- [ ] **Manual folder cleanup** — delete `reference/`, `org-test1/`, `imported images/`, old PNGs (see session 14 notes)

---

## What Was Done in Session 14 (2026-02-20)

*Folder reorganization, Flux images, git workflow walkthrough.*

### Folder reorganization — executed MIGRATION_MAP.md from org-test1
- SQL files (SEED_POSTS, SCHEMA_V2/V3/V4, PROFILE_MIGRATION, SUPABASE_SETUP.md) → `db/`
- Brand assets (PNGs, PDFs, style HTML) → `branding/`
- Governance docs (constitution, framework, UX spec) → `governance/`
- Archive (old mockups, early designs, v8/v9/v10 reference) → `reference/` (renamed from reference/)
- Created `db/README.md` — migration order & status table
- Created `QUICKSTART.md` — replaces Earthback_Setup_Reference.docx/.html as the go-to orientation file
- Updated `.gitignore` — excludes reference/, branding/, governance/, imported images/, org-test1/
- Updated path references in TRACKER.md and SESSION_NOTES.md

### Flux AI images added to site
- 8 AI-generated images from `imported images/` → `site/assets/img/posts/*.jpg`
- Converted from PNG (18MB total) → optimized JPG (~300KB total)
- SCHEMA_V4 updated to use `/assets/img/posts/*.jpg` paths instead of picsum placeholders
- Images: hempcrete-mix, utah-hemp-wall, greywater-system, solar-coop, food-forest, tiny-cabin, salvage-fir, lora-mesh

### Manual cleanup needed (Cowork sandbox can't delete)
- [ ] Delete `reference/` folder (contents copied to reference/)
- [ ] Delete `org-test1/` folder (was the test skeleton + MIGRATION_MAP.md)
- [ ] Delete `imported images/` folder (JPGs already in site/assets/img/posts/)
- [ ] Delete `Earthback_Setup_Reference.docx` and `.html` (replaced by QUICKSTART.md)
- [ ] Delete original PNGs from `site/assets/img/posts/` (the .png versions — keep the .jpg versions)

### Git workflow walkthrough
- Covered: status, diff, add, commit, push, pull, log
- Explained: working directory → staging area → local repo → remote (GitHub) → Netlify auto-deploy
- See QUICKSTART.md for the command reference

### SQL migrations — all still pending
- PROFILE_MIGRATION.sql — not yet run
- SCHEMA_V3_messages.sql — not yet run (conversations + messages tables)
- SCHEMA_V4_post_images.sql — not yet run (image_url column + demo image paths)
- All files now in `db/` folder with run order documented in `db/README.md`

### Immediate next
- [ ] Manual cleanup of old folders (see list above)
- [ ] Run the 3 pending SQL migrations in Supabase SQL Editor
- [ ] Git commit + push all session 13-14 changes
- [ ] Test compose post form end-to-end
- [ ] Continue building: media import pipeline, settings page

---

## What Was Done in Sessions 11-13 (2026-02-20)

*Sessions 11-12 built the core app features. Session 13 (this one) continued with compose form, images, and documentation.*

### Navigation overhaul — green topbar on all app pages
- Added consistent topbar nav across all 7 app pages (feed, profile, projects, project, create-project, messages, circles)
- Nav links: Home, Projects, Media, Marketplace (grayed/coming soon), Circles
- Messages icon (💬) added to topbar-right before avatar on all pages
- Mobile hamburger menu with all links including Messages on all pages
- "Join Earthback" changed to "Join / Sign In" across 10+ files

### "explore.html" → "circles.html" migration
- All links across 6+ files updated from explore.html to circles.html via sed
- explore.html kept as legacy (still accessible but not linked in nav)

### Pre-launch banner — all 7 app pages
- Fixed-bottom green gradient bar: "🌿 Pre-Launch Preview — You're seeing an early build..."
- Includes feedback mailto link to earthbackproject@gmail.com

### create-project.html — NEW (5-step wizard, ~1025 lines)
- Step 1: Name + Type selector (project/company/org/campaign) with visual grid
- Step 2: Location with Nominatim geocoding (forward + reverse + GPS)
- Step 3: Tagline (140 char) + Description (2000 char) + Category multi-select pills + Cover color picker
- Step 4: Up to 8 need rows with type selector (Skill/Resource/People/Place/Funding), urgency toggle
- Step 5: Live preview card + "next steps" list
- Inserts into `projects` table then `project_needs`, handles slug uniqueness, redirects to project.html
- Auth-gated: redirects to join.html if not logged in
- **Workaround:** `project_needs` table has no `type` column, so type emojis are prefixed onto the description string
- "Start a Project" buttons on projects.html wired to this page

### messages.html — NEW (~668 lines)
- Split-pane messaging inbox: thread list (320px) + chat panel
- 4 demo conversation threads with realistic multi-message dialogues
- Real Supabase integration: `loadConversations()`, `openConversation()`, `sendMessage()`
- URL params: `?conv=` for deep-link, `?new=1&project_id=&need_id=&need_desc=&owner_id=` for "I can help" flow
- Mobile-responsive: stacked layout with back button (768px breakpoint)
- **Requires SCHEMA_V3_messages.sql** to be run for real data

### SCHEMA_V3_messages.sql — NEW (~120 lines)
- `conversations` table: id, project_id, need_id, subject, conv_type (direct/project_help/project_team/system)
- `conversation_participants` table: conversation_id, profile_id, joined_at, last_read_at, is_muted
- `messages` table: conversation_id, sender_id, body, message_type (text/system/offer/media)
- RLS: Users can only see conversations they participate in
- Trigger: auto-updates `last_message_at` on new message insert
- **STATUS: NOT YET RUN** — needs to be executed in Supabase SQL Editor

### circles.html — NEW (~455 lines)
- 5 geographic circles: Southwest US, Pacific Northwest, Appalachia, Front Range, Great Lakes
- 8 thematic circles: Natural Building, Solar, Hemp, Permaculture, Water, Tiny Homes, Education, Indigenous Practices
- Filter tabs: All / Geographic / Thematic / Your Circles
- Join/view buttons with visual state toggle
- Color typos fixed: `'#6aa a5a'` → `'#6aaa5a'`, `'#a a7a4a'` → `'#aa7a4a'`

### "I can help" buttons wired on project.html
- Changed `onclick="window.location.href='join.html'"` to `onclick="offerHelp(this)"`
- `offerHelp()` checks auth and redirects to `messages.html?new=1&need_desc=...`

### project.html — major enhancement (company/business variant)
- `loadProject()` now detects `project_type === 'company'` and renders differently:
  - Square avatar (12px radius) for companies vs round for projects
  - "Services & Needs" board label vs "The Puzzle"
  - Hidden phase bar for companies/orgs
  - Dynamic stats: Services/Team/Followers for companies
- Loads real `project_needs(*)` and `project_members(*, profiles(...))` via Supabase joins
- Dynamic team members panel, links panel, cover band color
- Added `lightenHex()` helper function

### Compose post form — feed.html (Session 13)
- Compose card sits between welcome banner and "Community Activity"
- Collapsed state: avatar + "Share an update, resource, or question…" prompt
- Expanded state: title input, body textarea, post type selector (Resource/Milestone/Need/Question/Coordination), circle selector (all 12 circles), image upload (file picker or paste URL), Post/Cancel buttons
- Submits to Supabase `posts` table via `sb.from('posts').insert()`
- New post appears at top of feed immediately (local array + re-render)
- "post an update" text at bottom of feed now opens the composer
- Image upload attempts Supabase Storage (`public-assets` bucket), falls back to URL-only

### Post images — feed.html (Session 13)
- Added `image_url` field to `mapPostRow()` and `buildPostHTML()`
- Posts with `image_url` show a full-width image between body text and footer
- Lazy loading + onerror fallback (hides broken images)
- `.post-image` CSS class: 100% width, max-height 400px, object-fit cover, rounded corners

### SCHEMA_V4_post_images.sql — NEW (Session 13)
- Adds `image_url` TEXT column to posts table
- Adds `is_demo` BOOLEAN column to posts table
- Marks all existing seed posts as demo
- Updates 8 of 14 demo posts with picsum.photos placeholder images
- **Each UPDATE has an AI image generation prompt as a comment** — Nicco generating real images from these
- **STATUS: NOT YET RUN** — needs to be executed in Supabase SQL Editor

### Earthback_Setup_Reference.docx — NEW (Session 13)
- 9-page reference document covering all services, credentials, schema, file structure, session setup
- Generated with docx-js, validated, Earthback brand colors

### Earthback_Setup_Reference.html — NEW (Session 13)
- Local HTML version with clickable links to all dashboards and services
- **Reboot Startup Sequence** — numbered 1-6 steps in click order: GitHub → Netlify → Supabase → Live site → Sign in → Start Claude
- **Supabase Quick Access** — deep links to Table Editor, SQL Editor, Auth Users, Storage, URL Config, API Keys
- **Site Pages** — all app and public pages as clickable cards
- Full reference: credentials, schema, migrations, APIs, brand tokens, key concepts

### earthback-start.sh — NEW (Session 13)
- Startup script: opens 5 browser tabs in sequence, checks git, pings site, prints Claude handoff prompt
- Works on macOS, Linux, WSL
- Same 1-2-3-4-5 sequence as the HTML reference page

### Git setup (Session 13, separate chat)
- Nicco set up git in a separate session for incremental Netlify deploys
- Repo: https://github.com/earthbackproject/earthback.git
- Config: `Nicco <nicco.macintyre@gmail.com>`, branch `main`

### Consistency pass — all 7 checks passed, 0 issues
1. No explore.html links remaining (all → circles.html)
2. Matching Supabase credentials across all files
3. Pre-launch banners on all 7 app pages
4. handleSignOut() functions present
5. Messages links in all mobile menus
6. No duplicate Messages links
7. HTML tag balance verified

### Immediate next
- [ ] **Run SCHEMA_V3_messages.sql** — messaging tables (conversations, messages, participants)
- [ ] **Run SCHEMA_V4_post_images.sql** — image_url column + demo post placeholder images
- [ ] **Replace placeholder images** — Nicco generating AI images from the prompts in V4 SQL; UPDATE the image_url values with real URLs
- [ ] **Deploy via git push** — push to main, Netlify auto-deploys
- [ ] **Test compose post form** — sign in and create a real post
- [ ] **Test create-project flow** — create a project end-to-end
- [ ] **Media import pipeline** — still pending from session 10
- [ ] **Settings page** — still pending from session 10

### Real-world project updates (from Nicco)
- Earthback has received a donated semi-truck load of solar panels
- Helped outfit a mobile homeless shelter/bus with solar panels
- The platform is catching up to real-world work already happening
- Nicco has 6 monitors, ~1000 tabs open — reducing to only what's needed for building
- Payment/hosting situation being resolved with federal bank fraud score issue

---

## Account References

| Service | Account / Org | URL / Identifier |
|---|---|---|
| **GitHub** | earthbackproject | https://github.com/earthbackproject |
| **GitHub Repo** | earthbackproject/earthback | https://github.com/earthbackproject/earthback |
| **Supabase** | the_earthback_project | https://supabase.com/dashboard/project/yptktmzagctusbeqdaty |
| **Netlify** | TBD — connecting next | — |
| **Domain** | earthbackproject.org | Currently live via Netlify (to be connected to GitHub repo) |
| **Git local config** | Nicco / nicco.macintyre@gmail.com | Set in repo .git/config |

---

## What Earthback Is

A community platform for people doing green building and construction — hempcrete, off-grid solar, food systems, mutual aid, community housing. No algorithm, no data harvesting, no feed manipulation. Revenue comes from connecting members with aligned suppliers and materials partners — not from selling attention. People hang out, share techniques, form projects, coordinate work.

**The goal right now:** Get the pre-launch marketing/community site finished and live. The app platform (auth, projects, feeds) comes after.

---

## Entity Structure (Important — still being finalized)

| Entity | Role |
|---|---|
| **Earthback Project** | For-profit corp · holds all IP · the commercial vehicle |
| **Earthback [TBD]** | 501(c)(3) incoming · the nonprofit community org · this site lives here |
| **Earthback Alliance** | Was the name for the people/community layer · Nicco souring on it |

**Open naming question:** What to call the community/nonprofit side. "Alliance" feels too political. "Foundation" feels institutional. "Project" is taken by the corp. Leading candidate: just use **Earthback** publicly; entity names stay in legal/org docs only. Nicco is still researching other "Earthbacks" in the green building space — trademark clarity needed before finalizing.

**Phonetics note:** Nicco flagged that Earthback sounds like Facebook (same two-syllable cadence, "-back"/"-book" ending). General read: not a problem — the word "earth" anchors it strongly enough. Could even be intentional positioning.

---

## Site: Current State

**Location:** `/Earthback/site/`

| File | Status | Notes |
|---|---|---|
| `index.html` | ✅ Updated today | Main landing page — see changes below |
| `about.html` | ✅ Updated today | |
| `how-it-works.html` | ✅ Updated today | |
| `safety.html` | ✅ Updated today | |
| `use-cases.html` | ✅ Updated today | |
| `join.html` | ✅ Pre-existing, good shape | Multi-step signup UI — currently a demo (no backend) |

**Assets folder** (`site/assets/css`, `site/assets/js`, `site/assets/img`) — folders exist but are **empty**. All styles/scripts are currently inlined in each HTML file.

---

## What Was Done in Session 3 (2026-02-19)

### Brand treatment — "the Earthback Project" typography
- All 8 site pages updated with new typographic brand mark
- **Nav logos & footer logos:** `EARTHBACK` now reads `ᵗʰᵉ EARTHBACK PROJECT` — small faint "the" prefix, dominant "EARTHBACK" in full clay/parchment treatment, whisper-weight "PROJECT" suffix
- Implementation: three CSS classes (`.brand-the`, `.brand-back`, `.brand-project`) injected in every page's `<style>` block
- join.html uses a parallel treatment (`.topbar-the` + `.brand-sub`) matching the topbar's existing design language
- "Earthback Alliance" copy in join.html updated to "the Earthback Project"

### Domain decision
- earthback.org and earthback.com both taken; earthback.com showing imminent competing launch
- Registered domains in hand: earthbackproject / earthbackfoundation / earthbackalliance in .com/.net/.org
- **Decision:** Launch on `earthbackproject.org` — strongest of what's owned
- `earthback.build` ($75/yr) and `earthback.earth` ($24/yr) both available but deferred — budget saved for subscription continuity
- Revisit domain vanity purchase in 60 days once community is active

### Session 2 recap (completed prior session)
- join.html wired to Netlify Forms (hidden form + background AJAX submit, never blocks UX)
- Mobile hamburger nav added to all 7 site pages
- terms.html and privacy.html created (full ToS and Privacy Policy)
- Legal footer links (Terms · Privacy) added to all pages

## What Was Done in This Session (2026-02-19)

### index.html — major changes
- **Nav:** Added Use Cases and Safety links; Join button now goes directly to `join.html` (not a hash anchor)
- **Hero:** Copy warmed up — feels more like a community invitation than a startup pitch
- **Feed section:** All 4 posts now have interaction buttons (👍 helpful with live counts, ✋ I can help, 💬 Reply, 🔖 Save). Non-like buttons nudge visitor to `join.html`
- **How It Works:** Reframed from project-workflow-only (Form→Commit→Work→Archive) to community arc (Find Circles→Share What You Know→Start a Project→Archive & Keep Going)
- **Why Earthback:** Copy rewritten — now specifically names Facebook, Twitter, Reddit as what people are escaping from. Feels more human and direct.
- **Bottom CTA:** Fake email waitlist form **removed entirely**. Replaced with direct "Create your account →" button to `join.html`
- **Footer:** Cleaned up — removed dead "Pilot Program" and "Press" links

### All inner pages (about, how-it-works, safety, use-cases)
- **Nav "Join waitlist" → "Join Earthback" → `join.html`** on every page
- **CTA sections:** Email forms replaced with direct join buttons everywhere
- **All "Earthback is in pilot" / "join the waitlist" copy** updated to open-door language

---

## What's Still Not Done / Open Items
*Full detail in TRACKER.md — these are just the immediate next things.*

## What Was Done in Session 8 (2026-02-20)

### Supabase database migration — complete
- **All 7 tables verified live** in Supabase: profiles, posts, projects, project_members, project_needs, certifications, media_links
- **Migration order:** SEED_POSTS.sql first (creates `posts` table + RLS), then SCHEMA_V2.sql (creates remaining 5 tables + extends posts)
- **14 seed posts inserted** — all flagged with `is_demo = true` for easy cleanup; covers every circle (Natural Building, Solar, Water, Permaculture, Mutual Aid, Tiny Dwellings, Regen Ag, Salvage, Co-op Housing, Community Tech, Skills/Workshops)
- **Chrome automation notes:** Supabase SQL Editor uses Monaco (code editor) — standard browser clicks don't work on the editor. Used `window.monaco.editor.getModels()[0].setValue()` to paste SQL and dispatched click events on Run button. Verification used the virtualized result grid (scrolling required to see all 7 table rows).

### Live feed wired in join.html
- **Hardcoded POSTS array removed** — replaced with `loadFeed()` that queries `supabase.from('posts').select('*')` on dashboard load
- **Circle style lookup** — `CIRCLE_STYLES` object maps every `circle_slug` to icon, text color, and background color for the feed cards
- **Post type style lookup** — `TYPE_STYLES` maps `post_type` (resource, milestone, need, question, coordination, media) to labels and colors
- **`mapPostRow()`** — converts a Supabase row into the format `buildPostHTML()` expects (handles UUID IDs, relative time from timestamps, deterministic author colors)
- **Dynamic sidebar streams** — `buildStreamSidebar()` builds the circle filter sidebar from actual post data (counts per circle, sorted by frequency)
- **Helpful button persists** — `markHelpful()` now writes `helpful_count` back to Supabase (fire-and-forget)
- **Empty state** — shows "No posts yet in this stream" if filter yields zero results
- **Old array preserved** — commented out as `POSTS_FALLBACK` for emergency rollback
- **index.html left static** — landing page uses a different HTML structure for marketing; not worth the latency hit to wire to Supabase

### Immediate next
- [ ] **Redeploy to Netlify** — deploy session 8 changes (live feed)
- [ ] **Profile editing UI** — let users update bio, tagline, skills from their profile page
- [ ] **Project creation flow** — form to create project/company page

---

## What Was Done in Session 7 (2026-02-20)

### Sign Out button — fully wired
- **Dashboard topbar** (join.html screen 3): "Sign Out" button added next to user avatar; calls `sb.auth.signOut()` → redirects to index.html
- **Welcome-back banner** (join.html screen 1): "Sign Out" button added alongside "Go to your dashboard" link
- **All 6 nav pages** (index, about, how-it-works, safety, use-cases, explore): Supabase session check added before `</body>`; if signed in, "Sign In" link swaps to "Sign Out" with click handler
- **profile.html**: `addSignedInNav()` updated to insert "Sign Out" link next to user avatar in nav
- **login.html**: already-signed-in redirect updated to use `/community` URL

### Community URL rewrite — join.html no longer shows in address bar
- `history.replaceState()` fires when dashboard screen loads → URL changes to `/community`
- Netlify `_redirects` file created: `/community → /join.html` (200 rewrite, not redirect)
- Auth callback still uses `join.html?signed-in=1` (the `?signed-in=1` param triggers dashboard load, then `replaceState` cleans URL to `/community`)
- login.html redirect for already-signed-in users now sends to `/community`

### Projects, Companies & Organizations — full entity pages
- **SCHEMA_V2.sql** — new Supabase migration with 5 tables:
  - `projects` — owner_id, slug, type (project/company/org/campaign), status, location, media links, JSONB other_links, demo flag
  - `project_members` — many-to-many profile↔project with roles (member/admin/contributor/advisor)
  - `project_needs` — structured needs with urgency flags
  - `certifications` — profile certs with issuing org, credential URL, verified flag, expiry date
  - `media_links` — external content (YouTube, articles, podcasts) with platform detection, auto-post flag, thumbnail
- **`posts` table extended** — added 'media' to post_type CHECK, added project_id FK, media_url, media_thumbnail, is_demo columns
- **project.html** — NEW full page template for "Desert Sun Hemp Homes" demo:
  - Square avatar (8px radius) to differentiate from person profiles (circle)
  - Project type badge (Company/Org/Campaign), status badge, "Founded by" owner link
  - Sidebar: team members, current needs (with urgency), media & training links, circles, contact
  - Tabbed content: Updates (activity feed), Builds (sub-project cards), Media (video grid)
  - Supabase wired: loads real data from `?slug=` param, keeps demo if no slug
- **profile.html updated** with 3 new sidebar panels:
  - Certifications & Credentials — 3 demo certs (hempcrete installer, natural building practitioner, PDC)
  - Projects & Companies — 3 linked project cards (Desert Sun Hemp Homes, Taos ADU, NM Builders Network) with role badges
  - New "Media" tab — 4-card video grid + link import box with paste UI
- **explore.html updated** — "Projects & Companies" section added between People and CTA:
  - 3 demo project cards (Desert Sun Hemp Homes, Taos Natural Builders, Green Mountain Land Trust)
  - "Create a project" CTA card

### Immediate next
- [ ] **Redeploy to Netlify** — session 7 changes (everything above)
- [ ] **Trademark research** — Nicco working on this
- [ ] **Real feed** — run SEED_POSTS.sql, replace POSTS array with Supabase query

---

## What Was Done in Session 6 (2026-02-20)

### Filler content — site feels alive now
- **Demo feed expanded** — POSTS array in join.html went from 6 to 14 posts spanning every circle: Natural Building, Solar & Off-Grid, Water Systems, Permaculture & Food, Mutual Aid, Tiny Dwellings, Land & Regen Ag, Materials & Salvage, Cooperative Housing, Community Tech, Skills & Workshops, plus the Earthback Project curated stream
- **People section expanded** — explore.html Featured Members went from 3 cards to 7: added Rosa Delgado-Kwan (solar co-ops, Tucson), Yuki Tanaka (tiny cabins, Asheville), Saoirse Ó Briain (food forest, Ireland), Amara Diallo (land trusts, Vermont)
- **SEED_POSTS.sql created** — full Supabase `posts` table schema with RLS + all 14 posts seeded; ready to run when wiring the real feed (Phase 2)

### Demo content flagging system
- **`SHOW_DEMO_POSTS = true`** toggle at top of join.html JS — set to `false` and all sample feed posts vanish instantly
- **`SHOW_DEMO_MEMBERS = true`** toggle in explore.html JS — set to `false` and all sample member cards vanish
- **`demo: true`** property on every seed post in the POSTS array; `renderFeed()` filters them out when toggle is off
- **"Sample" badges** — subtle muted "SAMPLE" tag on every demo post (upper-right) and demo member card (next to name); CSS class `.demo-badge` / `.demo-badge-sm`
- **`class="demo-member"`** on all demo member cards in explore.html for easy JS show/hide

### Language softening (pre-launch honesty)
- index.html: "Real conversations, real projects, real people" → "Conversations that matter, projects that last, people who show up"
- join.html dashboard: "real projects, real needs, real people" → "projects, needs, and conversations from the community"
- use-cases.html: "real things built by real people" → "the kind of work that happens when people coordinate"
- safety.html: "real commitments and real people" → "genuine commitments and the people who make them"

### Tracking docs updated
- TRACKER.md — session 6 logged, build order updated, duplicate entries fixed
- SESSION_NOTES.md — this entry
- tracker/index.html — full overhaul to reflect sessions 4-6 progress

### Immediate next
- [ ] **Redeploy to Netlify** — all session 4-6 changes need to go live
- [ ] **Favicon + og:image** — step 8b in build order
- [ ] **Sign Out button** — noted as missing by Nicco

---

## What Was Done in Session 5 (2026-02-20)

### Real backend shipped — Supabase magic link auth fully wired

**Supabase project:** `yptktmzagctusbeqdaty` · URL: `https://yptktmzagctusbeqdaty.supabase.co`
**Key type used:** `sb_publishable_` (new Supabase format — client-side safe, not the secret key)

**`profiles` table created in Supabase** with RLS:
- Fields: id, first_name, last_name, display_name, tagline, bio, location, member_type, what_bring, what_seek, skills (jsonb), earth_score, is_public, created_at, updated_at
- Policies: public read on is_public=true · users can upsert their own row only

**New files:**
- `site/auth-callback.html` — handles magic link redirect; reads pending profile from localStorage; upserts to Supabase `profiles`; redirects to `join.html?signed-in=1`
- `site/login.html` — returning user sign-in page; single email field; calls `supabase.auth.signInWithOtp()`; shows "check your email" confirmation state
- `SUPABASE_SETUP.md` — reference doc with the SQL schema + dashboard config steps (Nicco ran these ✓)

**Modified files:**
- `site/join.html` — Supabase client added; `goToProfiler()` now also sends magic link + saves form data to localStorage; `goToDashboard()` accepts optional `profileOverride` for real-data path; `initAuth()` runs on page load checking for `?signed-in=1` or existing session; welcome-back banner added; magic-link-sent notice added under email field
- `site/profile.html` — `loadProfile()` added: reads `?id=UUID` from URL and fetches from Supabase; falls back to Maya Redhawk demo if no ID; shows "Edit Profile" button if viewing own profile; `addSignedInNav()` swaps Join CTA for user avatar when logged in
- All 8 nav pages — "Sign In" link added pointing to `login.html`

**Auth flow end-to-end (now real):**
1. User fills join.html Step 1 → Netlify Forms capture + Supabase magic link email sent
2. Form data saved to `localStorage` as `earthback_pending_profile`
3. User sees "✉️ We sent a sign-in link" notice; continues to demo profiler + dashboard
4. User clicks magic link in email → `auth-callback.html`
5. Supabase session established → profile upserted to DB → localStorage cleared
6. Redirected to `join.html?signed-in=1` → dashboard loads with real name from DB
7. Returning visits: session detected → welcome-back banner → "Go to your dashboard"
8. Sign In nav link → `login.html` → email → new magic link → same callback flow
9. Profile URL: `profile.html?id={supabase_user_id}`

### Immediate next (do now)
- [ ] **Redeploy to Netlify** — drop `/site/` folder again to pick up all session 4+5 changes
- [ ] **Test full flow** — sign up → get email → click link → confirm dashboard loads with real name
- [ ] **Favicon** — browsers show blank tab icon; quick win
- [ ] **og:image** — social sharing preview card (1200×630)

---

## What Was Done in Session 4 (2026-02-19)

### Magic link note on join.html
- Added explanatory note under the email field: "🔑 No password needed. When you're ready to sign in, we'll email you a magic link — just click it and you're in."
- No-password design is intentional (magic links per platform spec). Users were confused seeing no password field.

### profile.html — new member profile page
- Full demo profile page at `site/profile.html`
- Shows: cover band, avatar, name, location, tagline, bio, verified badge, member type badge, stats row (projects/posts/circles/helpful/earth score)
- Sidebar: skills (teach/experienced/learning), circles with role, Earth Score bar, connect section
- Main content: tabbed (Activity / Projects / Resources)
  - Activity tab: 3 sample posts (technique share, question, resource)
  - Projects tab: 3 projects (in-progress, forming, complete) with needs + collaborators
  - Resources tab: 2 shared resources with download prompt → join.html
- All action buttons gate to join.html ("Invite to Collaborate", "Follow", "Offer Help", downloads)

### Profile links wired throughout site
- **join.html feed**: author names are now clickable links → profile.html
- **join.html dashboard**: header avatar (initials circle) now links → profile.html
- **explore.html**: "People" nav link added; "Featured Members" section added before CTA showing 3 member cards + "your profile could be here" card, all linking to profile.html

### Immediate next (do now)
- [ ] **Favicon** — not created. Browsers show blank tab icon. Quick win.
- [ ] **og:image / social preview card** — when someone shares the URL, there's no preview image. Needs a 1200×630 image in site/assets/.
- [ ] **Push to Netlify** — redeploy with session 4 changes (profile.html + explore.html + join.html updates)

### High priority
- [ ] **join.html is a demo** — the multi-step signup flow (Create account → Build profile → See community) is hardcoded UI with no backend. No account is actually created. Needs: auth system (magic link per the spec), real profile creation, real feed.
- [ ] **Netlify Forms only captures on deploy** — the hidden form in join.html will work once the site is deployed to Netlify. Test after first deploy.
- [ ] **Nav on index.html** — currently 6 links + Join button. May be too many on mobile (nav collapses at 860px via hamburger, so it's handled — but worth a look).

### Medium priority
- [ ] **"Press" page** — currently "Press" in the footer/nav just goes to `about.html`. If press inquiries are real, needs its own section or at minimum a mailto.
- [ ] **Session notes system** — this file! Update it going forward.
- [ ] **Finish trademark research** — what other "Earthbacks" exist in green building space? Drives the naming decision.
- [ ] **Decide on the 501(c)(3) name** — once trademark research is done.

### Lower priority / later
- [ ] Site assets folder — styles could be extracted to a shared CSS file to make cross-page updates easier
- [ ] Mobile nav — hamburger menu for the full nav on small screens
- [ ] The v10 platform build (auth, projects, feed, Supabase, n8n) — separate work stream from the marketing site

---

## Key Decisions Made

| Decision | Outcome | Reasoning |
|---|---|---|
| Eliminate waitlist | Done | Moving to real functionality, not a holding page |
| Join button destination | `join.html` directly | The multi-step flow already exists |
| Feed interactions | Demo buttons on landing page | Makes it feel alive; non-like actions redirect to join |
| How It Works framing | Community-first, not project-first | Platform is "somewhere to hang out" not just a project tool |
| "Alliance" as community name | Dropped | Feels too political/formal; "the Earthback Project" is the public-facing brand |
| Brand typography | "the EARTHBACK PROJECT" treatment | Small "the" prefix + faint "PROJECT" suffix; Earthback dominant |
| Primary domain | `earthbackproject.org` | earthback.org/.com taken; best of the registered set |
| Vanity domains | Deferred | earthback.earth ($24) and earthback.build ($75) available but not urgent |

---

## Tech Stack (per v10 platform spec)

- **Identity/Data:** AT Protocol (Earthback-hosted PDS initially)
- **App:** Next.js
- **DB:** Supabase Postgres
- **Automation:** n8n
- **Email:** Postmark or Resend
- **AI:** OpenAI API (structured JSON outputs only)
- **Frontend (current site):** Plain HTML/CSS/JS, Google Fonts (Cormorant Garamond + Inter)

---

## Reference Files Worth Reading

- `/Earthback/reference/v10-pre-launch-db etc/docs/earthback_platform_spec_v1.md` — full technical spec
- `/Earthback/reference/v10-pre-launch-db etc/docs/decision log_v1/06_launch/v1_scope_freeze.md` — what's in/out of v1
- `/Earthback/reference/v10-pre-launch-db etc/docs/decision log_v1/06_launch/launch_checklist.md` — all unchecked
- `/Earthback/Earthback Core Constitution.pdf` — governance and mission document

---

## What Was Done in Session 10 (2026-02-20)

### Google OAuth sign-in — fully wired
- **"Continue with Google" button** added to both `join.html` and `login.html` — styled `.btn-google` with Google logo SVG
- **`signInWithGoogle()` / `signUpWithGoogle()`** — calls `sb.auth.signInWithOAuth({ provider: 'google' })` with redirect to auth-callback.html
- **auth-callback.html updated** — `saveProfile()` now pulls `given_name`, `family_name`, `full_name`, `avatar_url`/`picture` from Google OAuth user metadata
- **Google Cloud Console setup** — walked Nicco through OAuth consent screen, credential creation, redirect URI configuration
- **Tested and working** — "HELL YES! that worked perfectly!"

### Profile editing — fully functional
- **Inline edit mode** — clicking "Edit Profile" on own profile converts name, tagline, bio, location to input fields
- **Skills editing** — 3 comma-separated input fields for lead/experienced/learning skill levels; parsed into JSONB array `[{name, level}]`
- **Save function fixed** — original used broken `nth-of-type` CSS selectors; rewrote to use proper element IDs (`edit-name`, `edit-tagline`, `edit-bio`, `edit-location`, `edit-skills-lead`, `edit-skills-exp`, `edit-skills-learn`)
- **Save button shows "Saving…"** loading state, then reloads page with fresh data

### Avatar upload — working
- **Click avatar in edit mode** → file picker opens (JPG, PNG, GIF, WebP; max 5 MB)
- **Uploads to Supabase Storage** `avatars` bucket at `{userId}/avatar.{ext}` with upsert
- **Cache-busting** — appends `?t=timestamp` to public URL so browser shows new image immediately
- **Camera overlay** — `::after` pseudo-element shows 📷 icon on avatar hover in edit mode; turns green on hover
- **Avatar displays everywhere** — profile page, feed sidebar, feed header; falls back to colored initials

### Feed sidebar linked to profile
- Sidebar profile card changed from `<div>` to `<a>` linking to `profile.html?id=USER_ID`
- Header avatar also links to profile page

### Profile page UI polish
- **Cover band shrunk** from 120px to 56px — was a big blank green block, now a slim accent strip
- **Avatar z-index fixed** — sits on top of the band instead of behind it
- **Avatar enlarged** to 128px (from 80px) with deeper overlap into band

### Magic link security discussion
- Explained PKCE flow, single-use tokens, 1-hour expiry, rate limiting
- Discussed TOTP MFA (authenticator apps, not SMS) — Supabase supports via `sb.auth.mfa.enroll()`
- Account recovery approach: human-handled initially, then build self-service
- Industry comparison: Slack, Notion, Discord patterns

### Tracking
- Added social media setup task to TRACKER.md
- Added MFA task to TRACKER.md

### What's Next (session 11)
- [ ] **Settings page** — Nicco wants header avatar to link to settings, sidebar avatar to profile. Settings page doesn't exist yet.
- [ ] **Media import pipeline** — URL paste → oEmbed/OG scrape → auto-populate title + thumbnail → create post
- [ ] **Project creation flow** — form to create project/company page
- [ ] **Social media accounts** — set up official Earthback accounts
- [ ] **MFA (TOTP)** — implement authenticator app enrollment
- [ ] **Mobile check** — avatar size (128px) may need media query for small screens

---

## What Was Done in Session 9 (2026-02-20, continued)

**Split join.html into join.html + feed.html** — the big architectural cleanup.

### Problem
join.html was doing triple duty: signup form (screen 1), profile builder (screen 2), and the full community dashboard/feed (screen 3). This meant signed-in users clicking any nav link and coming back would land on the signup form with a "you're already signed in" banner — broken UX.

### What changed

1. **Created `feed.html`** — standalone dashboard page with all the app logic:
   - Dashboard HTML (topbar, sidebar with profile card + streams + invite, main feed with filter controls)
   - Dashboard CSS only (no signup/profiler CSS)
   - All feed JS: `CIRCLE_STYLES`, `TYPE_STYLES`, `loadFeed()`, `renderFeed()`, `buildStreamSidebar()`, `buildPostHTML()`, `markHelpful()`, `setFilter()`, `filterStream()`, `handleSignOut()`
   - New `initAuth()` that checks session → if not signed in, redirect to `join.html`; if signed in, load profile from sessionStorage (fresh from onboarding) or Supabase (returning user), populate sidebar, load feed
   - Served at `/community` via Netlify rewrite

2. **Trimmed `join.html`** — now onboarding only (screens 1 + 2):
   - Removed `#screen-dashboard` div (~90 lines HTML)
   - Removed all dashboard CSS (~140 lines)
   - Removed all feed-related JS: `SHOW_DEMO_POSTS`, `CIRCLE_STYLES`, `TYPE_STYLES`, `AUTHOR_COLORS`, `authorColor()`, `relativeTime()`, `mapPostRow()`, `POSTS`, `loadFeed()`, `POSTS_FALLBACK`, `currentFilter`, `currentStream`, `renderFeed()`, `buildStreamSidebar()`, `buildPostHTML()`, `markHelpful()`, `setFilter()`, `filterStream()`
   - Removed `#welcome-back-banner` — no longer needed since signed-in users redirect immediately
   - Simplified `goToDashboard()` — now saves profile to `sessionStorage` and redirects to `/community`
   - Simplified `initAuth()` — now redirects signed-in users to `/community` immediately

3. **Updated `auth-callback.html`** — all 3 redirect URLs changed from `join.html?signed-in=1` to `/community`

4. **Updated `_redirects`** — `/community` now serves `feed.html` instead of `join.html`

### Profile handoff mechanism
When a user finishes the profiler in join.html and clicks "Drop My Pin," the in-memory `user` object is saved to `sessionStorage` as `earthback_fresh_profile`. feed.html checks for this on load to avoid an extra DB round-trip for fresh signups. Returning users load their profile from Supabase directly.

### Files unchanged
- `login.html` — already redirects to `'community'`, which now correctly serves feed.html
- All marketing pages — "Join" buttons still point to join.html (correct for new users)
- All nav auth-swap scripts — unchanged
- `index.html` — feed preview stays static (marketing content)

### What's Next (session 10)
- Deploy to Netlify and test the full auth flow live
- Profile editing UI — let users update bio, tagline, skills from their profile page
- Project creation flow — form to create a project/company page
- Media import pipeline
- Verification + rate limiting

---

## How to Resume

1. Open Cowork and select the Earthback folder
2. Say: **"Read TRACKER.md and SESSION_NOTES.md and pick up where we left off"**
3. Optionally add what you want to focus on this session
4. Claude will orient in ~30 seconds and be ready

**Two-file system:**
- `TRACKER.md` — master project board, all workstreams, full checklist. The source of truth.
- `SESSION_NOTES.md` — this file. What happened last session, what's immediately next.

*Ask Claude to update both files before ending each session.*
