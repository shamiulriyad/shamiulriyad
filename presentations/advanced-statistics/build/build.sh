#!/usr/bin/env bash
# Rebuilds the deck: visuals -> pptx -> animations -> PDF.
#   PPTX_SKILL=<pptx skill dir> NODE_PATH=<node_modules with pptxgenjs, react-icons, react, react-dom, sharp> ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
DECK=../Advanced_Statistics_Presentation.pptx
python3 build_visuals.py
node build_deck.cjs "$PPTX_SKILL/scripts/apply_theme.js"
python3 add_animations.py "$DECK"
python3 "$PPTX_SKILL/scripts/office/validate.py" "$DECK"
python3 "$PPTX_SKILL/scripts/office/soffice.py" --headless --convert-to pdf --outdir .. "$DECK"
