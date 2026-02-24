-- ============================================================
-- SCHEMA V6b — Add UPDATE policy to visions table
-- ============================================================
-- V5 only created SELECT, INSERT, DELETE policies.
-- The share-to-gallery and like-count features need UPDATE.
-- ============================================================

-- Users can update their own visions (share, etc.)
CREATE POLICY "Users can update own visions"
  ON public.visions FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Also allow authenticated users to increment like_count on any shared vision
-- (needed for the like button on gallery/profile pages)
CREATE POLICY "Authenticated users can update shared vision counters"
  ON public.visions FOR UPDATE
  USING (is_shared = true)
  WITH CHECK (is_shared = true);
