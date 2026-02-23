# Earthback Creator Profiles & Content Libraries — Build Handoff

## Context

This extends the ghost profile system (see `earthback_ghost_profiles_handoff.md`) to **content creators**. Same search-trigger-invite pattern, but instead of a business card, the ghost profile is a **content library** — the creator's YouTube channel, podcast archive, blog posts, or any combination, imported and organized inside Earthback.

The companion mockup (`earthback_creator_profiles_mockup.html`) shows three states. Use it as the design spec.

This builds on the same profile system as business ghost profiles. Don't build a separate system — a creator profile IS a profile with `type: "creator"` and a content library attached.

---

## The Core Flow

1. Member searches "hempcrete building tutorial"
2. System returns existing Earthback content + auto-generated ghost creator profiles from YouTube, podcasts, blogs
3. Member clicks into a ghost creator → sees their full imported library, organized by AI-generated categories, playable inline
4. Member clicks "Invite to Earthback" → creator gets an email with the personal note + social proof
5. Creator clicks claim link → sees their library + community notes + who's waiting → claims it
6. Creator controls what's shown, publishes when ready, new content auto-syncs

---

## Content Sources (ranked by ease of integration)

### Tier 1: Trivially Easy (public API or RSS, legal embeds)

**YouTube**
- API: YouTube Data API v3 (Google Cloud, free tier = 10K quota units/day)
- What you get: every video (title, description, thumbnail, duration, view count, publish date), playlists, channel metadata, subscriber count
- Embed: `<iframe src="https://www.youtube.com/embed/{videoId}">`  — free, legal, creator gets their views/ad revenue
- Auto-sync: YouTube supports PubSubHubbub (now called WebSub) for push notifications on new uploads. Alternatively, poll the uploads playlist daily.
- Quota note: a full channel scan (list all videos) costs ~100-300 quota units depending on channel size. 10K/day = ~30-100 full scans.

**Podcasts (RSS)**
- API: none needed — every podcast has a public RSS feed (XML)
- What you get: every episode (title, description, duration, publish date, direct audio file URL)
- Embed: native HTML `<audio>` element with the direct MP3 URL. No iframe needed, no third-party dependency.
- Auto-sync: poll the RSS feed daily. New items appear at the top.
- Discovery: use Apple Podcasts Search API or Podcast Index API to find podcasts by name/topic and get their RSS feed URL.

**Blogs / Substack / WordPress / Ghost**
- API: RSS feed (nearly universal). Substack, WordPress, Ghost, Medium all expose RSS.
- What you get: every post (title, excerpt or full text, publish date, author, tags)
- Embed: display post excerpts inline, link to original for full read. Or display full text if the RSS feed includes it (many do).
- Auto-sync: poll RSS daily.
- Discovery: search for `{site} RSS feed` or try `{url}/feed`, `{url}/rss`, `{url}/feed.xml`.

**Vimeo**
- API: Vimeo API (free tier, needs registration)
- What you get: videos, metadata, thumbnails, embed codes
- Embed: `<iframe src="https://player.vimeo.com/video/{id}">`
- Less common than YouTube in this space but some documentary/workshop creators use it.

### Tier 2: Moderate Effort (API exists but needs more work)

**GitHub**
- API: GitHub REST API (generous free tier)
- What you get: repos, READMEs, stars, descriptions, topics
- Useful for: open-source building plans, design files, calculation tools, material databases
- Display: show repo cards with descriptions, link to GitHub for code

**Instagram**
- API: Meta Basic Display API (requires app review for long-term access)
- What you get: public posts, images, captions
- Embed: Instagram oEmbed endpoint (requires their JS SDK, clunkier than YouTube)
- Relevance: many natural builders post visual portfolios here
- Caveat: Meta's API access is more restrictive and changes frequently. Consider this Phase 2+.

**Eventbrite / Lu.ma**
- API: Eventbrite API (free tier)
- What you get: events (title, description, date, location, ticket info)
- Useful for: workshop facilitators, conference organizers
- Display: event cards with dates, "X workshops hosted" as a profile signal

### Tier 3: Scraping Required (no clean API)

**Google Scholar / ResearchGate** — publication lists for researchers
**Personal websites** — AI extraction from arbitrary web pages
**Facebook groups** — technically scrapeable but legally questionable, skip

### Recommendation: Start with YouTube + Podcasts + Blogs

These three cover 90%+ of the content in the natural building / sustainability space and are all trivially easy to integrate. Add Vimeo and GitHub in Phase 2. Leave Instagram and events for Phase 3.

---

## Data Model

Extends the ghost profile schema. A creator profile has a `content_sources` array and a `content_items` collection.

