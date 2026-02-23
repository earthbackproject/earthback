# Earthback Platform — Master Vision Document v4

## The Strategy

Earthback is the design, simulation, and community platform for construction 3D printing — all of it, not just one printer. Users design structures for whatever printer they have access to today: ICON Vulcan, COBOD BOD2/BOD3, WASP Crane, MudBots, Apis Cor, or any new entrant. The platform is printer-agnostic. Every manufacturer's machine is supported, profiled, and integrated.

Then, when the Earthback printer arrives — with layer-free deposition, mid-build frame placement, and structural cavity printing — it enters an ecosystem where thousands of users are already designing, a community is already trained, suppliers are already connected, and projects are already funded and waiting. It doesn't need to compete for attention. It just needs to be better. And it will be.

**Phase 1:** Be the platform for all construction 3D printing. Grow the community, the design library, the supplier network, and the game.

**Phase 2:** Launch the Earthback printer into a market you already own.

Every feature serves both phases. Nothing built for Phase 1 is wasted in Phase 2 — it just gets better when the Earthback printer arrives.

---

## The Construction 3D Printing Landscape

The platform should acknowledge and support these printers. Each has different specifications, constraints, and capabilities that the design editor needs to understand.

### Current Market

**COBOD BOD2 / BOD3 / BODXL** (Denmark)
- Type: Gantry system, modular steel truss
- Material: Concrete (open-source material approach)
- Build volume: BOD2 up to ~15m × 50m × 8m; BODXL up to 50m × 30m × 12m
- Speed: Up to 1,000 mm/s (BOD2)
- Layer method: Traditional layer-by-layer deposition
- Notable: World's best-selling construction printer, 85+ units deployed worldwide, used for residential, commercial, wind turbine towers, data centers
- Crew: 2-3 operators
- Status: Market leader, BOD3 launching with ground-based track system for sequential multi-building printing

**ICON Vulcan III** (Austin, TX)
- Type: Gantry system
- Material: Lavacrete (proprietary concrete blend)
- Build volume: ~12m × 3m × 8m
- Layer method: Layer-by-layer
- Notable: First permitted 3D-printed homes in the US (Community First! Village, Austin), NASA collaboration for lunar construction, Wolf Ranch community in Georgetown TX
- Pricing: System + materials + software integrated package, request-only pricing
- Status: Leading US manufacturer, focused on affordable housing

**WASP Crane WASP** (Italy)
- Type: Robotic arm on frame (not gantry)
- Material: Earth-based materials (clay, natural fibers), concrete
- Build volume: Single arm ~6.3m diameter × 3m height; multiple arms network for unlimited area
- Layer method: Layer-by-layer
- Notable: Pioneers in earth-based 3D printing (closest to hempcrete in the current market), TECLA habitat project using local raw earth
- Price: Starting ~€132,000 ($145,000)
- Status: Most relevant to the natural building community — uses earth, not just concrete

**MudBots** (USA)
- Type: Gantry system, smaller footprint
- Material: Standard concrete mixes
- Build volume: Up to ~22m × 15m
- Price: $35,000 - $60,000
- Notable: Most affordable entry point, plug-and-play operation, designed for accessibility
- Status: Good option for community groups and smaller projects

**Apis Cor** (Russia/USA)
- Type: Robotic arm (compact, mobile)
- Material: Concrete
- Notable: Printed a house in 24 hours, compact enough to transport on a truck
- Status: Focus on speed and mobility

**PERI 3D Construction** (Germany)
- Uses COBOD printers, focused on residential projects
- Notable: DREIHAUS project in Heidelberg — Germany's first serial 3D-printed housing, 30% faster and 10% more cost-effective than conventional, walls printed at 1 sq meter per 5 minutes

**Emerging / Notable:**
- Winsun (China) — multi-story buildings, villas
- MX3D (Netherlands) — metal 3D printing, famous for Amsterdam bridge
- Twente Additive Manufacturing (Netherlands) — concrete printing research
- Various university and research programs worldwide

### Where the Earthback Printer Fits (Future)

Every printer listed above shares the same fundamental limitation: **layer-by-layer deposition.** Each layer is a discrete horizontal band of material. The interface between layers is always structurally weaker than the material itself. This is the known weakness of all current construction 3D printing.

The Earthback printer, when it arrives, will be different in three fundamental ways:

**Layer-free continuous deposition.** No discrete layers. The result is a monolithic wall with no weak horizontal planes. This is a structural advantage that no current printer offers.

**Mid-build frame integration.** The printer accepts door and window frames during the print process, building around them. Frames are structurally bonded to the wall, not retrofitted. No post-print cutting or separate framing needed.

