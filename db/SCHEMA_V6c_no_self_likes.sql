-- ============================================================
-- SCHEMA V6c — Prevent self-likes
-- ============================================================
-- Users should not be able to like their own visions.
-- Replaces the INSERT policy on vision_likes to add a
-- subquery check that the vision's creator != the liker.
--
-- Run AFTER: SCHEMA_V6_gallery.sql, SCHEMA_V6b
-- ============================================================

-- Drop the old permissive INSERT policy
DROP POLICY IF EXISTS "Users can like visions" ON public.vision_likes;

-- Recreate with self-like guard
CREATE POLICY "Users can like visions (not own)"
  ON public.vision_likes FOR INSERT
  WITH CHECK (
    auth.uid() = user_id
    AND NOT EXISTS (
      SELECT 1 FROM public.visions v
      WHERE v.id = vision_id
        AND v.user_id = auth.uid()
    )
  );

-- Clean up any existing self-likes
DELETE FROM public.vision_likes
WHERE user_id IN (
  SELECT vl.user_id
  FROM public.vision_likes vl
  JOIN public.visions v ON v.id = vl.vision_id
  WHERE vl.user_id = v.user_id
);

-- Reset like_count on affected visions to accurate totals
UPDATE public.visions SET like_count = (
  SELECT COUNT(*) FROM public.vision_likes vl WHERE vl.vision_id = visions.id
)
WHERE is_shared = true;

-- Also reset credit_earned to match actual non-self like count
UPDATE public.visions SET credit_earned = LEAST(5, (
  SELECT COUNT(*) FROM public.vision_likes vl WHERE vl.vision_id = visions.id
))
WHERE is_shared = true;
