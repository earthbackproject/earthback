# Earthback Platform — Vision, Features & Game Architecture

## Master Document

This document captures the full product vision for Earthback as it evolves from a community platform into a design-to-build pipeline with a game layer. It includes every feature discussed, the technical architecture for the creation platform and game integration, and a prioritized roadmap.

Everything here should be treated as a living document — ideas to be refined, not commitments carved in stone.

---

## The Big Picture

Earthback is building toward something that doesn't exist yet: a platform where the line between "designing a building in a game" and "designing a building you'll actually construct" disappears. The platform has two halves that share an engine:

**The Real-World Side** — a building design tool where materials are real, physics are real, costs are real, and the output is a set of plans you can actually construct. Users design hempcrete homes, community hubs, workshops, and permaculture layouts using real material properties, real climate data, and real structural constraints. What they build here is exportable as floor plans, bills of materials, and construction sequences.

**The Post-Apocalyptic Side (Rust)** — a survival building game where the same structural principles apply but the material palette is scavenged, the aesthetic is survival-creative, and the constraints are looser. Built on modded Rust servers. The monthly wipe cycle becomes a feature — structures that are well-designed and community-maintained can persist across wipes (the "endurance" mechanic your Rust friends are building). Players learn real building science through gameplay, and when they're ready, they can cross over to the real-world editor and design something they'll actually build.

**The Bridge** — the AI visualizer, the creation platform, and the community are the connective tissue. Someone can describe a dream → get an AI render → open it in the editor → refine it into real plans → share it with their circles → find collaborators → build it. Or they can build something wild in the Rust world → realize the structural principles are real → cross over and design their actual home.

---

## What's Built / In Progress

| Feature | Status | Notes |
|---------|--------|-------|
| Community platform (circles, feed, profiles) | Live at earthbackproject.org | Core social layer |
| Profile build page | Next push | Foundation for all profile types |
| AI Visualizer | Mockup + handoff done | Prompt → image, free/Pro tiers |
| Ghost profiles (businesses) | Mockup + handoff done | Search-trigger-invite pattern |
| Content creator profiles | Mockup + handoff done | YouTube/podcast/blog import |
| Rust server infrastructure | Friends setting up | Server management, wipe persistence |

---

## Feature Catalog

### 1. AI Visualizer (Designed — Ready to Build)

**What it does:** User describes a project in natural language, selects structure type / climate / render style, gets an AI-generated architectural visualization.

**Monetization:** Free tier (3 renders) → Pro ($9/mo unlimited, HD, all styles).

**Evolution path:**
- **V1 (now):** Prompt → flat image via FLUX Pro API
- **V2:** Conversational AI Design Partner — back-and-forth refinement with Claude, generates multiple views
- **V3:** AI generates structured floor plan data (JSON: rooms, walls, dimensions) that feeds into the creation platform editor
- **V4:** "Build This" button opens the AI-generated design in the 3D editor / game

**Files:** `earthback_ai_visualizer_mockup.html`, `earthback_ai_visualizer_handoff.md`

---

### 2. Ghost Profiles — Businesses & Projects (Designed — Ready to Build)

**What it does:** Search-triggered auto-generation of profiles for businesses, projects, organizations, and practitioners not yet on Earthback. Community members can invite them to claim their profile.

**Key mechanics:**
- Search miss → system queries Google Places / web → creates ghost profile from public data
- Ghost profiles are publicly searchable with a "Not on Earthback yet" badge
- Community members can invite, vouch, and follow ghost profiles
- Claim flow: unique token link → preview → account creation → edit → publish when ready
- Social proof accumulates (search count, vouches, followers) creating conversion pressure
- Deduplication via fuzzy matching + LLM confirmation

**Files:** `earthback_ghost_profiles_mockup.html`, `earthback_ghost_profiles_handoff.md`

---

### 3. Content Creator Profiles (Designed — Ready to Build)

**What it does:** Same search-trigger-invite pattern, but for content creators. Ghost profile includes their imported content library (YouTube videos, podcast episodes, blog posts) organized by AI-generated categories, playable/readable inline.

**Supported sources (by integration ease):**
- **Tier 1 (trivial):** YouTube (Data API v3), Podcasts (RSS), Blogs/Substack (RSS), Vimeo (API)
- **Tier 2 (moderate):** GitHub (API), Instagram (Meta API), Eventbrite (API)
- **Tier 3 (scraping):** Google Scholar, personal websites, ResearchGate

