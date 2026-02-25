# Earthback — Auto-loaded Session Context

*This file is read automatically at the start of every Cowork session.*
*For full project state: read SESSION_NOTES.md and TRACKER.md*

---

## To Resume Work
Say: **"Read SESSION_NOTES.md and TRACKER.md and pick up where we left off."**
Or just describe what you want to work on and Claude will orient from there.

---

## This Machine — Important Quirks

**OS:** Windows (Nicco's workstation)
**WSL:** Non-functional due to a BIOS virtualization flaw. Do not suggest WSL-based workflows.
**ComfyUI:** Running at `http://127.0.0.1:8188` via `comfy-run.bat`
- Python env: `D:\AI\comfy-env\Scripts\python.exe` (NOT system Python 3.14)
- Output: `C:\users\adrxi\Earthback\comfyui-output`
- Models: `D:\AI\ComfyUI\models\`
- All pip installs must target comfy-env: `D:\AI\comfy-env\Scripts\python.exe -m pip install ...`

**Kohya SS:** Presumably at `D:\AI\kohya_ss\` — confirm before running training scripts.

---

## VM Crash Recovery

The CoworkVMService occasionally hangs. **If the VM crashes:** Nicco runs `maint scripts\fix-cowork-vm.ps1` as Administrator in PowerShell, then reopens Claude. That script restarts the service.

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

**Right now:** Pre-launch. Platform app is built and mostly wired. 3 SQL migrations still pending (PROFILE_MIGRATION, V3, V4). Analytics tracking live (SCHEMA_V9 run). Next focus: LoRA training.

**Image generation state (as of session 23, 2026-02-25):**
- Roster: **19 characters** — 12 originals + 7 new (Britta, Sofia, Owen, Callum, Joseph, Tariq, Devon)
- All charsheets, T4/T5/face batches generated; files renamed to `chars-NAME-*` convention
- **File naming convention:** `chars-NAME-TYPE_NNNNN_.png` / `charsheet-NAME-A/B/C_NNNNN_.png` / `site-THEME-NN_NNNNN_.png`
- **Next:** LoRA training (hempcrete + 3D printer) → PuLID face-locked generation → integrate Flux assets into site
- **PowerShell tip:** use `;` not `&&` to chain commands (PS5 doesn't support `&&`)

**Analytics (as of session 23):**
- `page_views` table live in Supabase (SCHEMA_V9 run ✓)
- nav.js fires fire-and-forget tracking on every page load
- eb-grove.html has Live Traffic Monitor (session trails, live feed, top pages, stat cards)
- SCHEMA_V9b_ip.sql ready — adds IP capture via RPC function (run when ready)

---

## Active AI Image Work (ComfyUI / Flux)

All batch scripts live in `/Earthback/` root:

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
| `train-3dprinter-lora.bat` | Kohya SS training command for 3D printer LoRA |

**Characters:** 19 characters — full bibles in `docs/CHARACTERS.md`, each with fixed seed for consistency.
**PuLID:** Node installed at `ComfyUI/custom_nodes/ComfyUI-PuLID-Flux`. Models need downloading via `setup-pulid.py`.
**Reference images:** Drop in `faces-reference/CharacterName.png` to enable PuLID for that character.

---

## Key Docs

| File | What it is |
|------|------------|
| `SESSION_NOTES.md` | What happened last session, immediate next steps |
| `TRACKER.md` | Full project board, all workstreams, checklist |
| `QUICKSTART.md` | Earthback orientation, services, credentials |
| `docs/CHARACTERS.md` | Full character bibles for all 12 AI characters |
| `docs/CIRCLES.md` | All 39 circle image categories with prompts |
| `docs/HANDOFF-3D-PRINTER-LORA.md` | 3D printer LoRA plan and pipeline |
| `maint scripts/fix-cowork-vm.ps1` | Run as Admin in PowerShell when Cowork crashes |

---

## Working Directory Convention

Scripts are run from: `cd C:\users\adrxi\earthback`
ComfyUI queue check: GET `http://127.0.0.1:8188/queue`
