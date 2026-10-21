# Lane 7 — Free-Trial Seedbox Angle (Seedhost.eu + Pulsed Media + others)

Date: 2026-10-20 (researched live this session)
Target: `Documents.zip` — ONE file, 350,016,069,428 B (= 350.0 GB decimal = ~326 GiB)
Infohash: `856d01039553693d51c2a98523ca2c9829e8bb63`
Actual need: ~125 GB of gap ranges INSIDE the zip. Because the torrent is a
single file, qBittorrent/ruTorrent **file** priorities cannot skip inner zip
entries — the only seedbox-side selective paths are (a) hold the whole file,
or (b) shell/SSH + a custom client (libtorrent piece priorities) that only
fetches the pieces covering the wanted byte ranges.

## VERDICT: DEAD for this torrent as a free-trial path

No free trial found holds the file, and none holds even the wanted ranges
at once. Numbers:

| Candidate | Free trial (verified) | Trial storage | SSH/shell on trial? | vs 350 GB full | vs ~125 GB gaps-at-once |
|---|---|---|---|---|---|
| **Pulsed Media** | 30-day free, **when slots open** | **50 GiB**, 250 MB RAM | **YES** — user-level SSH, full PMSS set | FAIL 6.5× (326 GiB needed) | FAIL 2.3× (~116 GiB needed) |
| **Seedhost.eu** | **NO free trial on current site** — 7-day money-back on PAID plans only | n/a (old 24 h trial no longer offered; its size was never published) | Paid: SSH on all Shared except HD 1 | FAIL — nothing free to hold it | FAIL |
| **Ultra.cc** | **No trials at all** (official FAQ) | — | — | FAIL | FAIL |
| Whatbox / Feral / Seedboxes.cc / RapidSeedbox | No free tier (Pulsed comparison table) | — | — | FAIL | FAIL |
| Seedbox.io | No free trial — 14-day money-back only | — | — | FAIL | FAIL |
| sdbx.moe | Free 2-day trial **on Discord request** | Not published, no ≥100 GB evidence | Unknown | FAIL / unproven, and Discord request = manual work | FAIL |

This lane is backup-path verification only — the TorBox direct path
(`requestdl` + CDN ranges) already works per the other lane. Nothing here
beats it, and nothing here is worth the browser lane's time.

## 1. Seedhost.eu — the "24-hour free trial" no longer exists

