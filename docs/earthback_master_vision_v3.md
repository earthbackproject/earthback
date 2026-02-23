# Earthback Platform — Master Vision Document v3

## The Strategy

Build the market before the printer ships. By the time the Earthback 3D hempcrete printer is ready, the platform already has thousands of designs waiting to be printed, a community trained on the principles, a material supply chain mapped and connected, real projects with land and funding that just need the machine, and a game where players have already been operating a virtual version of the printer for months.

The printer doesn't launch into a cold market. It drops into a fully warmed ecosystem as the missing piece everyone's been waiting for.

Every feature on the platform exists to make the printer's launch day feel like a starting gun, not a cold start.

---

## The Printer

### Current State
The printer is theoretical — in active design, not yet built. The core innovation is proven in concept but the physical machine, the ROS2 control system, and the AI integration that runs it are all ahead. The output file format is entirely undefined. The ROS2 and AI work will begin soon.

### What Makes It Different
This is not an incremental improvement on existing concrete 3D printers. It's a fundamentally different approach:

**Layer-free printing.** Existing construction printers deposit material in discrete horizontal layers, one on top of another. This creates the biggest structural weakness in 3D-printed construction: layer adhesion failure. The joint between layers is always weaker than the material itself. The Earthback printer eliminates this by depositing hempcrete without distinct layers — the result is a monolithic wall with no weak planes. This is a major structural advantage and one of the first things people will try to copy.

**Mid-build frame placement.** Existing printers print walls as continuous shells, then openings are cut after the fact (or the print path works around pre-defined voids). The Earthback printer can pause, accept a door or window frame placed by an operator or robotic arm, and continue printing around it — integrating the frame into the structure as it's built. This means:
- Frames are structurally bonded to the wall, not retrofitted
- No post-print cutting or framing
- The header/lintel above an opening is printed in place
- Faster overall build time

**Structural cavity printing.** The printer can create internal cavities within walls that are subsequently filled with concrete and rebar for full structural reinforcement. This means a hempcrete wall can serve as both insulation envelope AND structural element when the cavities are filled — eliminating the need for a separate structural frame. The wall is the structure. This is a significant departure from most hempcrete construction, where hempcrete is infill between a timber or steel frame.

**AI-controlled operation.** The printer runs on ROS2 (Robot Operating System 2) with an AI layer handling real-time decisions: material flow rate adjustment based on ambient conditions (temperature, humidity), print path optimization, cure monitoring, and adaptive response to variability in the hempcrete mix. The AI makes the printer robust enough for real-world jobsite conditions where nothing is perfectly controlled.

### What This Means for the Platform
The creation platform and game need to model these capabilities, not generic 3D printing:
- **No layer lines in visualization** — the design tool and game should show monolithic walls, not stacked layers
- **Frame placement as a design action** — in the editor, you place doors and windows and the system generates the print strategy around them (not a void to be cut later)
- **Cavity design** — the editor should let users define which wall sections have structural cavities and calculate concrete/rebar fill requirements
- **Print sequence visualization** — instead of a layer-by-layer time-lapse, show the continuous deposition path with frame insertion events and cavity formation

### On Being Copied
The design is simple enough that people will copy it quickly once they see it. The defense isn't the hardware — it's the ecosystem. Someone can copy the printer, but they can't copy:
- A community of thousands already designing for it
- A content library of training material
- A game where players already know how to operate it
- A supplier network mapped and connected
- A design library of print-ready files
- A skill passport of certified operators
- Relationships with tribal communities, housing authorities, and project partners

The platform IS the moat. The printer is the key that unlocks it, but the moat is everything around it.

---

## Platform Ecosystem

### Layer 1: Dream (AI Visualizer)

**Status:** Mockup and handoff document complete. Ready to build.

The entry point. Someone discovers 3D-printed hempcrete construction, sees a beautiful render of a home that was printed in days, and wants one.

**V1 (now):** Prompt → AI-generated image via FLUX Pro API. Free tier (3 renders), Pro tier ($9/mo unlimited). System prompt references the Earthback printing approach specifically: continuous hempcrete deposition (not layered), organic curved forms, natural material texture, monolithic walls, integrated window/door frames.

