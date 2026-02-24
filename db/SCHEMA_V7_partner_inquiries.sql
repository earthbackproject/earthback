-- ============================================================
-- SCHEMA V7 — Partner Inquiries
-- ============================================================
-- Simple table to collect training partner interest forms
-- from the /training.html page.
--
-- Run AFTER: SCHEMA_V6c
-- ============================================================

CREATE TABLE IF NOT EXISTS public.partner_inquiries (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_name     TEXT NOT NULL,
  contact_name TEXT,
  email        TEXT NOT NULL,
  focus_area   TEXT,
  message      TEXT,
  is_reviewed  BOOLEAN DEFAULT false,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.partner_inquiries ENABLE ROW LEVEL SECURITY;

-- Anyone can submit an inquiry (no auth required)
CREATE POLICY "Anyone can submit partner inquiry"
  ON public.partner_inquiries FOR INSERT
  WITH CHECK (true);

-- No public read — admin only (future)