- **Current official homepage (fetched this session, https://www.seedhost.eu):**
  under "NEED A TRIAL ACCOUNT?" it now says: *"All our hosting packages are
  covered with 7 days money back policy. You can order any of our account
  and use it as a test, you can cancel it with the first 7 days and we will
  refund your money."* That is a **paid order + refund**, not a free trial:
  it needs a payment method, a browser checkout, and a refund claim.
- Pulsed Media's competitor comparison (fetched this session) corroborates:
  Seedhost.eu — **Free Tier: No, Refund Period: 7 days**, clients
  rTorrent/Deluge/qBittorrent/Transmission.
- The "only ones to offer free seedboxes for 24 hours" line survives only in
  old third-party site mirrors (technofizi.net crawl of the old site copy)
  and a ~2012 press release (sbwire). **No current Seedhost page publishes a
  trial size** — there is nothing to verify ≥350 GB against, because there
  is no trial to size.
- Paid plans (official, fetched https://www.seedhost.eu/shared-app-hosting/):
  HD 1 = 1 TB disk / 1 TB traffic / €3/mo (**no SSH** — FAQ: *"Yes, we offer
  SSH access with all Shared App Hosting accounts, except HD 1"*; no root on
  Shared); HD 2 = 2 TB / 2 TB traffic / €5/mo with SSH, *"welcome to install
  anything locally via SSH in your HOME path."* Apps include
  rTorrent/ruTorrent, qBittorrent, Deluge, Transmission.
- So a paid HD 2 (€5) *would* fit the full 350 GB with shell access — but
  that is a purchase, not this lane's free-trial question, and it still
  requires the (currently flaky) browser lane for checkout.
- HTTPS file access: files are served via the account web space / apps
  (e.g. additional web users via `.htaccess`, per Seedhost knowledgebase).
  **HTTP Range support is not documented/published — UNVERIFIED.** SFTP/FTP
  access is documented (their migration KB references FTP/SSH access).

## 2. Pulsed Media — real free trial, real shell, 7× too small

Official wiki, fetched this session
(https://wiki.pulsedmedia.com/wiki/Computer_resource):

- *"A free 30-day trial (50 GiB, 250 MB RAM) is offered when trial slots
  are open"* + 14-day money-back on paid plans. Slot availability is
  conditional — no guarantee a slot is open today.
- User access (same page): *"SSH — User-level shell access (no root). Run
  commands, manage files, install user-space software"* + web panel with a
  browser shell console. Free tier is listed on the wiki as *"Free Seedbox
  — full PMSS feature set, evaluation use."*
- Stack (wiki Seedbox page, fetched): torrent clients rTorrent/ruTorrent,
  Deluge, qBittorrent; file access **SSH, SFTP, SCP, FTP, HTTPS downloads,
  WebDAV**; 100+ pre-installed CLI tools incl. Python 3, p7zip/unrar,
  rclone; rootless Docker on all plans; public trackers allowed.
- Limits that bite: the media-stack installer *"stops on accounts with less
  than 1000 MiB of memory, so it does not fit the free trial (250 MB)"* —
  irrelevant to torrenting, but it shows how thin the trial slice is.
- Free page (fetched https://pulsedmedia.com/free-seedbox.php): *"You may
  go beyond your storage limit by 25% for up to 7 days"* — even bursting,
  50 GiB → 62.5 GiB (~67 GB), still <125 GB and ≪350 GB.

### The shell / piece-priority path — why it still fails

Pulsed is the one candidate where the (b) path is *technically* real:

- SSH + Python/libtorrent (or a custom client) can set **piece** priorities
  so only pieces overlapping the wanted zip ranges download, stored as a
  sparse file — qBittorrent's own UI/API only exposes *file* priorities,
  which are useless inside a single-file torrent.
- **But the wanted ranges total ~125 GB and the quota is 50 GiB (53.7 GB).**
  Holding the wanted pieces at once overflows quota by ~2.3×; holding the
  full file overflows by ~6.5×. Quota enforcement would stall/kill the
  download long before completion.
- The only theoretical workaround is a rotating batch loop: fetch a
  <50 GiB batch of pieces → extract those zip entries locally on the box
  (p7zip is pre-installed) → offload via SFTP/rclone/HTTPS → delete →
  repeat. That is unproven custom tooling on a 250 MB RAM trial account,
  dependent on an open trial slot, with zip central-directory handling and
  quota behaviour untested. It is a research project, not a backup path —
  especially when the TorBox direct path already works today.
- HTTPS Range: files are served by per-user lighttpd over HTTPS, which in
  principle supports Range requests, but **Pulsed does not document a Range
  guarantee — UNVERIFIED.** SFTP (resumable) is documented and would be the
  reliable pull method.

## 3. Any other free-trial seedbox ≥100 GB?

None found. Web searches this session (queries on free-trial seedbox
storage/SSH, Seedhost/Pulsed/Ultra specifically) surfaced only:

- **Ultra.cc — explicitly no trials.** Official docs FAQ (via search):
  *"Does Ultra.cc Offer Trials? No. Ultra.cc does not offer free trials"* —
  new customers only get a 7-day first-order refund policy. Paid entry
  €4.95/mo / 1 TB would fit, but it is not free.
- **Pulsed comparison table** (fetched): Whatbox, Feral Hosting,
  Seedboxes.cc, RapidSeedbox, Seedhost.eu, Ultra.cc — **Free Tier: No**
  for every one; Pulsed is the only "Yes" in the table.
- **Seedbox.io:** money-back (14 days) only, no free trial found.
- **sdbx.moe ToS (via search):** *"A free 2 day trial is available … The
  request must be made on our Discord server"* — 2 days, request-by-Discord
  (manual step), storage not published, no evidence of ≥100 GB, let alone
  350 GB. Fails both the size-evidence and the no-manual-work tests.

No provider anywhere in the sweep offers a free trial with ≥100 GB
storage. The largest verified free seedbox storage in existence here is
Pulsed's 50 GiB.

## 4. Signup path (for completeness — NOT recommended)

Best candidate on paper is Pulsed (only real free trial + shell), and even
it is dead on storage (above). If the parent ever wanted to confirm a slot
anyway, it is **browser-dependent — flagging clearly: this subagent cannot
operate a live browser, and the parent's browser lane is noted as flaky.**

1. Browser → https://pulsedmedia.com/free-seedbox.php → order the free
   30-day trial (WHMCS-style email signup; no Google OAuth advertised —
   Google sign-in `fmmg.mars@gmail.com` does not appear to be an option).
2. If no slot is open, the flow dead-ends — availability is the first gate.
3. Credentials arrive by email; SSH/SFTP details are in that email.
4. Even with an account in hand: do NOT add the 350 GB magnet expecting
   selective download — see §2 math. The account cannot hold the result.

Seedhost "trial" path would be: browser → seedhost.eu → order HD 2 (€5,
payment method required) → cancel within 7 days for refund. That is a
purchase + refund gamble, requires payment details the owner has not
offered for this, and is out of scope for a free-trial lane.

## Honest math summary

- Full file: 350,016,069,428 B = 326 GiB. Best free trial: 50 GiB.
  **Shortfall 276 GiB (6.5×).**
- Wanted gaps only, all at once: ~125 GB ≈ 116 GiB vs 50 GiB.
  **Shortfall ~66 GiB (2.3×)**; vs 62.5 GiB burst limit, still ~1.9× short.
- Seedhost: free trial storage = **does not exist** in 2026 (paid + 7-day
  refund only).

**Angle declared DEAD for this torrent.** Keep the working TorBox direct
path as primary; the only seedbox that would fit is a *paid* one
(Seedhost HD 2 €5/mo / 2 TB + SSH, Ultra.cc €4.95/mo / 1 TB, Pulsed paid
≥1 TB tiers) — a purchase decision for the owner, not a free trial.

## Evidence (fetched this session)

- Seedhost homepage (trial = 7-day money-back; shared from €5/mo, 2 TB):
  https://www.seedhost.eu
- Seedhost shared plans + SSH FAQ (HD 1 1 TB €3 no SSH; HD 2 2 TB €5):
  https://www.seedhost.eu/shared-app-hosting/
- Pulsed wiki — free trial 50 GiB/250 MB, SSH user shell, money-back:
  https://wiki.pulsedmedia.com/wiki/Computer_resource
- Pulsed wiki — feature comparison (free tier: Pulsed Yes, all others No;
  Seedhost refund 7 days): https://wiki.pulsedmedia.com/wiki/Seedbox_Feature_Comparison
- Pulsed free seedbox page (25% over-limit for 7 days; 14-day money-back):
  https://pulsedmedia.com/free-seedbox.php
- Ultra.cc no-trials FAQ + sdbx.moe 2-day Discord trial + Seedbox.io
  money-back: via web search results this session (docs.ultra.cc FAQ,
  sdbx.moe/terms, the-bestvpn.com) — index-grade, not full-page fetches.
- Prior research read, not redone:
  `~/workspace/research_notes/torbox-alternatives-2026-20261016-2150/report.md` §2
  and `~/workspace/agent-ops/torbox-lane3-alternatives.md` (Pulsed 50 GiB —
  confirmed above from the official wiki).
