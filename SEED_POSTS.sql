-- ============================================================
-- Earthback — Posts Table Schema + Seed Data
-- Run this in Supabase SQL Editor (after SUPABASE_SETUP.md schema)
-- This is Phase 2: the real feed. Right now the feed uses
-- the hardcoded POSTS array in join.html / index.html.
-- Once you run this and wire up the front end, you'll replace
-- that array with a live Supabase query.
-- ============================================================

-- ── POSTS TABLE ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS public.posts (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Author (nullable for org/system posts, or until profiles are linked)
  author_id     UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  author_name   TEXT NOT NULL,
  author_initials TEXT,
  author_detail TEXT,                    -- e.g. "Hemp Build Network · Nashville, TN"

  -- Circle / stream
  circle_slug   TEXT NOT NULL,           -- e.g. "natural-building"
  circle_label  TEXT NOT NULL,           -- e.g. "Natural Building"

  -- Post classification
  post_type     TEXT NOT NULL            -- milestone | resource | need | question | coordination | celebration
    CHECK (post_type IN ('milestone','resource','need','question','coordination','celebration')),

  -- Content
  title         TEXT NOT NULL,
  body          TEXT NOT NULL,           -- plain text (no HTML in DB)
  tags          TEXT[],                  -- optional searchable tags

  -- Engagement
  helpful_count INTEGER DEFAULT 0,
  is_verified   BOOLEAN DEFAULT false,   -- Earthback verified project/person

  -- Visibility
  is_public     BOOLEAN DEFAULT true,
  is_pinned     BOOLEAN DEFAULT false,   -- pinned posts appear at top

  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public posts are viewable by everyone"
  ON public.posts FOR SELECT
  USING (is_public = true);

CREATE POLICY "Authors can manage their own posts"
  ON public.posts FOR ALL
  USING (auth.uid() = author_id)
  WITH CHECK (auth.uid() = author_id);

-- Index for common queries
CREATE INDEX IF NOT EXISTS posts_circle_slug_idx ON public.posts(circle_slug);
CREATE INDEX IF NOT EXISTS posts_post_type_idx   ON public.posts(post_type);
CREATE INDEX IF NOT EXISTS posts_created_at_idx  ON public.posts(created_at DESC);


-- ── SEED DATA — 14 Sample Posts ─────────────────────────────
-- NOTE: author_id is NULL for all seed rows (no real auth users).
-- When real users create posts, author_id will be their profile UUID.

INSERT INTO public.posts
  (author_name, author_initials, author_detail, circle_slug, circle_label,
   post_type, title, body, tags, helpful_count, is_verified, created_at)
VALUES

-- 1. Earthback Project resource
(
  'the Earthback Project', 'EA',
  'Curated stream · cross-posted from social',
  'earthback-project', 'the Earthback Project',
  'resource',
  'Hempcrete mix ratio guide for humid climates',
  'After three years of testing across the Southeast, we compiled what actually works — including seasonal adjustments, binder ratios for high-humidity regions, and curing timeline differences. Available as a free PDF in the resources section.',
  ARRAY['hempcrete','mix ratio','humid climate','lime binder'],
  34, true,
  NOW() - INTERVAL '2 hours'
),

-- 2. Milestone: first Utah hemp wall
(
  'James Okonkwo', 'JO',
  'Hemp Build Network · Nashville, TN',
  'natural-building', 'Natural Building',
  'milestone',
  'First hempcrete wall poured in Utah using locally grown industrial hemp',
  'Mix: 4 parts hemp hurd, 1 part hydraulic lime, 1 part water. Batching took 2 hours, pouring 6 hours for a 400 sq ft ground floor. Curing for 28 days before load testing. Build day photos coming shortly.',
  ARRAY['hempcrete','utah','hemp hurd','hydraulic lime','milestone'],
  47, false,
  NOW() - INTERVAL '5 hours'
),

-- 3. Need: straw bale build day volunteers
(
  'Priya Mehta', 'PM',
  'Skills & Workshops · Salt Lake City, UT',
  'skills-workshops', 'Skills & Workshops',
  'need',
  'Looking for 3 people for a weekend straw bale build day — March 8',
  'Small ADU project on a 1/3 acre lot in South Salt Lake. No experience required, just willing hands and a good attitude. Skilled help is very welcome. Meals provided. RSVP in comments so we know who is coming.',
  ARRAY['straw bale','volunteer','ADU','Salt Lake City','build day'],
  12, false,
  NOW() - INTERVAL '1 day'
),

-- 4. Resource: open-source greywater system
(
  'Blue Mesa Collective', 'BM',
  'Blue Mesa Collective · Durango, CO',
  'water-systems', 'Water Systems',
  'resource',
  'Open-sourcing our complete greywater reuse system — 3-bedroom scale',
  '$800 in materials, 2 days to install, zero permits required in most Western states. Handles bathroom sinks, showers, and laundry. Keeps 40+ gallons/day out of septic. Plans, parts list, and install guide all linked below.',
  ARRAY['greywater','water reuse','off-grid','open source','plans'],
  28, true,
  NOW() - INTERVAL '2 days'
),

-- 5. Question: root cellar under hempcrete
(
  'Tevita Fifita', 'TF',
  'Natural Building · Auckland, NZ',
  'natural-building', 'Natural Building',
  'question',
  'Has anyone integrated a root cellar below a hempcrete structure?',
  'Running into thermal bridge issues at the foundation transition — the lime binder conducts heat differently than I expected. Thinking about a poured concrete knee wall with insulation break but not sure what detail works best. Any experience welcome.',
  ARRAY['hempcrete','root cellar','thermal bridge','foundation','question'],
  9, false,
  NOW() - INTERVAL '3 days'
),

-- 6. Coordination: tribal housing project
(
  'the Earthback Project', 'EA',
  'Curated stream · partnership opportunity',
  'earthback-project', 'the Earthback Project',
  'coordination',
  'Tribal nation in New Mexico seeking building partners for 40-unit affordable housing project',
  'Community-owned land, existing utilities, grant funding secured. Looking for builders experienced with indigenous-led development, preference for earth-based construction methods. Community ownership built into the project structure from day one. Contact listed in the Alliance directory.',
  ARRAY['affordable housing','indigenous','New Mexico','partnership','coordination'],
  61, true,
  NOW() - INTERVAL '4 days'
),

-- 7. Milestone: neighborhood energy independence
(
  'Rosa Delgado-Kwan', 'RD',
  'Solar & Off-Grid · Tucson, AZ',
  'solar-off-grid', 'Solar & Off-Grid',
  'milestone',
  'Our 16-family neighborhood co-op officially hit energy independence this week',
  '48kW shared array + 120kWh LiFePO4 battery bank (DIY build). Grid bill: $0. Total project cost: $67,000 shared across 16 households = $4,200 per family. Took 14 months from idea to completion. Full budget breakdown available on request.',
  ARRAY['solar','energy co-op','LiFePO4','off-grid','neighborhood','milestone'],
  89, false,
  NOW() - INTERVAL '6 hours'
),

-- 8. Resource: food forest design
(
  'Saoirse Ó Briain', 'SB',
  'Permaculture & Food · County Clare, Ireland',
  'permaculture-food', 'Permaculture & Food',
  'resource',
  'Sharing our 7-year food forest design — 1.2 acres, temperate climate, zones 1–4 mapped',
  'Started from grass with clay soil. Now producing apples, pears, plums, hazelnuts, currants, and year-round salad. The guild plantings that actually worked (and those that did not) are all documented. PDF map, species list, and yearly progress photos linked below.',
  ARRAY['food forest','permaculture','temperate','guild planting','Ireland','design'],
  52, false,
  NOW() - INTERVAL '1 day'
),

-- 9. Coordination: emergency tool library
(
  'Detroit Roots Network', 'DR',
  'Mutual Aid · Detroit, MI',
  'mutual-aid', 'Mutual Aid',
  'coordination',
  'Spinning up an emergency tool library after the February ice storms',
  'Have: 2 generators, 3 chainsaw kits, battery jump packs, and a hydraulic jack. Need: another generator, extension cord reels, and a flatbed truck for 2 weekends. Serving 6 zip codes. If you are local and have something to lend or a way to help move supplies, please reply.',
  ARRAY['mutual aid','Detroit','ice storm','tool library','emergency','coordination'],
  37, false,
  NOW() - INTERVAL '18 hours'
),

-- 10. Milestone: hand-built cabin move-in
(
  'Yuki Tanaka', 'YT',
  'Tiny & Alternative Dwellings · Asheville, NC',
  'tiny-dwellings', 'Tiny & Alternative Dwellings',
  'milestone',
  'Moved into my hand-built 280 sq ft cabin after 18 months of weekends',
  'Timber frame with metal roof, woodstove, composting toilet, and a 600-gallon rainwater tank. Total materials cost: $18,400. No mortgage, no rent, property taxes under $200 per year. I kept a build diary the whole time — happy to share the whole thing with anyone who asks.',
  ARRAY['tiny house','cabin','timber frame','off-grid','composting toilet','rainwater'],
  143, false,
  NOW() - INTERVAL '2 days'
),

-- 11. Question: cover crop mix for transitioning field
(
  'Hamid Rezaei', 'HR',
  'Land & Regenerative Ag · Willamette Valley, OR',
  'land-regen-ag', 'Land & Regenerative Agriculture',
  'question',
  'Seeking advice on cover crop mix for a 12-acre field transitioning out of conventional corn',
  'Soil tests show compaction at 8 inches and very low organic matter (1.2%). Last two seasons were back-to-back corn. Thinking crimson clover, tillage radish, and oats — but not sure whether to terminate with roller-crimper or cold-kill. Anyone running something similar in the PNW?',
  ARRAY['cover crop','soil health','regenerative ag','Oregon','tillage','question'],
  14, false,
  NOW() - INTERVAL '3 days'
),

-- 12. Resource: free old-growth Douglas fir
(
  'Cascade Deconstruction', 'CD',
  'Materials & Salvage · Portland, OR',
  'materials-salvage', 'Materials & Salvage',
  'resource',
  'Free: 600 board feet of old-growth Douglas fir from a 1920s warehouse deconstruction',
  'Beautiful patina, mostly 2x10 and 2x12, some full-dimension. You haul. Warehouse is in NE Portland; access available this weekend only. First come, first served — reply to reserve a slot. Bring a truck and friends, there is a lot.',
  ARRAY['salvage','Douglas fir','reclaimed','Portland','free','deconstruction'],
  76, false,
  NOW() - INTERVAL '4 hours'
),

-- 13. Coordination: land trust forming in Vermont
(
  'Amara Diallo', 'AD',
  'Cooperative Housing · Burlington, VT',
  'cooperative-housing', 'Cooperative Housing',
  'coordination',
  'Forming a 6-household land trust in Vermont — looking for 3 more families',
  'We have a 22-acre parcel under option (expires April 30). Mixed forest and open field, town water hookup at the road, deed restrictions allow 8 dwellings. Seeking people serious about long-term community land ownership. Two founding families have co-housing experience. Intro call happening March 1st.',
  ARRAY['land trust','Vermont','community','co-housing','forming','cooperative'],
  31, false,
  NOW() - INTERVAL '5 days'
),

-- 14. Resource: LoRa mesh network
(
  'OffGrid.net Collective', 'OG',
  'Community Tech · Cascadia Region',
  'community-tech', 'Community Tech',
  'resource',
  'Our LoRa mesh network now covers 40 square miles of the Cascades — zero internet required',
  '12 nodes, solar powered, range of ~5 miles per hop. Used for farm-to-farm messaging, weather alerts, and emergency coordination. Full hardware list, firmware config, and antenna placement guide is public on our repo. Works on Meshtastic. Total cost per node: $38.',
  ARRAY['LoRa','mesh network','Meshtastic','off-grid','community tech','Cascadia'],
  58, false,
  NOW() - INTERVAL '6 days'
);


-- ── VERIFY ──────────────────────────────────────────────────
-- Run this after the INSERT to confirm 14 rows loaded:
-- SELECT count(*) FROM public.posts;
-- SELECT circle_label, post_type, title FROM public.posts ORDER BY created_at DESC;
