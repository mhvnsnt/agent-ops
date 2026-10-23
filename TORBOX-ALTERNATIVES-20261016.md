# TorBox Alternatives — Free/Open-Source Research
**Date:** 2026-10-16 | **Researcher:** subagent | **Budget:** $0

## Executive Summary

**Key finding:** Torrent swarms are DEAD from this VM (verified: 0 peers, 0 bytes in 60s test with libtorrent). This means self-hosted torrent clients (qBittorrent, Transmission, Deluge) CANNOT work here — they need peer connections that the network blocks.

For torrents, the ONLY free path is a **remote debrid/seedbox service** (they download on their servers, we pull via HTTPS). For everything else, **direct HTTP downloads** (Internet Archive, GitHub) already work great.

## What's Verified Working NOW ($0)

### 1. Internet Archive (archive.org) — PRIMARY ROUTE ✅
- **What:** Direct HTTP downloads from archive.org
- **Cost:** $0, no account needed
- **API:** Yes — `https://archive.org/download/<item>/<file>`
- **Status:** Already the team's primary route, working great
- **Use for:** Game ISOs, ROMs, large files hosted on IA

### 2. GitHub Releases — SECONDARY ROUTE ✅
- **What:** Direct HTTP downloads from release assets
- **Cost:** $0
- **API:** Yes — `gh` CLI + REST API
- **Status:** Already heavily used, working great
- **Use for:** Tools, extracted files, team deliverables

### 3. TorBox Free Tier — OWNER'S ACCOUNT ⚠️
- **What:** Debrid service with permanent free tier
- **Cost:** $0 (free tier: 1 slot/day, 10GB/file limit)
- **API:** Yes — full REST API, connector at `~/workspace/custom-connectors/custom.torbox/`
- **Status:** Owner has account, but API returning 401 (credential issue). Owner fixing himself.
- **Note:** Local helper scripts had a bug (credential placement changed from bearer_header to query_param). Fixed the scripts, but API still 401s — the stored key itself may be expired.
- **Use for:** Torrent → direct link (when working)

## Free Sign-ups Worth Doing (Browser Required)

### 4. World-Debrid — 1 Free Debrid/Month 🆓
- **URL:** https://world-debrid.com/
- **Free tier:** 1 debrid per month, permanent. Email or Google signup, NO credit card.
- **What it does:** File-hoster links (1fichier, RapidGator, Mega, Turbobit, Uploady, etc.) → direct download links
- **Torrent support:** NO — hosters only, not magnets
- **API:** Unclear — primarily browser-based
- **Verdict:** Useful for file-hoster links, NOT for torrents. Worth the free signup for the 1/month.
- **Action needed:** Browser sign-up with Google (fmmg.mars@gmail.com)

### 5. Seedhost.eu — 24-Hour Free Trial Seedbox 🆓
- **URL:** https://www.seedhost.eu/
- **Free tier:** 24-hour free trial seedbox (they claim "we are the only ones to offer free seedboxes for 24 hours")
- **What it does:** Full seedbox — add torrents via web UI, download via HTTPS/FTP
- **API:** qBittorrent Web API (standard)
- **Verdict:** Good for one-off large torrent pulls. 24h is enough to grab a specific torrent.
- **Action needed:** Browser sign-up

### 6. Pulsed Media — 30-Day Free Trial (When Available) 🆓
- **Free tier:** 30-day trial (50 GiB storage, 250 MB RAM) "when trial slots are open"
- **What it does:** Full seedbox with SSH access
- **Verdict:** Best free trial if slots are open. Check availability.
- **Action needed:** Browser sign-up, check trial availability

## What Does NOT Work (Verified)

### ❌ Self-Hosted Torrent Clients on VM
- **Tested:** libtorrent with real .torrent file (Big Buck Bunny from archive.org)
- **Result:** 0 peers, 0 bytes in 60 seconds. Swarm completely unreachable.
- **Why:** VM network blocks P2P peer connections (UDP blocked, TCP peers unreachable)
- **Applies to:** qBittorrent, Transmission, Deluge, aria2c — all dead for swarms on this VM
- **Note:** HTTP trackers are reachable, but no peer connections succeed

### ❌ Torrin (torrin.app)
- **Claimed:** "Free tier available"
- **Reality:** Only a 3-day trial (1 download at a time, 50GB max). Then $2.99/mo minimum.
- **Verdict:** NOT free. Skip.

### ❌ Debrid-Link / Real-Debrid / Premiumize / AllDebrid
- **Free tier:** None (AllDebrid has 7-day trial with SMS verification only)
- **Verdict:** Paid only. Owner already considering Debrid-Link €4/30d separately.

### ❌ World-Debrid for Torrents
- **Reality:** Hoster links only, no magnet/torrent support confirmed
- **Verdict:** Useful for hosters, not for our torrent needs

## Recommendations

### Immediate (no signup needed):
1. **Keep using Internet Archive + GitHub** — these handle 90% of download needs
2. **Fix TorBox** — owner is handling this himself; it's the best torrent route when working

### Quick wins (one browser signup each):
3. **Sign up for World-Debrid** (Google, no card) — bank the 1 free debrid/month for hoster links
4. **Grab Seedhost.eu 24h trial** when a specific large torrent needs pulling

### For large one-off pulls:
5. **Pulsed Media 30-day trial** — check if slots are open, best free option for sustained use

## Technical Notes

### TorBox Helper Scripts Fixed
The scripts in `~/workspace/custom-connectors/custom.torbox/bin/` were broken due to a credential placement change (bearer_header → query_param). Fixed:
- `tb_mylist.py` ✅
- `torbox_add_magnet.py` ✅  
- `tb_export.py` ✅

However, API still returns 401 — the stored credential itself needs refreshing (owner's domain).

### VM Network Constraints (Verified 2026-10-16)
- HTTP/HTTPS: ✅ Works (via egress proxy)
- Direct TCP to tracker ports: ✅ Reachable
- BitTorrent peer connections: ❌ Dead (0 peers)
- UDP: ❌ Blocked
- **Conclusion:** Any solution requiring P2P from the VM will fail. Must use server-side downloads (debrid/seedbox) or direct HTTP.
