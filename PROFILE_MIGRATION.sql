-- ═══════════════════════════════════════════════════════════
-- PROFILE SYSTEM MIGRATION — Run in Supabase SQL Editor
-- Adds avatar_url column + Storage policies
-- ═══════════════════════════════════════════════════════════

-- 1. Add avatar_url to profiles (Google OAuth + manual upload)
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS avatar_url TEXT DEFAULT '';

-- 2. Create storage buckets (run these in the Supabase dashboard
--    under Storage → New Bucket, or use SQL below)

-- Avatar bucket — profile pictures
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('avatars', 'avatars', true, 5242880)  -- 5 MB limit
ON CONFLICT (id) DO NOTHING;

-- Media bucket — uploaded photos, PDFs, documents
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('media', 'media', true, 20971520)  -- 20 MB limit
ON CONFLICT (id) DO NOTHING;

-- 3. Storage policies — allow authenticated users to upload to their own folder

-- Avatars: users can upload/update their own avatar
CREATE POLICY "Users can upload their own avatar"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users can update their own avatar"
  ON storage.objects FOR UPDATE
  TO authenticated
  USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

-- Avatars: anyone can view (public bucket)
CREATE POLICY "Public avatar access"
  ON storage.objects FOR SELECT
  TO public
  USING (bucket_id = 'avatars');

-- Media: users can upload to their own folder
CREATE POLICY "Users can upload their own media"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'media' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users can update their own media"
  ON storage.objects FOR UPDATE
  TO authenticated
  USING (bucket_id = 'media' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users can delete their own media"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (bucket_id = 'media' AND (storage.foldername(name))[1] = auth.uid()::text);

-- Media: anyone can view (public bucket)
CREATE POLICY "Public media access"
  ON storage.objects FOR SELECT
  TO public
  USING (bucket_id = 'media');
