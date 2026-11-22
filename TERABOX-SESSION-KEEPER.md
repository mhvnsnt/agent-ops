# TeraBox Session Keeper — Permanent Fix Design

**Owner order 2026-10-16:** "fix this thing that keeps signing me out."

## Root cause

TeraBox web auth rides on the `ndus` cookie (plus `ndut_fmt`, `csrfToken`,
`browserid`). Community tooling (TeraboxUploaderCLI, terabox-complete-api,
terabox-gateway) all confirm: **the `ndus` cookie is long-lived — it does NOT
expire on its own** unless the user explicitly clicks "Sign Out" on terabox.com
(then uploads fail with "need verify" / errno -6).

So the sign-outs are NOT natural cookie expiry. The causes on our side:

1. **The leased Chromium profile gets reset** — runtime restarts / VM
   replacements wipe the browser profile the tasks share. Cookies die with it.
2. **Watchdog false flags** — the read-only terabox.com probe reported
   "logged out" 4 times and was wrong every time (TRY-BEFORE-YOU-FLAG LAW).
   Lanes that trusted the probe stopped work for no reason.
3. **The API upload path was never activated** — `~/workspace/tools/terabox-uploader/`
   (`tbupload.py` + `setup_creds.py`) is complete and tested in design but
   `.creds.json` was never created. Every upload still goes through the
   225MB-per-browser-task bottleneck, which needs a live browser session.

## The fix (three layers)

### Layer 1 — Activate the API upload path (one-time, needs parent)

The VM cannot read the browser's cookie store (separate sandbox), so the
one-time setup needs a browser task:

1. Browser task: "Go to terabox.com (verify signed in — if not, sign in with
   Google as fmmg.mars@gmail.com per blanket permission). Then open
   `chrome://settings/cookies/detail?site=www.terabox.com` and report the
   VALUES of cookies: `ndus`, `ndut_fmt`, `csrfToken`, `browserid`."
2. On the VM: `cd ~/workspace/tools/terabox-uploader && python3 setup_creds.py
   <ndus> <ndut_fmt> <csrfToken> <browserid> && python3 tbupload.py resolve`
3. Test: `python3 tbupload.py mkdir /CN-Gigaleak/_test &&
   python3 tbupload.py upload test-upload-1mb.bin /CN-Gigaleak/_test &&
   python3 tbupload.py ls /CN-Gigaleak/_test`

Cookie values go straight into `setup_creds.py` — never logged, never
committed (`.creds.json` is chmod 600 + gitignored). This is the flow the
README already documents; the owner ordered this fix which covers it.

Once live: `tbupload.py upload <file> <remotedir>` replaces browser uploads
entirely — 4MB chunks, auto-verify, no 225MB cap, no browser needed.

### Layer 2 — Session keeper cron (every 6 hours, needs parent to install)

New cron `terabox-session-keeper`, interval 6h. Body:

1. Run `python3 ~/workspace/tools/terabox-uploader/tbupload.py resolve`.
   - If jsToken resolves AND `ls /` works → session healthy. Done, quiet.
2. If it fails → spawn browser task: "Go to terabox.com. If signed in,
   report fresh values of cookies ndus, ndut_fmt, csrfToken, browserid from
   chrome://settings/cookies. If signed OUT, sign back in with Google as
   fmmg.mars@gmail.com (blanket permission on file), THEN report the cookies."
3. Write values via `setup_creds.py`, re-run `resolve`. Verify with `ls`.
4. If the browser ALSO can't sign in (e.g. Google wants phone 2FA) → report
   to owner with exactly what's blocking. This is the only case needing him.

### Layer 3 — Stop trusting the probe (already law)

TRY-BEFORE-YOU-FLAG LAW already covers this. The watchdog's read-only probe
is not evidence. Only a failed real attempt (browser check or API call)
counts as "logged out."

## What the owner never needs to do again

- Nothing, unless Layer 2 step 4 hits a Google 2FA wall. The keeper handles
  everything else: detection, re-auth via his blanket Google permission,
  cookie refresh, verification.

## Files

- Uploader: `~/workspace/tools/terabox-uploader/tbupload.py`
- Setup: `~/workspace/tools/terabox-uploader/setup_creds.py`
- Creds: `~/workspace/tools/terabox-uploader/.creds.json` (chmod 600, gitignored)
- This doc: `~/workspace/agent-ops/TERABOX-SESSION-KEEPER.md`
