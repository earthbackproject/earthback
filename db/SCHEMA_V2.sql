-- ============================================================
-- Earthback — Schema v2: Projects, Certifications, Media Links
-- Run this in Supabase SQL Editor AFTER the existing profiles
-- and posts tables are in place.
-- ============================================================


-- ── PROJECTS TABLE ────────────────────────────────────────
-- A "project" can be a build, a company, an org, a campaign,
-- or any named entity that a person sponsors/owns.

CREATE TABLE IF NOT EXISTS public.projects (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Owner — the person who created this project page
  owner_id      UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  -- Identity
  name          TEXT NOT NULL,
  slug          TEXT UNIQUE NOT NULL,              -- URL-safe: "taos-adu-hempcrete"
  tagline       TEXT,                               -- one-liner under the name
  description   TEXT,                               -- full bio / about section
  cover_color   TEXT DEFAULT '#1F3A2E',             -- fallback gradient color

  -- Classification
  project_type  TEXT NOT NULL DEFAULT 'project'
    CHECK (project_type IN ('project','company','organization','campaign')),
  status        TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('forming','active','paused','complete','archived')),

  -- Location
  location      TEXT,                               -- free text: "Taos, New Mexico"
  latitude      DOUBLE PRECISION,
  longitude     DOUBLE PRECISION,

  -- Circle affiliation (primary circle this project belongs to)
  circle_slug   TEXT,
  circle_label  TEXT,

  -- Media & links
  website_url   TEXT,
  youtube_url   TEXT,
  instagram_url TEXT,
  other_links   JSONB DEFAULT '[]'::jsonb,          -- [{label, url}, ...]

  -- Engagement
  follower_count INTEGER DEFAULT 0,
  member_count   INTEGER DEFAULT 0,

  -- Flags
  is_public     BOOLEAN DEFAULT true,
  is_verified   BOOLEAN DEFAULT false,
  is_demo       BOOLEAN DEFAULT false,              -- sample/seed data flag

  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public projects are viewable by everyone"
  ON public.projects FOR SELECT
  USING (is_public = true);

CREATE POLICY "Owners can manage their own projects"
  ON public.projects FOR ALL
  USING (auth.uid() = owner_id)
  WITH CHECK (auth.uid() = owner_id);

-- Indexes
CREATE INDEX IF NOT EXISTS projects_owner_idx      ON public.projects(owner_id);
CREATE INDEX IF NOT EXISTS projects_slug_idx       ON public.projects(slug);
CREATE INDEX IF NOT EXISTS projects_circle_idx     ON public.projects(circle_slug);
CREATE INDEX IF NOT EXISTS projects_type_idx       ON public.projects(project_type);
CREATE INDEX IF NOT EXISTS projects_created_idx    ON public.projects(created_at DESC);


-- ── PROJECT MEMBERS (many-to-many) ───────────────────────
-- People who collaborate on a project (beyond the owner).

CREATE TABLE IF NOT EXISTS public.project_members (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  UUID NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
  profile_id  UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  role        TEXT DEFAULT 'member'
    CHECK (role IN ('member','admin','contributor','advisor')),
  joined_at   TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(project_id, profile_id)
);

ALTER TABLE public.project_members ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Project members are public"
  ON public.project_members FOR SELECT
  USING (true);

CREATE POLICY "Project admins can manage members"
  ON public.project_members FOR ALL
  USING (
    auth.uid() IN (
      SELECT owner_id FROM public.projects WHERE id = project_id
    )
  );

CREATE INDEX IF NOT EXISTS pm_project_idx ON public.project_members(project_id);
CREATE INDEX IF NOT EXISTS pm_profile_idx ON public.project_members(profile_id);


-- ── CERTIFICATIONS TABLE ─────────────────────────────────
-- Verifiable credentials, build certs, training completions.
-- Displayed on profile pages like a mini-LinkedIn credentials pane.