```
creator_profile extends ghost_profile {
  type: "creator"
  
  // Content sources (can have multiple)
  content_sources: [
    {
      platform: "youtube" | "podcast" | "blog" | "vimeo" | "github"
      source_id: string  // YouTube channel ID, RSS feed URL, etc.
      source_url: string // public URL for the source
      source_name: string
      subscriber_count: int | null
      last_synced: timestamp
      auto_sync: boolean (default true, owner can toggle off)
      total_items: int
    }
  ]
  
  // AI-generated categories (from title/description analysis)
  categories: [
    {
      name: string  // "Construction Techniques", "Tool Reviews", etc.
      icon: string  // emoji
      item_count: int
      generated_by: "ai" | "manual"  // owner can rename/reorganize
    }
  ]
}

content_item {
  id: uuid
  profile_id: uuid (FK to creator_profile)
  source_platform: "youtube" | "podcast" | "blog" | "vimeo" | "github"
  
  // Platform-specific ID
  platform_id: string  // YouTube video ID, podcast episode GUID, etc.
  
  // Metadata (pulled from API)
  title: string
  description: string
  thumbnail_url: string | null
  duration_seconds: int | null
  publish_date: timestamp
  view_count: int | null
  
  // Earthback-specific
  category_id: uuid | null (FK to categories)
  tags: string[]  // AI-generated from title + description
  
  // Embed data
  embed_type: "youtube_iframe" | "audio_player" | "article_preview" | "vimeo_iframe"
  embed_url: string  // YouTube embed URL, audio file URL, article URL
  
  // Community layer
  community_notes: [
    {
      user_id: uuid
      text: string
      timestamp_ref: string | null  // "skip to 6:30"
      created_at: timestamp
    }
  ]
  upvotes: int
  upvoted_by: user_id[]
}
```

---

## Search-Triggered Creation Flow

### When someone searches for content:

1. **Check internal:** search existing Earthback profiles + content items for matches
2. **Check external sources in parallel:**
   - YouTube Data API: `GET /youtube/v3/search?q={query}&type=channel,video`
   - Podcast Index API or Apple Podcasts Search: search by query
   - (Optional) Web search + AI extraction for blogs
3. **Deduplicate:** match external results against existing ghost profiles (fuzzy match on channel name + platform ID)
4. **Create ghost profiles** for new channels/podcasts/blogs found
5. **Import content library** for each new ghost profile (async — start immediately, complete in background)
6. **AI categorization pass:** run titles + descriptions through Claude Haiku to generate categories and tags
7. **Return blended results:** existing Earthback profiles first, then ghost profiles, sorted by relevance

### Content import (background job):

For a YouTube channel with 500 videos, the full import takes ~5-10 API calls (50 results per page). Store all metadata. Don't download any media — just store IDs and use embeds for playback.

For a podcast with 200 episodes, it's a single RSS fetch.

For a blog, it's a single RSS fetch.

**Cache aggressively.** Once imported, the library is stored locally. Daily sync checks for new items only.

---

## AI Categorization

After importing a content library, run a batch through Claude Haiku:

```
Given these video/episode titles and descriptions from a content creator's library,
generate 4-8 categories that organize this content for someone interested in
natural building, sustainable construction, and community development.

Return JSON: [{ "name": "Category Name", "icon": "emoji", "item_ids": [...] }]

Titles:
1. "Hempcrete Wall Pour — Complete Process"
2. "The Only Trowels You'll Ever Need"
3. "Foundation Layout — Getting It Right"
...
```

Cost: ~$0.01-0.03 per channel (Haiku is very cheap). Run once on import, re-run when owner claims and new items sync.

The owner can rename, merge, or reorganize categories after claiming. The AI-generated ones are a starting point.

---

## Playback

**YouTube:** Standard iframe embed in a modal overlay. When user clicks a video card, open a modal with `<iframe src="https://www.youtube.com/embed/{videoId}" allowfullscreen>`. The video plays inline without leaving Earthback. Creator gets their view counted.

**Podcasts:** Native HTML5 audio player. `<audio controls src="{episode_mp3_url}">`. Can be styled to match Earthback's design. Episode plays inline.

**Blogs:** Show the article excerpt or full text (if RSS provides it) in an expandable card. Link to original for full read.

**Vimeo:** Same iframe pattern as YouTube: `<iframe src="https://player.vimeo.com/video/{id}">`

---

## Community Layer

The differentiator over just linking to YouTube. Members can:

**Add notes to content items** — "Skip to 6:30 for the mix ratio" or "This technique worked great on my cob build." Notes are visible on the content card and in the library page sidebar. Requires Earthback account.

**Upvote content items** — surfaces the most useful content to the top of each category. "Most upvoted" becomes a sort option.

**Link content to projects** — a member working on a hempcrete project can link a tutorial video to their project post: "We followed this technique." Creates a web of connections between content and real work.

**Link content to circle discussions** — someone posts a question in Natural Building, another member links a video from a creator's library as the answer. The video now has context within the community conversation.

---

## Creator Claim Experience

When a creator clicks their claim link, they see everything a public viewer sees PLUS:

**Claim banner:** "Your content library is waiting for you. The Earthback community has been watching your videos and wants you here." Shows who invited them, their personal note, and social proof (X people searched, Y vouched, Z will be notified when you publish).

**Content sync settings** (sidebar toggles):
- Auto-import new uploads (on by default)
- Show view counts (on by default)
- Allow community notes (on by default)
- Show in circle feeds (off by default — let them opt in)

**Suggested circles** based on content categories.

After claiming, they can edit their bio, reorganize categories, hide specific videos, and publish when ready.