**V2:** Conversational AI Design Partner — Claude API back-and-forth that refines the vision into specifications: square footage, room count, climate, budget, site constraints. Outputs a specification document, not just a pretty picture.

**V3:** AI generates a structured design file (JSON: rooms, walls with cavity specifications, frame placements, dimensions) that can be opened in the creation platform editor. This is the bridge from dreaming to designing.

**V4:** "Print Preview" render style — shows the structure as the printer would build it: continuous deposition path visualization, frame insertion points, cavity locations, structural analysis overlay.

**Files:** `earthback_ai_visualizer_mockup.html`, `earthback_ai_visualizer_handoff.md`

---

### Layer 2: Design (Creation Platform)

**Status:** Architecture defined. Needs detailed design and build.

Where designs become real. The editor understands the Earthback printer's capabilities and constraints, enforces them in real time, and will eventually export print-ready files when the output format is defined.

**Phase 1 — 2D Floor Plan Editor (MVP):**
- Browser-based, no install (Canvas API or SVG)
- Draw walls by clicking/dragging on a grid
- Wall types: printed hempcrete (solid), printed hempcrete (with structural cavity), non-printed elements (timber roof, conventional foundation)
- Place doors and windows — editor shows how the printer will handle the frame integration
- Material calculator: hempcrete volume, concrete fill for cavities, rebar, frame materials
- Cost estimator (pulls from supplier profiles when available)
- Export: floor plan PDF, bill of materials, design data (JSON — format-agnostic, ready for whatever print file format emerges)
- Achievable in 2-3 months

**Phase 2 — 3D Viewer/Walkthrough:**
- Three.js (browser-based)
- Import floor plan from 2D editor → auto-generate 3D walls, roof, openings
- Walk through the design in first person
- Sun simulation (how light enters through windows at different times of day/year for your latitude)
- Material visualization (what hempcrete actually looks like — texture, color, organic feel)

**Phase 3 — Full 3D Editor:**
- Three.js or Unity WebGL
- Direct 3D manipulation with real-time feedback
- Print sequence visualization: watch how the printer would build the structure, including frame insertion events and cavity filling
- Structural analysis overlay (stress, load paths, reinforcement needs)
- Terrain/site modeling
- Service routing (electrical, plumbing cavities)
- Collaborative editing (multiple users, same design)

**Phase 4 — Print File Export:**
- When the output format is defined, add export pipeline
- Editor validates design against actual printer constraints
- Generates the control instructions the printer consumes
- Pre-print checklist: foundation ready, materials staged, frames prepared, weather check
- Until the format exists, the editor outputs format-agnostic design data (JSON) that can be converted later

**Design Library:**
- Community-shared designs, rated and reviewed
- Parametric templates: "2-bedroom desert home" that auto-adjusts for lot size and climate
- "Successfully printed" badge on designs that have been built in the real world
- Open designs (free) and premium designs (marketplace)

---

### Layer 3: Simulate (The Game)

**Status:** Rust server infrastructure being set up by team members. Mod development ahead.

Two game environments that teach the same principles through different experiences.

**Real-World Simulation (Web-Based):**
- Virtual Earthback printer on a virtual build site
- Load a design → watch/control the printer as it builds
- Learn operations: starting a print, monitoring material flow, placing frames at the right moment, managing cure conditions
- Problem scenarios: mix inconsistency, weather changes, equipment issues — how to diagnose and respond
- Completing virtual prints earns Printer Operator credentials in the skill passport
- This can be built as a simplified Three.js simulation before the full Rust integration

**Post-Apocalyptic Side (Rust):**

*Why Rust works:*
- Already a survival building game — core mechanic is construction
- Massive modding community via Oxide/uMod — custom plugins in C#
- Proven server architecture, team already experienced
- Monthly wipe is a natural game loop Earthback can redefine
- Large existing player base who enjoy building