**Key mechanics:**
- YouTube iframe embeds for video playback (legal, free, creator gets views)
- HTML5 audio player for podcast episodes (direct from RSS enclosure URLs)
- AI categorization of content via Claude Haiku (~$0.01-0.03 per library)
- Community notes on individual content items ("skip to 6:30 for the mix ratio")
- Content upvoting to surface best material
- Auto-sync for new uploads (YouTube WebSub + daily RSS polling)
- Creator controls visibility, sync settings, community note permissions

**Files:** `earthback_content_creator_mockup.html`, `earthback_content_creator_handoff.md`

---

### 4. Project Tracker with Material Calculator (Idea — Needs Design)

**What it does:** Transforms "project forming" posts into living project pages with phases, roles, material calculations, cost estimates, and timelines.

**Key mechanics:**
- Project phases: foundation → walls → roof → systems → finish (customizable)
- Members claim roles ("I'll handle the electrical"), mark phases complete
- Material calculator: input square footage + wall type + thickness → get quantities, costs, and supplier links
- Pulls pricing from business profiles on Earthback (supplier integration)
- Real-time cost estimator updates as the design changes
- Construction sequence generator (what to build first, dependencies)
- Completed projects become archived references for the community
- Bill of materials exportable as PDF/spreadsheet

**Monetization:**
- Free: basic calculator (how much hempcrete for X sq ft)
- Pro: full BOM generation with cost estimates and supplier connections
- B2B: suppliers pay for featured placement ("Desert Sun Hempcrete can deliver this for $X")

**Why it matters:** This is the bridge between "cool community" and "tool I can't work without." People will come back to Earthback every time they're planning a build because this is where the calculations live.

---

### 5. Skill Passport / Reputation System (Idea — Needs Design)

**What it does:** Formalizes project participation into verifiable skill credentials. Not gamified badges — professional reputation built from real work.

**Key mechanics:**
- Participate in a hempcrete pour → earn "Hempcrete Construction" credential
- Credentials are vouched by other participants ("Maria can confirm I was on this build")
- Skill levels emerge naturally: someone with 1 build is different from someone with 12
- Profile becomes a trades resume: "Participated in 3 hempcrete pours, 2 earthen floors, 1 living roof. Vouched by 8 community members."
- Ties into mentorship matching (see below)
- Ties into project formation (people search for skills when assembling a team)
- Importable: when a practitioner claims their ghost profile, they can import their history

**Why it matters:** LinkedIn completely fails at representing hands-on skills and trades work. This fills that gap for the natural building world. It also creates a trust layer that makes project collaboration safer — you can see what someone has actually done.

---

### 6. Resource & Tool Library (Geo-Located) (Idea — Needs Design)

**What it does:** Persistent, searchable, map-based inventory of shared resources — tools, equipment, materials, and available land.

**Key mechanics:**
- Members list items: concrete mixer, trailer, scaffolding, form systems, surplus lumber
- Each listing has: location, availability window, condition, delivery radius, cost (free/rental/fuel-only)
- Map view: "Show me all available tools within 100 miles of Santa Fe"
- List view with filters: category, distance, availability date, cost
- Trust layer: see the lister's profile, project history, vouches
- Booking/reservation system (Phase 2): request a tool, owner confirms, pickup arranged
- Transaction layer (Phase 3): Earthback takes a small cut on rentals

**Why it matters:** Right now these resources surface in the feed and disappear after a day. A persistent searchable layer makes them findable when you need them, not just when someone happens to post.

---

### 7. Mentorship Matching (Idea — Needs Design)

**What it does:** Connects experienced builders with newcomers based on skills, location, and availability.

**Key mechanics:**
- Experienced builders mark themselves as available for mentorship in their profile
- Their skill passport serves as credibility
- Newcomers browse mentors by skill, location, and availability
- Request system: "I'm planning my first earthen floor and I see you've done four. Could I ask some questions?"
- Lightweight — not a scheduling/payment platform, just the introduction
- The relationship happens organically through DMs, circle discussions, or in-person meetups
- Optional: mentors can link to their content library ("watch these 3 videos first, then let's talk")

**Why it matters:** The gap between "interested in natural building" and "actually doing it" is almost always bridged by a person. This makes finding that person trivial.

---

### 8. Local Building Code Navigator (Idea — Needs Design)

**What it does:** Searchable database of building code information for alternative construction, organized by jurisdiction (county/state/country).

