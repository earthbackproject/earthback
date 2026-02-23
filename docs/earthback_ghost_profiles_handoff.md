# Earthback Ghost Profiles — Build Handoff

## Context

The live site is **earthbackproject.org** — a community platform with circles, feeds, and profiles. The **profile build page is the next push** in the main build thread. Ghost profiles should be built on top of that same profile system, not as a separate thing.

A companion mockup (`earthback_ghost_profiles_mockup.html`) shows three interactive states. Use it as the design spec.

---

## What Ghost Profiles Are

Pre-built profile shells for businesses, projects, organizations, and individual practitioners that don't have an Earthback account yet. They exist in the database, are publicly searchable in a basic form, but can only be fully seen and edited by the intended owner after they claim them via a unique link.

The core insight: **search becomes the profile creation engine.** When a member searches for an entity that doesn't exist on Earthback, the system auto-generates a ghost profile from public data and displays it immediately. The searcher can then invite that entity to claim it. Every search for a missing entity is a signal of community demand.

---

## Five Input Channels (all feed the same pipeline)

1. **Search-triggered auto-generation** — someone searches, entity not found, system creates ghost profile from web data in real time. This will be the dominant channel.
2. **Community nominations** — member fills out "Nominate a business/person" form, or mentions an entity in a post that triggers a prompt.
3. **Manual curation** — Earthback team creates ghost profiles for known entities (e.g., after a conference, from an industry directory).
4. **Web seeding** — scraper/AI agent pulls from directories and public sources, creates drafts for team review.
5. **Individual practitioners** — same pipeline, different profile type.

**Critical rule:** Search-triggered profiles can display immediately with basic public data. All other channels require human review before any invitation email goes out.

---

## Profile Status Flow

```
[search miss or manual creation]
        ↓
     GHOST — exists in DB, visible as basic card in search,
             not in circles or feed
        ↓
[someone clicks "Invite to Earthback"]
        ↓
     INVITED — claim email sent, claim token active (30-day expiry)
        ↓
[owner clicks claim link, sees full preview]
        ↓
     PREVIEWING — only visible to the owner via claim URL,
                  they see everything including who searched/vouched
        ↓
[owner creates account + claims profile]
        ↓
     CLAIMED — attached to user account, fully editable,
               still private (not in search/circles/feed)
        ↓
[owner hits publish toggle]
        ↓
     PUBLISHED — full profile visible in circles, searchable,
                 appears in feed as subtle "just joined" post
```

Owner can unpublish at any time (reverts to claimed, disappears from public).

---

## Data Model

```
ghost_profile {
  id: uuid
  type: "business" | "project" | "organization" | "practitioner"
  status: "ghost" | "invited" | "claimed" | "published"

  // Claim mechanics
  claim_token: string (cryptographically random, e.g. "eb_claim_8f3a9c2d7e...")
  claim_token_expires: timestamp (30 days from invite)
  claimed_by: user_id | null
  claimed_at: timestamp | null
  published_at: timestamp | null

  // Pre-populated data (from web enrichment)
  name: string
  location: string
  description: string
  website_url: string | null
  contact_email: string | null (for invitation delivery)
  phone: string | null
  category: string[]
  tags: string[]

  // Source tracking
  source: "search" | "nomination" | "manual" | "scraped"
  created_by_search_query: string | null
  nominated_by: user_id | null
  reviewed_by: admin_id | null
  reviewed_at: timestamp | null

  // Social signals
  search_count: int (incremented each time someone searches and sees this)
  vouched_by: user_id[] 
  followed_by: user_id[] (notified when published)
  invited_by: user_id | null
  invite_note: string | null (personal message from inviter)

  // After claim — owner edits these
  avatar: image_url | null
  cover_image: image_url | null
  gallery: image_url[]
  services: string[]
  circle_memberships: circle_id[]
  linked_projects: project_id[]
}
```

**Important:** This should extend or share the same schema as regular user profiles. Don't build a parallel system. The ghost profile IS a profile — it just has a `status` field and a `claim_token` that regular profiles don't need.

---

## State 1: Search Results

### What the searcher sees

When someone searches and the entity doesn't exist on Earthback:

