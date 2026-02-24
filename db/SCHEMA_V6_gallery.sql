-- ============================================================
-- SCHEMA V6 — Shared Gallery, Likes, Flags
-- ============================================================
-- Adds social sharing layer to visions:
--   • Share visions to a public gallery
--   • Like system (1 per person per vision)
--   • Community flagging / reporting
--   • Circle-only visibility (schema only, UI deferred)
--
-- Run AFTER: SCHEMA_V5_visions.sql (visions table must exist)
-- ============================================================

-- ── 1. Extend visions table with sharing + engagement columns ──

ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS is_shared BOOLEAN DEFAULT false;
ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS is_circle_only BOOLEAN DEFAULT false;
ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS circle_slugs TEXT[] DEFAULT '{}';
ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS like_count INTEGER DEFAULT 0;
ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS credit_earned INTEGER DEFAULT 0;
ALTER TABLE public.visions ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT false;

-- Gallery listing query: shared + not flagged, newest first
CREATE INDEX IF NOT EXISTS visions_shared_idx
  ON public.visions(is_shared, is_flagged, created_at DESC);

-- Future "most liked" sorting
CREATE INDEX IF NOT EXISTS visions_like_count_idx
  ON public.visions(like_count DESC);

-- ── 2. Add public read policy for shared visions ──
-- (Existing policies: users can view/insert/delete own visions)

CREATE POLICY "Anyone can view shared visions"
  ON public.visions FOR SELECT
  USING (is_shared = true AND is_flagged = false);

-- ── 3. Vision likes table ──

CREATE TABLE IF NOT EXISTS public.vision_likes (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vision_id   UUID NOT NULL REFERENCES public.visions(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(vision_id, user_id)  -- one like per person per vision
);

CREATE INDEX IF NOT EXISTS vision_likes_vision_idx ON public.vision_likes(vision_id);
CREATE INDEX IF NOT EXISTS vision_likes_user_idx ON public.vision_likes(user_id);

ALTER TABLE public.vision_likes ENABLE ROW LEVEL SECURITY;

-- Anyone can see likes (public gallery shows counts)
CREATE POLICY "Vision likes are public"
  ON public.vision_likes FOR SELECT
  USING (true);

-- Authenticated users can like (own user_id only)
CREATE POLICY "Users can like visions"
  ON public.vision_likes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can remove their own likes
CREATE POLICY "Users can unlike visions"
  ON public.vision_likes FOR DELETE
  USING (auth.uid() = user_id);

-- ── 4. Vision flags table (community reporting) ──

CREATE TABLE IF NOT EXISTS public.vision_flags (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vision_id       UUID NOT NULL REFERENCES public.visions(id) ON DELETE CASCADE,
  reported_by_id  UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  reason          TEXT NOT NULL,    -- 'inappropriate', 'spam', 'offensive', 'other'
  details         TEXT,             -- optional additional context
  is_reviewed     BOOLEAN DEFAULT false,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS vision_flags_vision_idx ON public.vision_flags(vision_id);
CREATE INDEX IF NOT EXISTS vision_flags_unreviewed_idx ON public.vision_flags(is_reviewed) WHERE is_reviewed = false;

ALTER TABLE public.vision_flags ENABLE ROW LEVEL SECURITY;

-- Authenticated users can report visions
CREATE POLICY "Users can report visions"
  ON public.vision_flags FOR INSERT
  WITH CHECK (auth.uid() = reported_by_id);

-- No public read on flags — admin review only (future)
-- Vision creators could see flag count on their own visions (future)

-- ============================================================
-- NOTES:
-- • is_circle_only + circle_slugs are in the schema but not
--   exposed in the UI yet. Easy to turn on later.
-- • credit_earned tracks how many like-credits the creator has
--   earned per vision (max 5). Checked client-side on like.
-- • is_flagged is set client-side when a flag is submitted.
--   Future: use a DB trigger or admin action instead.
-- ============================================================
