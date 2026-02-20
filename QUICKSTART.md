# Earthback — Quick Start

## Services & Logins

| Service | URL | Account |
|---|---|---|
| **Live Site** | https://earthbackproject.org | — |
| **GitHub** | https://github.com/earthbackproject/earthback | earthbackproject |
| **Supabase** | https://supabase.com/dashboard/project/yptktmzagctusbeqdaty | the_earthback_project |
| **Netlify** | https://app.netlify.com | nicco.macintyre@gmail.com |

## Start a Work Session

1. Run `./earthback-start.sh` from the project root — opens all dashboards, checks git, verifies site is live
2. Open Cowork and say: **"Read TRACKER.md and SESSION_NOTES.md and pick up where we left off"**

## Deploy the Site

```bash
git add -A
git commit -m "describe what changed"
git push
```
Netlify auto-deploys from the `main` branch. The `site/` folder is the publish directory.

## Folder Guide

| Folder | What's in it |
|---|---|
| `site/` | The live website — HTML, CSS, JS, images. What gets deployed to Netlify. |
| `db/` | SQL migrations and Supabase setup docs. See `db/README.md` for run order. |
| `branding/` | Current brand assets — logos, style guides, mockups. |
| `governance/` | Constitution, governance framework, org docs, product spec. |
| `reference/` | The archive — old versions, early designs, origin story. |
| `tracker/` | Visual project dashboard (open `tracker/index.html` in browser). |
| `app/` | Future Next.js app (placeholder). |
| `docs/` | Future knowledge base (placeholder). |

## Key Files at Root

| File | Purpose |
|---|---|
| `SESSION_NOTES.md` | What happened last session + what's next. Claude reads this to resume. |
| `TRACKER.md` | Master project checklist. The source of truth for what's done and what's left. |
| `QUICKSTART.md` | This file. How to get oriented fast. |
| `earthback-start.sh` | Opens all dashboards and checks project health. |
| `netlify.toml` | Netlify deployment configuration. |
| `.gitignore` | Tells git what NOT to track (node_modules, .env, etc.). |

## Supabase Quick Links

- [Table Editor](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/editor)
- [SQL Editor](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/sql)
- [Auth Users](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/auth/users)
- [Storage](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/storage/buckets)
- [Auth URL Config](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/auth/url-configuration)
- [API Keys](https://supabase.com/dashboard/project/yptktmzagctusbeqdaty/settings/api)

## Git Basics

```bash
git status          # What changed?
git diff            # See the actual changes
git add site/       # Stage specific files/folders
git commit -m "msg" # Save a snapshot locally
git push            # Send to GitHub → triggers Netlify deploy
git pull            # Get latest from GitHub (if someone else pushed)
git log --oneline   # See recent commits
```
