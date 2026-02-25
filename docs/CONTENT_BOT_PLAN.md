# Earthback Content Bot & Social Pipeline — Plan
*Written: 2026-02-25 | Status: Planning*

---

## What It Is

A platform-native automated account — **"Earthback Dispatch"** — that posts daily content across every circle. It acts like a member but is powered by a script. It keeps every circle alive and populated with relevant news and developments, even before real members are active in that circle.

These posts are also the raw material for the social media presence being built this week. The pipeline: bot posts on Earthback → curate/approve → auto-format for social → post.

---

## Why This Works

The core community problem: circles feel empty when there are 3 members in them. The Dispatch bot solves this before any real users show up. Someone joins the Hempcrete circle and sees a week's worth of posts about hempcrete techniques, project updates, and research. The circle is alive. They engage, post themselves, invite others.

The social media side works the same way: a daily stream of high-signal content about natural building, community housing, food systems, and solar, all formatted for sharing. No one has to write it. It comes from the platform itself.

---

## Bot Account Structure

### One platform-wide org account

**Earthback Dispatch** — an org-type profile on the platform (not a user account, but uses the same profiles/projects system).

```
display_name: "Earthback Dispatch"
username:     "dispatch"
bio:          "Daily developments in natural building, community housing, and resilient systems."
avatar:       Earthback logo / globe icon
is_bot:       true   (add this flag to profiles table)
```

The `is_bot` flag lets the frontend style bot posts differently (subtle badge: "Earthback Dispatch"), prevents bot accounts from appearing in "Find members near you," and ensures bot posts don't affect credit/like systems the same way member posts do.

### Circle-specific sub-accounts (later, optional)

Once the platform is mature, each major circle could have its own dispatch account:
- **Hempcrete Digest** — posts only in the Hempcrete circle
- **Solar & Energy Dispatch** — posts in solar/energy circles
- etc.

For launch: one unified Dispatch account, posts tagged to the relevant circle(s).

---

## What It Posts

### Content types

**1. Technique + knowledge posts** (most common)
Short summaries of a natural building technique, material property, or system. Educational. Examples:
- "Hempcrete has a ~40-year carbon absorption curve. Here's what that means for your build timeline."
- "Lime plaster breathability vs. vapor barriers — when each is right."
- "A 2-foot strawbale wall has R-30+ and can be built with 4 people in a weekend."

**2. Project spotlights** (2-3x per week)
Highlight a real build somewhere in the world — from the hotspot seed list, from partner orgs, from member projects. Always links to more.

**3. News roundup** (1x per day)
Aggregated from public sources: new research, policy changes, completed builds, funding announcements in the natural building / community housing space.

**4. Resource links** (ongoing)
Tools, calculators, downloadable guides, videos, training programs — useful, low-noise, no spam.

**5. Community prompts** (2-3x per week)
Questions that invite member response: "What's your go-to lime plaster mix ratio?" "Who's done a hempcrete build in a humid climate?" These drive engagement more than any other post type.

---

## The Social Media Pipeline

### The flow

```
Script generates post content
       ↓
Post created in Earthback Dispatch account (Supabase)
       ↓
Nicco reviews queue (takes 5 minutes, just approve/skip)
       ↓
Approved posts → format for social (auto-crop, add branding, add URL)
       ↓
Post to Twitter/X, Instagram, maybe LinkedIn
```

### Social format per post type

