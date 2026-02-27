-- ═══════════════════════════════════════════════════════════════
-- SCHEMA_V9b_ip.sql
-- Adds IP address + member tracking to page_views analytics
-- Run in Supabase SQL Editor after SCHEMA_V9_analytics.sql
-- Safe to re-run (idempotent)
-- ═══════════════════════════════════════════════════════════════

-- Add ip_address and user_id columns (safe if already exist)
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS ip_address TEXT;
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS user_id UUID;
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS display_name TEXT;

-- ── RPC function: insert_page_view ────────────────────────────
-- Called by nav.js instead of inserting directly into the table.
-- PostgREST passes request headers via current_setting('request.headers')
-- so we can extract the real visitor IP server-side.
-- If a user_id is passed, we look up their display_name from profiles.
CREATE OR REPLACE FUNCTION public.insert_page_view(
  p_page       TEXT,
  p_referrer   TEXT DEFAULT NULL,
  p_session_id TEXT DEFAULT NULL,
  p_user_id    UUID DEFAULT NULL
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_ip      TEXT;
  v_headers JSON;
  v_name    TEXT;
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

  -- Look up display name from profiles if user_id provided
  IF p_user_id IS NOT NULL THEN
    SELECT display_name INTO v_name
    FROM public.profiles
    WHERE id = p_user_id
    LIMIT 1;
  END IF;

  INSERT INTO public.page_views (page, referrer, session_id, ip_address, user_id, display_name)
  VALUES (p_page, p_referrer, p_session_id, v_ip, p_user_id, v_name);
END;
$$;

-- Allow anon + authenticated to call this function
GRANT EXECUTE ON FUNCTION public.insert_page_view(TEXT, TEXT, TEXT, UUID) TO anon, authenticated;

-- Drop old function signature if it exists (3-param version)
DROP FUNCTION IF EXISTS public.insert_page_view(TEXT, TEXT, TEXT);
