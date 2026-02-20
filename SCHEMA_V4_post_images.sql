-- ============================================================
-- Earthback — V4: Post Images + Demo Post Image URLs
-- Run this in Supabase SQL Editor
-- Adds image_url column to posts + updates ~8 demo posts
-- with placeholder images from picsum.photos
-- ============================================================

-- ── ADD IMAGE_URL COLUMN ──────────────────────────────────
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS is_demo BOOLEAN DEFAULT false;

-- Mark all existing seed posts as demo
UPDATE public.posts SET is_demo = true WHERE author_id IS NULL;

-- ── UPDATE DEMO POSTS WITH PLACEHOLDER IMAGES ─────────────
-- Using picsum.photos for instant placeholders.
-- Replace these with AI-generated images later.
-- AI image prompts are provided as comments above each UPDATE.

-- Post 1: Hempcrete mix ratio guide
-- AI PROMPT: "Close-up of hands mixing hempcrete in a wooden form, warm golden light, lime binder and hemp hurd visible, workshop setting, photorealistic, earthy tones"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/hempcrete-mix/800/400'
WHERE title LIKE 'Hempcrete mix ratio guide%' AND is_demo = true;

-- Post 2: First hempcrete wall poured in Utah
-- AI PROMPT: "Workers pouring hempcrete into wooden wall forms on a construction site in Utah desert landscape, golden hour, dust in the air, teamwork, documentary photography style"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/utah-hemp-wall/800/400'
WHERE title LIKE 'First hempcrete wall poured%' AND is_demo = true;

-- Post 4: Open-source greywater system
-- AI PROMPT: "A handmade greywater filtration system with PVC pipes and gravel beds in a sunny backyard garden, water flowing through, DIY aesthetic, lush green plants around it, warm natural light"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/greywater-system/800/400'
WHERE title LIKE 'Open-sourcing our complete greywater%' AND is_demo = true;

-- Post 7: Neighborhood energy independence
-- AI PROMPT: "Aerial view of a small neighborhood with solar panels on every rooftop, desert Southwest setting with mountains in background, golden hour, community feel, bright and hopeful"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/solar-coop/800/400'
WHERE title LIKE '%neighborhood co-op officially hit energy%' AND is_demo = true;

-- Post 8: Food forest design
-- AI PROMPT: "Lush permaculture food forest garden with layered canopy of fruit trees, berry bushes, and ground cover plants, misty morning light in Ireland, pathways winding through, abundant and wild"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/food-forest/800/400'
WHERE title LIKE '%food forest design%' AND is_demo = true;

-- Post 10: Hand-built cabin move-in
-- AI PROMPT: "Small beautiful timber frame cabin (280 sq ft) nestled in the Appalachian forest, metal roof, a porch with a woodstove chimney, morning fog, warm interior light glowing from windows, cozy and handmade"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/tiny-cabin/800/400'
WHERE title LIKE 'Moved into my hand-built%' AND is_demo = true;

-- Post 12: Free Douglas fir salvage
-- AI PROMPT: "Stacks of beautiful reclaimed old-growth Douglas fir lumber with rich honey patina in a warehouse, beams of light streaming through industrial windows, 1920s warehouse deconstruction, beautiful wood grain"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/salvage-fir/800/400'
WHERE title LIKE '%old-growth Douglas fir%' AND is_demo = true;

-- Post 14: LoRa mesh network
-- AI PROMPT: "Small solar-powered LoRa radio node mounted on a wooden post in the Cascade mountains, antenna pointing at forested ridgeline, clear sky, off-grid technology meets wilderness, documentary style"
UPDATE public.posts
SET image_url = 'https://picsum.photos/seed/lora-mesh/800/400'
WHERE title LIKE '%LoRa mesh network%' AND is_demo = true;


-- ── VERIFY ──────────────────────────────────────────────
-- Check that images were added:
-- SELECT title, image_url FROM public.posts WHERE image_url IS NOT NULL;