**Twitter/X:**
- First 2 sentences of the post
- Earthback URL or relevant external link
- 2-3 hashtags (#NaturalBuilding #Hempcrete #CommunityHousing)
- If post has an image (Flux-generated or linked photo): attach it

**Instagram:**
- Lead image (Flux asset or project photo) — required
- Caption = full post text
- Link in bio rotation (Linktree or similar, or just earthbackproject.org)
- Hashtag block: 10-15 tags

**LinkedIn (later):**
- Full post text, slightly more professional tone
- Best for the partner orgs / training / policy content

### The approval queue

A simple page — `admin/dispatch-queue.html` — shows today's pending posts. Nicco sees title + first 2 lines + target circle. One click = approve + schedule. One click = skip. No editing needed in phase 1 — if the content is wrong, fix the generation script.

Or even simpler pre-UI: a Supabase filter on `posts WHERE is_bot=true AND status='pending'` — approve by changing status to 'published' directly in the table view. Upgrade to a real UI when the volume warrants it.

---

## How Posts Are Generated

### Phase 1 — Curated seed content (start here)

Write 30-50 high-quality posts manually (or with Claude's help) across all the major circles. Load them into the database with `scheduled_for` timestamps spread out over the first 2-3 weeks.

This is the fastest path to launch and produces the highest quality content. No automation needed at first — just a well-curated seed pack.

### Phase 2 — Script-generated from known sources

A Python script (`generate-dispatch.py`) that:
1. Pulls from a curated list of RSS feeds (BuildingGreen.com, Natural Building Network, hempcrete.com, etc.)
2. Summarizes each item into 2-3 sentence post format
3. Assigns it to the correct circle based on topic keywords
4. Saves it to `posts` table with `status='pending'` and `author_id = dispatch_bot_id`
5. Runs daily via a scheduled task or cron

### Phase 3 — AI-generated original content

Claude (via API) generates original short posts on demand. Input: circle slug + topic seed. Output: formatted post ready to publish.

A daily script calls the Anthropic API with something like:
```
"Write a 3-sentence educational post about [topic] for a community of natural builders.
Tone: direct, knowledgeable, warm. No fluff. Include one specific fact or measurement."
```

Phase 3 is where the content becomes truly self-sustaining.

---

## Data Model Changes

### Profiles table
```sql
ALTER TABLE profiles ADD COLUMN is_bot BOOLEAN DEFAULT false;
ALTER TABLE profiles ADD COLUMN bot_type TEXT; -- 'dispatch', 'circle', etc.
```

### Posts table (assuming it exists from schema)
The existing posts table likely needs:
```sql
ALTER TABLE posts ADD COLUMN scheduled_for TIMESTAMPTZ; -- publish at this time
ALTER TABLE posts ADD COLUMN status TEXT DEFAULT 'published'
  CHECK (status IN ('draft','pending','published','archived'));
ALTER TABLE posts ADD COLUMN source_url TEXT; -- where the content came from (for news posts)
```

### Bot account seed
```sql
INSERT INTO profiles (id, username, display_name, bio, is_bot, bot_type, is_public)
VALUES (
  gen_random_uuid(),
  'dispatch',
  'Earthback Dispatch',
  'Daily developments in natural building, community housing, and resilient systems.',
  true,
  'dispatch',
  true
);
```

---

## Build Sequence

**Phase 1 — Seed content pack (this week, pre-code)**
1. Write 30-50 seed posts across all major circles (can do this in a session with Claude)
2. Create the Dispatch bot account in Supabase manually
3. Load seed posts with staggered `scheduled_for` timestamps
4. Circles are populated on day one of launch

**Phase 2 — Social formatting (this week)**
1. Decide platforms (Twitter, Instagram — start with two)
2. Write the post formatter (takes a post, outputs platform-specific text + image)
3. Manual posting initially — copy/paste from the queue. Not worth automating until volume is proven.

**Phase 3 — RSS → post pipeline (week 2)**
1. `generate-dispatch.py` script
2. Supabase pending queue
3. Simple approval flow (table view or admin page)
4. Scheduled run (Windows Task Scheduler or a Supabase cron function)

**Phase 4 — AI generation (week 3+)**
1. Claude API integration in the script
2. Prompt templates per circle
3. Automatic scheduling with human review gate

---

## Moonback / Marsback

Register these now. The namespace is valuable and the concept is obvious once Earthback proves out the model.

Natural building for off-world habitats is not science fiction — it's the actual direction of serious research. Basalt fiber (lunar regolith analog), mycelium composites, 3D-printed earthen structures — the Earthback knowledge base translates almost directly. The community of people thinking about this already exists and has nowhere to gather.

The same platform, the same circles structure, the same bot/dispatch system. Different context, same infrastructure. When the time comes, it's a template deployment.

For now: register the domains. Come back to it after Earthback launches.

---

## The Bigger Picture

The content bot + social pipeline is how the community becomes self-reinforcing. The sequence:

1. Dispatch bot keeps circles alive before members show up
2. New members join, see active circles, engage, post
3. Their posts + bot posts → social media queue
4. Social media drives more signups → more members posting
5. Member posts displace bot posts as the dominant content type
6. Bot shifts from "keeping the lights on" to "surfacing the best member content"

By the time the community is self-sustaining, the bot is a curation layer, not a content generator. That's the right end state.

The other thing this enables: the social media presence becomes a genuine signal about what the community is learning and doing. Not promotional content — actual knowledge. That's what gets shared. That's what builds trust. That's what makes someone say "I need to be in that room."
