"""Checkpoint schema — pydantic v2, tolerant by design.

The fleet writes checkpoints in more than one historical shape (the
CHECKPOINT_PROTOCOL.md schema plus looser lane variants). Validation must
classify, never crash: a checkpoint that fails hard validation is a
finding (CORRUPT), not an exception that kills the whole scan — that is
exactly how the old prompt-only watchdog died on a 0-byte file and then
looped on it for 8 days.
"""
from __future__ import annotations

import json
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class CheckpointClass(str, Enum):
    ZERO = "zero"                # 0 bytes — wiped or truncated
    CORRUPT = "corrupt"          # non-empty but unparseable / not an object
    DONE = "done"                # status completed/done
    NEEDS_OWNER = "needs_owner"  # status needs_owner / blocked_on_owner
    ACTIVE = "active"            # live status, recently touched
    STALE = "stale"              # live status, untouched past the stale window
    DEAD = "dead"                # ZERO/CORRUPT and old — archived news, not an alarm
    OTHER = "other"              # parseable, terminal/other status, not watched


LIVE_STATUSES = {"running", "queued", "in_progress", "active"}
# "paused" is deliberately NOT live: a paused lane is parked on purpose,
# not stalled. (First live scan flagged two lanes paused for 500+ hours
# as "stalls" — a false alarm by design, fixed here.)
DONE_STATUSES = {"completed", "done", "complete", "success", "landed"}
OWNER_STATUSES = {"needs_owner", "blocked", "blocked_on_owner", "awaiting_owner"}


class Checkpoint(BaseModel):
    """Tolerant view of one checkpoint file. Unknown fields are kept out
    of the way (ignored), missing fields are None — the fleet's real files
    do not all carry the full protocol schema."""

    model_config = ConfigDict(extra="ignore")

    task_id: str | None = None
    status: str | None = None
    goal: str | None = None
    progress_seq: int | None = None
    last_heartbeat: str | None = None
    last_progress_at: str | None = None


def classify_file(path: Path, *, now: float, stale_after_h: float = 6.0,
                    dead_after_h: float = 72.0) -> tuple[CheckpointClass, Checkpoint | None, str]:
    """Return (classification, parsed-or-None, detail). Pure read."""
    size = path.stat().st_size
    age_h = (now - path.stat().st_mtime) / 3600.0
    if size == 0:
        cls = CheckpointClass.DEAD if age_h > dead_after_h else CheckpointClass.ZERO
        return cls, None, f"0 bytes, {age_h:.1f}h old"
    try:
        raw = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except Exception as exc:  # unparseable is a classification, not a crash
        cls = CheckpointClass.DEAD if age_h > dead_after_h else CheckpointClass.CORRUPT
        return cls, None, f"unparseable: {exc.__class__.__name__}"
    if not isinstance(raw, dict):
        cls = CheckpointClass.DEAD if age_h > dead_after_h else CheckpointClass.CORRUPT
        return cls, None, f"top level is {type(raw).__name__}, not an object"
    cp = Checkpoint.model_validate(raw)
    status = (cp.status or "").strip().lower()
    if status in DONE_STATUSES:
        return CheckpointClass.DONE, cp, f"status={status}"
    if status in OWNER_STATUSES:
        return CheckpointClass.NEEDS_OWNER, cp, f"status={status}"
    if status in LIVE_STATUSES:
        cls = CheckpointClass.STALE if age_h > stale_after_h else CheckpointClass.ACTIVE
        return cls, cp, f"status={status}, {age_h:.1f}h since touch"
    return CheckpointClass.OTHER, cp, f"status={status or 'none'}"