*The in-game printer:*
- Rare, high-value piece of technology found/built/repaired in the game world
- Operates on the same principles as the real Earthback printer: continuous deposition, frame integration, structural cavities
- Players who control a printer have a massive advantage — printed structures are stronger, faster to build, and more resistant to raiding
- Materials are scavenged: salvaged hemp, improvised lime, experimental mixes
- Operating the printer requires skill — it's not just "click and wait," you manage material flow, placement, and timing
- The printer becomes a social magnet: clans form around printer access, players trade operator skills for resources

*The Endurance Mechanic:*
Structures that survive the monthly wipe. Approaches being explored:
- Blueprint persistence: server exports structure data before wipe, players reconstruct at reduced cost after
- Community voting: the community chooses which structures are "landmark" quality and deserve persistence
- Material quality tiers: better-built structures (properly reinforced, well-maintained) have higher survival chance
- Printed vs. hand-built: structures made with the in-game printer are inherently more durable and more likely to survive
- Maintenance requirement: actively maintained structures persist, abandoned ones decay — mirrors real-world building

*Rust Server Mods Needed:*
- Custom building rules: Earthback structural physics (wall thickness, load bearing, reinforcement)
- Custom material system: hempcrete, rammed earth, timber, salvaged materials with real properties
- In-game 3D printer entity: operational mechanics, material consumption, build animation
- Structure export: serialize structures to portable format for web editor import
- Structure import: spawn/build structures designed in the web editor
- Persistence plugin: wipe-survival logic
- Earthback account link: connect Rust player ID to Earthback profile for cross-platform reputation

*The Crossover:*
- Player builds a printed structure in Rust → "This design is buildable. Export to Earthback?" → design appears on their profile
- Designer creates a structure on the web → "Test this in Rust?" → structure spawns in the game world
- Skills earned in Rust contribute to the skill passport on the platform
- Suppliers, creators, and community members exist in both worlds

---

### Layer 4: Connect (Community Platform)

**Status:** Live at earthbackproject.org. Profile build is the next push.

The social layer that holds everything together.

**Existing:**
- Circles (Natural Building, Solar, Water, Permaculture, Mutual Aid, Housing, Skills, Land, Dwellings, Materials)
- Feed (circle-curated, no algorithm)
- Profiles (in development)
- Basic post types (project forming, technique share, resource available, project complete)

**Adding:**
- 🖨️ **3D Printing circle** — printer operators, designers, material researchers, project teams
- **Printer Operator** profile subtype — certified operators available for hire
- **Print Designer** profile subtype — people who create printable designs
- **Print Service Provider** profile subtype — businesses that own a printer and offer construction services
- **Print Project** post type — includes design file, printer assignment, operator, materials, timeline
- **Material Supplier** profile subtype — hempcrete mix suppliers, hemp farmers, lime producers (via ghost profiles)

**Ghost profiles** (businesses, creators, practitioners) are the onboarding engine:
- Search → auto-generate profile from public data → community invites them → they claim and join
- By the time the printer launches, the supplier network, operator pool, and designer community are already populated

**Files:** `earthback_ghost_profiles_mockup.html`, `earthback_ghost_profiles_handoff.md`, `earthback_content_creator_mockup.html`, `earthback_content_creator_handoff.md`

---

### Layer 5: Supply (Material & Supplier Network)

**Status:** Designed as part of ghost profiles. Needs printer-specific expansion.

The supply chain for the printer, built on the ghost profile infrastructure.

**Supplier types:**
- Hemp farmers (raw hemp hurd/shiv)
- Lime producers (hydraulic lime, hydrated lime)
- Pre-mixed hempcrete suppliers (ready-to-print mixes — when mix specs are defined)
- Concrete suppliers (for cavity fill)
- Rebar/reinforcement suppliers
- Frame manufacturers (doors, windows sized for printer integration)

**Printer network (future):**
- Map of all active Earthback printers
- Availability calendar and booking system
- Operator matching: find a certified operator near your build site
- Service radius, pricing, track record

**Material calculator (printer-aware):**
- Input: design file or floor plan dimensions + wall types
- Output: hempcrete volume, cavity concrete volume, rebar quantity, frame count, total material cost
- Supplier connections: "Nearest hempcrete supplier: Desert Sun, Flagstaff AZ, 85 miles, $X/yd³"
- Delivery logistics and lead time estimates

---

### Layer 6: Learn (Content Library + Training)