---

## Integration with Existing Systems

### Ghost Profiles
Creator profiles ARE ghost profiles with `type: "creator"` and a content library attached. Same claim flow, same status progression (ghost → invited → claimed → published), same social proof system.

### Circles
Published creator libraries surface in relevant circles. New auto-synced content can appear as feed items: "Essential Craftsman posted a new video: 'Advanced Hempcrete Techniques'" — if the creator has enabled "Show in circle feeds."

### Search
Content items are searchable alongside posts, profiles, and projects. A search for "hempcrete mix ratio" might return: a circle post, a creator's video (with a community note saying "skip to 6:30"), and a blog article — all from different sources, all inside Earthback.

### Profiles
A creator's library is a tab on their profile page. If they're also a business (e.g., they sell hempcrete AND make videos about it), they have both a business profile and a content library — same profile, two facets.

### Visualizer
Future: creator content could be linked to AI visualizer renders. "Want to learn how to build this? Here are 3 videos from creators in your circles."

---

## YouTube API Specifics

### Setup
1. Create a Google Cloud project
2. Enable YouTube Data API v3
3. Create an API key (no OAuth needed for public data)
4. Free quota: 10,000 units/day

### Key endpoints

**Find a channel:**
```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &q=essential+craftsman
  &type=channel
  &key={API_KEY}
```
Returns channel IDs matching the search. Cost: 100 units.

**Get channel details:**
```
GET https://www.googleapis.com/youtube/v3/channels
  ?part=snippet,contentDetails,statistics
  &id={CHANNEL_ID}
  &key={API_KEY}
```
Returns subscriber count, description, and the "uploads" playlist ID. Cost: 1 unit.

**List all videos (via uploads playlist):**
```
GET https://www.googleapis.com/youtube/v3/playlistItems
  ?part=snippet,contentDetails
  &playlistId={UPLOADS_PLAYLIST_ID}
  &maxResults=50
  &key={API_KEY}
```
Paginate with `pageToken`. 50 items per page. Cost: 1 unit per page.

**Get video details (duration, view count):**
```
GET https://www.googleapis.com/youtube/v3/videos
  ?part=contentDetails,statistics
  &id={VIDEO_ID_1},{VIDEO_ID_2},...
  &key={API_KEY}
```
Batch up to 50 video IDs per request. Cost: 1 unit.

**Get playlists:**
```
GET https://www.googleapis.com/youtube/v3/playlists
  ?part=snippet,contentDetails
  &channelId={CHANNEL_ID}
  &maxResults=50
  &key={API_KEY}
```

### New upload detection
YouTube supports WebSub (formerly PubSubHubbub). Subscribe to a channel's feed:
```
POST https://pubsubhubbub.appspot.com/subscribe
  hub.callback={YOUR_WEBHOOK_URL}
  hub.topic=https://www.youtube.com/xml/feeds/videos.xml?channel_id={CHANNEL_ID}
  hub.mode=subscribe
```
YouTube will POST to your webhook when the channel uploads a new video. Subscriptions expire after ~10 days and need renewal, so also poll daily as a fallback.

---

## Podcast RSS Specifics

### Finding the RSS feed
- **Apple Podcasts Search API:** `GET https://itunes.apple.com/search?term={query}&media=podcast` — returns feed URLs
- **Podcast Index API:** free, open-source alternative to Apple's search. `GET https://api.podcastindex.org/api/1.0/search/byterm?q={query}`
- **Manual:** most podcasts list their RSS URL on their website or podcast page

### Parsing RSS
Standard XML parsing. Each `<item>` in the feed is an episode:
```xml
<item>
  <title>Episode Title</title>
  <description>Episode description...</description>
  <enclosure url="https://example.com/episode.mp3" type="audio/mpeg" length="54321"/>
  <pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate>
  <itunes:duration>3600</itunes:duration>
</item>
```

The `<enclosure>` URL is the direct audio file. Use it in an HTML5 `<audio>` player.

### Embedding
```html
<audio controls preload="none">
  <source src="{episode_mp3_url}" type="audio/mpeg">
</audio>
```
Style the player to match Earthback's design using CSS or a lightweight audio player library.

---

## Implementation Phases

### Phase 1: YouTube Only (ship first)
- YouTube channel search via Data API
- Ghost creator profile creation from channel data
- Full video library import + storage
- AI categorization (Claude Haiku)
- Video grid display with YouTube iframe embed playback
- Invite flow (reuse ghost profile invitation system)
- Claim flow with content sync settings

### Phase 2: Podcasts + Blogs + Community Layer
- RSS feed discovery and parsing
- Podcast episode display with inline audio player
- Blog article display with excerpt/link
- Community notes on content items
- Upvoting
- Multi-source profiles (one creator with YouTube + podcast + blog)

### Phase 3: Auto-Sync + Deep Integration
- WebSub for YouTube new upload notifications
- Daily RSS polling for podcasts and blogs
- New content → circle feed posts (if creator enables)
- Content ↔ project linking
- Content ↔ circle discussion linking
- Vimeo, GitHub, Eventbrite sources
- "Learn how to build this" connections from Visualizer to creator content
