# Earthback — Master Project Tracker
*The source of truth for project status. Updated by Claude at the end of each session.*
*To resume: "Read TRACKER.md and SESSION_NOTES.md and pick up where we left off."*
*Visual version: `/tracker/index.html` — open in browser for the full dashboard.*

**Last updated:** 2026-04-14 (session 41 autonomous — hempcrete LoRA verified, web optimization pipeline built, 3237 web-ready JPGs processed, 3 og:image variants created, site deployment staging ready)

---

## 🗺 Quick Status

| Workstream | Status | Blocking? |
|---|---|---|
| Marketing Site (HTML) | 🟢 Live | earthbackproject.org · all pages deployed · 20+ pages |
| Platform / App | 🟡 In progress | Auth live · feed · gallery · visualizer · estimator · training · projects · circles · messaging (demo) · **community map** · **admin portal (eb-grove)** |
| Database Migrations | 🟡 Partial | V1-V2, V5-V9 all run ✅ · PROFILE_MIGRATION, V3 (messages), V4 (post images), V9b (IP), V9c (device), V10 (methods+skills) still pending |
| Source Control | 🟢 Current | GitHub repo connected, git push → Netlify auto-deploy · all pushed through session 28 |
| Folder Organization | 🟢 Done | SQL→db/, brand assets→branding/, governance→governance/, archive→reference/, QUICKSTART.md at root |
| Org, Legal & Naming | 🟡 In progress | Trademark research still pending |
| Branding | 🟢 SVG system live | 30 SVGs deployed · Georgia font · mixed-case brand · emoji replaced sitewide · favicon live |
| Hosting & Launch | 🟢 Live | earthbackproject.org on Netlify · git-based deploys |
| Documentation | 🟢 Done | CLAUDE.md (auto-loaded), QUICKSTART.md, command-center.html, session notes, tracker |
| AI Image Generation | 🟡 In progress | **Character Manager pipeline UI** (6-step guided flow, dual-GPU, triptych gen, **PuLID triptych from single photo**, panel gallery, **editable prompt editor with project save**, **gallery metadata viewer**) · **Dual-GPU ComfyUI** (GPU 0 :8189 triptychs, GPU 1 :8188 PuLID) · **Hempcrete Flux LoRA verified** (3 checkpoints, test script ready) · **Web optimization pipeline** (3237 web-ready JPGs from 1508 PNGs, 29× compression) · **3 og:image social cards** created · **Site deployment staging** (87 images staged, preview gallery) · PuLID v2 ready (0.60 strength, angle negatives, 3-ref rotation) · multi-project support · character LoRA training next |
| Earthmesh / EMF Products | 🟡 In progress | **Material locked: CRS (not Galvalume)** · **V2b deck ready** (CK-series integrated, Utah de-emphasized) · CK-Series Design Brief v1 done · Design Brief v13 + Spengler Proposal v4 updated · Laser at LA port · 30+ SKUs priced · **Nomad gap analysis done, Docker stack drafted** |

---

## 1 — Marketing Site (`/site/`)

The public-facing community site. Goal: live and functional before platform build begins.