**Structural cavity printing.** Internal wall cavities that get filled with concrete and rebar for full structural reinforcement. The hempcrete wall is both insulation envelope and structural element. No separate frame required.

**AI-controlled via ROS2.** Real-time adaptive operation: material flow adjustment for ambient conditions, path optimization, cure monitoring. Makes the printer robust for real-world jobsite variability.

**Status:** Theoretical — in active design. ROS2 and AI integration coming soon. Output file format undefined. The design is simple enough that it will be copied once demonstrated, which is why the platform (the moat) needs to be established first.

---

## Platform Ecosystem

### Layer 1: Dream (AI Visualizer)

**Status:** Mockup and handoff complete. Ready to build.

Entry point. Visitors describe a project, get an AI-rendered visualization of what 3D-printed construction looks like.

- V1: Prompt → image (FLUX Pro API). Free tier (3 renders) / Pro tier ($9/mo).
- V2: Conversational AI Design Partner (Claude API). Back-and-forth refinement into specifications.
- V3: AI generates structured design data (JSON) consumable by the creation platform editor.
- V4: "Print Preview" mode — visualize how a specific printer would build the structure.

System prompt should reference 3D-printed construction broadly: printed concrete and hempcrete walls, organic forms achievable through additive manufacturing, natural material textures, real structural elements. Not just one printer's aesthetic.

**Files:** `earthback_ai_visualizer_mockup.html`, `earthback_ai_visualizer_handoff.md`

---

### Layer 2: Design (Creation Platform)

**Status:** Architecture defined. Needs build.

The design tool where structures are created, validated against printer constraints, and exported.

**Printer Profiles:** The editor maintains a library of supported printers, each with its own constraint set:
- Build volume (max dimensions)
- Minimum/maximum wall thickness
- Layer height (for layer-based printers) or deposition parameters (for continuous printers)
- Material compatibility (concrete, hempcrete, earth, etc.)
- Maximum overhang angle
- Print speed range
- Nozzle diameter
- Special capabilities (frame integration, cavity printing, multi-material, etc.)

When designing, the user selects their target printer (or "generic / no specific printer" for general designs). The editor enforces that printer's constraints and provides real-time feedback.

**Phase 1 — 2D Floor Plan Editor (MVP):**
- Browser-based (Canvas API or SVG)
- Draw walls, place doors/windows on a grid
- Select target printer from profile library → constraints adjust automatically
- Material selection: concrete, hempcrete, earth (depending on printer compatibility)
- Wall types: solid, insulated, structural cavity (where supported)
- Real-time calculations: print time estimate, material volume, cost estimate
- Export: floor plan PDF, bill of materials, design data (JSON)
- Print file export: deferred until formats are defined, but the design data captures everything needed

**Phase 2 — 3D Viewer:** Three.js walkthrough, sun simulation, material textures.

**Phase 3 — Full 3D Editor:** Direct 3D manipulation, structural analysis, print sequence visualization (layer-by-layer for traditional printers, continuous path for Earthback printer), service routing, terrain modeling.

**Phase 4 — Print File Export:** When printer-specific output formats are defined (G-code variants, proprietary formats, or the eventual Earthback format), the editor adds export pipelines per printer profile.

**Design Library:**
- Community-shared designs, tagged by compatible printers
- "Printed and verified" badge for designs that have been built in the real world
- Parametric templates that auto-adjust for lot, climate, and selected printer
- Open (free) and premium (marketplace) designs

---

### Layer 3: Simulate (The Game)

**Status:** Rust server infrastructure being set up.

Two environments teaching the same principles.

**Real-World Simulation (Web-Based):**
- Virtual 3D printer on a virtual build site
- Select a printer model → simulation matches its behavior
- Learn operations: starting a print, monitoring progress, handling issues
- Problem scenarios: weather, mix inconsistency, equipment trouble
- Earn Printer Operator credentials in skill passport
- Can be built as a simplified Three.js application before full Rust integration

**Post-Apocalyptic Side (Rust):**
- 3D printers are rare, high-value in-game technology
- Finding/building/repairing a printer is a major gameplay milestone
- In-game printers operate on real construction principles (structural physics, material properties)
- Printed structures are stronger than hand-built ones → gameplay advantage
- The printer is a social magnet: clans form around printer access
- When the Earthback printer design is finalized, it can be added as the top-tier in-game printer — the one everyone wants

**The Endurance Mechanic:**
- Structures that survive monthly wipes
- Printed structures inherently more durable (higher survival chance)
- Community voting on landmark structures
- Active maintenance required for persistence
- Mirrors real-world building maintenance principles

