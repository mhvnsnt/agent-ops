# The Three Sitting Takes — Plain-Language Comparison

**For the owner, 2026-10-19.** All three takes are stored safely on GitHub and off the local disk. Nothing was lost, nothing was destroyed, and no winner was picked. Read this, then choose in your own time.

Short version: the three takes are three different bets on the same problem — getting Cape Jones to sit in his chair and look right.

- **Take 1 (Auto-Seat)** is the *measuring tool* — code that figures out exactly where the seat is and puts him on it.
- **Take 2 (Sitting Canon)** is the *whole room* — the full scene with his chair, his colors, a working recliner, and things that fall over when you knock them.
- **Take 3 (Mocap Sit)** is the *real human motion* — an actual recorded person sitting down, copied onto his body so it moves like a person, not a puppet.

---

## Take 1 — Auto-Seat (the chair-measuring solver)

**What it is:** Code, not a finished scene. Earlier sitting tests kept floating him above the chair or sinking him through it, because the old code measured the top of the chair's invisible bounding box instead of the real seat. This take fixes that: it shoots virtual measuring rays at the chair to find the true seat surface, loads a real seated motion clip, and places his body so his butt touches the seat, his back touches the backrest, and his feet touch the floor. It saves the seated pose and proof pictures.

**What it does well:**
- Solves the actual root problem — *where* the seat really is — with measurements instead of eyeballing.
- Small and focused: it's a tool the other approaches can use.

**What's rough:**
- It's a solver and test files, not something you watch. No finished scene comes out of it by itself.
- It went through several versions (v1, v2, v4, v5) chasing the right math, and the newest version's last test run ended in a divide-by-zero error — the trail is honest, the final version isn't proven clean yet.

**Where it lives:** GitHub repo `mhvnsnt/cape-jones`, branch `auto-seat-solver-20261019`, merged into main (PR #168). Full backup: release `sitting-wt-autoseat-20261019` (9 file parts + a checksum file; whole-package fingerprint `3c99be49…`).

**Get it back:** `gh release download sitting-wt-autoseat-20261019 --repo mhvnsnt/cape-jones` then join the parts (`cat part-* > wt-autoseat-full.tar`) — or just check out the branch.

---

## Take 2 — Sitting Canon (the whole room)

**What it is:** The full scene. He sits in his actual chair, in his actual living room, in his own colors — measured seat placement (his butt sinks 3.5 cm into the cushion like a real person's weight), facing out into the room the way you locked it, body-shape fixes applied (10 sculpted corrections, 23 over-twisted joints straightened), full 4K textures and the violet LED lighting. The chair is a working recliner — extend the footrest and his feet ride it. There's simple physics: knock the mug and it falls, hit the table hard and it tips. He gets a separate cloth cape that hangs from his shoulders instead of floating.

**What it does well:**
- The most complete picture of the three — it's the room, not just the sit.
- Placement is measured and locked as canon, and the proof pictures were checked with human eyes before shipping.
- Physics is modest: things only move when touched.

**What's rough:**
- The cape built into his body still bunches up when posed, and the separate cloth cape isn't finished simulating — that step needs a stronger machine (GPU) than the one this was built on.
- His feet don't reach the floor — the chair is tall for a character his size. Not a bug, but he won't look grounded.
- The pose is upright and neutral — he's not leaning back or relaxing yet.
- Full-quality renders crashed the small 8 GB machine; the proof pictures used a lower-detail stand-in body. A final beauty render still needs Kaggle GPU or similar.
- Honest gap: this take's big scene files (164 MB of Blender scenes) live in a different folder (`~/workspace/sitcanon-work/`, another lane's directory) that is **not** in this backup — the code, placement, and fixes are stored; the living scene files are stored only where that lane keeps them.

**Where it lives:** `mhvns
...[truncated 3454 chars]