**Status:** Content creator profiles designed. Training path needs development.

The knowledge base and training pipeline.

**Content Library** (from creator profiles):
- YouTube, podcast, and blog content auto-imported and AI-categorized
- Community notes and upvoting surface the best material
- Printer-relevant content tagged and organized into training sequences

**Training Path for Printer Operators:**
1. **Watch** — curated content on hempcrete science, 3D printing principles, structural engineering basics
2. **Read** — guides on site prep, foundation requirements, mix design, curing conditions, finishing techniques
3. **Design** — complete beginner projects in the 2D editor with AI assistance
4. **Simulate** — complete virtual prints in the web-based simulation (and/or Rust)
5. **Attend** — in-person workshop with a real printer (event board listings)
6. **Certify** — skill passport shows completed path: content consumed, designs created, virtual prints completed, workshop attendance, community vouches

**Skill Passport credentials:**
- Virtual Print Operator (completed simulations)
- Certified Printer Operator (real-world training)
- Print Designer (published designs, bonus for designs that get printed)
- Material Specialist (mix design expertise)
- Site Prep Specialist (foundation and terrain preparation)
- Build phases from project participation (hempcrete pours, finishing, systems installation)

---

### Layer 7: Comply (Building Code Navigator)

**Status:** Idea stage. Needs design.

Searchable database of building code information for alternative construction, with specific focus on 3D-printed hempcrete.

**Key content:**
- Which jurisdictions allow hempcrete construction?
- Which jurisdictions have approved 3D-printed structures?
- What engineering certifications are required?
- Successful permit applications shared by community members
- Recommended structural engineers experienced with alternative construction
- Code change tracking: when a jurisdiction updates its rules, the community knows

**Drives organic search traffic:** "Can I 3D print a hempcrete home in [county]?" is a question that will be googled increasingly often. Every result leads to Earthback.

**Disclaimer needed:** Earthback provides community-contributed information, not engineering or legal advice. Always consult a licensed professional.

---

### Layer 8: Share (Resource & Tool Library)

**Status:** Idea stage. Needs design.

Persistent, searchable, geo-located inventory of shared resources.

- Tools and equipment (concrete mixers, trailers, scaffolding, generators)
- Materials (surplus lumber, reclaimed materials, bulk hemp)
- Land (available build sites, community land trusts)
- Printers (the highest-value shared resource — when they exist)
- Map view with radius search
- Availability calendars and booking
- Trust layer: see the lister's profile, project history, vouches

---

### Layer 9: Match (Mentorship)

**Status:** Idea stage. Needs design.

Connecting experienced builders with newcomers.

- Experienced builders mark themselves as available
- Skill passport as credibility
- Browse by skill, location, availability
- Lightweight request system: "I'm planning my first build and I see you've done four. Can I ask questions?"
- Not a scheduling/payment platform — just the introduction
- Optional link to content library: "Watch these 3 videos first, then let's talk"

---

### Layer 10: Gather (Events & Workshops)

**Status:** Idea stage. Needs design.

Dedicated calendar for in-person events.

- Build days, workshops, skill shares, open houses, printer demos, conferences
- Searchable by location, date, topic, circle
- RSVP with headcount
- Ties into skill passport (attendance → credential)
- Ties into creator profiles (facilitators list events)
- Post-event documentation linked back

---

## Revenue Model

The printer is the anchor. Everything else drives printer adoption or generates recurring revenue from the ecosystem.

| Stream | Description | Phase |
|--------|-------------|-------|
| **Printer Sales/Leasing** | The hardware | Launch |
| **Platform Pro** | $9-20/mo — unlimited AI, editor features, print export | 1 |
| **AI Design Partner** | Premium conversational design (bundled or $15-20/mo) | 2 |
| **Operator Certification** | Training program fees | 2 |
| **Print File Marketplace** | Community designs, free and paid | 2 |
| **Supplier Placement** | B2B — featured in material calculator | 2 |
| **Material Marketplace** | Transaction fee on supplier connections | 2-3 |
| **Print Service Booking** | Fee on printer rentals/bookings | 3 |
| **Game Access** | Rust server access, cosmetics, printer blueprints | 3 |
| **Enterprise** | Large-scale projects: tribal housing, disaster response, community development | 3+ |

