-- ============================================================
-- SCHEMA V5 — Visions (AI Visualizer saved renders)
-- Run AFTER: V4 (post_images)
-- ============================================================
-- Stores every AI render a user generates, along with the full
-- prompt inputs so the form can be repopulated on click.
-- Images are stored in the 'visions' Supabase Storage bucket;
-- this table holds the permanent public URL.
-- ============================================================

-- 1. Create the visions table

CREATE TABLE IF NOT EXISTS public.visions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  prompt      TEXT NOT NULL,              -- the user's "Your vision" text
  structure   TEXT DEFAULT 'single-home', -- chip value (single-home, duplex, community-hub, workshop, full-village)
  climate     TEXT DEFAULT 'high-desert', -- chip value (high-desert, prairie, forest, coastal, mountain, tropical)
  style       TEXT DEFAULT 'photorealistic', -- render style (photorealistic, sketch, blueprint)
  image_url   TEXT,                       -- permanent Supabase Storage public URL
  replicate_url TEXT,                     -- original Replicate URL (expires ~1hr)
  full_prompt TEXT,                       -- the assembled prompt sent to Replicate (for debugging/reference)
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Enable RLS

ALTER TABLE public.visions ENABLE ROW LEVEL SECURITY;

-- Users can see their own visions
CREATE POLICY "Users can view own visions"
  ON public.visions FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own visions
CREATE POLICY "Users can insert own visions"
  ON public.visions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own visions
CREATE POLICY "Users can delete own visions"
  ON public.visions FOR DELETE
  USING (auth.uid() = user_id);

-- 3. Index for fast lookup by user
CREATE INDEX IF NOT EXISTS visions_user_idx ON public.visions(user_id, created_at DESC);

-- 4. Storage bucket (run this manually in Supabase Dashboard > Storage if needed)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('visions', 'visions', true);
--
-- Then add a policy to allow authenticated users to upload to their own folder:
-- CREATE POLICY "Users can upload own visions"
--   ON storage.objects FOR INSERT
--   WITH CHECK (bucket_id = 'visions' AND auth.uid()::text = (storage.foldername(name))[1]);
--
-- And read access for public URLs:
-- CREATE POLICY "Vision images are public"
--   ON storage.objects FOR SELECT
--   USING (bucket_id = 'visions');
