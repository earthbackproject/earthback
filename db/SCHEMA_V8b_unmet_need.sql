-- ============================================================
-- SCHEMA_V8b — Add 'unmet-need' to map_hotspots category
-- Run this after SCHEMA_V8_map.sql
-- ============================================================

-- Drop the existing category check constraint (auto-named by Postgres)
-- and recreate it with the new value added
DO $$
DECLARE
  cname text;
BEGIN
  SELECT conname INTO cname
  FROM pg_constraint
  WHERE conrelid = 'public.map_hotspots'::regclass
    AND contype = 'c'
    AND pg_get_constraintdef(oid) LIKE '%category%';

  IF cname IS NOT NULL THEN
    EXECUTE 'ALTER TABLE public.map_hotspots DROP CONSTRAINT ' || quote_ident(cname);
  END IF;
END $$;

ALTER TABLE public.map_hotspots
  ADD CONSTRAINT map_hotspots_category_check
  CHECK (category IN ('rebuilding', 'resource', 'build', 'partner', 'opportunity', 'unmet-need'));
