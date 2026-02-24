-- ============================================================
-- SCHEMA V7b — Add website_url to partner_inquiries
-- ============================================================
-- Run AFTER: SCHEMA_V7
-- ============================================================

ALTER TABLE public.partner_inquiries
  ADD COLUMN IF NOT EXISTS website_url TEXT;
