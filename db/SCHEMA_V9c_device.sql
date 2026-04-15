-- ═══════════════════════════════════════════════════════════════
-- SCHEMA_V9c_device.sql
-- Adds user_agent + user_location to page_views analytics
-- Run in Supabase SQL Editor after SCHEMA_V9b_ip.sql
-- Safe to re-run (idempotent)
-- ═══════════════════════════════════════════════════════════════

-- Add new columns (safe if already exist)
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS user_agent TEXT;
ALTER TABLE public.page_views
  ADD COLUMN IF NOT EXISTS user_location TEXT;

-- ── Updated RPC function: insert_page_view ──────────────────
-- Now also extracts User-Agent from request headers (device/OS/browser)
-- and looks up user's location from their profile.
-- Always stores IP even for logged-in users.
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
  v_ua      TEXT;
  v_headers JSON;
  v_name    TEXT;
  v_loc     TEXT;
BEGIN
  -- Extract IP and User-Agent from PostgREST request headers
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
    -- User-Agent header
    v_ua := v_headers->>'user-agent';
  EXCEPTION WHEN OTHERS THEN
    v_ip := NULL;
    v_ua := NULL;
  END;

  -- Look up display name and location from profiles if user_id provided
  IF p_user_id IS NOT NULL THEN
    SELECT display_name, location INTO v_name, v_loc
    FROM public.profiles
    WHERE id = p_user_id
    LIMIT 1;
  END IF;

  INSERT INTO public.page_views (
    page, referrer, session_id, ip_address, user_id, display_name, user_agent, user_location
  ) VALUES (
    p_page, p_referrer, p_session_id, v_ip, p_user_id, v_name, v_ua, v_loc
  );
END;
$$;

-- Permissions unchanged — same signature, just new columns in the INSERT
GRANT EXECUTE ON FUNCTION public.insert_page_view(TEXT, TEXT, TEXT, UUID) TO anon, authenticated;