1. System queries external data source (see Data Enrichment section below)
2. Ghost profile is created in DB with status `ghost`
3. Search results display a mix of existing Earthback profiles and ghost profiles

**Existing profile card:** Green "On Earthback" badge, full info, "View Profile" and "Message" buttons.

**Ghost profile card:** Warm amber "Not on Earthback yet" badge, basic info from web, three action buttons:
- **View Profile** — goes to the ghost profile page (State 2)
- **Invite to Earthback** — triggers invitation flow
- **I vouch** — adds social proof, no email sent
- Social indicator: "2 people searched" / "1 person vouched"

### Deduplication

If three people search "Desert Sun Hempcrete," "desert sun hemp," and "Desert Sun Hemp-Crete Flagstaff AZ," you need ONE ghost profile, not three. 

Implementation: before creating a new ghost profile, fuzzy-match the search query against existing ghost profiles on `name` + approximate `location`. If match confidence > 80%, increment `search_count` on the existing profile instead of creating a new one. If ambiguous (60-80%), flag for human review. If no match, create new ghost profile.

Consider using an LLM call for dedup: send the search query + top 5 existing ghost profiles in the same region → ask "Is this the same entity as any of these? Return the matching ID or 'new'."

---

## State 2: Public Ghost Profile Page

### Route: `/profile/ghost/{id}` or `/p/{slug}`

Anyone can visit this page. It shows:

**Banner at top:** "This business isn't on Earthback yet. This profile was created from public information. Know them? Invite them to claim it and join the community." + Invite button.