---

## Roadmap

### Now
- Profile build page (main build thread)
- AI Visualizer V1 (with print-aware system prompt — no layers, monolithic walls, organic forms)
- Ghost profiles for businesses (including supplier and printer-related types)
- Content creator profiles (YouTube first, then podcast/blog)

### Next (3-6 months)
- Material calculator (printer-aware: hempcrete volume, cavity concrete, rebar, supplier links)
- 2D floor plan editor MVP (wall types: solid printed, cavity printed, non-printed; frame placement; basic structural feedback)
- AI Design Partner V2 (conversational, outputs structured design data)
- Skill passport (including future printer operator track — can start with general building skills)
- Project tracker with "Print Project" template

### Medium (6-12 months)
- 3D viewer/walkthrough (Three.js)
- Web-based print simulation (virtual printer operation training)
- Design library (community sharing/remixing)
- Rust server mods begin (custom building rules, material system)
- Supplier network / material marketplace foundations
- Event/workshop board
- Building code navigator (community-contributed)
- Resource/tool library
- Mentorship matching

### Long (12-18 months)
- Full 3D editor with structural analysis
- Print sequence visualization (continuous deposition path, frame events, cavity formation)
- Rust in-game printer entity and operational mechanics
- Rust ↔ web editor bridge
- Endurance mechanic (wipe persistence)
- Operator certification program launch

### Printer Launch Alignment
- Print file format defined → editor export pipeline built
- ROS2/AI control system developed → simulator updated to match real printer behavior
- First physical prints → "Successfully Printed" badges on designs, real-world documentation feeds content library
- Commercial availability → platform is the storefront, support system, and ecosystem

### Future (18+ months)
- Print service marketplace
- Parametric design library (auto-adjusting templates by climate/lot/budget)
- Printer IoT integration (real-time monitoring on project page)
- Enterprise tools (housing authorities, tribal communities, disaster response)
- International expansion (climate libraries, local suppliers, translated content)
- Collaborative real-time editing
- Full game crossover (Rust designs → real prints, real designs → Rust world)

---

## Open Questions

1. **ROS2 architecture:** What's the planned control hierarchy? (AI decision layer → ROS2 motion planning → printer hardware?) This affects how the simulator models printer behavior.
2. **Mix specifications:** What hempcrete mix does the printer require? (Fiber length, binder ratio, moisture content, additives?) This defines the material calculator and supplier specs.
3. **Printer dimensions:** What's the build envelope? (Max wall height per pass, max print area, nozzle reach?) This constrains the design editor.
4. **Frame integration mechanics:** How exactly does the printer handle frame placement? (Full stop → manual insertion → resume? Robotic frame handler? Pre-positioned frames the printer detects?) This affects both the editor design flow and the game simulation.
5. **Cavity specifications:** What cavity dimensions support structural concrete fill? (Min/max width, rebar placement rules, pour timing relative to print timing?) This is a key editor constraint.
6. **IP protection strategy:** Patent the printer design? The print method? The AI control system? Open-source the platform but protect the hardware?
7. **First target project:** What's the first real-world print? (Proof of concept demo? A specific community's housing project? A partnership with a tribe?) This drives the marketing narrative.
8. **Timeline alignment:** Rough estimate — when does the team expect to have a working prototype? First print? Commercial unit? The platform roadmap should sync.

---

## The Moat

Someone will copy the printer. The design is elegant and simple enough that once people see it work, competitors will emerge. The defense is not the hardware. The defense is:

- Thousands of users already designing for it
- A content library of training material people have been learning from for months
- A game where players already know how to operate it
- A supplier network mapped and ready to deliver
- A design library of tested, community-rated print files
- A skill passport of certified operators
- Active projects with land, funding, and teams just waiting for the machine
- Relationships with tribal communities, housing authorities, and partners built over time
- A brand that means "the future of sustainable construction" to a growing community

The printer is the key. The platform is the lock, the door, the house, and the neighborhood.

*Master document v3 — February 2026. Living document. Update as printer development, platform build, and game development progress.*
