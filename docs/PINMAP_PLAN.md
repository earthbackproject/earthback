# Earthback Pin Map — Feature Plan
*Written: 2026-02-24 | Status: Planning*

---

## What It Is

A geographic map — eventually its own `/map` page and embedded in Explore — that shows where Earthback activity is happening in the world. Three audiences for this map:

1. **Prospective members** — "This is real. Here's where people are working."
2. **Existing members** — "Find collaborators near me, see what's happening."
3. **Communities in need** — "We can get you from dirt to functional in a year. Here's the proof."

The Ukraine use case makes this concrete: you have friends there who want to rebuild using natural building. The map becomes a campaign tool — not just a directory but a declaration of capacity and intent. *We go here. We've done it here. This is what's possible.*

This is not a surveillance tool. It's a **community presence map** — more "we're here" than "here's exactly where I live."

---

## What Goes On the Map

Five pin types, visually distinct:

**Members** — people who've opted in and set a location
- Shown at city or region level (not street address)
- Pin: small avatar circle or dot in Earthback green
- Click → profile card popup with name, one-liner, primary circle, "View Profile" link

**Projects** — public projects with a latitude/longitude set
- Already have `latitude` + `longitude` in the `projects` table
- Pin: square or diamond marker, terracotta/clay color
- Click → project card popup with name, type (build/org/campaign), circle tag, "View Project" link

**Circles** — where there's a concentration of circle members in a region
- Not per-user pins — aggregated: "7 hempcrete members in this region"
- Shown as a soft cluster badge over a geographic area
- Click → link to the relevant circle page

**Curated Hotspots** — editorial pins placed by the Earthback team, not tied to any user account
- These populate the map before there's enough member density to be visually interesting
- Multiple categories, each with its own color (see Hotspot System section below)
- Managed directly in the database or via a simple admin form

---

## Curated Hotspot System

This is what makes the map useful on day one and what tells the story to new visitors.

### Why hotspots matter
When a community platform launches with no users, the map is empty and that emptiness is a message. Hotspots let the Earthback team seed the map with real, meaningful information before the community fills it in — and then the community data grows around and through that foundation.

For the Ukraine situation specifically: you can pin communities that want to rebuild, active partners on the ground, material suppliers in adjacent countries, and completed builds as proof points. That map tells a story no feed can tell.

### Hotspot categories and colors

| Category | Color | Use |
|----------|-------|-----|
| **Rebuilding** | Amber `#E8A838` | Communities actively rebuilding from conflict, disaster, or neglect — Ukraine, flood zones, fire zones |
| **Resource Hub** | Teal `#2D8A7A` | Material suppliers, tool libraries, training centers, certified builders available in area |
| **Active Build** | Clay `#C26B42` | Team-curated build sites — partner projects, demonstration builds, case studies |
| **Partner Org** | Blue `#4A6FA5` | NGOs, universities, co-ops, governments partnering with Earthback |
| **Opportunity** | Forest `#1F3A2E` | Communities that have expressed need/interest but build hasn't started yet — "We want this here" |

Colors are distinct enough to be legible at a glance without a legend, but a legend is still included.

### Hotspot popup card

```
[ 🔶 REBUILDING ]  Kherson Oblast, Ukraine
─────────────────────────────────────────────
Community of ~800 households. Seeking hempcrete
and strawbale builders. 3 partner orgs active.
Timeline: Spring 2026 start.

[ Contact Partner ]  [ Join This Effort ]
```

The "Join This Effort" button could trigger a circle join, a message to the coordinating org, or just an email to Earthback — whatever makes sense for the situation.

### Hotspot data model

New table — `map_hotspots`. Entirely admin-managed (no user submission for now).

```sql
CREATE TABLE public.map_hotspots (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Location
  latitude      DOUBLE PRECISION NOT NULL,
  longitude     DOUBLE PRECISION NOT NULL,
  location_name TEXT NOT NULL,              -- "Kherson Oblast, Ukraine"

  -- Content
  category      TEXT NOT NULL
    CHECK (category IN ('rebuilding','resource','build','partner','opportunity')),
  title         TEXT NOT NULL,
  description   TEXT,                       -- 1-3 sentence summary
  status        TEXT DEFAULT 'active'
    CHECK (status IN ('active','planned','complete','paused')),

  -- Links
  url           TEXT,                       -- partner site, project page, etc.
  contact_email TEXT,                       -- who to reach about this location
  circle_slug   TEXT,                       -- associated Earthback circle if any

  -- Display
  is_visible    BOOLEAN DEFAULT true,       -- toggle without deleting
  priority      INTEGER DEFAULT 0,          -- higher = shown at lower zoom levels

  -- Meta
  created_by    UUID REFERENCES profiles(id),
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Public read — these are intentionally public story points
ALTER TABLE public.map_hotspots ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Hotspots are publicly readable"
  ON public.map_hotspots FOR SELECT USING (is_visible = true);
CREATE POLICY "Admins can manage hotspots"
  ON public.map_hotspots FOR ALL USING (auth.uid() IN (SELECT id FROM profiles WHERE is_admin = true));
```

