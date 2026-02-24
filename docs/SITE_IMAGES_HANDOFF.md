# Earthback — Site Image Generation Handoff
*Last updated: Feb 2026 · For any Claude session continuing this work*

---

## What this document covers

All non-character visual assets for the Earthback platform — hero images, circle card thumbnails, post feed images, material textures, and game concept art. Character LoRA training images are documented separately in `lora-training/README.md`.

---

## How image generation works

**No browser needed.** Two Python scripts drive ComfyUI directly via its REST API:

| Script | Purpose |
|--------|---------|
| `queue-batches.py` | Character training images (12 characters × multiple angles) |
| `queue-site-images.py` | All site UI images (hero, circles, posts, textures, game art) |

ComfyUI must be running first (via `start-comfy-claude.bat`). Images land automatically in `comfyui-output/`. The scripts handle variable resolutions per image type — no need to change ComfyUI settings manually.

**Basic usage:**
```powershell
cd C:\users\adrxi\Earthback

# Check ComfyUI is reachable
python queue-site-images.py --status

# Preview what would be queued
python queue-site-images.py --dry-run

# Queue everything
python queue-site-images.py

# Queue specific groups
python queue-site-images.py --group hero
python queue-site-images.py --group circles
python queue-site-images.py --group posts
python queue-site-images.py --group textures
python queue-site-images.py --group game

# Generate 3 variants of each for curation
python queue-site-images.py --loops 3
```

---

## Image groups and counts

| Group | Count | Resolution | Purpose |
|-------|-------|-----------|---------|
| `hero` | 4 | 1536×640, 1232×640 | Landing page hero + OG social card |
| `circles` | 12 | 1344×768 | One per circle on explore.html |
| `posts` | 8 | 1024×768 | Feed post thumbnails (assets/img/posts/) |
| `textures` | 6 | 896×896 | Material macros for section backgrounds |
| `game` | 5 | 1536×640 | Game concept art (world, container, build, player) |
| **Total** | **35** | | ~25 mins to generate all at 2.5s/it |

---

## Where images land and where they go

**Generated:** `comfyui-output/site-[slug]_00001_.png`

**Deploy to:**

| Generated slug | Deploy to | Notes |
|---------------|-----------|-------|
| `site-hero-home-01` | `site/assets/img/hero-home.jpg` | Main landing hero |
| `site-og-social-card` | `site/assets/img/og-image.png` | Social sharing card |
| `site-circle-natural-building` | `site/assets/img/circles/natural-building.jpg` | explore.html card |
| `site-circle-solar-offgrid` | `site/assets/img/circles/solar-offgrid.jpg` | explore.html card |
| `site-post-hempcrete-mix` | `site/assets/img/posts/hempcrete-mix.jpg` | Replaces placeholder |
| `site-post-food-forest` | `site/assets/img/posts/food-forest.jpg` | Replaces placeholder |
| `site-texture-hempcrete-surface` | `site/assets/img/textures/hempcrete.jpg` | CSS background |
| `site-game-world-overview` | `site/assets/img/game/world-overview.jpg` | Game concept page |
| *(etc — see full list in queue-site-images.py)* | | |

**Note:** The `site/assets/img/circles/` and `site/assets/img/textures/` and `site/assets/img/game/` directories don't exist yet — create them when deploying images.

---

## Curation workflow

1. Run `python queue-site-images.py --loops 3` to get 3 variants of each
2. Open `comfyui-output/` in Explorer — images named `site-[slug]_00001_.png`, `_00002_`, `_00003_`
3. Pick best variant, rename to drop the counter suffix
4. Convert PNG → JPEG if needed (saves significant bandwidth for web use)
5. Copy to appropriate `site/assets/img/` subdirectory
6. Update HTML to reference the new paths

---

## HTML integration needed (build-Claude tasks)

### explore.html — circle cards
Currently the circle cards have no background images — CSS-only. To add images:
```html
<!-- Each .ex-card needs a background image or an <img> tag -->
<div class="ex-card" style="background-image: url('assets/img/circles/natural-building.jpg')">
```
Or better: add a `.ex-card-img` element inside each card and style with CSS.

### index.html — hero section
The `.hero` section currently uses a CSS gradient only. To add a photo:
```css
.hero {
    background:
        linear-gradient(158deg, rgba(11,26,18,0.88) 0%, rgba(31,58,46,0.75) 60%, transparent 100%),
        url('assets/img/hero-home.jpg') center/cover no-repeat;
}
```

### index.html — OG image
Already referenced: `<meta property="og:image" content=".../og-image.png">` — just replace the file.

### feed.html — post images
Post images are already referenced in post data as `imageUrl` fields. The static placeholders in `assets/img/posts/` just need replacing with generated versions.

---

## Visual style reference

All site images follow the same documentary aesthetic as character images:

- **Style:** Documentary photograph, 35mm film, natural light only
- **Palette:** Deep forest green (`#1F3A2E`), clay gold (`#C2A56C`), warm parchment (`#F2EFE6`), moss green (`#7e9b73`)
- **No:** neon, oversaturation, studio backdrop, stock photography feel, AI-looking
- **People:** Anonymous or absent — no faces, or very small distant figures
- **Materials:** Hempcrete, cob, rammed earth, bamboo, salvaged timber, hemp fiber, mycelium, solar panels, metal roofing
- **Lighting:** Golden hour, soft overcast, directional sidelight — never flat studio light

---

## ComfyUI workflow settings (confirmed working)

| Setting | Value |
|---------|-------|
| Model | flux1-dev-fp8.safetensors |
| Steps | 20 |
| CFG | 1.0 |
| Sampler | euler |
| Scheduler | simple |
| Denoise | 1.0 |
| Guidance | 3.5 |
| VRAM mode | `--normalvram` (NOT `--gpu-only`) |
| Output dir | `--output-directory C:\users\adrxi\Earthback\comfyui-output` |

**Launch:** `C:\users\adrxi\Earthback\comfy-run.bat` (or `start-comfy-claude.bat` to open Chrome too)

---

## ComfyUI node IDs (for scripting)

| Node | ID | Purpose |
|------|----|---------|
| CLIP Text Encode (positive) | `6` | Prompt text |
| VAE Decode | `8` | — |
| Save Image | `9` | Filename prefix |
| EmptySD3LatentImage | `27` | Width / height / batch_size |
| CheckpointLoaderSimple | `30` | Model name |
| KSampler | `31` | Seed, steps, cfg |
| CLIP Text Encode (negative) | `33` | Empty for Flux |
| FluxGuidance | `35` | Guidance value |

---

## Current status

| Task | Status |
|------|--------|
| `queue-site-images.py` written | ✅ Done |
| Site images generated | ⬜ Run script |
| Images curated | ⬜ After generation |
| explore.html — circle card images integrated | ⬜ Build-Claude task |
| index.html — hero photo added | ⬜ Build-Claude task |
| og-image.png replaced | ⬜ Build-Claude task |
| post images replaced | ⬜ Build-Claude task |
| Textures used in CSS backgrounds | ⬜ Optional stretch goal |
| Game concept page built | ⬜ Future |

---

## Related files

- `queue-site-images.py` — the image generation script (run this)
- `queue-batches.py` — character training image script (separate)
- `lora-training/README.md` — character LoRA training pipeline
- `docs/SITE_BUILDER_HANDOFF.md` — overall site build handoff
- `site/content/flux-image-prompts.md` — earlier prompt drafts (superseded by the script)
- `site/content/flux-production-prompts.md` — character prompt reference
