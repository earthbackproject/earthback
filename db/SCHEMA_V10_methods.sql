-- ============================================================
-- SCHEMA_V10_methods.sql
-- Construction Methods Directory + Member Skill Badges
-- Run in Supabase SQL Editor
-- ============================================================

-- 1. Construction Methods table
CREATE TABLE IF NOT EXISTS construction_methods (
  id            SERIAL PRIMARY KEY,
  sort_order    INT NOT NULL,
  slug          TEXT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  subtitle      TEXT,
  category      TEXT NOT NULL CHECK (category IN ('green', 'conventional')),
  difficulty    TEXT CHECK (difficulty IN ('easy', 'moderate', 'hard')),
  badges        JSONB DEFAULT '[]',          -- display tags like "Earth-Based", "Zero Waste"
  description   TEXT,                         -- main writeup paragraph(s)
  materials     JSONB DEFAULT '[]',          -- array of strings
  climates      JSONB DEFAULT '[]',          -- array of strings
  pros          JSONB DEFAULT '[]',          -- advantages
  cons          JSONB DEFAULT '[]',          -- limitations
  practitioners JSONB DEFAULT '[]',          -- notable practitioners / resources
  image_folder  TEXT,                         -- e.g. "01-cob" — maps to reference images
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Index for public listing (sorted by sort_order)
CREATE INDEX IF NOT EXISTS idx_methods_sort ON construction_methods (sort_order);

-- 2. Member Skills — links a member to a method with an experience tier
--    Tiers: curious → hands_on → experienced → trainer
CREATE TABLE IF NOT EXISTS member_skills (
  id          SERIAL PRIMARY KEY,
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  method_id   INT  NOT NULL REFERENCES construction_methods(id) ON DELETE CASCADE,
  tier        TEXT NOT NULL CHECK (tier IN ('curious', 'hands_on', 'experienced', 'trainer')),
  note        TEXT,                          -- optional: "Built a cob oven in 2019"
  claimed_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (user_id, method_id)               -- one claim per method per member
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_member_skills_user   ON member_skills (user_id);
CREATE INDEX IF NOT EXISTS idx_member_skills_method ON member_skills (method_id);
CREATE INDEX IF NOT EXISTS idx_member_skills_tier   ON member_skills (tier);

-- 3. Row-Level Security
ALTER TABLE construction_methods ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_skills ENABLE ROW LEVEL SECURITY;

-- Methods: anyone can read, no public writes
CREATE POLICY "Methods are publicly readable"
  ON construction_methods FOR SELECT
  USING (true);

-- Member skills: anyone can read (public profiles), members manage their own
CREATE POLICY "Skills are publicly readable"
  ON member_skills FOR SELECT
  USING (true);

CREATE POLICY "Members can insert their own skills"
  ON member_skills FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Members can update their own skills"
  ON member_skills FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Members can delete their own skills"
  ON member_skills FOR DELETE
  USING (auth.uid() = user_id);

-- 4. Helper view: method with claim counts (for the public listing)
CREATE OR REPLACE VIEW method_stats AS
SELECT
  cm.*,
  COALESCE(ms.total_claims, 0)   AS total_claims,
  COALESCE(ms.trainer_count, 0)  AS trainer_count,
  COALESCE(ms.experienced_count, 0) AS experienced_count
FROM construction_methods cm
LEFT JOIN (
  SELECT
    method_id,
    COUNT(*)                                    AS total_claims,
    COUNT(*) FILTER (WHERE tier = 'trainer')    AS trainer_count,
    COUNT(*) FILTER (WHERE tier = 'experienced') AS experienced_count
  FROM member_skills
  GROUP BY method_id
) ms ON ms.method_id = cm.id
ORDER BY cm.sort_order;

-- 5. RPC: Claim or update a skill
CREATE OR REPLACE FUNCTION claim_skill(
  p_method_id INT,
  p_tier TEXT,
  p_note TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_result  member_skills;
BEGIN
  IF v_user_id IS NULL THEN
    RETURN jsonb_build_object('error', 'Not authenticated');
  END IF;

  IF p_tier NOT IN ('curious', 'hands_on', 'experienced', 'trainer') THEN
    RETURN jsonb_build_object('error', 'Invalid tier');
  END IF;

  INSERT INTO member_skills (user_id, method_id, tier, note)
  VALUES (v_user_id, p_method_id, p_tier, p_note)
  ON CONFLICT (user_id, method_id)
  DO UPDATE SET
    tier       = EXCLUDED.tier,
    note       = EXCLUDED.note,
    updated_at = NOW()
  RETURNING * INTO v_result;

  RETURN jsonb_build_object(
    'ok', true,
    'method_id', v_result.method_id,
    'tier', v_result.tier
  );
END;
$$;

-- 6. RPC: Remove a skill claim
CREATE OR REPLACE FUNCTION unclaim_skill(p_method_id INT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_user_id UUID := auth.uid();
BEGIN
  IF v_user_id IS NULL THEN
    RETURN jsonb_build_object('error', 'Not authenticated');
  END IF;

  DELETE FROM member_skills
  WHERE user_id = v_user_id AND method_id = p_method_id;

  RETURN jsonb_build_object('ok', true, 'method_id', p_method_id);
END;
$$;

-- ============================================================
-- DONE — Now run SCHEMA_V10_seed.sql to populate the 30 methods
-- ============================================================