**Rust Server Mods:**
- Custom building rules (structural physics)
- Custom material system (hempcrete, concrete, earth, salvaged materials)
- In-game 3D printer entity (with real operational mechanics)
- Structure export/import (↔ web editor)
- Earthback account integration (cross-platform reputation)
- Persistence plugin (wipe-survival logic)

**The Crossover:**
- Rust design → export to Earthback profile → real-world-ready blueprint
- Web design → import to Rust → test in the game world
- Game skills → skill passport credentials → real-world reputation

---

### Layer 4: Connect (Community Platform)

**Status:** Live at earthbackproject.org. Profile build next.

**Existing:** Circles, feed, profiles, post types (project forming, technique share, resource available, project complete).

**Adding:**
- 🖨️ **3D Printing circle** — all printers, all manufacturers, operators, designers, researchers
- **Printer profiles** — each printer manufacturer/model gets a profile page (ghost profile pattern!) with specs, capabilities, known operators, completed projects, compatible designs
- **Printer Owner** profile subtype — lists their printer model, availability, service radius
- **Printer Operator** profile subtype — certified operators, which printers they can run
- **Print Designer** profile subtype — designers, which printers they design for
- **Print Service Provider** — businesses offering printing services
- **Print Project** post type — design file, printer, operator, materials, timeline, status

**Ghost profiles extend to printer manufacturers and dealers:** Search for "COBOD dealer near me" → ghost profile auto-generated → community can invite them → they claim and join.

**Files:** `earthback_ghost_profiles_mockup.html`, `earthback_ghost_profiles_handoff.md`, `earthback_content_creator_mockup.html`, `earthback_content_creator_handoff.md`

---

### Layer 5: Supply (Material & Supplier Network)

**Status:** Designed as ghost profiles. Needs printer-specific expansion.

