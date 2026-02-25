-- ═══════════════════════════════════════════════════════════════
-- SCHEMA_V9b_ip.sql
-- Adds IP address capture to page_views analytics
-- Run in Supabase SQL Editor after SCHEMA_V9_analytics.sql
-- Safe to re-run (idempotent)
-- ═══════════════════════════════════════════════════════════════

-- Add ip_address column (safe if already exists)
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS ip_address TEXT;

-- ── RPC function: insert_page_view ────────────────────────────
-- Called by nav.js instead of inserting directly into the table.
-- PostgREST passes request headers via current_setting('request.headers')
-- so we can extract the real visitor IP server-side.
CREATE OR REPLACE FUNCTION public.insert_page_view(
  p_page       TEXT,
  p_referrer   TEXT DEFAULT NULL,
  p_session_id TEXT DEFAULT NULL
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_ip      TEXT;
  v_headers JSON;
BEGIN
  -- Extract IP from PostgREST request headers
  BEGIN
    v_headers := current_setting('request.headers', true)::json;
    v_ip := COALESCE(
      v_headers->>'x-forwarded-for',
      v_headers->>'x-real-ip',
      inet_client_addr()::text
    );
    -- x-forwarded-for can be "1.2.3.4, 10.0.0.1" — take the first (real client)
    IF v_ip LIKE '%,%' THEN
      v_ip := trim(split_part(v_ip, ',', 1));
    END IF;
  EXCEPTION WHEN OTHERS THEN
    v_ip := NULL;
  END;

  INSERT INTO public.page_views (page, referrer, session_id, ip_address)
  VALUES (p_page, p_referrer, p_session_id, v_ip);
END;
$$;

-- Allow anon + authenticated to call this function
GRANT EXECUTE ON FUNCTION public.insert_page_view(TEXT, TEXT, TEXT) TO anon, authenticated;