CREATE TABLE IF NOT EXISTS public.certifications (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  -- Cert details
  title           TEXT NOT NULL,                     -- "Certified Hempcrete Installer"
  issuing_org     TEXT NOT NULL,                     -- "Hemp Building Association"
  issuing_url     TEXT,                              -- link to the org
  credential_id   TEXT,                              -- external credential number
  credential_url  TEXT,                              -- link to verify

  -- Dates
  issued_date     DATE,
  expiry_date     DATE,                              -- NULL = does not expire

  -- Display
  badge_icon      TEXT DEFAULT '🏅',                 -- emoji or icon key
  is_verified     BOOLEAN DEFAULT false,             -- Earthback has verified this
  is_demo         BOOLEAN DEFAULT false,

  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.certifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Certifications are public"
  ON public.certifications FOR SELECT
  USING (true);

CREATE POLICY "Users manage their own certifications"
  ON public.certifications FOR ALL
  USING (auth.uid() = profile_id)
  WITH CHECK (auth.uid() = profile_id);

CREATE INDEX IF NOT EXISTS certs_profile_idx ON public.certifications(profile_id);


-- ── MEDIA LINKS TABLE ────────────────────────────────────
-- External content (YouTube, articles, podcasts, etc.) that
-- a user or project wants to showcase. When added, the system
-- can auto-generate a feed post of type 'media'.

CREATE TABLE IF NOT EXISTS public.media_links (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Owner: either a profile or a project (one must be set)
  profile_id    UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  project_id    UUID REFERENCES public.projects(id) ON DELETE CASCADE,

  -- Link details
  url           TEXT NOT NULL,
  title         TEXT NOT NULL,
  description   TEXT,
  thumbnail_url TEXT,                               -- og:image or yt thumbnail
  platform      TEXT                                -- auto-detected: youtube, instagram, podcast, article, other
    CHECK (platform IN ('youtube','instagram','tiktok','podcast','article','website','other')),

  -- Classification
  content_type  TEXT DEFAULT 'video'
    CHECK (content_type IN ('video','article','podcast','tutorial','gallery','other')),
  circle_slug   TEXT,                               -- which circle this belongs to

  -- Auto-post flag
  auto_posted   BOOLEAN DEFAULT false,              -- has a feed post been created from this?
  post_id       UUID REFERENCES public.posts(id) ON DELETE SET NULL,

  -- Flags
  is_pinned     BOOLEAN DEFAULT false,
  is_demo       BOOLEAN DEFAULT false,

  created_at    TIMESTAMPTZ DEFAULT NOW(),

  -- At least one owner must be set
  CHECK (profile_id IS NOT NULL OR project_id IS NOT NULL)
);

ALTER TABLE public.media_links ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Media links are public"
  ON public.media_links FOR SELECT
  USING (true);

CREATE POLICY "Profile owners manage their media"
  ON public.media_links FOR ALL
  USING (auth.uid() = profile_id)
  WITH CHECK (auth.uid() = profile_id);

CREATE INDEX IF NOT EXISTS media_profile_idx  ON public.media_links(profile_id);
CREATE INDEX IF NOT EXISTS media_project_idx  ON public.media_links(project_id);
CREATE INDEX IF NOT EXISTS media_platform_idx ON public.media_links(platform);


-- ── UPDATE POSTS TABLE — add 'media' post type ──────────
-- Extend the CHECK constraint to allow 'media' as a post_type.

ALTER TABLE public.posts DROP CONSTRAINT IF EXISTS posts_post_type_check;
ALTER TABLE public.posts ADD CONSTRAINT posts_post_type_check
  CHECK (post_type IN ('milestone','resource','need','question','coordination','celebration','media'));

-- Add optional project_id to posts (so a project can be the "author")
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS media_url TEXT;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS media_thumbnail TEXT;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS is_demo BOOLEAN DEFAULT false;

CREATE INDEX IF NOT EXISTS posts_project_idx ON public.posts(project_id);


-- ── PROJECT NEEDS (structured) ───────────────────────────
-- What a project currently needs — displayed as pills on the
-- project page and surfaced in the feed.

CREATE TABLE IF NOT EXISTS public.project_needs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  UUID NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  is_urgent   BOOLEAN DEFAULT false,
  is_filled   BOOLEAN DEFAULT false,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.project_needs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Needs are public"
  ON public.project_needs FOR SELECT
  USING (true);

CREATE POLICY "Project owners manage needs"
  ON public.project_needs FOR ALL
  USING (
    auth.uid() IN (
      SELECT owner_id FROM public.projects WHERE id = project_id
    )
  );

CREATE INDEX IF NOT EXISTS needs_project_idx ON public.project_needs(project_id);


-- ── VERIFY ───────────────────────────────────────────────
-- SELECT 'projects'       AS tbl, count(*) FROM public.projects
-- UNION ALL
-- SELECT 'certifications' AS tbl, count(*) FROM public.certifications
-- UNION ALL
-- SELECT 'media_links'    AS tbl, count(*) FROM public.media_links
-- UNION ALL
-- SELECT 'project_needs'  AS tbl, count(*) FROM public.project_needs;