Supplier types:
- **Concrete suppliers** (for concrete-printing machines)
- **Hemp farmers** (hemp hurd/shiv for hempcrete)
- **Lime producers** (for hempcrete binder)
- **Pre-mixed suppliers** (ready-to-print mixes, when specs exist)
- **Rebar/reinforcement suppliers**
- **Frame manufacturers** (doors, windows)
- **Printer dealers/resellers** (ghost profiles for each manufacturer's sales network)
- **Parts and maintenance** (nozzles, pumps, hoses, control systems)

**Printer network map:**
- All known construction 3D printers, searchable by location
- Availability and booking
- Operator matching
- Service radius and pricing

**Material calculator (printer-aware):**
- Select your printer → calculator adjusts for that printer's material type and consumption rate
- Hempcrete volume, concrete volume, reinforcement, frames
- Links to nearby compatible suppliers

---

### Layer 6: Learn (Content Library + Training)

**Status:** Content creator profiles designed.

Content library with YouTube, podcast, blog imports, AI-categorized, community-annotated. Training paths for:
- General construction 3D printing principles
- Specific printer operation (COBOD, ICON, WASP, etc.)
- Design for 3D printing (editor tutorials)
- Material science (concrete mixes, hempcrete, earth-based materials)
- Site preparation and finishing
- Business/permitting (how to start a 3D print construction business)

Skill passport credentials:
- Virtual Print Operator (simulations completed, by printer model)
- Certified Printer Operator (real-world training, by printer model)
- Print Designer (published designs, by compatible printers)
- Material Specialist (mix design expertise)
- Site Prep Specialist
- Project participation badges

---

### Layer 7: Comply (Building Code Navigator)

Community-contributed, searchable database of building code info for 3D-printed and alternative construction by jurisdiction. Which counties/states/countries have approved 3D-printed structures? What certifications are needed? Successful permit applications shared. Drives organic search traffic.

---

### Layer 8: Share (Resource & Tool Library)

Geo-located, searchable inventory of shared resources: tools, equipment, materials, land, and printers. Map view, availability calendars, booking system.

---

### Layer 9: Match (Mentorship)

Connect experienced builders/operators with newcomers. Skill passport as credibility. Lightweight intro system, not a scheduling platform.

---

### Layer 10: Gather (Events & Workshops)

Dedicated calendar for build days, workshops, printer demos, conferences. Searchable, RSVP, skill passport integration.

---

## Revenue Model

| Stream | Description | Phase |
|--------|-------------|-------|
| **Platform Pro** | $9-20/mo — unlimited AI, editor features, design exports | 1 |
| **AI Design Partner** | Premium conversational design (bundled or standalone) | 2 |
| **Design Marketplace** | Community designs, free and paid, tagged by compatible printer | 2 |
| **Supplier Placement** | B2B — featured in material calculator and search | 2 |
| **Operator Certification** | Training program fees, by printer model | 2 |
| **Material Marketplace** | Transaction fee on supplier connections | 2-3 |
| **Printer Listing Fees** | Manufacturers/dealers pay for featured profiles | 2 |
| **Print Service Booking** | Fee on printer rentals/bookings | 3 |
| **Game Access** | Rust server access, cosmetics, printer blueprints | 3 |
| **Earthback Printer Sales** | The hardware, when ready | Future |
| **Enterprise** | Large-scale projects: housing authorities, tribal communities, disaster response | 3+ |

The platform generates revenue before the Earthback printer exists. The printer adds a major revenue line when it arrives, but the platform is a standalone business either way.

---

## Roadmap

### Now
- Profile build page
- AI Visualizer V1 (construction 3D printing-aware system prompt)
- Ghost profiles (businesses, suppliers, printer dealers)
- Content creator profiles (YouTube first)

### Next (3-6 months)
- Material calculator (printer-aware, supports multiple printer models)
- 2D floor plan editor MVP (select target printer → constraints adjust)
- Printer profile pages (specs, capabilities, compatible designs, known operators)
- AI Design Partner V2 (conversational, structured output)
- Skill passport foundations
- Project tracker with Print Project template

### Medium (6-12 months)
- 3D viewer/walkthrough
- Web-based print simulation (select printer model → virtual operation)
- Design library (community sharing, tagged by compatible printers)
- Rust server mods (building rules, material system, in-game printers)
- Supplier network / material marketplace
- Event/workshop board
- Building code navigator
- Resource/tool library
- Mentorship matching

### Long (12-18 months)
- Full 3D editor with structural analysis
- Print sequence visualization (per-printer behavior)
- Rust in-game printer mechanics
- Rust ↔ web editor bridge
- Endurance mechanic
- Operator certification program (by printer model)

### Earthback Printer Integration (timeline TBD)
- Add Earthback printer to printer profile library
- Update editor with Earthback-specific capabilities (layer-free, frame integration, cavity printing)
- Update game with Earthback printer as top-tier technology
- Define and implement print file export format
- ROS2/AI integration with platform (real-time monitoring, adaptive control)
- Launch printer into a market that's already using the platform daily

### Future
- Print service marketplace
- Parametric design library
- Printer IoT integration
- Enterprise tools
- International expansion
- Collaborative real-time editing
- Full game crossover

---

## The Moat

The platform is the moat — for the Earthback printer and for the platform as a business in its own right.

Someone can copy the Earthback printer design. They cannot copy:
- Thousands of users already designing on the platform
- A design library of tested, community-rated, printer-compatible files
- A content library people have been learning from for months
- A game where players already know construction 3D printing principles
- A supplier network mapped and connected
- A skill passport of certified operators
- Active projects with land, funding, and teams
- Relationships with communities, housing authorities, and partners
- A brand that means "the future of sustainable construction"

And by being printer-agnostic from day one, the platform has users who own COBOD, ICON, WASP, and MudBots machines — all of whom become potential Earthback printer customers when it launches. You're not asking them to switch platforms. You're asking them to try a better printer on the platform they already use.

---

## Open Questions

1. **Printer profile data:** Who maintains the specs for each printer model? Community-contributed? Manufacturer-verified? Both?
2. **Printer manufacturer relationships:** Should Earthback pursue partnerships with COBOD, ICON, WASP, etc.? They could see the platform as a sales channel, or as a threat. Probably best positioned as a neutral design platform that benefits everyone.
3. **ROS2 architecture:** What's the planned control hierarchy for the Earthback printer? Affects the simulation and eventual IoT integration.
4. **Mix specifications:** What hempcrete mix does the Earthback printer require? Defines material calculator and supplier specs.
5. **Earthback printer constraints:** Build envelope, deposition parameters, frame integration mechanics, cavity specs — needed for the editor profile.
6. **IP strategy:** Patent the Earthback printer innovations? Open-source the platform? Both?
7. **First target project:** What's the first real-world demonstration of the Earthback printer?
8. **Timeline:** Rough estimate for working prototype → first print → commercial availability?
9. **Printer file formats:** Do COBOD, ICON, etc. publish their input file formats? If so, the editor could export directly to existing printers immediately, which would be a huge value proposition.
10. **Game IP:** Does using real printer brand names in the Rust game require licensing? May need fictional analogs for some manufacturers.

---

*Master document v4 — February 2026. Living document. Printer-agnostic platform with Earthback printer as the future endgame.*