**Key mechanics:**
- Enter your county → see what alternative materials are permitted, what requires variances, what's prohibited
- Community-contributed: members who've navigated the permit process share their experience
- "I got hempcrete approved in Coconino County — here's the engineer's report I used"
- Links to relevant code sections, successful permit applications, and recommended engineers
- Gradually enriched as more members contribute
- Doesn't need to be perfect at launch — imperfect community knowledge is still better than nothing

**Monetization:** Drives massive organic search traffic. "Can I build with hempcrete in [county]" is a question people google constantly. Every search result leads to Earthback → community discovery → sign up.

**Why it matters:** This is a utilitarian tool that becomes the reason people recommend Earthback. It's the kind of boring-but-essential feature that creates daily active usage.

---

### 9. Event & Workshop Board (Idea — Needs Design)

**What it does:** Dedicated calendar/board for in-person events — build days, workshops, skill shares, open houses, conferences.

**Key mechanics:**
- Searchable by location, date, topic, and circle
- Ties into creator profiles (workshop facilitators list their events)
- Ties into business profiles (suppliers hosting demos)
- Ties into skill passport (attend a workshop → learning credential)
- RSVP system with headcount tracking
- Post-event: photos, notes, and project updates link back to the event
- Recurring events support (monthly build days, weekly skill shares)

**Why it matters:** Makes the community feel real and grounded in physical space. Online platforms that never translate to in-person connection feel hollow over time.

---

### 10. AI Design Partner — Conversational Visualizer (Idea — Needs Design)

**What it does:** Evolution of the AI Visualizer into a full conversational design assistant. Not just prompt → image, but a back-and-forth dialogue that produces increasingly refined designs.

**Key mechanics:**
- User describes their situation: lot size, location, budget, family size, climate, goals
- AI asks clarifying questions about priorities, materials preference, water access, solar exposure
- AI generates not just an image but:
  - Preliminary floor plan (structured data)
  - Material suggestions with pros/cons for their climate
  - Rough cost estimate
  - Links to relevant creator content ("here's a video on the technique I'm suggesting")
  - Links to nearby suppliers (from business profiles)
- Iterative: "make the kitchen bigger," "add a rainwater system," "what if we used timber frame instead"
- Each iteration updates all outputs (plan, cost, materials, image)
- Final output is importable into the creation platform editor

**Monetization:** This is the premium tier feature. Free gets the basic visualizer. Pro ($9-15/mo) gets the conversational design partner. Could justify $20+/mo given the value.

**Why it matters:** This IS the bridge between "I have a dream" and "I have a plan." And it feeds directly into the creation platform and the game.

---

## The Creation Platform & Game Architecture

### The Vision

A browser-based building design tool where users create real, buildable structures using real materials with real physical properties. Designs created here can be:
- Exported as floor plans, BOMs, and construction sequences (for real-world building)
- Entered in 3D for walkthrough and refinement
- Dropped into the Rust game world for the post-apocalyptic experience
- Shared on Earthback profiles and in circles

### The Two Worlds

**Real-World Editor**
- Materials: hempcrete, rammed earth, cob, adobe, timber frame, straw bale, stone, recycled materials
- Every material has real properties: R-value, compressive strength, weight/ft³, cost/ft², carbon footprint
- Structural validation: walls glow green/yellow/red based on structural soundness
- Climate-responsive: set your GPS coordinates → editor adjusts recommendations based on real weather data
- Code-aware: ties into the building code navigator to flag potential permitting issues
- Exportable: floor plans (2D), 3D model, bill of materials, cost estimate, construction sequence

**Post-Apocalyptic World (Rust)**
- Same structural physics engine, different material palette
- Materials: scavenged metal, salvaged timber, reclaimed concrete, makeshift composites
- Aesthetic: survival-creative, improvised, weathered
- Looser constraints: no code compliance, no cost tracking, just structural physics + creativity
- Monthly wipe cycle with the "endurance" mechanic — well-designed, community-maintained structures persist
- Players learn building science through gameplay without realizing it
- Crossover: "This base design is actually structurally sound — want to build it for real?"

### Rust Integration Architecture

**Why Rust (the game) works:**
- Already a survival building game — the core mechanic is building structures
- Massive modding community via Oxide/uMod — custom plugins, custom items, custom building rules
- Proven server architecture your friends already know
- Monthly wipe is a natural game loop that Earthback can redefine
- Large existing player base who already enjoy building

