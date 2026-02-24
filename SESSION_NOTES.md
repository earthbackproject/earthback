# Earthback — Session Notes & Handoff
*Update this file at the end of every Cowork session. To resume: open Cowork, say "read SESSION_NOTES.md and pick up where we left off."*

---

## Last Updated
2026-02-24 — Session 20 with Nicco via Cowork

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
