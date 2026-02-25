# Earthback Supplier & Partner Relationships — Plan
*Written: 2026-02-25 | Status: Planning*

---

## The Core Principle

Earthback's revenue model is connecting members with aligned suppliers and materials partners — not selling attention. This means the supplier relationship has to be structured as genuine value exchange, not advertising.

The difference in practice:
- **Advertising model**: supplier pays for visibility, content is promotional, members distrust it
- **Connection model**: supplier gets listed because they're useful, content is editorial, members trust it

Everything in this plan flows from that distinction. When a supplier spotlight post runs, it runs because it genuinely answers a member question about sourcing — not because someone paid for a post. The commercial relationship happens at the connection layer (referral fees, directory listings, facilitated introductions), not at the content layer.

---

## What Suppliers Get

**Tier 1 — Directory listing (free)**
- Resource Hub pin on the community map with their location and service area
- Listed in the relevant circle(s) as a "Resource" (not a member, a resource)
- Visible to members searching for suppliers in their region
- No curation fee, no featured placement

**Tier 2 — Partner org (paid, low cost)**
- Everything in Tier 1
- An org profile page on the platform (same as member projects)
- Ability to post in their relevant circles (max 2 posts/week, non-promotional content only — technique sharing, sourcing guidance, project stories)
- Badge on their profile ("Aligned Supplier" or "Materials Partner")
- Annual fee — priced to be accessible to small regional suppliers, not just large companies

**Tier 3 — Featured partner (paid, higher)**
- Everything in Tier 2
- A sourcing guide post (like the ones in DISPATCH_POSTS_V2) written collaboratively and published through Earthback Dispatch — reviewed for accuracy, explicitly editorial
- Inclusion in region-specific "find a supplier" matching (when a member says they're building in X region and need hempcrete materials, Tier 3 partners in that region are surfaced first)
- Quarterly review calls with the Earthback team
- Co-promotion opportunities (newsletter, social)

---

## What Earthback Gets

**Referral fees**: when a member connection leads to a verified purchase, Earthback receives a referral fee. This requires tracking — either a unique referral code per connection, or self-reporting by the supplier. Start with self-reporting (trust-based), build tracking infrastructure when volume warrants it.

**Directory fees**: Tier 2 and 3 annual fees. Priced modestly to start — the value of being in front of a self-selected community of serious natural builders is high for suppliers; the fee should be low enough that every qualified supplier joins.

**Future: marketplace integration**: direct product listings, cart integration, regional materials finder. This is a phase 3 feature, not launch.

---

## The Intake Flow

The intake path already exists: `training.html` partner inquiry form → `partner_inquiries` Supabase table.

The form needs a few additions for supplier-specific intake:
- Type of organization: Builder / Supplier / Training Program / NGO / Research
- What they supply (free text + circle tags)
- Service region (country + state/province level)
- Website URL (already added in V7b)

After form submission:
1. Nicco reviews (or a team member reviews)
2. Approved → create org profile, add map pin, send welcome email
3. Tier 2/3 → payment link, then activate enhanced features
4. Declined / not aligned → honest note back about why

For launch, this process is entirely manual. Automate when volume exceeds what manual review can handle.

---

## Editorial Independence

The dispatch bot and supplier relationships must stay clearly separated. Rules:

1. **Dispatch posts are editorial, never paid**. A supplier spotlight runs because it answers a real member question, not because the supplier paid for it. Suppliers cannot buy dispatch coverage.

2. **Supplier org accounts can post in circles**, but their posts are visibly from their org account (labeled "Aligned Supplier"), not from Earthback Dispatch.

3. **If a sourcing guide mentions a supplier**, it mentions all relevant suppliers for the region — not only paying partners. The distinction is that Tier 3 partners may be mentioned first or more prominently, but non-partners are not excluded.

4. **Members can rate and review suppliers** (phase 2). Bad reviews don't get hidden because the supplier is a paying partner. This is what makes the directory trustworthy and distinguishes it from a paid listing service.

---

## Priority Supplier Categories to Recruit at Launch

The circles with the most acute sourcing problems — where members are most likely to be frustrated trying to find materials — are the best early targets:

**Natural building materials:**
- Hemp hurds / hemp shiv (very few suppliers in each region)
- Hydraulic lime / NHL (niche product, hard to find locally)
- Natural clay for plaster (widely available but hard to identify reliable sources)
- Straw bale suppliers (regional grain farms)

**Seeds and growing:**
- Open-pollinated/heirloom seed companies (many to list, very willing to partner)
- Mycology spawn suppliers (small but active community)

**Energy:**
- Off-grid solar installers / system designers (high member demand)
- Rocket stove builders / kits

**Training and education:**
- Natural building workshops and courses
- Permaculture design certificate programs
- Solar training programs

Each of these categories has a small number of high-quality aligned suppliers who would benefit from targeted visibility to a community of serious builders. The ask is not large; many of them already give their time freely to community education.

---

## The Map as the Sales Pitch

When approaching a potential supplier partner, the map is the most compelling demonstration of what Earthback offers. Show them:

1. The community map with member concentration in their service region
2. The circles their customers belong to
3. The dispatch post format (high-quality editorial, not promotional)
4. The intake flow

The pitch is: "Your customers are already here looking for you. We help them find you, and we help you tell your story to the right audience — builders who are already convinced they want natural building materials, not people who need to be sold on it first."

That's a genuinely differentiated offer from any other advertising channel available to a small natural building supplier.

---

## Supplier Spotlight Post Format

From DISPATCH_POSTS_V2, the format that works best:

1. **Lead with the member problem**: "Sourcing hydraulic lime for hempcrete in North America has gotten easier..."
2. **Name specific suppliers**: give the actual answer — company name, location, what they supply, who they serve
3. **Include one technical detail** that demonstrates genuine knowledge (not generic)
4. **No pricing, no exclusive endorsements** — multiple suppliers where possible
5. **Close with a broader resource** (directory, network, association) for options not covered

Posts that name specific suppliers should be reviewed for accuracy before publishing. Supplier details change: companies merge, change focus, or shut down. Add a "last verified" date to sourcing guide posts so outdated info is visible.

---

## Moonback / Marsback Supplier Implications

When those platforms launch, the same supplier relationship model applies — but the supplier category is entirely different:

- Basalt fiber and regolith-analog building materials (research stage)
- Mycelium composite manufacturers (small but growing commercial sector)
- Closed-loop life support and agriculture suppliers
- Off-world habitat design and engineering firms

The same platform, the same circles structure, the same connection model — the suppliers are just operating at a different frontier. Many of the Earth-based natural building suppliers will already be researching and developing materials for off-world applications. The crossover audience is real.

---

## Near-Term Actions

1. **Update partner intake form** — add org type, supply category, service region fields
2. **Create first 5 Resource Hub map pins manually** — pick the most useful suppliers from the sourcing posts and seed the map
3. **Email outreach to 10 priority suppliers** — short, personal, point to the platform, ask if they want to be listed. Most will say yes.
4. **Publish first 3 sourcing guide posts** — hempcrete materials, seeds, natural plaster — as proof of the editorial model
5. **Set pricing for Tier 2 and 3** before outreach — have an answer ready when they ask what it costs
