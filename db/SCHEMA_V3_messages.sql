-- ============================================================
-- Earthback — Schema v3: Messages & Conversations
-- Run this in Supabase SQL Editor AFTER Schema v2.
-- Supports: "I can help" threads, direct messages, project threads.
-- ============================================================


-- ── CONVERSATIONS TABLE ────────────────────────────────────
-- A conversation between two or more users, optionally tied to
-- a project need. Thread-based: one conversation per topic.

CREATE TABLE IF NOT EXISTS public.conversations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Context — what started this thread
  project_id    UUID REFERENCES public.projects(id) ON DELETE SET NULL,
  need_id       UUID REFERENCES public.project_needs(id) ON DELETE SET NULL,
  subject       TEXT,                               -- auto-generated or user-provided

  -- Participants stored via conversation_participants table
  -- Type helps with filtering
  conv_type     TEXT NOT NULL DEFAULT 'direct'
    CHECK (conv_type IN ('direct','project_help','project_team','system')),

  -- Timestamps
  last_message_at TIMESTAMPTZ DEFAULT NOW(),
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;

-- Users can only see conversations they participate in
CREATE POLICY "Users see own conversations"
  ON public.conversations FOR SELECT
  USING (
    id IN (
      SELECT conversation_id FROM public.conversation_participants
      WHERE profile_id = auth.uid()
    )
  );

CREATE POLICY "Authenticated users can create conversations"
  ON public.conversations FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE INDEX IF NOT EXISTS conv_project_idx ON public.conversations(project_id);
CREATE INDEX IF NOT EXISTS conv_need_idx ON public.conversations(need_id);
CREATE INDEX IF NOT EXISTS conv_last_msg_idx ON public.conversations(last_message_at DESC);


-- ── CONVERSATION PARTICIPANTS ──────────────────────────────

CREATE TABLE IF NOT EXISTS public.conversation_participants (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
  profile_id      UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  joined_at       TIMESTAMPTZ DEFAULT NOW(),
  last_read_at    TIMESTAMPTZ DEFAULT NOW(),
  is_muted        BOOLEAN DEFAULT false,

  UNIQUE(conversation_id, profile_id)
);

ALTER TABLE public.conversation_participants ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own participations"
  ON public.conversation_participants FOR SELECT
  USING (profile_id = auth.uid());

CREATE POLICY "Users can join conversations"
  ON public.conversation_participants FOR INSERT
  WITH CHECK (profile_id = auth.uid());

CREATE POLICY "Users can update own participation"
  ON public.conversation_participants FOR UPDATE
  USING (profile_id = auth.uid());

CREATE INDEX IF NOT EXISTS cp_conv_idx ON public.conversation_participants(conversation_id);
CREATE INDEX IF NOT EXISTS cp_profile_idx ON public.conversation_participants(profile_id);


-- ── MESSAGES TABLE ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS public.messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
  sender_id       UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  body            TEXT NOT NULL,
  message_type    TEXT NOT NULL DEFAULT 'text'
    CHECK (message_type IN ('text','system','offer','media')),

  -- Optional: reference to a need this message is about
  need_id         UUID REFERENCES public.project_needs(id) ON DELETE SET NULL,

  -- Metadata
  is_edited       BOOLEAN DEFAULT false,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Users can only see messages in conversations they participate in
CREATE POLICY "Users see messages in own conversations"
  ON public.messages FOR SELECT
  USING (
    conversation_id IN (
      SELECT conversation_id FROM public.conversation_participants
      WHERE profile_id = auth.uid()
    )
  );

CREATE POLICY "Users can send messages to own conversations"
  ON public.messages FOR INSERT
  WITH CHECK (
    sender_id = auth.uid()
    AND conversation_id IN (
      SELECT conversation_id FROM public.conversation_participants
      WHERE profile_id = auth.uid()
    )
  );

CREATE INDEX IF NOT EXISTS msg_conv_idx ON public.messages(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS msg_sender_idx ON public.messages(sender_id);


-- ── HELPER: Update last_message_at on new message ──────────

CREATE OR REPLACE FUNCTION update_conversation_last_message()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.conversations
  SET last_message_at = NEW.created_at
  WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trg_update_conv_last_message
  AFTER INSERT ON public.messages
  FOR EACH ROW
  EXECUTE FUNCTION update_conversation_last_message();


-- ── VERIFY ─────────────────────────────────────────────────
-- SELECT 'conversations'              AS tbl, count(*) FROM public.conversations
-- UNION ALL
-- SELECT 'conversation_participants'  AS tbl, count(*) FROM public.conversation_participants
-- UNION ALL
-- SELECT 'messages'                   AS tbl, count(*) FROM public.messages;
