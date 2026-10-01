#!/bin/sh
# Rebuild the C797 deck from the WSQ source: convert_deck.py, then fix_deck.py.
set -e
cd "$(dirname "$0")/.."
OUT="courseware/Sustainability Reporting Masterclass (C797)-v1.0.pptx"
python3 ~/.claude/skills/wsq-to-non-wsq/scripts/convert_deck.py \
  --src "source-wsq/courseware/Sustainability-Reporting-and-Engineering-Strategies-for-Senior-Leaders-v5.0.pptx" --out "$OUT" \
  --old-title "Sustainability Reporting and Engineering Strategies for Senior Leaders" --new-title "Sustainability Reporting Masterclass" \
  --old-code TGS-2025052343 --new-code C797 --tsc "EGS-EPM-6065-1.1" \
  --old-version v5.0 --new-version v1.0 \
  --sub "Version 5.0 • 01 Oct 2026=>Version 1.0 • 01 Oct 2026" \
  --wsq-slides 1,4,6,7,8,214,215,216 --feedback-slide 217
python3 tools/fix_deck.py
