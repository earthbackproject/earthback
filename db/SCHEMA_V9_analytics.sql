-- ═══════════════════════════════════════════════════════════════
-- SCHEMA_V9_analytics.sql
-- Earthback page-view analytics table
-- Run in Supabase SQL Editor (one time)
-- ═══════════════════════════════════════════════════════════════

-- Page views table: logs every page load from nav.js
CREATE TABLE IF NOT EXISTS public.page_views (
  id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  page        TEXT         NOT NULL,                -- e.g. "map.html", "index.html"
  referrer    TEXT,                                 -- previous page within the site (if any)
  session_id  TEXT,                                 -- random ID from sessionStorage, persists across a browsing session
  created_at  TIMESTAMPTZ  DEFAULT NOW()
);

-- Indexes for the most common admin queries
CREATE INDEX IF NOT EXISTS idx_pv_created_at  ON public.page_views (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pv_session_id  ON public.page_views (session_id);
CREATE INDEX IF NOT EXISTS idx_pv_page        ON public.page_views (page);

-- Enable RLS
ALTER TABLE public.page_views ENABLE ROW LEVEL SECURITY;

-- Anyone (anon + authenticated) can INSERT a page view
-- This is intentional — the tracking script in nav.js uses the publishable key
DROP POLICY IF EXISTS "anon_insert_page_views" ON public.page_views;
CREATE POLICY "anon_insert_page_views"
  ON public.page_views FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Anyone can SELECT — no PII is stored, just page names + opaque session IDs
DROP POLICY IF EXISTS "public_read_page_views" ON public.page_views;
CREATE POLICY "public_read_page_views"
  ON public.page_views FOR SELECT
  TO anon, authenticated
  USING (true);

-- Enable Supabase Realtime on this table so eb-grove.html gets live pushes
-- (Run in SQL Editor — may already be enabled globally)
ALTER PUBLICATION supabase_realtime ADD TABLE public.page_views;
