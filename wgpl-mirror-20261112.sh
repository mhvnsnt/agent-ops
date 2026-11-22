#!/bin/bash
# Mirror lane: wizard-gang-part-libraries (2.0G, 23k files, untouched 7+ days)
# NO deletion in this lane. A later guardian pass downloads the release assets
# and hash-verifies against MANIFEST.sha256 before any local clear (ONE-STORE RULE).
set -u
STAGE="$HOME/workspace/_wgpl-mirror-20261112"
SRC="$HOME/workspace/your_files/wizard-gang-part-libraries"
REPO="mhvnsnt/clouddog-storage"
TAG="wizard-gang-part-libraries-20261112"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
mkdir -p "$STAGE"
{
echo "START $(date -Is)"
echo "src: $SRC"
find "$SRC" -type f | wc -l | xargs echo "file_count:"
du -sb "$SRC" | xargs echo "src_bytes:"
} | tee "$STAGE/CHECKPOINT.md"

# 1. tar (no compression; content is mostly images) piped to 1900M splits
tar -cf - -C "$HOME/workspace/your_files" wizard-gang-part-libraries \
  | split -b 1900M -d - "$STAGE/wgpl.tar.part"
echo "tar+split done $(date -Is)" | tee -a "$STAGE/CHECKPOINT.md"
ls -lh "$STAGE" | tee -a "$STAGE/CHECKPOINT.md"

# 2. chunk manifest
( cd "$STAGE" && sha256sum wgpl.tar.part* > MANIFEST.sha256 )
cat "$STAGE/MANIFEST.sha256" | tee -a "$STAGE/CHECKPOINT.md"

# 3. release (avoid tag collision)
if gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then TAG="${TAG}-b"; fi
echo "tag: $TAG" | tee -a "$STAGE/CHECKPOINT.md"
gh release create "$TAG" --repo "$REPO" \
  --title "Wizard Gang part libraries — 2026-11-12" \
  --notes "Mirror of ~/workspace/your_files/wizard-gang-part-libraries (~2.0G, 23k files, untouched 7+ days). Chunks: wgpl.tar.partNN (plain tar, split at 1900M). Verify with MANIFEST.sha256. Guardian mirror lane 2026-11-12. Local copy NOT yet cleared — clearing only after a later guardian pass downloads and hash-verifies."
echo "release $TAG created $(date -Is)" | tee -a "$STAGE/CHECKPOINT.md"

# 4. upload chunks + manifest
gh release upload "$TAG" --repo "$REPO" "$STAGE"/wgpl.tar.part* "$STAGE"/MANIFEST.sha256 --clobber
echo "upload done $(date -Is)" | tee -a "$STAGE/CHECKPOINT.md"
gh release view "$TAG" --repo "$REPO" | tee -a "$STAGE/CHECKPOINT.md"
{
echo ""
echo "## 2026-11-12 ~20:5x CST — mirror lane wizard-gang-part-libraries (background)"
echo "- Mirror upload to $REPO release $TAG started by disk-space-guardian; see $STAGE/CHECKPOINT.md for chunk hashes."
echo "- Local copy NOT cleared; verification (download + sha256) is a later guardian pass's job per ONE-STORE RULE."
} >> "$LOG"
echo "LANE DONE $(date -Is)"