**The Endurance Mechanic:**
Your friends' key innovation — structures that survive the monthly wipe. Possible approaches:
- **Blueprint persistence:** Before wipe, the server exports structure blueprints (position, materials, design). After wipe, players can "reconstruct" from the blueprint at reduced cost, like finding the plans in the rubble.
- **Community voting:** Before each wipe, the community votes on which structures are "landmark" quality and deserve persistence. Creates a social curation mechanic.
- **Material quality tiers:** Structures built with higher-quality materials (harder to obtain in-game) have a chance to survive the wipe. Incentivizes investment in better building.
- **Decay vs. maintenance:** Structures that are actively maintained (repaired, upgraded, visited) by their owners/community persist. Abandoned structures decay normally. Mirrors real-world building maintenance.

**Server-Side Mods Needed:**
- Custom building rules plugin: enforce Earthback's structural physics (minimum wall thicknesses, load-bearing requirements, foundation depths)
- Custom material system: map Rust's default materials to Earthback's material library (hempcrete, rammed earth, etc.) with appropriate properties
- Blueprint export: serialize structures to a portable format that can be imported into the web-based editor
- Blueprint import: allow structures designed in the web editor to be spawned/built in Rust
- Persistence plugin: handle the wipe-survival logic
- Earthback account integration: link Rust player identities to Earthback profiles so builds, skills, and reputation carry across

**Data Flow:**
```
Web Editor (browser) ←→ Earthback API ←→ Rust Server (mods)
      ↕                      ↕                    ↕
  AI Visualizer         User Profiles          Game World
  Floor Plans           Skill Passport         Structures
  Material Calcs        Content Library        Player Data
  Cost Estimates        Social Layer           Wipe Persistence
```

### Technology Stack for the Web Editor

**Phase 1: 2D Floor Plan Editor (MVP)**
- Browser-based, no install required
- Built with Canvas API or SVG (lightweight, fast)
- Grid-based: draw walls by clicking/dragging on a grid
- Material palette sidebar: select hempcrete, timber, etc.
- Real-time calculations panel: sq footage, material quantities, estimated cost
- Export: PNG floor plan, JSON data (for import into 3D/Rust), PDF with BOM
- This is achievable in 2-3 months with a focused developer

**Phase 2: 3D Viewer / Walkthrough**
- Three.js (browser-based 3D, no install)
- Import floor plan from 2D editor → auto-generate 3D walls, roof, openings
- First-person walkthrough mode
- Lighting simulation (see how sun hits the building at different times of day/year)
- Material textures that show what hempcrete, rammed earth, timber actually look like
- This is the "wow" moment that makes people share the platform

**Phase 3: Full 3D Editor**
- Three.js or Unity WebGL (if performance demands it)
- Place/modify elements directly in 3D
- Real-time structural feedback (green/yellow/red indicators)
- Terrain modeling: place your building on a slope, in a valley, on flat ground
- Site planning: solar panels, gardens, water systems, outbuildings
- Collaborative editing: multiple users working on the same design simultaneously

**Phase 4: Rust Bridge**
- Export from web editor → import into Rust server as a buildable blueprint
- Export from Rust → import into web editor for refinement and real-world planning
- Shared material language between web editor and Rust mod
- Skill passport events triggered by Rust gameplay (built a structure → credential)

### AI Integration in the Editor

**Floor Plan Generation (V3 Visualizer):**
- User describes project in natural language
- AI generates structured JSON floor plan: `{ rooms: [...], walls: [...], doors: [...], windows: [...] }`
- Editor consumes the JSON and renders it as an editable floor plan
- User tweaks manually, AI re-renders the visualization

**Real-Time Design Assistance:**
- As user builds, AI suggests improvements: "Adding a thermal mass wall on the north side would improve winter performance by 15%"
- Material recommendations based on climate, budget, and availability
- "A builder in your area (Carlos Rivera) has experience with this technique"

**Cost Estimation:**
- AI pulls material pricing from supplier profiles on Earthback
- Adjusts for location (shipping costs, local availability)
- Compares alternatives: "Hempcrete walls cost $X, straw bale would cost $Y and perform similarly in your climate"

---

## Monetization Summary

