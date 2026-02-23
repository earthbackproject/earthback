# Earthback AI Visualizer — Build Handoff

## Context for the Build Claude

The live site is at **earthbackproject.org**. It's a community platform — circles, feeds, profiles, projects — not the old pitch/foundation pages in the project files. The design language is clean, warm, minimal: white cards on warm off-white backgrounds, subtle borders, DM Sans body text, Source Serif 4 for headings, green accent (#2d5a27). No dark hero sections or heavy gradients in the current site — everything feels grounded and editorial.

The **profile build page** is the next push in the main build thread. This visualizer feature should be designed to integrate with that — generated images become profile content.

**Reference the mockup file (`earthback_ai_visualizer_mockup.html`) for all visual decisions.** It matches the live site's design system.

---

## What This Page Is

A `/visualizer` page where users describe a sustainable building project and get an AI-generated image of it. Three purposes:

1. **Engagement** — visitors immediately see what earth/hemp/timber construction could look like for *their* project
2. **Revenue** — free tier (3 renders) → Pro upgrade ($9/mo unlimited)
3. **Game bridge** — generated visions eventually feed into the planned interactive builder/game

---

## Navigation

Add "Visualizer" to the main nav between "How It Works" and the Join button. Give it an `active` state when on this page. No separate badge needed in nav — the page itself has an "AI Preview" badge.

Current live nav: `The Feed | Circles | How It Works | Use Cases | About | Safety | Sign In | Join`

Proposed: `The Feed | Circles | How It Works | Use Cases | Visualizer | About | Safety | Sign In | Join`

---

## Page Structure (top to bottom)

1. **Site header** — standard, "Visualizer" nav link active
2. **Page header** — centered: "AI Preview" badge, "Envision your *build.*" headline, one-line description
3. **Two-column grid** — left: prompt panel, right: image display
4. **Refine bar** — single-line input for iterating on results
5. **Upgrade CTA** — card with Pro pricing
6. **Profile hint** — warm banner teasing the profile integration (coming soon)
7. **Site footer** — standard

---

## Left Panel: Prompt Interface

### Chip Selectors (structured context)
These get prepended to the user's text as hidden system context — the user never sees the combined prompt.

**Structure** (single-select): Single Home · Duplex · Community Hub · Workshop · Full Village

**Climate / Region** (single-select): High Desert · Prairie · Forest · Coastal · Mountain · Tropical

### Text Prompt
Large textarea. Placeholder: *"A 1,200 sq ft rammed earth home with a living roof, passive solar orientation, large south-facing windows, a shaded courtyard with rainwater cisterns, native xeriscape plantings and a small hemp garden..."*

### Render Style (single-select cards, 3-column grid)
- **Photorealistic** (default) — DSLR architectural photo
- **Sketch** — hand-drawn concept art
- **Blueprint** — technical schematic

### Generate Button
Green, full-width: "Generate vision" with sparkle SVG icon.

---

## Right Panel: Image Display

### Three states
1. **Placeholder** — dashed circle icon + "Your vision will appear here"
2. **Loading** — dark overlay, white spinner, "Rendering your vision..."
3. **Generated** — full-bleed image, 4:3 aspect ratio

### Toolbar (below image)
Left group: Regenerate · Variations (Pro only)
Right group: Download · Save to profile (ties into profile build)

---

## Refine Bar

Below both columns. Single-line input: *"Add a greenhouse on the south side, make the roof steeper..."*

Backend should stack refinements onto the original prompt context.

---

## Profile Integration (coordinate with profile build)

The "Save to profile" button should write the generated image + prompt metadata to the user's profile. When the profile page ships, these saved visions appear as "Project Visions" or similar — a gallery of what they're imagining. This bridges naturally into:
- Circle posts ("I'm envisioning this build — anyone done something similar?")
- Project formation ("Here's what we're planning")
- Eventually, the interactive game/builder

For now, "Save to profile" can require login and store to the user record. Display can come when the profile page is ready.

---

## Backend: Prompt Engineering Layer

This is the product differentiator. Every user prompt gets wrapped:

```
SYSTEM PREFIX (always prepended, user never sees):
"Photorealistic architectural visualization of sustainable construction.
Natural building materials: hempcrete, rammed earth, cob, adobe, living
roofs, timber frame. Permaculture landscaping. Warm natural lighting.
The building should look real, lived-in, and beautiful — not futuristic
or sci-fi. Professional architectural photography."

STYLE MODIFIER (based on render style):
Photorealistic → "DSLR photo, golden hour, 85mm lens, shallow depth of field"
Sketch → "Architectural concept sketch, pencil and watercolor, warm paper texture"  
Blueprint → "Technical blueprint, white lines on dark blue, annotated dimensions"

CLIMATE CONTEXT (based on chip):
High Desert → "Red rock landscape, sage, juniper, wide sky, arid"
Prairie → "Grassland, big sky, windbreak trees, gentle terrain"
Forest → "Dense conifers, dappled light, moss, fern undergrowth"
Coastal → "Ocean breeze, salt-tolerant plants, sandy soil, weathered wood"
Mountain → "Alpine meadow, snow-capped peaks, stone foundation, steep pitch roof"
Tropical → "Lush vegetation, palm shade, open-air design, cross-ventilation"

STRUCTURE CONTEXT (based on chip):
Single Home → "Single family residence"
Community Hub → "Community gathering building, large open interior"
[etc.]

USER PROMPT:
[their text]
```

**Store these as config**, not hardcoded — they'll need frequent tuning.

---

## API Provider Recommendation

**Primary: FLUX Pro via fal.ai**
- Best quality-to-cost ratio for architectural visualization
- Simple REST API: `POST https://fal.run/fal-ai/flux-pro`
- ~$0.05–0.10 per generation
- Can fine-tune later on earth-building imagery

**Premium tier: Midjourney API** (best raw architectural quality)

**Conversational/game bridge: OpenAI GPT-4o** (chat + image in one call — ideal for v2 "AI Design Partner" feature)

---

## Monetization

| Tier | Renders | Resolution | Styles | Notes |
|------|---------|-----------|--------|-------|
| Free (no account) | 3 total | Standard | Photorealistic only | localStorage counter |
| Free (signed in) | 5/month | Standard | Photorealistic only | Server-side counter |
| Pro ($9/mo) | Unlimited | HD | All 3 styles | Stripe subscription |

---

## Design Tokens (from live site + mockup)

```css
--bg: #faf9f6;
--bg-card: #ffffff;
--bg-warm: #f5f3ef;
--border: #e8e5df;
--border-light: #f0ede8;
--text-primary: #1a1a1a;
--text-secondary: #6b6b6b;
--text-muted: #999;
--accent: #2d5a27;
--accent-hover: #3d7a35;
--accent-light: #e8f2e6;
```

Fonts: `DM Sans` (body/UI), `Source Serif 4` (headlines). Loaded from Google Fonts.

Border radius: 12px (cards), 8px (inputs/buttons), 6px (chips).

---

## Implementation Phases

**Phase 1 (MVP):** Static page, FLUX API, generate + display + download. Free counter via localStorage. No auth required.

**Phase 2 (with profile build):** "Save to profile" writes to user record. Server-side usage tracking. Stripe for Pro tier. Refinement/iteration (conversation context).

**Phase 3 (game bridge):** Saved visions become "project cards." "Build This" button launches interactive experience. AI design partner mode via OpenAI conversational API. Community gallery.
