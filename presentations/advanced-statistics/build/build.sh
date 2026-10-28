#!/usr/bin/env bash
# Rebuilds all three decks: visuals -> pptx -> animations -> PDF.
#   PPTX_SKILL=<pptx skill dir> NODE_PATH=<node_modules with pptxgenjs, react-icons, react, react-dom, sharp> ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 build_visuals.py
node build_deck.cjs "$PPTX_SKILL/scripts/apply_theme.js"
node build_short_deck.cjs "$PPTX_SKILL/scripts/apply_theme.js"
node build_six_deck.cjs "$PPTX_SKILL/scripts/apply_theme.js"
for DECK in ../Advanced_Statistics_Presentation.pptx ../Advanced_Statistics_Presentation_6_Slides.pptx ../Advanced_Statistics_Short_Presentation.pptx; do
	python3 add_animations.py "$DECK"
	python3 "$PPTX_SKILL/scripts/office/validate.py" "$DECK"
	python3 "$PPTX_SKILL/scripts/office/soffice.py" --headless --convert-to pdf --outdir .. "$DECK"
done
