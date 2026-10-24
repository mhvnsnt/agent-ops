#!/bin/bash
# research-check.sh "topic" — check if research on a topic already exists before starting new work.
# Searches the master index + all agent-ops research docs.
if [ -z "$1" ]; then
  echo "usage: ./research-check.sh \"topic keywords\""
  exit 1
fi
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "=== RESEARCH-PULLIN-INDEX.md ==="
grep -i -n "$1" "$DIR/RESEARCH-PULLIN-INDEX.md" | head -20
echo ""
echo "=== other agent-ops docs ==="
grep -i -l "$1" "$DIR"/*.md 2>/dev/null | grep -v RESEARCH-PULLIN-INDEX | head -20
echo ""
echo "If nothing above: topic is new — research it, doc it in the right repo, add an index line."
