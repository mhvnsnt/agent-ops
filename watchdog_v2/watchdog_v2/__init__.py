"""watchdog_v2 — read-only lane-registry watchdog.

Design rule #1: this package has NO write path to the things it watches.
It reads checkpoint files, disk stats, process tables and HTTP endpoints,
and writes only to its own state directory (SQLite ledger + lock file).
It cannot resume, kill, delete, launch, or edit any lane, file, or job.
"""

__version__ = "1.0.0"
