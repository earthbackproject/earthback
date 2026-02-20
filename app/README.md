# Earthback App — Phase 2

**Status:** Not started · Begins after Phase 1 waitlist + pilot validation

## What this is

The coordination instrument — the actual tool that groups use to form, commit, execute, and archive projects.

## Planned stack (per Build Plan v1.1)

- **Frontend:** Next.js (React) + TypeScript
- **Backend:** FastAPI (Python) or NestJS (Node)
- **Database:** PostgreSQL (Supabase or Neon)
- **Auth:** Auth.js (NextAuth) or Clerk
- **Hosting:** Vercel (frontend) + managed Postgres

## Phase 2 feature set (MVP)

- [ ] Auth + minimal profiles (email + optional Google login)
- [ ] Create / join groups with invite links
- [ ] Commitments: pledge time, skills, resources
- [ ] Tasks + events with basic tracking
- [ ] Group chat + announcements (no global feed)
- [ ] Archiving: projects end cleanly, history preserved
- [ ] Basic admin tooling and audit trails

## Phase 3 (overlapping, after real usage)

- [ ] Local reputation: vouching inside a group/network
- [ ] Verified actions: attendance, task completion, resource delivery
- [ ] Abuse prevention: rate limits, reporting, graduated permissions

## Phase 4 (after real activity exists)

- [ ] Search by intent (skills, location, timeframe)
- [ ] Project templates
- [ ] Directory of active groups (privacy-respecting defaults)

## Core data model (six primitives)

```
People → Projects → Resources
Skills → Places  → Needs
```

Every feature must be expressible with these six. No new primitives unless irreducible.

---

*Build plan reference: `reference/Earthback_Coordination_Platform_Build_Plan_v1_1.pdf`*
*Governance reference: `reference/Earthback Core Constitution.pdf`*