**Profile card:** Name, location, website, description, tags. All pulled from web data. Generic cover pattern (not a photo — they haven't uploaded one). Intentionally minimal and slightly sparse — the incompleteness signals "this is a placeholder, come fill it in."

**Sidebar:**
- **Community interest** — "2 members searched for this business" with avatar stack, "1 member vouched" with avatar
- **Action box** — "Know this business?" with Invite and Vouch buttons, plus "Follow this profile" link (notified when they join)

---

## State 3: Claim Preview (Business Owner View)

### Route: `/claim/{claim_token}`

Only accessible via the unique claim link from the invitation email. Shows:

**Blue banner at top:**
- "This profile is waiting for you."
- "We built this from public information about your business. Only you can see this full preview. Claim it to edit the details and choose when to make it visible to the Earthback community."
- Shows who invited them with their personal note and avatar
- **"Claim This Profile"** button (primary)
- "Not your business? Let us know" link

**Full profile preview** with dashed "Editable" indicators on fields they'll be able to change (name, description, avatar, etc.)

**Sidebar:**
- **"People waiting for you"** — same social proof but reframed: "2 members searched for you," "1 member vouched for you," "3 people will be notified when you publish"
- **Suggested circles** — auto-matched based on tags: "Based on your profile, you'd fit in these communities: 🌾 Natural Building (412 members), ♻️ Materials & Salvage (143 members)..."

### Claim flow
1. Click "Claim This Profile"
2. Account creation form (or login if they have one)
3. Profile attached to their account, status → `claimed`
4. Redirected to profile editor (same editor as regular profiles)
5. They edit, then publish when ready

---

## Invitation Email

**Subject:** "Someone in Earthback is looking for you"

**Body (warm, short, personal):**

> Hi [Business Name],
>
> [Inviter Name] from the [Circle Name] circle on Earthback thinks you'd be a great addition to the community.
>
> [If invite_note exists:] *They said: "[invite_note]"*
>
> We've started a profile for you based on what we could find. [X] people in the community have searched for you or vouched for your work.
>
> **[See Your Profile →]** ← links to `/claim/{claim_token}`
>
> Earthback is a community for people building with natural materials, renewable energy, and mutual aid. No algorithm, no data harvesting — just the people and the projects.
>
> This link expires in 30 days. If this isn't your business, just ignore this email or [let us know].

**From:** earthbackproject@gmail.com (or a noreply@ if you set up transactional email)

**Important:** Only ONE invitation email per ghost profile, ever. Don't spam. If the token expires, a team member or another community member can trigger a re-send, which generates a new token.

---

## Data Enrichment Layer

When a search miss triggers ghost profile creation, something needs to find public data fast. Two approaches, use whichever fits your stack:

### Option A: Google Places API
Best for businesses with physical locations. One API call gives you name, address, phone, hours, rating, website, photos, and a place_id for dedup.

Cost: ~$0.017 per request (Place Details). Very cheap.

Limitation: doesn't cover individual practitioners, small projects, or entities without a Google listing.

### Option B: Web Search + AI Extraction
Search the entity name with a web search API (e.g., Serper, Brave Search, or even Google Custom Search). Feed the top 3-5 results into Claude Haiku with a prompt:

```
Extract structured profile data for this entity from the following search results.
Return JSON: { name, location, description, website, phone, tags[], type }
If you can't confidently determine a field, return null.
```

Cost: ~$0.01-0.03 per enrichment (search API + Haiku call).

Advantage: works for everything — businesses, practitioners, projects, orgs. More flexible.

### Recommended: Combine both
Try Google Places first (fast, structured, high confidence). If no result or low confidence, fall back to web search + AI extraction. Cache all results — don't re-enrich on every page view.

---

## Security

**Claim tokens** must be:
- Cryptographically random (use `crypto.randomUUID()` or equivalent)
- Single-use (dead after claiming)
- Time-limited (30-day expiry, regeneratable)
- Not guessable (no sequential IDs, no business-name-based slugs)

**The claim preview page** shows the full profile without requiring login — the owner needs to see what's there before committing. But claiming requires authentication.

**Expired/claimed links** show a friendly message: "This profile has already been claimed" or "This link has expired — contact us if you need a new one."

**Rate limiting on search-triggered creation:** Don't let someone spam searches to create thousands of ghost profiles. Limit to ~10 ghost profile creations per user per hour. Unauthenticated searches get a lower limit.

---

## Integration Points

### Profile Build Page (next push)
Ghost profiles use the SAME profile editor as regular profiles. The only difference is the claim banner and pre-populated fields. Don't build two systems.

### Circles
When a ghost profile is published, auto-suggest circle memberships based on tags. The owner confirms which circles to join. Publishing triggers a subtle feed post in those circles: "[Business Name] just joined [Circle Name]."

### Feed
- Ghost profiles do NOT appear in the feed (they're not members yet)
- When published, a gentle "just joined" post appears in relevant circles
- Members who followed the ghost profile get a notification

### Visualizer
Future: businesses could be tagged as suppliers/contractors in the AI visualizer. "This render uses materials from 3 suppliers in your region." Phase 3.

### Search
Ghost profiles ARE searchable — that's the whole point. They appear in search results with the amber "Not on Earthback yet" badge. Published profiles appear normally. Claimed-but-unpublished profiles are invisible to everyone except the owner.

---

## Admin Panel

Needs a simple admin view (can be a protected page, doesn't need to be fancy):

- **Queue:** scraped/nominated profiles pending review
- **Status dashboard:** ghost → invited → claimed → published counts
- **Manual creation:** form to create ghost profiles by hand
- **Bulk import:** CSV upload (name, location, email, tags) for seeding from a conference list or directory
- **Re-send invitations:** for expired tokens
- **Merge duplicates:** when dedup catches something after the fact

---

## Implementation Priority

### Phase 1: Manual + Search (ship with profile build)
- Ghost profile data model (extends regular profile schema)
- Manual ghost profile creation (admin only)
- Ghost profiles appear in search results with basic card
- Ghost profile public page (State 2)
- "Invite to Earthback" sends email with claim link
- Claim flow (State 3) → account creation → profile editor
- Publish toggle

### Phase 2: Auto-enrichment + Social
- Search-triggered auto-generation with data enrichment (Google Places + AI)
- Deduplication layer
- Vouch system
- Follow ghost profile (notify on publish)
- Search count tracking
- "X people are looking for this business" social proof

### Phase 3: Scale + Intelligence
- Bulk import / web seeding
- Nomination flow from community posts
- AI-powered circle matching
- Visualizer integration (supplier/contractor tagging)
- Analytics: which ghost profiles convert best, which circles drive most claims
