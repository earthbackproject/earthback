#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 🌿 Earthback Project — Startup Script
# Opens all dashboards, checks environment, prints status.
# Run from the Earthback project root folder.
# ═══════════════════════════════════════════════════════════

set -e

# ── Colors ──
GREEN='\033[0;32m'
SAGE='\033[0;36m'
CLAY='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}${BOLD}  🌿 the Earthback Project${NC}"
echo -e "${DIM}  ─────────────────────────────────────${NC}"
echo ""

# ── Detect OS for 'open' command ──
if [[ "$OSTYPE" == "darwin"* ]]; then
  OPEN_CMD="open"
elif command -v xdg-open &> /dev/null; then
  OPEN_CMD="xdg-open"
elif command -v wslview &> /dev/null; then
  OPEN_CMD="wslview"
else
  OPEN_CMD=""
fi

# ── Open browser tabs ──
echo -e "${SAGE}${BOLD}  Opening dashboards...${NC}"

URLS=(
  "https://github.com/earthbackproject/earthback"
  "https://app.netlify.com"
  "https://supabase.com/dashboard/project/yptktmzagctusbeqdaty"
  "https://earthbackproject.org"
  "https://earthbackproject.org/login.html"
)

LABELS=(
  "1. GitHub repo — check for changes"
  "2. Netlify — verify deploy status"
  "3. Supabase — backend home base"
  "4. Live site — verify it's up"
  "5. Sign in — log into the app"
)

if [ -n "$OPEN_CMD" ]; then
  for i in "${!URLS[@]}"; do
    $OPEN_CMD "${URLS[$i]}" 2>/dev/null &
    echo -e "  ${GREEN}✓${NC} ${LABELS[$i]} — ${DIM}${URLS[$i]}${NC}"
    sleep 0.3
  done
else
  echo -e "  ${CLAY}⚠${NC} Could not detect browser command. Open these manually:"
  for i in "${!URLS[@]}"; do
    echo -e "    ${LABELS[$i]}: ${SAGE}${URLS[$i]}${NC}"
  done
fi

echo ""

# ── Check git status ──
echo -e "${SAGE}${BOLD}  Checking git...${NC}"

if command -v git &> /dev/null && [ -d ".git" ]; then
  BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
  echo -e "  ${GREEN}✓${NC} Branch: ${BOLD}${BRANCH}${NC}"

  REMOTE=$(git remote get-url origin 2>/dev/null || echo "none")
  echo -e "  ${GREEN}✓${NC} Remote: ${DIM}${REMOTE}${NC}"

  # Check for uncommitted changes
  CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ "$CHANGES" -gt "0" ]; then
    echo -e "  ${CLAY}⚠${NC} ${CHANGES} uncommitted change(s)"
  else
    echo -e "  ${GREEN}✓${NC} Working tree clean"
  fi

  # Check if ahead/behind remote
  git fetch --quiet origin "$BRANCH" 2>/dev/null || true
  AHEAD=$(git rev-list --count "origin/${BRANCH}..HEAD" 2>/dev/null || echo "?")
  BEHIND=$(git rev-list --count "HEAD..origin/${BRANCH}" 2>/dev/null || echo "?")
  if [ "$AHEAD" != "?" ] && [ "$BEHIND" != "?" ]; then
    if [ "$AHEAD" -gt "0" ]; then
      echo -e "  ${CLAY}↑${NC} ${AHEAD} commit(s) ahead of origin — consider pushing"
    fi
    if [ "$BEHIND" -gt "0" ]; then
      echo -e "  ${CLAY}↓${NC} ${BEHIND} commit(s) behind origin — consider pulling"
    fi
    if [ "$AHEAD" -eq "0" ] && [ "$BEHIND" -eq "0" ]; then
      echo -e "  ${GREEN}✓${NC} Up to date with origin/${BRANCH}"
    fi
  fi
else
  if ! command -v git &> /dev/null; then
    echo -e "  ${RED}✗${NC} git not found — install git first"
  elif [ ! -d ".git" ]; then
    echo -e "  ${CLAY}⚠${NC} Not a git repo. Run: ${SAGE}git init && git remote add origin https://github.com/earthbackproject/earthback.git${NC}"
  fi
fi

echo ""

# ── Check site is live ──
echo -e "${SAGE}${BOLD}  Checking site...${NC}"

if command -v curl &> /dev/null; then
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "https://earthbackproject.org" 2>/dev/null || echo "000")
  HTTP_CODE=$(echo "$HTTP_CODE" | grep -oE '[0-9]{3}$' || echo "000")
  if [ "$HTTP_CODE" = "200" ]; then
    echo -e "  ${GREEN}✓${NC} earthbackproject.org is live (HTTP ${HTTP_CODE})"
  elif [ "$HTTP_CODE" = "000" ]; then
    echo -e "  ${RED}✗${NC} Could not reach earthbackproject.org (timeout or network issue)"
  else
    echo -e "  ${CLAY}⚠${NC} earthbackproject.org returned HTTP ${HTTP_CODE}"
  fi
else
  echo -e "  ${DIM}  (curl not found — skipping site check)${NC}"
fi

echo ""

# ── File count ──
echo -e "${SAGE}${BOLD}  Project files...${NC}"
if [ -d "site" ]; then
  HTML_COUNT=$(find site -name "*.html" -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
  SQL_COUNT=$(find . -name "*.sql" -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
  echo -e "  ${GREEN}✓${NC} ${HTML_COUNT} HTML pages in site/"
  echo -e "  ${GREEN}✓${NC} ${SQL_COUNT} SQL migration files"
else
  echo -e "  ${RED}✗${NC} site/ directory not found — are you in the right folder?"
fi

echo ""

# ── Claude handoff prompt ──
echo -e "${SAGE}${BOLD}  Claude session prompt:${NC}"
echo -e "${DIM}  ─────────────────────────────────────${NC}"
echo -e "  ${GREEN}Read TRACKER.md and SESSION_NOTES.md and pick up where we left off.${NC}"
echo -e "${DIM}  ─────────────────────────────────────${NC}"
echo ""
echo -e "${DIM}  Tip: Also open Earthback_Setup_Reference.html in your browser${NC}"
echo -e "${DIM}  for clickable links to all dashboards and services.${NC}"
echo ""
echo -e "${GREEN}${BOLD}  Ready to build. 🌿${NC}"
echo ""
