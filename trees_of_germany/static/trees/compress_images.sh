#!/usr/bin/env bash
# requires: ImageMagick

find . -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.gif' \) -print0 |
while IFS= read -r -d '' src; do
  dst="${src%.*}.webp"
  echo "→ $src → $dst"
  convert "$src" -resize 524x -define webp:lossless=true "$dst" \
    && rm "$src"
done