| Revenue Stream | Source | Timeline |
|---------------|--------|----------|
| AI Visualizer Pro | $9-15/mo subscription | Phase 1 |
| AI Design Partner | $15-20/mo subscription (or bundled with Pro) | Phase 2 |
| Creation Platform Pro | Premium editor features, unlimited exports | Phase 3 |
| Supplier Featured Placement | B2B — suppliers pay for visibility in material calculator | Phase 2 |
| Tool Library Transaction Fees | Small % on rental bookings | Phase 3 |
| Rust Game Access | Server access fee or cosmetic purchases | Phase 3-4 |
| Building Code Navigator Sponsorship | Engineering firms, code consultants sponsor entries | Phase 3 |
| Workshop Listings | Paid promoted events for businesses | Phase 2 |

---

## Prioritized Roadmap

### Now (in progress)
- Profile build page (main build thread)
- AI Visualizer mockup + handoff ready

### Next Wave (build after profiles)
1. AI Visualizer — ship MVP with FLUX API
2. Ghost profiles (businesses) — ship with profile system
3. Content creator profiles — YouTube import first
4. Material calculator — standalone tool, drives organic traffic

### Medium Term (3-6 months)
5. Project tracker — living project pages with phases, roles, materials
6. Skill passport — formalized credentials from project participation
7. Resource/tool library — map-based shared inventory
8. Mentorship matching — lightweight connection system
9. Event/workshop board — calendar with RSVP
10. Building code navigator — community-contributed, searchable by jurisdiction

### Long Term (6-12 months)
11. 2D floor plan editor — browser-based, material-aware
12. AI Design Partner — conversational visualizer → structured floor plans
13. AI floor plan generation — natural language → editable plans
14. Rust server mods — custom building rules, material system
15. Rust ↔ web editor bridge — export/import structures between platforms

### Future (12+ months)
16. 3D viewer/walkthrough — Three.js, first-person, lighting simulation
17. Full 3D editor — place/modify in 3D with real-time structural feedback
18. Rust endurance mechanic — wipe-persistent structures
19. Collaborative editing — multiple users, same design, real-time
20. Cross-platform skill passport — Rust gameplay → real-world credentials

---

## Technical Dependencies

| Component | Technology | Notes |
|-----------|-----------|-------|
| Community platform | Current stack (live) | earthbackproject.org |
| AI Visualizer | FLUX Pro via fal.ai | ~$0.05-0.10 per generation |
| AI Design Partner | Claude API (Sonnet/Haiku) | Conversational + structured output |
| Ghost profile enrichment | Google Places API + Claude Haiku | ~$0.02-0.05 per enrichment |
| YouTube import | YouTube Data API v3 | 10K free quota units/day |
| Podcast import | RSS parsing | No API key needed |
| Blog import | RSS parsing | No API key needed |
| AI categorization | Claude Haiku | ~$0.01-0.03 per library |
| 2D floor plan editor | Canvas API or SVG (browser) | Lightweight, no dependencies |
| 3D viewer | Three.js | Browser-based, no install |
| 3D editor | Three.js or Unity WebGL | Depends on performance needs |
| Rust servers | Oxide/uMod modding framework | Friends managing infrastructure |
| Rust mods | C# (Oxide plugin language) | Custom building rules, persistence |
| Payments | Stripe | Subscriptions + marketplace transactions |
| Transactional email | SendGrid / Resend / Postmark | Invitation emails, notifications |
| Maps | Google Maps or Mapbox | Tool library, business locations |

---

## Open Questions

1. **Rust mod scope:** How deep do the custom building rules go? Full structural physics, or just aesthetic/material reskinning with some rules layered on top?
2. **Editor-to-Rust fidelity:** Does a structure designed in the web editor look identical in Rust, or is it a "close approximation" given Rust's building system constraints?
3. **Real-world material database:** Who maintains the material properties and pricing data? Community-contributed? Supplier-maintained? Earthback team?
4. **Code navigator liability:** Providing building code information carries some liability risk. Needs a clear disclaimer that Earthback is not providing engineering or legal advice.
5. **Creator content rights:** When importing YouTube/podcast content, the embed approach is legally clean. But if Earthback adds community notes and upvotes to someone's content before they've claimed their profile, is there a courtesy/ethics question?
6. **Rust server costs:** Who pays for server infrastructure? Subscription model, community-funded, or absorbed by Earthback?
7. **Game monetization ethics:** The community ethos is "no extraction." How does game monetization align with that? Cosmetics-only? Access-fee-only? Free for Earthback Pro subscribers?

---

*This document covers everything discussed through February 2026. It should be updated as features are built, decisions are made, and the vision evolves.*
