-- ============================================================
-- Earthback — V4: Post Images + Demo Post Image URLs
-- Run this in Supabase SQL Editor
-- Adds image_url column to posts + updates ~8 demo posts
-- with real AI-generated images (served from /assets/img/posts/)
-- ============================================================

-- ── ADD IMAGE_URL COLUMN ──────────────────────────────────
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS is_demo BOOLEAN DEFAULT false;

-- Mark all existing seed posts as demo
UPDATE public.posts SET is_demo = true WHERE author_id IS NULL;

-- ── UPDATE DEMO POSTS WITH AI-GENERATED IMAGES ─────────────
-- Images generated via Flux from the prompts below.
-- Served as static assets from the site repo.

-- Post 1: Hempcrete mix ratio guide
UPDATE public.posts
SET image_url = '/assets/img/posts/hempcrete-mix.jpg'
WHERE title LIKE 'Hempcrete mix ratio guide%' AND is_demo = true;

-- Post 2: First hempcrete wall poured in Utah
UPDATE public.posts
SET image_url = '/assets/img/posts/utah-hemp-wall.jpg'
WHERE title LIKE 'First hempcrete wall poured%' AND is_demo = true;

-- Post 4: Open-source greywater system
UPDATE public.posts
SET image_url = '/assets/img/posts/greywater-system.jpg'
WHERE title LIKE 'Open-sourcing our complete greywater%' AND is_demo = true;

-- Post 7: Neighborhood energy independence
UPDATE public.posts
SET image_url = '/assets/img/posts/solar-coop.jpg'
WHERE title LIKE '%neighborhood co-op officially hit energy%' AND is_demo = true;

-- Post 8: Food forest design
UPDATE public.posts
SET image_url = '/assets/img/posts/food-forest.jpg'
WHERE title LIKE '%food forest design%' AND is_demo = true;

-- Post 10: Hand-built cabin move-in
UPDATE public.posts
SET image_url = '/assets/img/posts/tiny-cabin.jpg'
WHERE title LIKE 'Moved into my hand-built%' AND is_demo = true;

-- Post 12: Free Douglas fir salvage
UPDATE public.posts
SET image_url = '/assets/img/posts/salvage-fir.jpg'
WHERE title LIKE '%old-growth Douglas fir%' AND is_demo = true;

-- Post 14: LoRa mesh network
UPDATE public.posts
SET image_url = '/assets/img/posts/lora-mesh.jpg'
WHERE title LIKE '%LoRa mesh network%' AND is_demo = true;


-- ── VERIFY ──────────────────────────────────────────────
-- Check that images were added:
-- SELECT title, image_url FROM public.posts WHERE image_url IS NOT NULL;
