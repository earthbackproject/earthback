# Earthback — Auto-loaded Session Context

*This file is read automatically at the start of every Cowork session.*
*For full project state: read SESSION_NOTES.md and TRACKER.md*

---

## To Resume Work
**MANDATORY:** At the start of every session, read SESSION_NOTES.md and TRACKER.md before doing anything else. Do not skip this even if the user describes the task — the notes contain critical context, version history, and file locations that prevent costly mistakes (e.g. editing the wrong source file).

Say: **"Read SESSION_NOTES.md and TRACKER.md and pick up where we left off."**
Or just describe what you want to work on and Claude will orient from there.

---

## CRITICAL: File Versioning Rule

**NEVER overwrite generated document files.** When rebuilding any output file (docx, pptx, pdf, etc.), always increment the version number in the filename. For example: `_v2.docx` → `_v3.docx`. Old versions are kept so Nicco can compare or roll back. This applies to every generated file, every time, no exceptions.

---

## This Machine — Important Quirks

**OS:** Windows (Nicco's workstation)
**WSL:** Non-functional due to a BIOS virtualization flaw. Do not suggest WSL-based workflows.
**GPU:** 2x NVIDIA RTX 3060 (12 GB VRAM each)

### Python Environments

Three separate Python installs — they don't share packages:

| Environment | Python | Location | Purpose |
|---|---|---|---|
| System | 3.14 | `python` / `py` | Default — too new for most AI libs |
| comfy-env | 3.11 | `D:\AI\comfy-env\Scripts\python.exe` | ComfyUI (torch + CUDA 13.0) |
| kohya venv | 3.11 | `D:\AI\kohya_ss\venv\Scripts\python.exe` | Kohya SS LoRA training (torch + CUDA 12.4) |
| ai-toolkit | 3.11 | `D:\AI\ai-toolkit\venv\Scripts\python.exe` | Flux LoRA training (torch 2.4.1+cu121) |

**Why:** Each venv is an isolated Python install in a folder. Activating one (`.\venv\Scripts\activate`) makes `python` and `pip` point to that copy. Training .bat files call the venv python directly so activation isn't strictly required.

**Rule:** Always use the right Python for the right tool:
- ComfyUI pip installs: `D:\AI\comfy-env\Scripts\python.exe -m pip install ...`
- Kohya pip installs: `D:\AI\kohya_ss\venv\Scripts\python.exe -m pip install ...`
- ai-toolkit pip installs: `D:\AI\ai-toolkit\venv\Scripts\python.exe -m pip install ...`
- Queue scripts (just use `requests`): system Python is fine

### ComfyUI
Running at `http://127.0.0.1:8188` via `comfy-run.bat`
- Output: `C:\users\adrxi\Earthback\comfyui-output`
- Models: `D:\AI\ComfyUI\models\`

### Kohya SS (LoRA Training — SDXL)
Installed at `D:\AI\kohya_ss\` with own venv (Python 3.11, torch 2.6+cu124).
- Activate: `cd D:\AI\kohya_ss; .\venv\Scripts\activate`
- SDXL training: `sdxl_train_network.py` (works well on 12GB)
- Flux training via Kohya: **unviable on 12GB** (deadlocks, 286s/step) — use ai-toolkit instead

### ai-toolkit (LoRA Training — Flux)
Installed at `D:\AI\ai-toolkit\` with own venv (Python 3.11, torch 2.4.1+cu121).
- **Why this works on 12GB:** layer offloading moves transformer blocks to CPU/RAM (needs 64GB system RAM)
- Install: `powershell -ExecutionPolicy Bypass -File "local\scripts\install-ai-toolkit.ps1"`
- Train: `local\scripts\train-flux-lora.bat` (defaults to hempcrete config)
- Train custom: `local\scripts\train-flux-lora.bat configs\my-config.yaml`
- Generate config: `python local\scripts\make-flux-config.py --name X --trigger X_EB --dataset "path"`
- Configs live in: `local\scripts\configs\`
- CRITICAL: torch must be ≤2.5.1+cu121 (not newer — torch >2.7 has diffusers bug). Currently at 2.5.1.

---

## VM Crash Recovery

The CoworkVMService occasionally hangs. **If the VM crashes:** Nicco runs `maint-scripts\fix-cowork-vm.ps1` as Administrator in PowerShell, then reopens Claude. That script restarts the service.

---

## How ComfyUI / Flux Is Used

Scripts talk directly to ComfyUI via its REST API.

**Key endpoints:**
- `POST http://127.0.0.1:8188/api/prompt` — queue a generation job (JSON workflow body)
- `GET  http://127.0.0.1:8188/queue` — check pending/running queue
- `POST http://127.0.0.1:8188/upload/image` — upload a reference image (for PuLID)

**Flux workflow node IDs (do not change these — they match the saved workflow):**
| Node ID | Role |
|---------|------|
| 6  | CLIPTextEncode — positive prompt |
| 9  | SaveImage — output filename prefix |
| 27 | EmptySD3LatentImage — width / height / batch_size |
| 30 | CheckpointLoader — model file |
| 31 | KSampler — seed / steps / cfg / sampler / scheduler |
| 33 | CLIPTextEncode — negative prompt |
| 35 | FluxGuidance — guidance scale |

**PuLID workflow additional nodes (in `queue-pulid-faces.py`):**
| Node ID | Role |
|---------|------|
| 40 | LoadImage — reference face |
| 41 | PulidFluxModelLoader |
| 42 | ApplyPulidFlux — face injection (model patching) |
| 43 | PulidFluxInsightFaceLoader |
| 44 | PulidFluxEvaClipLoader — separate EVA CLIP loader |

**PuLID compatibility patch (applied session 39):**
`D:\AI\ComfyUI\custom_nodes\ComfyUI-PuLID-Flux\pulidflux.py` line 65 — added `transformer_options=None, **kwargs` to `forward_orig()` signature for ComfyUI 0.11.1 compatibility. **If PuLID is updated via Manager, this patch may be overwritten — re-apply if PuLID breaks with "forward_orig() got an unexpected keyword argument 'attn_mask'".**

**Dual GPU setup (CUDA ≠ Task Manager numbering):**
- CUDA device 0 = Task Manager GPU 1 — used for LoRA training
- CUDA device 1 = Task Manager GPU 0 — used for ComfyUI
- comfy-run.bat uses `CUDA_VISIBLE_DEVICES=1` (NOT `--cuda-device 1`) to ensure ALL libs (facexlib, insightface) use the correct GPU

**Seed strategy:**
- Each character has a fixed `seed` in `queue-batches.py` CHARS dict
- Face angle variants: `char_seed + angle_offset` (0=front, 1=left, 2=right, 3=down, 4=talk)
- Scenario batches: `char_seed + 1000 + (batch_idx * 50) + (loop * 100)`
- T5 scenes: `char_seed + 2000 + (i * 10) + (loop * 100)`

**Image output:** `C:\users\adrxi\Earthback\comfyui-output\`
**Model used:** Flux (flux1-dev or similar) loaded in node 30
**Python to run scripts:** System Python is fine for queue scripts (they just use `requests`)
**Python for pip installs into ComfyUI:** `D:\AI\comfy-env\Scripts\python.exe -m pip install ...`

---

## What Earthback Is

A community platform for people doing green building — hempcrete, solar, food systems, mutual aid, community housing. No algorithm, no data harvesting, no feed manipulation. Revenue comes from connecting members with aligned suppliers and materials partners — not from selling attention. People share techniques, form projects, coordinate work.

**Live site:** https://earthbackproject.org
**GitHub:** https://github.com/earthbackproject/earthback (auto-deploys to Netlify on push)
**Supabase project:** `yptktmzagctusbeqdaty`

**Right now:** Pre-launch. Platform app is built and mostly wired. Pending SQL migrations: PROFILE_MIGRATION, V3, V4, V9b, V9c, V10 (methods+skills). Analytics tracking live (SCHEMA_V9 run). Construction methods directory built.

**Navigation (as of session 31, 2026-03-02):**
- `nav.js` — public pages: Facebook-style visible link row (Feed · Circles · Map · Methods · Visualizer · Estimator · Gallery) + More ▾ grouped dropdown, self-contained CSS
- `app-nav.js` — app pages: same pattern + Methods link, self-contained CSS, `position: fixed` nav with spacer div (pages have NO topbar CSS of their own)
- `footer.js` — shared footer on all public pages

**Construction Methods (as of session 31):**
- `methods.html` — public directory of 30 building methods (23 green + 7 conventional)
- `construction_methods` table — full method data (description, materials, climates, pros, cons, practitioners)
- `member_skills` table — user↔method claims with 4 tiers: curious, hands_on, experienced, trainer
- `method_stats` view — aggregated claim counts per method
- `claim_skill()` / `unclaim_skill()` RPC functions
- Profile page (`profile.html`) shows claimed skills as colored badges in sidebar
- Research data in `eb_research/construction_methods-01/` — 1,273 curated images across 24 folders + HTML guide

**Image generation state (as of session 30, 2026-02-27):**
- Roster: **19 characters** — 12 originals + 7 new (Britta, Sofia, Owen, Callum, Joseph, Tariq, Devon)
- All charsheets, T4/T5/face batches generated; files renamed to `chars-NAME-*` convention
- **File naming convention:** `chars-NAME-TYPE_NNNNN_.png` / `charsheet-NAME-A/B/C_NNNNN_.png` / `site-THEME-NN_NNNNN_.png`
- **Hempcrete SDXL LoRA v1 trained** — 1500 steps, avg loss 0.134, in `local/lora-output/hempcrete-sdxl/`
- **Flux LoRA training not viable on 12GB VRAM** — use SDXL via Kohya, or investigate ai-toolkit for Flux
- **Next:** improve captions (voice-caption.py + USB mic) → retrain → test in scene compositions → PuLID
- **PowerShell tip:** use `;` not `&&` to chain commands (PS5 doesn't support `&&`)

**Analytics (as of session 23):**
- `page_views` table live in Supabase (SCHEMA_V9 run ✓)
- nav.js fires fire-and-forget tracking on every page load
- eb-grove.html has Live Traffic Monitor (session trails, live feed, top pages, stat cards)
- SCHEMA_V9b_ip.sql ready — adds IP capture via RPC function (run when ready)
- SCHEMA_V9c_device.sql ready — adds user_agent + user_location columns to page_views
- SCHEMA_V10_methods.sql + SCHEMA_V10_seed.sql ready — construction methods + member skills

---

## Active AI Image Work (ComfyUI / Flux)

All local scripts live in `local/scripts/` (gitignored):

| Script | Purpose |
|--------|---------|
| `queue-batches.py` | Main character + scenario image queuer (T1-T5 batches) |
| `queue-charsheets.py` | Character reference triptychs — 3 sheets × 2 seeds × 19 chars = 114 wide images |
| `queue-site-assets.py` | Site asset batch — 14 themes, ~80 prompts, landscape + portrait |
| `queue-circles.py` | 39 circle categories × 3 prompts for explore/circles pages |
| `queue-hempcrete-lora.py` | Hempcrete LoRA training images (Nadia Benali character) |
| `queue-pulid-faces.py` | PuLID face-locked generation (needs reference images) |
| `collect-3dprinter-images.py` | Download CC0 3D printer photos for LoRA training |
| `curate-3dprinter-images.py` | Crop/resize dataset to 1024×1024 |
| `caption-3dprinter-images.py` | Generate .txt captions for Kohya |
| `train-hempcrete-sdxl.bat` | SDXL hempcrete LoRA training (Kohya SS, rank 16, 1500 steps) |
| `train-3dprinter-lora.bat` | Kohya SS training command for 3D printer LoRA |
| `scrape-reference-images.py` | Scrape hempcrete + 3D concrete images from curated URLs |
| `voice-caption.py` | Whisper-powered voice captioning tool for LoRA datasets |
| `quick-caption.py` | WhisperFlow image captioning (show/replace/append/exclude) |
| `patch-pulid.py` | Re-apply PuLID compatibility patch after ComfyUI/PuLID updates |
| `crop-charsheet-refs.py` | Crop charsheet triptychs into 3 individual face refs per character |
| `sort-comfyui-output.py` | Sort comfyui-output/ into categorized subdirectories (re-runnable, has --undo) |
| `train-character-pipeline.py` | Full drop-folder-to-LoRA pipeline: generate 90 images (4 tiers), auto-caption, train |
| `charmanager.py` | Flask GUI for character ref management, triptych cropping, PuLID queuing (port 5111) |
| `charmanager.bat` | Startup script for Character Manager (auto-installs Flask if needed) |
| `setup-hempcrete-flux-lora.bat` | Copy Flux LoRA checkpoints to ComfyUI loras folder |
| `test-hempcrete-lora.py` | Queue 9 comparison images: 3 prompts × 3 LoRA variants (final, step-800, no-lora) |
| `optimize-for-web.py` | PNG → JPEG pipeline: strip metadata, resize to hero/card/thumb, compress, auto-watermark |
| `deploy-site-images.py` | Stage best web-ready-watermarked images for site deployment, generate HTML preview |
| `watermark.py` | Reusable watermark module — `apply_watermark(img)`. Diagonal EARTHBACK pattern + bottom-left wordmark `the Earthback Project.org` |
| `batch_watermark_all.py` | One-time batch: `local/web-ready/` → `local/web-ready-watermarked/`. Re-runnable, skips existing. |

Local data directories (all in `local/`, gitignored):
- `local/datasets/dataset-hempcrete/` — 105 curated hempcrete photos with .txt captions
- `local/lora-output/` — trained LoRA checkpoints
- `local/lora-reference/workflows/` — ComfyUI workflow JSONs for testing
- `local/lora-training/` — character LoRA configs and scripts
- `local/lora-pipeline/` — drop-folder for train-character-pipeline.py (CharName/ with ref-1/2/3.png + desc.txt)
- `local/faces-reference/` — PuLID reference face images (CharName.png = single, CharName-1/2/3.png = multi-ref from charsheet panels)
- `local/docs/` — Character-LoRA-Pipeline-Guide.docx (prompt reference, swap process, training settings)
- `local/web-ready/` — 3,237 web-optimized JPGs (hero/card/thumb) + inventory.json + og:image variants (UNwatermarked masters)
- `local/web-ready-watermarked/` — Same 3,232 images with `the Earthback Project.org` watermark applied. **Source for public deployment.** og:image excluded (already branded).
- `local/site-staging/` — Best-of WATERMARKED images staged for site deployment + preview.html gallery

**comfyui-output/ directory structure (after sort-comfyui-output.py):**
New PuLID/generation output lands in the root. Run `python local\scripts\sort-comfyui-output.py` to re-sort. Subdirs: `charsheets/`, `characters/[Name]/{faces,pulid,scenes-t4,scenes-t5}/`, `circles/`, `site-assets/`, `methods/`, `earthmesh/`, `hempcrete-lora/`, `misc/`

**Characters:** 19 characters — full bibles in `docs/CHARACTERS.md`, each with fixed seed for consistency.
**PuLID:** Node installed at `ComfyUI/custom_nodes/ComfyUI-PuLID-Flux`. Models need downloading via `setup-pulid.py`.
**Reference images:** Drop in `local/faces-reference/CharacterName.png` to enable PuLID for that character.
**Swap a reference:** Place new triptych in comfyui-output (root, charsheets/, or characters/Name/), then run `python local\scripts\crop-charsheet-refs.py --char "Name" --force`. See SESSION_NOTES.md for full process.

---

## Key Docs

| File | What it is |
|------|------------|
| `SESSION_NOTES.md` | What happened last session, immediate next steps |
| `TRACKER.md` | Full project board, all workstreams, checklist |
| `QUICKSTART.md` | Earthback orientation, services, credentials |
| `docs/CHARACTERS.md` | Full character bibles for all 19 AI characters |
| `docs/CIRCLES.md` | All 39 circle image categories with prompts |
| `docs/HANDOFF-3D-PRINTER-LORA.md` | 3D printer LoRA plan and pipeline |
| `maint-scripts/fix-cowork-vm.ps1` | Run as Admin in PowerShell when Cowork crashes |

---

## Git — Do NOT Commit From the VM

The Cowork VM accesses the repo through a virtiofs FUSE mount. Git's `unlink()` fails intermittently through this bridge, leaving orphan `.lock` files that block future operations.

**Convention:** Claude edits files. Nicco commits from PowerShell using the `g` alias:
```
g add -A
g commit -m "describe what changed"
g push
```
The `g` alias runs `maint-scripts/eb-git.ps1`, which auto-cleans stale lock files before every git command.

---

## End-of-Session Update Checklist

**Always update (every session):**
1. **SESSION_NOTES.md** — What was done, what's next, handoff context for next session
2. **TRACKER.md** — Session number in header, workstream status changes, checkbox progress

**Update when relevant:**
3. **CLAUDE.md** — Only if structural changes occurred (new scripts, new conventions, changed paths, new tools)
4. **docs/CHARACTERS.md** — If characters were added or modified
5. **docs/CIRCLES.md** — If circle categories changed

**Static (not session-updated):**
- **command-center.html** (in project root, gitignored) — credentials, service links, paths, startup sequence. Only update if services or paths change.

---

## Working Directory Convention

Scripts are run from: `cd C:\users\adrxi\earthback`
ComfyUI queue check: GET `http://127.0.0.1:8188/queue`
