#!/bin/bash
# ============================================================
# Earthback — ComfyUI → Site Assets Import Pipeline
# ============================================================
# Processes Flux-generated PNGs from comfyui-output/ into
# web-optimized JPGs organized by type.
#
# Usage:
#   bash scripts/import-comfyui.sh              # process all
#   bash scripts/import-comfyui.sh avatars      # avatars only
#   bash scripts/import-comfyui.sh posts        # post images only
#   bash scripts/import-comfyui.sh social       # social media images only
#
# Requires: ImageMagick (convert command)
# ============================================================

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/comfyui-output"
IMG="$ROOT/site/assets/img"
MODE="${1:-all}"

# Quality settings
AVATAR_SIZE="400x400"
AVATAR_QUALITY=85
POST_SIZE="800x400"
POST_QUALITY=80
SOCIAL_SIZE="1080x1080"
SOCIAL_QUALITY=85

echo "═══════════════════════════════════════════"
echo "  Earthback Media Import Pipeline"
echo "  Source: comfyui-output/"
echo "  Mode:   $MODE"
echo "═══════════════════════════════════════════"

# ── HELPER: find best source for a character ─────────────
find_char_source() {
  local name="$1"
  for t in T4 T3 T2 T1; do
    local found=$(find "$SRC" -name "*${t}-chars-${name}*_00001_.png" 2>/dev/null | head -1)
    if [ -n "$found" ]; then
      echo "$found"
      return
    fi
  done
}

# ── HELPER: find source for a post image ─────────────────
find_post_source() {
  local name="$1"
  find "$SRC" -name "*T1-${name}*_00001_.png" 2>/dev/null | head -1
}

# ── AVATARS ──────────────────────────────────────────────
import_avatars() {
  echo ""
  echo "── Character Avatars ──────────────────────"
  mkdir -p "$IMG/avatars"

  local count=0
  process_avatar() {
    local name="$1"
    local slug="$2"
    local dest="$IMG/avatars/${slug}.jpg"
    local src=$(find_char_source "$name")
    if [ -n "$src" ]; then
      if [ -f "$dest" ]; then
        echo "  SKIP: ${slug}.jpg (exists)"
      else
        convert "$src" -resize "${AVATAR_SIZE}^" -gravity center \
          -extent "$AVATAR_SIZE" -quality "$AVATAR_QUALITY" -strip "$dest"
        local sz=$(du -k "$dest" | cut -f1)
        echo "  OK: ${slug}.jpg (${sz}K)"
      fi
      count=$((count + 1))
    else
      echo "  MISS: $name"
    fi
  }

  process_avatar "Amara Diallo"    "amara-diallo"
  process_avatar "Dara Okonkwo"    "dara-okonkwo"
  process_avatar "Elena Vasquez"   "elena-vasquez"
  process_avatar "James Osei"      "james-osei"
  process_avatar "Kenji Nakamura"  "kenji-nakamura"
  process_avatar "Lena Hartmann"   "lena-hartmann"
  process_avatar "Marcus Webb"     "marcus-webb"
  process_avatar "Mei Lin"         "mei-lin"
  process_avatar "Priya Sharma"    "priya-sharma"
  process_avatar "Rosa Mendez"     "rosa-mendez"
  process_avatar "Sam Torres"      "sam-torres"
  process_avatar "Tom Westhall"    "tom-westhall"

  echo "  Processed: $count avatars"
}

# ── POST IMAGES ──────────────────────────────────────────
import_posts() {
  echo ""
  echo "── Feed Post Images ───────────────────────"
  mkdir -p "$IMG/posts"

  local count=0
  process_post() {
    local name="$1"
    local slug="$2"
    local dest="$IMG/posts/${slug}.jpg"
    local src=$(find_post_source "$name")
    if [ -n "$src" ]; then
      if [ -f "$dest" ]; then
        echo "  SKIP: ${slug}.jpg (exists)"
      else
        convert "$src" -resize "$POST_SIZE" -quality "$POST_QUALITY" -strip "$dest"
        local sz=$(du -k "$dest" | cut -f1)
        echo "  OK: ${slug}.jpg (${sz}K)"
      fi
      count=$((count + 1))
    else
      echo "  MISS: '$name'"
    fi
  }

  process_post "Hempcrete mix guide"  "hempcrete-mix"
  process_post "Desert hemp wall"     "utah-hemp-wall"
  process_post "Greywater system"     "greywater-system"
  process_post "Solar co-op"          "solar-coop"
  process_post "Food Forest"          "food-forest"
  process_post "Tiny cabin"           "tiny-cabin"
  process_post "Salvage lumber"       "salvage-fir"
  process_post "Lora mesh"            "lora-mesh"

  echo "  Processed: $count post images"
}

# ── SOCIAL MEDIA LIBRARY ─────────────────────────────────
import_social() {
  echo ""
  echo "── Social Media Library ───────────────────"
  mkdir -p "$ROOT/site/content/social/processed"

  local count=0
  for f in "$SRC"/EB-fp-01-social\ media-T*-chars-*.png; do
    [ -f "$f" ] || continue
    local base=$(basename "$f" .png)
    local dest="$ROOT/site/content/social/processed/${base}.jpg"
    if [ -f "$dest" ]; then
      count=$((count + 1))
      continue
    fi
    convert "$f" -resize "${SOCIAL_SIZE}^" -gravity center \
      -extent "$SOCIAL_SIZE" -quality "$SOCIAL_QUALITY" -strip "$dest"
    count=$((count + 1))
  done
  echo "  Processed: $count social images"
}

# ── RUN ──────────────────────────────────────────────────
case "$MODE" in
  avatars) import_avatars ;;
  posts)   import_posts ;;
  social)  import_social ;;
  all)
    import_avatars
    import_posts
    echo ""
    echo "  (Run 'bash scripts/import-comfyui.sh social' for social library — ~80 images)"
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Usage: bash scripts/import-comfyui.sh [avatars|posts|social|all]"
    exit 1
    ;;
esac

echo ""
echo "═══════════════════════════════════════════"
echo "  Done! Check site/assets/img/"
echo "═══════════════════════════════════════════"
