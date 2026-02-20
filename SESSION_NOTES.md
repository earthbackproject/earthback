# Earthback — Session Notes & Handoff
*Update this file at the end of every Cowork session. To resume: open Cowork, say "read SESSION_NOTES.md and pick up where we left off."*

---

## Last Updated
2026-02-20 — Session 10 with Nicco via Cowork

---

## What Earthback Is

A community platform for people doing green building and construction — hempcrete, off-grid solar, food systems, mutual aid, community housing. Positioned as the anti-Facebook: no algorithm, no politics, no ads. People can hang out, share techniques, form projects, coordinate work.

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

- `/Earthback/external_reference_docs/v10-pre-launch-db etc/docs/earthback_platform_spec_v1.md` — full technical spec
- `/Earthback/external_reference_docs/v10-pre-launch-db etc/docs/decision log_v1/06_launch/v1_scope_freeze.md` — what's in/out of v1
- `/Earthback/external_reference_docs/v10-pre-launch-db etc/docs/decision log_v1/06_launch/launch_checklist.md` — all unchecked
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
