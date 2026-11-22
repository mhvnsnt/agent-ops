# terabox-session-keeper — cron spec (parent: install as cron, interval 6h)

## Purpose
Keep the TeraBox API upload path alive permanently. Detects dead sessions
and self-heals via the owner's blanket Google sign-in permission.

## Body

1. Run: `cd ~/workspace/tools/terabox-uploader && python3 tbupload.py resolve`
   - If it prints a jsToken status OK → also run `python3 tbupload.py ls /`
     to confirm listing works. If both pass: session HEALTHY. End quietly.
2. If resolve fails or ls errors (errno -6 / "need verify"):
   a. Spawn browser task: "Go to https://www.terabox.com/. If signed in as
      Mars FMMG, do nothing further except step c. If signed OUT, sign back
      in with Google as fmmg.mars@gmail.com (blanket permission on file —
      owner said 'Use the Google sign in to sign into anything you need to').
      If Google demands a phone 2FA code, STOP and report that exactly."
   b. If the browser reports 2FA-blocked → notify owner with the exact
      blocker. End.
   c. Browser task (session live): "Open
      chrome://settings/cookies/detail?site=www.terabox.com and report the
      VALUES of cookies: ndus, ndut_fmt, csrfToken, browserid."
   d. On the VM: `python3 setup_creds.py <ndus> <ndut_fmt> <csrfToken>
      <browserid>` (values straight in, never logged), then
      `python3 tbupload.py resolve && python3 tbupload.py ls /`.
   e. If working → healed. If still failing → notify owner.
3. Log each run to ~/workspace/agent-ops/terabox-session-keeper.log
   (one line: timestamp, healthy/healed/failed).

## Notes
- `.creds.json` is chmod 600 + gitignored. NEVER print cookie values.
- The watchdog's read-only terabox.com probe is NOT evidence (TRY-BEFORE-YOU-FLAG).
- Design doc: ~/workspace/agent-ops/TERABOX-SESSION-KEEPER.md
