# SLPS02182 dedup evidence — browser_downloads/sess-3802796762

Game: Tokyo Wakusei Planetokio (PSX, 3 discs), SLPS02182.
Source lane: `_sato-wh-minigames-20261120/CHECKPOINT.md` line 116 (archive.org item
tokyowakuseiplanetokio_psx, access-restricted; torrent btih
540b9b0c9e4b994569d922789268098fb0b8c4f1). Planned destination: release
`sato-planetokio-rhythm-20261120`, mhvnsnt/game-reverse-engineering, streamed in
24 MiB verified parts.

## Hash verification (md5sum, 2026-11-21 ~21:20 UTC — all match Redump MD5s in the checkpoint)

| Disc | MD5 | Size (bytes) | Copies on disk |
|---|---|---|---|
| SLPS02182_1.BIN | af980faf3acb1f12182ab9c9f336a779 | 633,407,712 | 3 |
| SLPS02182_2.BIN | ce2b6ba1bcd6bee3715cc6d47ea4245a | 660,810,864 | 2 |
| SLPS02182_3.BIN | 60d7a1e0e6435bc1bd97765648c0ec51 | 695,399,376 | 2 |

Sizes also match the archive.org metadata sha1/sizes in the checkpoint exactly
(sha1 86d312f0…, 50bd9029…, 9a30499d…).

## Dedup opportunity

Extra copies: 2× disc 1 + 1× disc 2 + 1× disc 3 = **2,623,025,664 bytes (~2.44 GiB)**
reclaimable by deleting the duplicate files while keeping one verified copy of
each disc on disk. (7 CUE files, 77 B each, also duplicated; negligible.)

## Why NOT deleted this run (2026-11-21 16:xx EST guardian run)

1. The discs are NOT one-store verified: release
   `sato-planetokio-rhythm-20261120` currently holds only SLPS02634.BIN parts +
   planetokio-scans.rar parts (a different game) — no SLPS02182 assets yet.
   The local copies are the only copy of these discs. They stay.
2. The MANDATORY PRE-CLEAR GATE on the session dir returns BLOCKED on
   [recency] (downloaded 2026-11-20 22:38–23:24 UTC, <24 h old at run time).
   Gate verdict is logged in `disk-cleanup-log.md`.
3. The Sato checkpoint does NOT literally name `browser_downloads` or the
   session dir (grep count 0), so [dependency] does not block on that
   checkpoint — recency is the live blocker, clearing ~23:24 UTC 2026-11-21.

## What a future run needs

- After recency clears AND the discs are uploaded to the release per the Sato
  lane's plan (24 MiB verified parts), the whole session dir becomes a
  manifest-based clear candidate (~4.3 GiB), not just a dedup.
- Dedup-alone (2.44 GiB, content stays on disk) is a gate-scope question: the
  gate covers whole-directory clears and has no dedup mode — do not do it
  unilaterally; it needs either a manifest-based clear after store-verify or
  an owner/main-agent call.
- Do NOT re-hash to confirm: MD5s above are the evidence.
