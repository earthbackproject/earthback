# Earthback — Site Builder Handoff
*For Claude sessions focused on site + platform work*
*Last updated: Feb 2026 · Image generation session ongoing in parallel*

---

## How to orient yourself

Read these three files first — they're the source of truth:
- `QUICKSTART.md` — logins, deploy workflow, folder map
- `TRACKER.md` — master checklist of what's done and what's left
- `SESSION_NOTES.md` — what happened most recently

Then say: **"I've read the docs. What needs doing on the site today?"** and the owner will direct you.

---

## What Earthback is

A coordination platform for the natural building / regenerative construction community. Think: a cross between a professional network and a project board, built around verified real-world projects using hemp, cob, rammed earth, bamboo, mycelium composites, and similar materials.

Two tracks running in parallel:
1. **Real platform** — actual coordination tool for builders, researchers, farmers, designers
2. **Game / narrative layer** — same characters exist as NPCs in a post-collapse building game (currently in concept phase)

The platform is NOT a social media clone. It's a knowledge and coordination layer: people post what they're building, what they need, what they know. Verification of real projects is core to the design.

---

## Live site

**URL:** https://earthbackproject.org
**Deploy:** git push to `main` → Netlify auto-deploys from `site/` folder
**GitHub:** https://github.com/earthbackproject/earthback

```bash
# Standard deploy
git add site/
git commit -m "describe what changed"
git push
```

---

## Tech stack

| Layer | Tool |
|---|---|
| Frontend | Vanilla HTML/CSS/JS — no framework, no build step |
| Hosting | Netlify (free tier) |
| Database | Supabase Postgres |
| Auth | Supabase Auth (magic link + Google OAuth) |
| Forms | Netlify Forms (join.html) |
| Future app | Next.js (placeholder in `app/`) |

**Supabase project:** https://supabase.com/dashboard/project/yptktmzagctusbeqdaty

---

## Site structure (`site/`)

| Page | Status | Notes |
|---|---|---|
| `index.html` | ✅ Live | Landing page — static marketing, demo feed preview |
| `feed.html` | ✅ Live | Community dashboard — live Supabase feed, compose, sidebar |
| `profile.html` | ✅ Live | Member profile — inline edit, avatar upload, projects, certs, media |
| `explore.html` | ✅ Live | Browse circles, members, projects |
| `about.html` | ✅ Live | Origin story, mission |
| `how-it-works.html` | ✅ Live | Three-pillar explainer |
| `use-cases.html` | ✅ Live | Six project archetypes |
| `join.html` | ✅ Live | Signup / onboarding only (no dashboard here) |
| `login.html` | ✅ Live | Return user login |
| `auth-callback.html` | ✅ Live | Handles OAuth + magic link redirect, persists to DB |
| `project.html` | ✅ Demo | Full project page template ("Desert Sun Hemp Homes") |
| `projects.html` | ✅ Demo | Project listing / browse |
| `circles.html` | ✅ Live | Circles hub |
| `messages.html` | ✅ Demo | Messaging UI (demo, not wired) |
| `create-project.html` | ✅ Demo | Create project wizard (demo, not wired) |
| `terms.html` | ✅ Live | Terms of Service |
| `privacy.html` | ✅ Live | Privacy Policy |
| `safety.html` | ✅ Live | Community trust & safety |

---

## What's done

The marketing site is fully live. Auth is working end-to-end (magic link + Google OAuth). The feed shows real Supabase data. Profiles are live with avatar upload and inline editing. Projects, certifications, and media tabs are scaffolded in the UI with demo data.

See `TRACKER.md` for the full checkmark list.

---

## What needs work — prioritized

### 🔴 Top priority

**1. Social media accounts** (`TRACKER.md` item 12e)
Set up official accounts on: Instagram, YouTube, TikTok, LinkedIn, Facebook, Bluesky, X.
Link from site footer on all pages. This is blocking launch marketing.

**2. og:image / social sharing card**
1200×630px image for social link previews. Should match brand palette (forest green, parchment, clay gold). Currently `assets/img/og-image.png` exists as a placeholder — needs real design.
Referenced in `<meta property="og:image">` in all HTML `<head>` sections.

**3. Project creation flow** (`TRACKER.md` item 14)
`create-project.html` exists as a demo wizard but isn't wired to Supabase.
The `projects` table schema exists at `db/SCHEMA_V2.sql`. Needs:
- Form submit → insert to `projects` table
- Redirect to `project.html?slug=xxx`
- Link project to user's profile in `project_members`

### 🟡 Medium priority

**4. Wire `project.html` to real data**
Currently hardcoded with "Desert Sun Hemp Homes" demo content.
Needs: load from `?slug=` query param → fetch from Supabase `projects` table.

**5. Media import pipeline** (`TRACKER.md` item 15)
Paste a URL (YouTube, Vimeo, article, etc.) → scrape oEmbed/Open Graph → auto-populate title + thumbnail → create feed post.
The `media_links` table schema is in `db/SCHEMA_V2.sql`.

**6. Email transactional setup**
Currently magic link emails are sending but from Supabase's generic domain.
Set up Postmark or Resend for custom domain email. Write templates for: magic link, welcome, digest.

**7. Missing `use-cases.html` from footer**
It's in the footer community column on most pages but missing from `index.html` footer.
Quick fix — just add the link.