### How to add hotspots (pre-admin-UI)

Until a proper admin interface is built, hotspots are added directly in the Supabase SQL editor or table view. The table is simple enough that this is fine for the first 20-50 pins. A script (`seed-hotspots.py` or a SQL seed file) can batch-load an initial set.

### Initial hotspot seed list (to build out)

Starting locations to populate before launch:
- Kherson Oblast, Ukraine — Rebuilding
- Mykolaiv, Ukraine — Rebuilding / Opportunity
- New Orleans Lower Ninth Ward, USA — Rebuilding / Opportunity (Devon Clarke's territory)
- Oaxaca, Mexico — Resource Hub (active natural building schools)
- Marrakech region, Morocco — Opportunity (post-2023 earthquake recovery)
- Rural Appalachia — Opportunity (affordable housing crisis)
- Tamil Nadu, India — Active Build (earthen architecture tradition + modern builds)
- Accra, Ghana — Partner Org
- Taos, New Mexico — Resource Hub / Active Build (hempcrete hub)

---

## Claim Your Pin — First Visit Activation

This is the single most important UX decision for the map. If members don't put themselves on the map in the first session, most of them never will. The goal: get from signup to pinned in under 60 seconds.

### The moment

Immediately after email confirmation (or right after first login via OAuth), before they see the feed or explore page, members land on a **one-screen welcome interstitial**:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   🌍  You just joined a global community.           │
│       Let people find you.                          │
│                                                     │
│   Where are you building?                           │
│   ┌─────────────────────────────────────────────┐  │
│   │  Kherson, Ukraine                           │  │
│   └─────────────────────────────────────────────┘  │
│                                                     │
│   Show me on the map as:                           │
│   (●) My city  ( ) My region  ( ) Not yet          │
│                                                     │
│   [ Put me on the map → ]                          │
│                                 [ Skip for now ]   │
└─────────────────────────────────────────────────────┘
```

Two taps. No explanation. The map behind the interstitial is live — they can already see the hotspot pins. They're placing themselves *into* something that's already happening.

### Why this works

- **Social proof is visible immediately.** The map behind the dialog already has hotspots and (eventually) other member pins. They're not joining an empty room — they're joining a world.
- **The ask is minimal.** One text field (location) and one choice (visibility level). Not a full profile form.
- **"Skip for now" is honest.** Don't hide it or guilt-trip. But the primary CTA is large and the default (city level) is already selected.
- **The payoff is instant.** After they tap "Put me on the map," the map zooms to their pin. First experience of the platform is seeing themselves placed in a global community of builders.

### The map as the onboarding hook

On the welcome screen shown to new signups, instead of showing the feed or circles, **show the map first** with a banner:

> "312 builders in 47 countries. Add yourself."

This reframes the map from a feature to a community contract. You're not just exploring — you're showing up.

### Re-engagement prompts (for members who skipped)

Members who skipped during onboarding get:
- A soft banner on their profile page: "You're not on the map yet. [Add your location →]"
- A one-time notification (in-app, not email) when they first visit the map page: "You're viewing the community map but you're not on it. Want to add yourself? [Yes, place my pin]"
- No nagging after that. One ask per channel.

### Claiming a Rebuilding pin

For the Ukraine use case and others like it: if someone signs up from a location that matches an existing **Rebuilding or Opportunity hotspot**, show them a special version of the onboarding:

```
┌─────────────────────────────────────────────────────┐
│  🔶  There's an active rebuilding effort near you.  │
│      Kherson Oblast — 3 partners working here.      │
│                                                     │
│  Put yourself on the map and connect with them.     │
│  [ I'm in Kherson — add me → ]                      │
└─────────────────────────────────────────────────────┘
```

This ties the map to action from the very first interaction.

---

## Privacy Design

This is the most important design decision on the map. Members must feel safe.

**Location granularity options (user-controlled in profile settings):**
- Off — not shown on map at all (default)
- Region — city or county level only (e.g. "Taos, New Mexico" → pin at city centroid)
- Neighborhood — zip code or postal code centroid

No member pin should ever show an exact address. The `location` field in profiles is already free text ("Taos, New Mexico") — geocoding that to city/region centroid is the right approach. The geocode result is stored in `latitude`/`longitude` at that granularity level, not at the member's actual address.

**Profile privacy settings needed:**
```
map_visibility: 'off' | 'region' | 'neighborhood'
```
Default: `'off'` — opt-in only.

---

## Data Model Changes Needed

### Profiles table additions
```sql
map_visibility   TEXT NOT NULL DEFAULT 'off'
  CHECK (map_visibility IN ('off', 'region', 'neighborhood')),
longitude        DOUBLE PRECISION    -- already exists for projects; add to profiles
```
(The profiles table already has `latitude` — `longitude` may need to be added if not already there.)

### New index for map queries
```sql
CREATE INDEX profiles_map_idx ON profiles(latitude, longitude)
  WHERE map_visibility != 'off' AND latitude IS NOT NULL;
CREATE INDEX projects_map_idx ON projects(latitude, longitude)
  WHERE is_public = true AND latitude IS NOT NULL;
```

### Map query view (optional, simplifies frontend)
A single Supabase view or RPC function that returns all visible pins in a bounding box:
```
GET /rpc/map_pins?min_lat=...&max_lat=...&min_lng=...&max_lng=...
```
Returns: `[{ type: 'member'|'project', lat, lng, id, name, slug, avatar, circle_slug, tagline }]`

---

## Map Provider

**Recommendation: Mapbox GL JS (free tier)**

Why Mapbox over Google Maps:
- Free tier is generous (50,000 map loads/month — more than enough pre-launch)
- Style customization — can make it match Earthback's earthy, low-contrast aesthetic (dark green/parchment)
- Marker clustering built in via `mapbox-gl-cluster`
- Self-hostable tiles option if we ever want full data sovereignty
- No per-request billing paranoia on a community site with variable traffic

Alternative if Mapbox adds friction: **Leaflet.js + OpenStreetMap tiles** — fully free, no API key needed, slightly less polished but totally viable and 100% open.

---

## Page Integration

### Option A — Embedded section on Explore page (recommended for launch)
The Explore page (`explore.html`) gets a "Members Near You" section with a map panel, sitting between the circles grid and the projects list. Toggled on/off with a tab or "Show map" button to avoid loading the map for everyone on every visit.

### Option B — Standalone `/map` page
A dedicated `map.html` with the full-screen map and filter sidebar. More powerful but more build. Better for v2 after the embed is working.

**Recommendation:** Ship Option A first. The map code is the same either way — it's just a container size question.

---

## Interaction Design

### Layer controls (sidebar or top toolbar)
Five toggles, color-coded to match pin colors:
- [●] Members — green
- [◆] Projects — clay
- [○] Circle clusters — muted
- [🔶] Rebuilding — amber
- [🔷] Resources & Partners — teal/blue

Default state: Rebuilding + Projects on, Members off (until member density is high enough to be useful). This ensures the map looks alive on day one.

Plus: filter by circle — select one or more circles and only show pins affiliated with those circles.

### Zoom behavior
- Zoomed out (country/continent): show circle cluster badges + project markers only. Member dots suppressed to avoid clutter.
- Zoomed to region (state/county): member dots appear, clusters dissolve into individual pins
- Zoomed to city: full detail, avatars visible on member pins

### Pin click → popup card
Each pin click opens a small card anchored to the pin:

**Member card:**
```
[ avatar ] James Osei
           Hempcrete builder · Accra, Ghana
           [ Hempcrete ] [ Solar ]
           → View Profile
```

**Project card:**
```
[ cover ] Taos ADU Hempcrete
          Active Build · Taos, New Mexico
          [ Hempcrete ] [ Housing ]
          → View Project
```

### "Near me" feature
A "Show members near me" button uses the browser's Geolocation API to center the map on the user's location and show nearby members/projects. No location is stored — it's client-side only.

---

## Settings / Profile Integration

On the profile edit page, add a "Map visibility" section:

```
Show me on the community map?
( ) No — keep me off the map
(•) City/Region — show me at city level
( ) Neighborhood — show me at zip code level

[ Your location will show as "Taos, New Mexico" — never your exact address ]
```

When a user sets their location text and map visibility, the frontend geocodes the location string to coordinates at the appropriate granularity and saves `latitude`, `longitude`, and `map_visibility` to the profiles table.

**Geocoding:** Use the Mapbox Geocoding API (same SDK) or the free Nominatim (OpenStreetMap) API — send city name, get centroid back. Cap precision to city level (truncate to ~2 decimal places).

---

## Build Sequence

**Phase 1 — Foundation (1 session)**
1. Schema migration: `map_hotspots` table + `longitude` and `map_visibility` to profiles
2. Seed initial hotspots (Ukraine, Taos, Oaxaca, etc.) via SQL seed file
3. Create Supabase map query returning hotspots + projects + opted-in members
4. Add map visibility controls to profile edit page

**Phase 2 — Map page + hotspot pins (1 session)**
1. Build `map.html` — full-screen layout with sidebar controls
2. Set up Mapbox GL JS (or Leaflet)
3. Load and render hotspot pins with color-coded markers by category
4. Popup cards on click — hotspot variant (title, description, Join This Effort)
5. Add "Map" link to nav

*At the end of Phase 2, the map is publicly usable and tells a real story — even with zero members pinned.*

**Phase 3 — Member + project pins (1 session)**
1. Load project pins (already have lat/lng)
2. Load opted-in member pins
3. Popup cards — member and project variants
4. Layer toggles
5. "Near me" button

**Phase 4 — Onboarding activation (1 session)**
1. Post-signup interstitial — "Claim your pin" screen
2. Location geocoding flow (free text → lat/lng centroid)
3. Proximity detection for Rebuilding hotspot match → special onboarding variant
4. Re-engagement banner on profile page for members who skipped
5. Map embed on Explore page (smaller version, "see more" links to map.html)

**Phase 5 — Clustering + scale (when member count warrants it)**
1. Supercluster for member density zones
2. Circle cluster badges by region
3. Zoom-level behavior (suppress member pins at country zoom)
4. More advanced filters (project type, status, skills)

---

## Open Questions / Decisions Needed

1. **Mapbox vs Leaflet** — Mapbox is nicer but requires an API key. Leaflet requires zero accounts. Which feels more aligned with Earthback's open/low-dependency values? (My lean: Leaflet + OpenStreetMap for the ethos alignment, Mapbox if custom styling matters a lot.)

2. **Hotspot management** — Direct Supabase table edit is fine for the first 20-30 pins. When do we want a simple admin UI? Could be a basic protected HTML page with a form that inserts into `map_hotspots`.

3. **"Join This Effort" action** — What does clicking this do for a Rebuilding pin? Options: (a) joins the associated circle, (b) sends a message to the coordinating org, (c) opens a contact form to Earthback. Probably (a) with a circle per active rebuilding zone.

4. **Projects without coordinates** — Many seed projects won't have lat/lng. Show project owners a prompt: "Add your project location to appear on the map"? Or just skip silently for now.

5. **Map style** — Earthback's palette (`#1F3A2E`, `#C26B42`, `#F5EFE0`) on a custom Mapbox style would look incredible. A muted terrain style (not satellite, not street map) fits the land-stewardship vibe best. Worth doing for launch.

6. **Ukraine specifically** — Do you want to introduce your friends there to the platform now (pre-launch) so they can help seed the map and tell the story? A few real Ukrainian builders on the map before public launch makes it much more compelling to the next wave of signups.

---

## What This Enables Long-Term

Once the map is working, it becomes a foundation for:
- **Local matching** — "There are 4 hempcrete builders within 50 miles of you"
- **Regional circles** — automatically generated circles for a metro area or bioregion
- **Project discovery** — "Active builds in your state"
- **IRL events** — pin events on the map (workshops, site visits, skill shares)
- **Supplier proximity** — show aligned supplier/partner locations relative to a build site

The pin map is one of the most important differentiation features Earthback has. Most community platforms are purely chronological feeds — geography is almost entirely absent. Showing where people actually are makes the mutual aid and collaboration angle real.

The hotspot system turns the map from a member directory into a **declaration of purpose** — here's where the work is needed, here's where it's happening, here's where you can show up. For a platform about rebuilding communities, that's exactly the right thing to put on the homepage.