### Pages
- [x] `index.html` — Landing page, hero, feed preview, circles, why, how it works, CTA
- [x] `about.html` — Origin story, mission, values
- [x] `how-it-works.html` — Three-pillar explainer
- [x] `safety.html` — Community trust & safety
- [x] `use-cases.html` — Six project archetypes
- [x] `join.html` — Onboarding only (signup + profile builder); dashboard moved to feed.html
- [x] `feed.html` — Community dashboard/feed (served at /community via Netlify rewrite)
- [x] `terms.html` — Terms of Service (plain language, 10 sections)
- [x] `privacy.html` — Privacy Policy (explicit what we collect / don't collect / never do)
- [x] `login.html` — Returning user sign-in (magic link + Google OAuth)
- [x] `auth-callback.html` — Magic link / OAuth redirect handler
- [x] `profile.html` — Member profile page with edit mode, avatar upload, skills, activity
- [x] `explore.html` — Browse circles, people, projects
- [x] `circles.html` — Circle hubs (geographic + thematic)
- [x] `projects.html` — Projects hub with cards
- [x] `project.html` — Individual project/company page
- [x] `create-project.html` — 5-step project creation wizard
- [x] `messages.html` — Split-pane messaging inbox (demo, needs V3 migration)
- [x] `visualizer.html` — AI vision generator with credits + personal gallery + sharing
- [x] `gallery.html` — Community shared visions gallery with likes + reporting
- [x] `designer.html` — Three.js parametric building **estimator** with **6 construction methods** (added Hemp Block Masonry) + exports
- [x] `training.html` — Skills & Training partner inquiry page with contact form
- [x] `sitemap.html` — Full site map organized by section
- [x] `map.html` — Community map (Leaflet + OpenStreetMap) with 88 curated hotspot pins, 6 categories, layer toggles, Supabase-powered
- [x] `methods.html` — **Building Methods directory** — 30 construction methods (23 green + 7 conventional), filterable/searchable card grid, expandable detail panels, 4-tier skill claiming system (Curious/Hands-On/Experienced/Trainer), community builder counts, profile badge integration
- [x] `eb-grove.html` — **Admin operations portal** (auth-gated, obscured URL) — real-time members, traffic monitor, system health, platform activity, visions feed

### What's still needed on the site

**High priority**
- [x] **join.html — Netlify Forms wired** · Step 1 submits real data in background · Auth connection (magic link) comes when platform is built
- [x] **Public nav** — Facebook-style visible link row: Feed · Circles · Map · Visualizer · Estimator · Gallery + More ▾ grouped dropdown · Estimator linked · orphaned CSS cleaned from 13 pages
- [x] **App nav** — app-nav.js rewritten with self-contained styles, same Facebook-style link row + More ▾ dropdown, orphaned `.topbar*` CSS removed from 7 app pages
- [x] **Mobile nav** — hamburger menu on all pages (all 8 files)
- [x] **Brand typography** — "the Earthback Project" treatment across all nav + footer logos · Georgia font · mixed case · leaf icon on all brand touchpoints
- [x] **SVG icon system** — 30 SVGs deployed; ~130 emoji replaced sitewide with proper icons
- [x] **Early access banner** — centralized in `early-access-banner.js` (app bottom) + sub-headers in nav.js/app-nav.js; copy: "Claim your username and get in early — your voice shapes what gets built. Join free →"
- [x] **Deploy to Netlify** — LIVE at earthbackproject.org ✓
- [x] **DNS + SSL** — Netlify auto-SSL active ✓
- [x] **Email address** — updated to earthbackproject@gmail.com across all pages ✓
- [x] **Netlify Forms verified** — signups confirmed capturing ✓
- [x] **Circles expanded** — 10 circles on homepage with tags; explore.html with all 12 + filter bar + geo discovery
- [x] **Create post demo** — demo composer on landing page, flows to join.html
- [x] **explore.html** — full circles browse page, filter by category, nearby section, geo search
- [x] **profile.html** — demo member profile page (person: bio, skills, circles, activity, projects)
- [x] **Magic link note** — join.html step 1 now explains no-password design under email field
- [x] **People discovery** — explore.html has "Featured Members" section + "People" nav link

**Medium priority**
- [x] **Favicon** — Eb monogram (SVG/ICO/PNG), shows on all tabs ✓
- [x] **og:image** — 3 variants created in `local/web-ready/og/` (build, homestead, timber scenes with brand overlay) — pick one and deploy to `site/assets/img/og-image.png`
- [ ] **Site tour page** — guided walkthrough for new visitors explaining causes, tools, and possibilities
- [x] **join.html → feed.html split** — dashboard moved to feed.html, join.html is onboarding only, /community serves feed.html ✓
- [ ] `join.html` — "See the community" step shows fake feed; connect to real feed once platform exists
- [ ] Add `use-cases.html` to index.html footer (currently missing from footer community column)
- [ ] Review all page titles/meta descriptions for SEO once name is finalized
- [ ] Press/contact page or section (currently just a mailto link)

**Lower priority**
- [ ] Extract shared CSS to `assets/css/main.css` — makes cross-page updates much easier
- [ ] Cookie/privacy banner if needed (depends on any analytics added)
- [ ] Analytics — if wanted (Plausible or Fathom are privacy-respecting options)

---

## 2 — Platform / App

The actual application: auth, profiles, circles, feed, projects, ingest, verification.
Per v1 scope freeze (2026-02-18): everything below is required for v1.

### Stack (per platform spec v1)
- Identity/Data: AT Protocol (Earthback-hosted PDS)
- App framework: Next.js
- Database: Supabase Postgres (scaffold exists at `/reference/v10-pre-launch-db etc/db/supabase_ops_scaffold_v1.sql`)
- Automation: n8n
- Email: Postmark or Resend
- AI: OpenAI API (structured JSON, no autonomous writes)

### Auth & Identity
- [x] Magic link auth — Supabase OTP, real emails sending ✓
- [x] Google OAuth sign-in — "Continue with Google" button on join.html and login.html; auth-callback pulls name/avatar from Google metadata ✓
- [x] Signup → profile creation flow — join.html creates account with email+password → saves profile to Supabase → proceeds to profiler or skip ✓
- [x] Session management — getSession() on page load, auto-redirect to /community ✓
- [x] Profile persistence — `profiles` table live in Supabase with RLS ✓
- [ ] DID storage (AT Protocol) — future phase
- [x] Avatar upload — click-to-upload on profile page; Supabase Storage 'avatars' bucket; 5 MB limit; file type validation; cache-busting; shows on profile + feed sidebar/header ✓
- [ ] MFA (TOTP) — Supabase supports authenticator apps; enroll via QR code; require aal2 for sensitive actions
- [x] Sign Out flow — button in dashboard topbar + nav on all pages; calls sb.auth.signOut() ✓

### Project & Company Pages (new v2)
- [x] `projects` table schema — owner_id, slug, type (project/company/org/campaign), status, media links, JSONB other_links ✓
- [x] `project_members` table — many-to-many with roles ✓
- [x] `project_needs` table — structured needs with urgency flags ✓
- [x] project.html — full demo page template ("Desert Sun Hemp Homes") ✓
- [x] Profile → Projects sidebar panel — linked cards with role badges ✓
- [x] Explore page → "Projects & Companies" section with 3 demo cards + CTA ✓
- [ ] Wire project.html to Supabase (load real data from ?slug= param)
- [ ] Create project form / flow

### Certifications & Credentials (new v2)
- [x] `certifications` table schema — title, issuing_org, credential_url, verified flag ✓
- [x] Certifications sidebar panel on profile.html — 3 demo certs ✓
- [ ] Add certification form / flow
- [ ] Verification workflow (admin marks cert as verified)

### Media & Content Import (new v2)
- [x] `media_links` table schema — url, platform detection, auto-post flag, thumbnails ✓
- [x] Media tab on profile.html — video grid + import box UI ✓
- [x] Media panel on project.html sidebar ✓
- [x] 'media' post_type added to posts table CHECK constraint ✓
- [ ] URL paste → auto-populate title/thumbnail (oEmbed or Open Graph scraping)
- [ ] Auto-create feed post from imported media link

### AI Visualizer & Gallery (new v5-v6)
- [x] `visualizer.html` — AI-powered vision generator with Flux image generation
- [x] `visions` table schema — user_id, prompt, structure, climate, style, image_url, is_shared, like_count, credit_earned, is_flagged ✓
- [x] `visions` Supabase Storage bucket — public, with user-folder upload policy ✓
- [x] Vision persistence — render → save → upload to Storage → insert DB row → gallery reload ✓
- [x] Rotating credit system — 1 credit/render, earn 1 every 2h, cap 25, localStorage-based ✓
- [x] Personal gallery — saved visions shown below generator with image, prompt, chips, date ✓
- [x] Share to gallery — "Share" button on personal vision cards, sets `is_shared = true` ✓
- [x] `gallery.html` — public shared gallery page with vision cards, creator links ✓
- [x] Like system — toggle like with `vision_likes` table, unique per user per vision ✓
- [x] Self-like prevention — users cannot like their own visions ✓
- [x] Report system — flag visions with reason + details via `vision_flags` table ✓
- [x] Credit award on like — likes earn credits for creator (max 5 per vision) ✓
- [x] SCHEMA_V5 (visions) — ✅ run in Supabase
- [x] SCHEMA_V6 (gallery — vision_likes, vision_flags, sharing columns) — ✅ run in Supabase
- [x] SCHEMA_V6b (visions UPDATE policy) — ✅ run in Supabase
- [x] SCHEMA_V6c (no self-likes RLS) — ✅ run in Supabase

### 3D Project Estimator (new v20, rebranded session 24)
- [x] `designer.html` — Three.js parametric building estimator ✓
- [x] 5-step wizard: Foundation & Type → Interior Layout → Roof & Energy → Materials & Finish → Export ✓
- [x] 3D preview with OrbitControls, shadows, fog, ground plane ✓
- [x] **6 construction methods:** 3D Printed Hemp, 3D Printed Concrete, Manual Hemp, Conventional, Hybrid, **Hemp Block Masonry** ✓
  - Hemp Block Masonry: ~120 blocks/yd³, R-2.4/inch, -0.34 tCO₂/yd³ carbon, $750/yd³ material, $16/sqft labor
- [x] Live material/cost/carbon calculations ✓
- [x] Working exports: glTF/GLB, CSV BOM, JSON config ✓
- [x] Auto-generated needs list per construction method ✓
- [ ] Wire to Supabase — save/load project configs per user
- [ ] Community project gallery — browse shared designs

### Community Map (new v22)
- [x] `map.html` — full-viewport Leaflet.js + OpenStreetMap community map ✓
- [x] `map_hotspots` Supabase table — lat/lng, category, title, description, url, status, is_visible, priority, RLS ✓
- [x] SCHEMA_V8_map.sql — ✅ run in Supabase
- [x] SCHEMA_V8b_unmet_need.sql — adds 'unmet-need' to category CHECK constraint ✅ run in Supabase
- [x] hotspots-seed.csv — 89 rows, RFC 4180 compliant, all supplier + unmet-need pins ✓
- [x] hotspots-seed.sql — full 88-pin INSERT (run after DELETE FROM to rebuild) ✓
- [x] SEED_unmet_need_pins.sql — incremental 24-pin unmet-need-only insert ✓
- [x] 6 pin categories: Rebuilding, Resource Hub, Active Build, Partner Org, Opportunity, Unmet Need ✓
- [x] Nav link added to nav.js (desktop + mobile) ✓
- [ ] Member pins — add lat/lng + map_visibility to profiles, show on map
- [ ] Project pins — wire project lat/lng to map layer
- [ ] "Claim your pin" onboarding interstitial post-signup

### Training Partners (new v7)
- [x] `training.html` — Skills & Training page with partner contact form ✓
- [x] `partner_inquiries` table — org_name, contact_name, email, focus_area, website_url, message ✓
- [x] SCHEMA_V7 + V7b — ✅ run in Supabase

### Hotspot Seed Data (v22)
- [x] `db/hotspots-seed.csv` — 89 rows, RFC 4180 compliant (QUOTE_ALL), all supplier + unmet-need pins ✓
- [x] `db/generate-hotspots-sql.py` — regenerates `hotspots-seed.sql` from CSV ✓
- [x] `db/hotspots-seed.sql` — full 88-pin INSERT for full rebuilds ✓
- [x] `db/SEED_unmet_need_pins.sql` — 24-pin incremental for live DB adds ✓
- [x] `docs/DISPATCH_POSTS_V2.md` — hemp-blocks circle (3 posts + SRC-16) + hempwood circle (3 posts + SRC-17) appended ✓

### Admin Operations Portal — eb-grove.html (new v20, expanded v23)
Nicco's main interface to the site. Auth-gated to `earthbackproject@gmail.com` and `nicco.macintyre@gmail.com`. URL deliberately obscured (not `/admin`).
- [x] Auth gate — checks Supabase session, denies access to non-whitelisted emails ✓
- [x] Stats cards — total members, new this week, new today ✓
- [x] Real-time member table — Supabase Realtime subscription, live rows on signup ✓
- [x] Desktop notifications — browser push on new member signup ✓
- [x] Activity log — recent signups with timestamps ✓
- [x] System Health panel — site ping, DB check, auth check, visions check; auto-refresh every 5 min ✓
- [x] Service quick links — GitHub, Supabase, Netlify (no project IDs exposed) ✓
- [x] What's Next priorities panel ✓
- [x] Recent Platform Activity feed — latest posts, projects, etc. ✓
- [x] Recent Visions feed — latest shared AI visions ✓
- [x] Live Traffic Monitor — stat cards (active now, today, sessions, all-time), session trails, live feed, top pages bar chart ✓
- [x] `noindex, nofollow` meta tag — hidden from search engines ✓
- [x] Linked from command-center.html topbar ✓
- [x] Flagged visions review panel — restore or delete flagged visions with reporter reasons ✓
- [x] Partner inquiry inbox — view training.html form submissions, mark reviewed, reply via email ✓
- [ ] Add quick-action buttons — run common admin tasks (e.g. seed content, check queue)

### Analytics & Traffic Tracking (new v23)
- [x] `db/SCHEMA_V9_analytics.sql` — `page_views` table with RLS + realtime subscription ✓
- [x] SCHEMA_V9_analytics.sql — ✅ run in Supabase · traffic monitor live and working
- [x] `site/assets/js/nav.js` — fire-and-forget page-view tracking on every page load ✓
- [x] `db/SCHEMA_V9b_ip.sql` — adds `ip_address` column + `insert_page_view()` RPC function ✓
- [ ] Run SCHEMA_V9b_ip.sql in Supabase — enables IP capture in session trails + live feed

### Shared Components
- [x] `assets/js/nav.js` — shared nav for all public pages: Facebook-style link row + More ▾ dropdown, auth state, page-view tracking ✓
- [x] `assets/js/app-nav.js` — shared nav for all app/authenticated pages: self-contained styles, visible link row + More ▾ dropdown, messages icon + avatar ✓
- [x] `assets/js/footer.js` — shared footer component for all public pages ✓

### Core User Flow (v1 required)
- [ ] Create Project
- [ ] Add Source URL
- [ ] Create Ingest Job
- [ ] Scraper worker (safe fetch + extract, HTTPS only, SSRF protected)
- [ ] Store ingest artifacts with TTL
- [ ] AI Draft generation (structured JSON output)
- [ ] Draft review UI
- [ ] User Accept Fields → canonical record update
- [ ] Publish Project
- [ ] Project visible in Feed

### Verification
- [ ] Earthback Labeler service
- [ ] Verified Human label
- [ ] Verified Project label
- [ ] Feed filter by verification status

### Feed & Circles
- [ ] Real feed (replaces demo on join.html and landing page)
- [ ] Circle membership
- [ ] Post types: Project forming / Technique share / Resource available / Project complete
- [ ] Feed filter by circle / verified status

### Rate Limiting & Security
- [ ] DID-based rate limits
- [ ] IP-based safety cap
- [ ] Tier quotas: unverified (2 proj/day) vs verified (20 proj/day)
- [ ] SSRF protection on URL ingest
- [ ] Audit logging

### Operations
- [ ] Ingest job tracking dashboard
- [ ] Incident reporting table
- [ ] Error monitoring (uptime/error rate)
- [ ] Daily digest (optional but preferred per spec)

### Email
- [ ] Transactional email service set up (Postmark or Resend)
- [ ] SPF/DKIM/DMARC configured
- [ ] Magic link email template
- [ ] Welcome email

---

## 3 — Org, Legal & Naming

### Naming (🟡 Provisional decision made — trademark research still needed)
- [ ] **Finish trademark research** — identify all existing "Earthbacks" in green building / sustainability space
- [x] **Provisional public brand name: "the Earthback Project"** — typography treatment applied to all pages
  - "Alliance" dropped — too political
  - "Foundation" reserved for the 501(c)(3)
  - Public-facing = **the Earthback Project** · entity names stay in legal docs
- [ ] **Apply finalized name** to title tags and meta descriptions once trademark research is complete

### Entity Structure (as of 2026-02-19)
| Entity | Purpose | Status |
|---|---|---|
| Earthback Project | For-profit corp · holds IP | Exists |
| Earthback [TBD] | 501(c)(3) · nonprofit · community org | Forming |

### Legal
- [ ] 501(c)(3) application / formation
- [ ] IP assignment from Project to appropriate entity
- [x] Terms of Service written — `/site/terms.html` (placeholder needed before any real signups)
- [x] Privacy Policy written — `/site/privacy.html` (required before collecting any user data)
- [ ] Community Guidelines / Code of Conduct (can draw from safety.html content)

---

## 4 — Branding

- [x] Color palette — established (forest green, parchment, clay/gold, moss)
- [x] Typography — Cormorant Garamond (serif/display) + Inter (body)
- [x] Brand standards documented (`/reference/Earthback_Brand_Standards_v1.0_Expanded_Feb2026.pdf`)
- [x] Brand wordmark treatment — `ᵗʰᵉ EARTHBACK PROJECT` typographic system applied to all 8 site pages (`.brand-the` / `.brand-back` / `.brand-project` CSS classes)
- [ ] Logo — finalized vector/raster version needed for og:image, app
- [x] Favicon — Eb monogram SVG/ICO/PNG, shows on all tabs ✓
- [x] og:image / social sharing card — 3 photo-backed variants with brand overlay in `local/web-ready/og/` (session 41)

---

## 5 — Hosting & Launch

All items below are blocked until Site and Org decisions are made.

### Pre-launch
- [x] Choose hosting platform — **Netlify** (free tier, native Forms support)
- [x] Domain decided — **earthbackproject.org** (earthback.org/.com both taken; .com has competing launch)
- [x] Set up Netlify deployment from folder or repo ✓
- [x] Point earthbackproject.org DNS to Netlify ✓
- [x] SSL active (auto via Netlify) ✓
- [x] Redirect www → root (or vice versa) ✓
- [x] Verify Netlify Forms capturing data from join.html ✓

### Launch checklist (from `/docs/decision log_v1/06_launch/launch_checklist.md`)
- [ ] Production environment deployed
- [ ] SSL active
- [ ] DNS configured
- [ ] Environment variables verified
- [ ] Auth working end-to-end
- [ ] Feed loads
- [ ] Rate limits active
- [ ] Error monitoring live
- [ ] Public homepage ready
- [ ] Legal pages present (Terms + Privacy)
- [ ] Contact route working

---

## 6 — Content & Copy

- [x] Landing page copy
- [x] About / origin story
- [x] How it works
- [x] Safety & trust
- [x] Use cases (6 archetypes)
- [x] Join flow copy
- [x] Terms of Service — `/site/terms.html`
- [x] Privacy Policy — `/site/privacy.html`
- [ ] Email templates (welcome, magic link, digest)
- [ ] Community Guidelines / Code of Conduct (can draw from safety.html)
- [ ] Press/media one-pager (if needed pre-launch)

---

## Suggested Build Order

Given current state, this is the recommended sequence:

- [x] 1. **Site pages complete** — 8 pages, all launch-ready copy and nav
- [x] 2. **Terms of Service + Privacy Policy** — written and linked
- [x] 3. **Netlify Forms wired** — join.html captures real signups on deploy
- [x] 4. **Mobile nav** — hamburger on all pages
- [x] 5. **Brand name + typography** — "the Earthback Project" applied everywhere
- [x] 6. **Deploy to Netlify on earthbackproject.org** — LIVE ✓
- [x] 7a. **Profile page** — profile.html demo template, people discovery on explore.html ✓
- [x] 7b. **Real backend** — Supabase auth + profiles DB + login.html + auth-callback.html ✓
- [x] 8a. **Filler content** — 14-post demo feed, 7 member cards in explore.html; SEED_POSTS.sql ready for Phase 2
- [x] 8b. **Favicon + og:image** — Eb monogram favicon (SVG/ICO/PNG) + og:image social card on all pages ✓
- [x] 9. **Sign Out** — dashboard topbar button + nav link swap on all pages + welcome-back banner ✓
- [x] 10. **Projects, certifications, media** — project.html page, certs on profile, media tabs, SCHEMA_V2.sql, explore.html projects section ✓
- [ ] 11. **Trademark research → naming finalized** — then update title tags / meta ← NICCO WORKING ON THIS
- [x] 12a. **Database migration** — SEED_POSTS.sql + SCHEMA_V2.sql run in Supabase; all 7 tables live + 14 seed posts inserted (all flagged is_demo=true) ✓
- [x] 12b. **Real feed (join.html)** — POSTS array replaced with live Supabase query; circle styles lookup, relative time, dynamic sidebar streams; index.html kept static (marketing preview) ✓
- [x] 12c. **Page split (join.html → feed.html)** — dashboard moved to feed.html, join.html is onboarding only, auth-callback + _redirects updated, sessionStorage handoff for fresh profiles ✓
- [x] 12d. **Google OAuth sign-in** — "Continue with Google" on join + login pages; auth-callback extracts Google name/avatar ✓
- [ ] 12e. **Social media accounts** — Set up official Earthback accounts (Instagram, YouTube, TikTok, LinkedIn, etc.); link from site footer
- [x] 13. **Profile editing + avatar upload** — inline editing for name, tagline, bio, location, skills (3 levels); avatar upload to Supabase Storage; feed shows uploaded avatar; cover band slimmed down ✓
- [x] 14. **AI Visualizer** — Flux-powered vision generator with credit system, personal gallery, save to Supabase Storage ✓
- [x] 15. **Shared Gallery** — gallery.html with likes, self-like prevention, reporting, credit rewards ✓
- [x] 16. **3D Project Estimator** — Three.js parametric building estimator with 6 construction methods, live calculations, GLB/CSV/JSON exports ✓
- [x] 17. **Training Partners** — training.html with contact form, partner_inquiries table ✓
- [x] 18. **Shared nav/footer components** — nav.js + footer.js injected on all public pages ✓
- [x] 19. **Sitemap** — sitemap.html with all pages organized by section ✓
- [x] 20. **Community Map** — map.html with Leaflet, 88 curated hotspot pins, 6 categories, Unmet Need, Supabase-powered ✓
- [ ] 21. **Integrate Flux assets** — use rendered images for site heroes, sections, textures
- [ ] 22. **Project creation flow** — form to create a project/company page, link to profile
- [ ] 23. **Media import pipeline** — paste URL → scrape oEmbed/OG → auto-populate title + thumbnail → create post
- [ ] 24. **Verification + rate limiting** — safety layer before public launch
- [ ] 25. **Operations tooling** — monitoring, incident pipeline, digest

---

## 7 — AI Image Generation (ComfyUI / Flux)

All scripts in `local/scripts/`. ComfyUI at `http://127.0.0.1:8188`. Output: `comfyui-output/`.
**File naming convention:** `chars-NAME-TYPE_NNNNN_.png` (character-first for Explorer curation)

### Character Images (19 characters × shots)
- [x] 19 characters defined in `docs/CHARACTERS.md` with fixed seeds (12 originals + 7 new: Britta, Sofia, Owen, Callum, Joseph, Tariq, Devon)
- [x] Face angle batches built — front / left / right / down / talk (36 images generated, keepers in `comfyui-output/`)
- [x] T5 literal scenes built — 5 scenes × 12 characters (162 images generated, keepers in `comfyui-output/`)
- [x] T4 scenario batches built — 5 prompts × 12 characters (T4-01 through T4-05)
- [x] T1-T4 images from fixed seeds — all 237 rejected (near-duplicates); moved to `comfyui-output/_rejected/`
- [x] File naming overhaul — all keeper files renamed to `chars-NAME-*` convention
- [x] `queue-batches.py` prefixes updated to match new naming
- [x] T4 re-run queued with `--reseed --batch-size 3` (180 images, random seeds, genuine variety)
- [x] Character triptych reference sheets — `queue-charsheets.py` (72 images, 3 sheets × 2 seeds × 12 chars)
- [x] Site asset batch — `queue-site-assets.py` (14 themes, ~80 prompts, ~160 images)
- [ ] **Review overnight output** — charsheets, site assets, T4 re-run in `comfyui-output/`
- [ ] **Pick PuLID reference faces** — best charsheet panel per character → `faces-reference/CharacterName.png`

### PuLID Face-Locked Generation
- [x] PuLID node installed at `ComfyUI/custom_nodes/ComfyUI-PuLID-Flux`
- [x] PuLID models downloaded — pulid_flux_v0.9.1.safetensors + EVA CLIP
- [x] InsightFace antelopev2 models installed at `D:\AI\ComfyUI\models\insightface\models\antelopev2\`
- [x] Reference face images prepared — 8 characters (512×640 center crops) in `local/faces-reference/`
- [x] **Workflow JSON fixed** — updated class_types for PuLID Flux nodes + added PulidFluxEvaClipLoader (node 44)
- [x] **comfy-run.bat fixed** — `--cuda-device 1` for dual GPU operation
- [x] **PuLID generation confirmed working** (test: Lena Hartmann)
- [x] **Overnight orchestrator ready** — `run-pulid-all.py` restarts ComfyUI per character, safe alongside LoRA training
- [x] **v2 angle fixes** — strength 0.60, per-angle negatives, 4 prompt templates/angle, 3-ref rotation from charsheet panels
- [x] **comfyui-output organized** — 2,362 files sorted into 51 subdirs via `sort-comfyui-output.py`
- [ ] **Run PuLID v2 batch** — `python local\scripts\run-pulid-all.py --rounds 3` (3 rounds = 1 per ref image)
- [ ] **Review PuLID v2 quality** — if angles still flat, try strength 0.50 or `start_at: 0.2` in node 42
- [ ] **Re-sort new output** — `python local\scripts\sort-comfyui-output.py`
- [ ] **Caption PuLID output** — run quick-caption.py on character face images
- [ ] **Generate character LoRA configs** — make-flux-config.py per character
- [ ] **Train 8 character LoRAs** — ~11hrs each on cuda:0

### Hempcrete LoRA Training
- [x] Script built: `queue-hempcrete-lora.py` (Flux generation for training images)
- [x] Dataset voice-captioned — 77 images (44 excluded), trigger word EBHEMPCRETE, via quick-caption.py + WhisperFlow
- [x] Kohya SS installed at `D:\AI\kohya_ss\` with sd-scripts submodule
- [x] **SDXL LoRA v1 trained** — `train-hempcrete-sdxl.bat`, 1500 steps, 83min, avg loss 0.134
- [x] ai-toolkit installed at `D:\AI\ai-toolkit\` (torch 2.5.1+cu121, diffusers 0.36.0)
- [x] **Flux LoRA training complete** — `hempcrete-flux-12gb.yaml`, 1200 steps @ ~36s/step, layer_offloading, cuda:0
- [x] **Flux LoRA checkpoints verified** (session 41) — 3 valid safetensors: 400, 800, 1200 steps (165 MB each)
- [x] `setup-hempcrete-flux-lora.bat` — copies all 3 Flux LoRA checkpoints to ComfyUI loras folder
- [x] `test-hempcrete-lora.py` — queues 9 comparison images (3 prompts × 3 variants: final, step-800, no-lora)
- [ ] **Run LoRA test** — `setup-hempcrete-flux-lora.bat` then `python local\scripts\test-hempcrete-lora.py`
- [ ] **Compare LoRA outputs** — pick best checkpoint, evaluate quality
- [x] 4 checkpoints in `local/lora-output/hempcrete-sdxl/` (steps 500, 1000, 1500 + final)
- [x] Final LoRA copied to `D:\AI\ComfyUI\models\loras\hempcrete-sdxl-v1.safetensors`
- [x] Voice captioning tool built (`local/scripts/voice-caption.py`) — Whisper-powered, mic-based
- [ ] **USB mic arrives** → re-caption dataset with voice tool for better descriptions
- [ ] **Re-train with improved captions** → hempcrete-sdxl-v2
- [ ] **Test in context** — characters + hempcrete in Earthback scene compositions

### Circle Category Images (39 categories × 3 prompts)
- [x] `queue-circles.py` script built
- [x] 363 circle images generated in `comfyui-output/` — review pending

### 3D Printer LoRA Pipeline
- [x] `collect-3dprinter-images.py` — downloads CC0 photos from Pexels + Pixabay (15 search terms)
- [x] `curate-3dprinter-images.py` — smart center-crop to 1024×1024, quality filtering
- [x] `caption-3dprinter-images.py` — template or BLIP-2 captions, Kohya `.txt` format
- [x] `scrape-reference-images.py` — scrapes hempcrete + 3D concrete images from curated URLs; supports external URL file + custom categories
- [x] `train-3dprinter-lora.bat` — Kohya SS Flux LoRA training command (rank 16, 1500 steps)
- [x] `docs/HANDOFF-3D-PRINTER-LORA.md` — full plan, visual grammar, pipeline, eval prompts
- [ ] **Get API keys** — Pexels (free) + Pixabay (free); add to script flags
- [ ] **Run collection** — `python collect-3dprinter-images.py --pexels-key KEY --pixabay-key KEY`
- [ ] **Curate + caption dataset**
- [x] **Kohya SS confirmed** at `D:\AI\kohya_ss\` with venv (Python 3.11, torch+cu124)
- [ ] **Run training** — use SDXL approach (not Flux) per session 30 findings

---

## 8 — Earthmesh / EMF Products & Investor Outreach

Focused product line: Faraday enclosures, LoRa mesh comms kits, and solar trailer fleet. Goal: raise $250K seed round to stock radio and metal materials before supply chain disruptions.

### Material Decision
- [x] **Material locked: cold-rolled steel (CRS)** — Nicco + Erno confirmed. Not Galvalume. Higher ferrous content = dramatically better magnetic shielding for EMP. Same coil formats, same supply chain as metal roofing stock.

### Laser Table
- [x] Fiber laser ordered
- [ ] **Laser in port of LA** (March 26, 2026) — track delivery to Spengler's shop
- [ ] Laser installed and operational

### Investor Deck
- [x] V1a — Broad Earthback Industries deck (21 slides) → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1a.pptx`
- [x] V1b — Focused EMF/comms deck with real product data (16 slides) → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1b.pptx` + `.pdf`
- [x] V1c — Material updated to CRS, laser status updated → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1c.pptx` + `.pdf`
- [x] V1d — GSM credential prominent on founder slide + Earthmesh node slide → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1d.pptx` + `.pdf`
- [x] V1e — 30-year full circle narrative (GSM 1996 → Earthmesh 2026) woven through slides 2, 6, 14
- [x] V1f — LoRa bandwidth accuracy pass (messaging only, no voice/streaming claims)
- [x] V1g — Wi-Fi HaLow roadmap note on mesh radio slide → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V1g.pptx` + `.pdf`
- [x] V2a — 18-slide overhaul: pptxgenjs rewrite, new card layouts, full product matrix, maker platform slide → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V2a.pptx` + `.pdf`
- [x] V2b — CK-series comms kits integrated (5 SKUs, real verified pricing $89-$999), Utah references removed/softened across 10 slides, Go-To-Market slide rewritten → `admin_docs/Earthmesh-EMF_Investor_Deck_2026-V2b.pptx` **(CURRENT)**
- [ ] V2b PDF — needs conversion on Windows (LibreOffice or PowerPoint Save As)
- [ ] V3 — Post-investor-feedback revision

### Research
- [x] `eb_research/Earthmesh/WiFi_HaLow_Research.md` + `.docx` + `.pdf` — Wi-Fi HaLow (802.11ah) comparison vs LoRa, hardware availability, integration recommendations. Phase 2 complementary layer, not LoRa replacement.
- [x] `eb_research/offline-emp-restart/Nomad_vs_Earthback_Analysis_v1.docx` + `.pdf` — Project N.O.M.A.D. gap analysis: feature comparison table (18 capabilities), 3-phase integration plan, Docker container inventory by trailer tier, content pre-loading strategy

### CK-Series Communications Kits
- [x] Price research — browser-verified wholesale/retail for 12+ components (GMRS, SDR, LoRa, RTL-SDR, accessories) — March 26, 2026
- [x] `eb_research/offline-emp-restart/CK_Series_Design_Brief_v1.docx` + `.pdf` — 12-page design brief with BOM tables, component price reference, revenue projections
- [x] 5 kits defined: CK-10 ($89, 58%), CK-20 ($249, 48%), CK-30 ($169, 75%), CK-40 ($399, 73%), CK-50 ($999, 54%)
- [ ] Source supplier quotes for volume pricing (MOQ 100+)
- [ ] Prototype CK-10 and CK-30 packaging
- [ ] FCC GMRS license QR code artwork

### Offline Station Software Stack (Docker)
- [x] `eb_research/offline-emp-restart/docker-compose.yml` — Tiered Docker Compose with profiles: scout, field, hub, command, dev. 13 services.
- [x] `eb_research/offline-emp-restart/.env.example` — Environment configuration template
- [x] `eb_research/offline-emp-restart/containers/mesh-bridge/` — Meshtastic AI bridge Dockerfile + script
- [ ] **Test Kiwix + ProtoMaps + CyberChef on Windows** via Docker Desktop
- [ ] **Download ZIM files** — wikipedia_en_100_mini (test), wikimed, first-aid
- [ ] **Download Kolibri content packs** — Khan Academy math/science
- [ ] **Download PMTiles** — test one tribal region
- [ ] **Test llama.cpp CUDA container** — official image with RTX 3060
- [ ] **Build Earthback Dashboard** — web UI for managing all station services
- [ ] **Offline provisioning** — pre-built SSD images per tier
- [ ] **Authentication layer** — role-based login (Nomad doesn't have this)
- [ ] **Station-to-station sync** — auto-merge knowledge bases when stations are in range

### Product Data Sources (current versions)
- `eb_research/offline-emp-restart/Entry_Products_Design_Brief_v13.docx` — 6 entry SKUs, 3 config levels, maker platform (**CRS material, was v12/Galvalume**)
- `eb_research/offline-emp-restart/Spengler_CEO_Proposal_v4.docx` — 30-SKU matrix, full pricing, margins 48-62% (**CRS material, was v3/Galvalume**)
- `eb_research/Earthmesh/Earthmesh_Investor_Deck_v7.pptx` — node specs, trailers, market segments, financials

### Partners (political notes)
- **Spengler Industries** — 40-year credibility, present in deck but NOT as anchor/lead (Erno must not get leverage for partnership role)
- **BFFT (Bountiful Food Truck & Trailer)** — trailer manufacturer, company name only (Jon Fletcher not mentioned per political sensitivity)

### Next
- [ ] Get investor feedback on V1g
- [ ] Iterate to V2 based on feedback
- [ ] **CRS coil stock pre-order** — lock in pricing on 24 ga + 20 ga, full truckload buy
- [ ] Open 130E 1100N building (or alternate) for manufacturing
- [ ] Begin radio and metal stock procurement

---

## How to Use This File

- **Check boxes** as tasks complete: change `- [ ]` to `- [x]`
- **Add tasks** under the relevant workstream section
- **Update Quick Status** table when a workstream changes state
- **Update "Last updated"** date at the top each session
- At the **end of each session**, tell Claude: "Update TRACKER.md with what we did today"
