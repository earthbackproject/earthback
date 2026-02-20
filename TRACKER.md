# Earthback — Master Project Tracker
*The source of truth for project status. Updated by Claude at the end of each session.*
*To resume: "Read TRACKER.md and SESSION_NOTES.md and pick up where we left off."*
*Visual version: `/tracker/index.html` — open in browser for the full dashboard.*

**Last updated:** 2026-02-20 (session 14 — folder reorganization, .gitignore update, QUICKSTART.md, post images from Flux, git workflow)

---

## 🗺 Quick Status

| Workstream | Status | Blocking? |
|---|---|---|
| Marketing Site (HTML) | 🟢 Live | earthbackproject.org · all pages deployed |
| Platform / App | 🟡 In progress | Auth live · feed with compose · projects hub · create-project wizard · messaging (demo) · circles hub · company profiles · post images |
| Database Migrations | 🟡 Pending | PROFILE_MIGRATION, SCHEMA_V3 (messages), V4 (post images) — all in `db/` folder |
| Source Control | 🟢 Set up | GitHub repo connected, git push → Netlify auto-deploy |
| Folder Organization | 🟢 Done | SQL→db/, brand assets→branding/, governance→governance/, archive→reference/, QUICKSTART.md at root |
| Org, Legal & Naming | 🟡 In progress | Trademark research still pending |
| Branding | 🟡 In progress | Typography done · logo still needed · og:image + favicons done |
| Hosting & Launch | 🟢 Live | earthbackproject.org on Netlify · git-based deploys |
| Documentation | 🟢 Done | Setup reference (HTML + DOCX), startup script, session notes, tracker |

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

### What's still needed on the site

**High priority**
- [x] **join.html — Netlify Forms wired** · Step 1 submits real data in background · Auth connection (magic link) comes when platform is built
- [x] **Mobile nav** — hamburger menu on all pages (all 8 files)
- [x] **Brand typography** — "the Earthback Project" treatment across all nav + footer logos
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
- [ ] **og:image** — social sharing preview card (1200×630); needed before any social sharing
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
- [x] Signup → profile creation flow — join.html sends magic link + saves to localStorage → auth-callback.html persists to DB ✓
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
- [ ] Logo — finalized vector/raster version needed for favicon, og:image, app
- [ ] Favicon — 32×32 / 180×180 versions for browser tab + iOS home screen
- [ ] og:image / social sharing card — 1200×630, ideally generated from brand palette

---

## 5 — Hosting & Launch

All items below are blocked until Site and Org decisions are made.

### Pre-launch
- [x] Choose hosting platform — **Netlify** (free tier, native Forms support)
- [x] Domain decided — **earthbackproject.org** (earthback.org/.com both taken; .com has competing launch)
- [ ] Set up Netlify deployment from folder or repo
- [ ] Point earthbackproject.org DNS to Netlify
- [ ] SSL active (auto via Netlify)
- [ ] Redirect www → root (or vice versa)
- [ ] Verify Netlify Forms capturing data from join.html

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
- [ ] 14. **Project creation flow** — form to create a project/company page, link to profile
- [ ] 15. **Media import pipeline** — paste URL → scrape oEmbed/OG → auto-populate title + thumbnail → create post
- [ ] 16. **Verification + rate limiting** — safety layer before public launch
- [ ] 17. **Operations tooling** — monitoring, incident pipeline, digest

---

## How to Use This File

- **Check boxes** as tasks complete: change `- [ ]` to `- [x]`
- **Add tasks** under the relevant workstream section
- **Update Quick Status** table when a workstream changes state
- **Update "Last updated"** date at the top each session
- At the **end of each session**, tell Claude: "Update TRACKER.md with what we did today"