### 🟢 Lower priority

**8. Extract shared CSS**
Every HTML page has inline `<style>` blocks with duplicated styles.
Extract to `assets/css/main.css` — makes global changes much easier.

**9. Trademark research** (Nicco doing this personally)
Once done: update all `<title>` and `<meta name="description">` tags with finalized name.

**10. Community Guidelines / Code of Conduct**
Can draw mostly from existing `safety.html` content. Needed for platform launch.

---

## Branding

| Element | Status | File |
|---|---|---|
| Color palette | ✅ Done | Forest green, parchment, clay/gold, moss |
| Typography | ✅ Done | Cormorant Garamond (display) + Inter (body) |
| Brand name treatment | ✅ Done | `ᵗʰᵉ EARTHBACK PROJECT` — CSS classes `.brand-the`, `.brand-back`, `.brand-project` |
| Wordmark / logo | ❌ Needed | Vector version for app, og:image, print |
| Favicon | ✅ Done | Eb monogram — SVG/ICO/PNG in `assets/img/` |
| og:image | ⚠️ Placeholder | `assets/img/og-image.png` — needs real design |

Brand standards: `branding/Earthback_Brand_Standards_v1.0_Expanded_Feb2026.pdf`

---

## Cast / Characters

12 fictional characters who are real-seeming members of the platform. They appear as demo content throughout the site (feed posts, explore page, etc.) and will eventually be NPCs in the game layer.

All 12 have been fully described and are in the process of getting LoRA-trained consistent AI portraits. Portrait images are being generated in parallel in a separate Cowork session.

| Handle | Character | Role |
|---|---|---|
| @james.osei | James Osei | Earthback trainer, Ghana |
| @lena.hartmann | Lena Hartmann | Cob builder, Morocco |
| @tom.westhall | Tom Westhall | Hemp farmer, Oregon |
| @rosa.mendez | Rosa Mendez | Bamboo architect, Costa Rica |
| @mei.lin | Mei Lin | Community developer, Philippines |
| @elena.vasquez | Elena Vasquez | Housing coordinator, New Mexico |
| @amara.diallo | Amara Diallo | Master builder, Senegal |
| @marcus.webb | Marcus Webb | Retired engineer, Kentucky |
| @kenji.nakamura | Kenji Nakamura | Mycelium researcher, Delft |
| @priya.sharma | Priya Sharma | Solar specialist, Queensland |
| @dara.okonkwo | Dara Okonkwo | Land trust organizer, Detroit |
| @sam.torres | Sam Torres | 3D printer tech, Phoenix |

Character profiles, seed posts, and image prompts all live in `site/content/`.

---

## Database

Supabase project: `yptktmzagctusbeqdaty`

| Migration | File | Status |
|---|---|---|
| Core schema | `db/SCHEMA_V2.sql` | ✅ Run |
| Messages | `db/SCHEMA_V3_messages.sql` | ⚠️ Pending |
| Post images | `db/SCHEMA_V4_post_images.sql` | ⚠️ Pending |
| Seed posts | `db/SEED_POSTS.sql` | ✅ Run (14 demo posts) |
| Profile migration | `db/PROFILE_MIGRATION.sql` | ⚠️ Pending |

Run order and notes: `db/README.md`

---

## Key content files

| File | What it is |
|---|---|
| `site/content/feed-posts/seed-posts-all.md` | All 14 demo feed posts — text, character, circle, image |
| `site/content/flux-image-prompts.md` | Original portrait + UI prompts |
| `site/content/flux-lora-batch2-prompts.md` | Action + environmental prompts for all 12 characters |
| `site/content/lora-training-pipeline.md` | Full LoRA training plan — don't touch, used by image generation thread |
| `site/content/batch-queue-scripts.js` | ComfyUI queue scripts — image gen thread only |
| `site/content/cast-photos/` | T1 portrait images per character (subfolders by character) |
| `comfyui-output/` | All generated images — T1/T2/T3/T4 batches landing here automatically |

---

## What's happening in the parallel image session

A separate Cowork thread is running ComfyUI overnight generating training images for character LoRAs. When that's done, the cast will have 15–20 consistent AI-generated images per character. Those images will be used to:
1. Train individual Flux LoRAs (one per character)
2. Generate profile photos, feed post images, and social media content at scale

**Don't touch:** `site/content/lora-training-pipeline.md`, `site/content/batch-queue-scripts.js`, `comfyui-output/` — these are managed by the image generation thread.

**Do use:** `site/content/cast-photos/` — the T1 portrait images in subfolders are available for use on the site now.

---

## Quick reminder on how to deploy

```bash
git add site/
git commit -m "what you changed"
git push
```
That's it. Netlify picks it up automatically. Usually live within 60 seconds.

---

## Where things get complicated

- **No shared CSS yet** — styles are duplicated across all HTML files. To change something site-wide (nav, footer, fonts) you have to update every file. Worth fixing but not urgent.
- **Demo data vs. real data** — some pages (project.html, messages.html, parts of explore.html) are still hardcoded demo content. Real data comes when the Supabase wiring is complete.
- **feed.html vs index.html** — `index.html` has a static fake feed for marketing purposes. `feed.html` has the real live feed. Don't confuse them.
- **The `_redirects` file** — tells Netlify to serve `/community` → `feed.html` and handles auth callbacks. Don't delete it.
