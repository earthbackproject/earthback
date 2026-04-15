-- ============================================================
-- SCHEMA_V10b_submissions.sql
-- Method Image Submissions — members submit build photos
-- Run AFTER SCHEMA_V10_methods.sql + SCHEMA_V10_seed.sql
-- ============================================================

-- 1. Add hero image column to construction_methods
ALTER TABLE construction_methods
  ADD COLUMN IF NOT EXISTS hero_image_url TEXT,
  ADD COLUMN IF NOT EXISTS hero_credit_user_id UUID REFERENCES auth.users(id),
  ADD COLUMN IF NOT EXISTS hero_credit_name TEXT;

-- 2. Method submissions table
CREATE TABLE IF NOT EXISTS method_submissions (
  id            SERIAL PRIMARY KEY,
  user_id       UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  method_id     INT  NOT NULL REFERENCES construction_methods(id) ON DELETE CASCADE,
  image_url     TEXT NOT NULL,
  caption       TEXT,
  status        TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'approved', 'featured', 'rejected')),
  reviewed_at   TIMESTAMPTZ,
  submitted_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_method_subs_user   ON method_submissions (user_id);
CREATE INDEX IF NOT EXISTS idx_method_subs_method ON method_submissions (method_id);
CREATE INDEX IF NOT EXISTS idx_method_subs_status ON method_submissions (status);

-- 3. Row-Level Security
ALTER TABLE method_submissions ENABLE ROW LEVEL SECURITY;

-- Anyone can see approved/featured submissions
CREATE POLICY "Approved submissions are publicly readable"
  ON method_submissions FOR SELECT
  USING (status IN ('approved', 'featured'));

-- Users can see their own submissions (any status)
CREATE POLICY "Users can see their own submissions"
  ON method_submissions FOR SELECT
  USING (auth.uid() = user_id);

-- Authenticated users can submit (must have a skill claim — enforced in app)
CREATE POLICY "Authenticated users can submit images"
  ON method_submissions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own pending submissions
CREATE POLICY "Users can delete own pending submissions"
  ON method_submissions FOR DELETE
  USING (auth.uid() = user_id AND status = 'pending');

-- 4. RPC: Submit a method image
CREATE OR REPLACE FUNCTION submit_method_image(
  p_method_id INT,
  p_image_url TEXT,
  p_caption TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_skill   RECORD;
  v_result  method_submissions;
BEGIN
  IF v_user_id IS NULL THEN
    RETURN jsonb_build_object('error', 'Not authenticated');
  END IF;

  -- Verify user has claimed this method at experienced or trainer level
  SELECT * INTO v_skill FROM member_skills
    WHERE user_id = v_user_id AND method_id = p_method_id
    AND tier IN ('experienced', 'trainer');

  IF NOT FOUND THEN
    RETURN jsonb_build_object('error',
      'You need Experienced or Trainer status on this method to submit photos');
  END IF;

  INSERT INTO method_submissions (user_id, method_id, image_url, caption)
  VALUES (v_user_id, p_method_id, p_image_url, p_caption)
  RETURNING * INTO v_result;

  RETURN jsonb_build_object(
    'ok', true,
    'submission_id', v_result.id,
    'status', v_result.status
  );
END;
$$;

-- 5. RPC: Feature a submission (admin use — call from Supabase dashboard)
--    Sets the submission to 'featured', updates the method hero image,
--    and un-features any previous featured submission for that method.
CREATE OR REPLACE FUNCTION feature_submission(p_submission_id INT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_sub     RECORD;
  v_profile RECORD;
BEGIN
  -- Get the submission
  SELECT * INTO v_sub FROM method_submissions WHERE id = p_submission_id;
  IF NOT FOUND THEN
    RETURN jsonb_build_object('error', 'Submission not found');
  END IF;

  -- Un-feature any existing featured submission for this method
  UPDATE method_submissions
    SET status = 'approved', reviewed_at = NOW()
    WHERE method_id = v_sub.method_id AND status = 'featured';

  -- Feature this one
  UPDATE method_submissions
    SET status = 'featured', reviewed_at = NOW()
    WHERE id = p_submission_id;

  -- Get display name for credit
  SELECT display_name INTO v_profile
    FROM profiles WHERE id = v_sub.user_id;

  -- Update method hero image
  UPDATE construction_methods SET
    hero_image_url     = v_sub.image_url,
    hero_credit_user_id = v_sub.user_id,
    hero_credit_name   = COALESCE(v_profile.display_name, 'Community Member')
  WHERE id = v_sub.method_id;

  RETURN jsonb_build_object(
    'ok', true,
    'method_id', v_sub.method_id,
    'featured_by', COALESCE(v_profile.display_name, 'Community Member')
  );
END;
$$;

-- ============================================================
-- STORAGE BUCKET SETUP (run these in Supabase Dashboard → Storage)
-- ============================================================
-- 1. Create bucket: "method-images" (public)
-- 2. Add policy: Allow authenticated uploads to own folder
--    - Policy name: "Users can upload to own folder"
--    - Allowed operation: INSERT
--    - Policy: (bucket_id = 'method-images') AND (auth.uid()::text = (storage.foldername(name))[1])
-- 3. Add policy: Public read access
--    - Policy name: "Public read access"
--    - Allowed operation: SELECT
--    - Policy: bucket_id = 'method-images'
-- ============================================================
