-- ============================================================
-- SCHEMA_V8 — Community Map: map_hotspots table
-- Run this FIRST, then run hotspots-seed.sql to load pins
-- ============================================================

-- Map hotspots: curated pins placed by the Earthback team
-- Not user-submitted — admin-managed only for now
CREATE TABLE IF NOT EXISTS public.map_hotspots (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Location
  latitude      DOUBLE PRECISION NOT NULL,
  longitude     DOUBLE PRECISION NOT NULL,
  location_name TEXT NOT NULL,

  -- Content
  category      TEXT NOT NULL
    CHECK (category IN ('rebuilding', 'resource', 'build', 'partner', 'opportunity')),
  title         TEXT NOT NULL,
  description   TEXT,
  status        TEXT DEFAULT 'active'
    CHECK (status IN ('active', 'planned', 'complete', 'paused')),

  -- Links
  url           TEXT,
  contact_email TEXT,
  circle_slug   TEXT,

  -- Display
  is_visible    BOOLEAN DEFAULT true,
  priority      INTEGER DEFAULT 0,

  -- Meta
  created_by    UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Index for map bounding-box queries (lat/lng range lookups)
CREATE INDEX IF NOT EXISTS idx_map_hotspots_location
  ON public.map_hotspots (latitude, longitude)
  WHERE is_visible = true;

CREATE INDEX IF NOT EXISTS idx_map_hotspots_category
  ON public.map_hotspots (category)
  WHERE is_visible = true;

-- RLS
ALTER TABLE public.map_hotspots ENABLE ROW LEVEL SECURITY;

-- Anyone (including logged-out) can read visible hotspots
CREATE POLICY "Hotspots are publicly readable"
  ON public.map_hotspots FOR SELECT
  USING (is_visible = true);

-- Service role (used by seed scripts and Supabase dashboard) bypasses RLS entirely,
-- so no explicit write policy is needed for admin management.
-- Add an is_admin column to profiles and a proper policy here when needed.

-- Auto-update updated_at on any change
CREATE OR REPLACE FUNCTION public.set_hotspot_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hotspot_updated_at
  BEFORE UPDATE ON public.map_hotspots
  FOR EACH ROW EXECUTE FUNCTION public.set_hotspot_updated_at();
