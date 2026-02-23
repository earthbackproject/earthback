# Earthback Database Migrations

All SQL files for the Supabase Postgres database.

## Migration Order & Status

| # | File | Status | Run Date | Notes |
|---|---|---|---|---|
| 1 | SEED_POSTS.sql | ✅ Run | 2026-02-20 | Creates `posts` table + RLS + 14 demo posts (is_demo=true) |
| 2 | SCHEMA_V2.sql | ✅ Run | 2026-02-20 | Creates projects, project_members, project_needs, certifications, media_links; extends posts |
| 3 | PROFILE_MIGRATION.sql | ❌ Not run | — | Profile table updates — run before V3 |
| 4 | SCHEMA_V3_messages.sql | ❌ Not run | — | Creates conversations, conversation_participants, messages tables with RLS |
| 5 | SCHEMA_V4_post_images.sql | ❌ Not run | — | Adds image_url + is_demo columns; sets AI-generated image paths on 8 demo posts |
| 6 | SCHEMA_V5_visions.sql | ❌ Not run | — | Creates visions table for AI Visualizer saved renders; needs 'visions' Storage bucket |

## How to Run

1. Open [Supabase SQL Editor](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/sql)
2. Paste the contents of each file **in order**
3. Click Run
4. Update this table when done

## Setup

See `SUPABASE_SETUP.md` in this folder for initial Supabase project configuration.

## Supabase Project

- **Project ID:** yptktmzagctusbeqdaty
- **Dashboard:** https://supabase.com/dashboard/project/yptktmzagctusbeqdaty
