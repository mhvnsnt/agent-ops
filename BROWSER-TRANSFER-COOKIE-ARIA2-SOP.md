# Cookie -> aria2/curl Lane SOP (browser-transfer replacement)

**Cluster:** FRICTION-RESEARCH 2026-10-19 · pull-in 6/6 (owner order 2026-10-19 ~23:33 CDT: "Fix it all wire it all in wire it all up pull it all in")
**Research:** [[research-friction-20261019/06-browser-transfer-alternatives]] · **Index:** [[RESEARCH-PULLIN-INDEX]]
**Status:** SOP DOCUMENTED 2026-10-20 — docs only; queue #17 script (`tools/dl/tb-pull.sh`) and #15 rclone install still belong to the CloudDog integration lane
**Related:** [[ALIST-TERABOX-WEBDAV-EVALUATION]] (the preferred TeraBox path, owner-gated)

## Why this SOP exists

TeraBox `.blend` downloads (794MB + 515MB) failed **10/10** via the browser file-transfer tool —
every attempt returned "transfer's outcome is unknown" with zero file references. The browser
transfer path is unreliable for large files, and no native rclone TeraBox backend exists
(verified across rclone backend lists — the only path out is the browser session cookie).
This SOP is the recipe for pulling a file with zero browser-tool involvement after the
initial cookie capture: export cookies from a signed-in browser session once, then download
from the shell with resume, segmentation, retries, and hash verification.

Every flag below was verified against the real tool docs this session (Ubuntu aria2c manpage,
openSUSE yt-dlp manpage, gallery-dl upstream options.md, local `curl --help`) — no training-data flags.

## Tool availability on this VM (checked 2026-10-20)

- `curl` 8.5.0 — INSTALLED (flags verified via `curl --help all`)
- `rclone` v1.75.2 — LANDED as a static binary at `~/workspace/tools/rclone/rclone`
  (SHA256-verified, smoke-tested by pull-in 1/6; **not on PATH** — call it by full path
  or set `RCLONE_PATH`). Its WebDAV backend + `config create`/`copy`/`check` were verified
  against this binary's own `--help` for [[ALIST-TERABOX-WEBDAV-EVALUATION]].
- `aria2c`, `yt-dlp`, `gallery-dl` — NOT installed on this VM. Installing them belongs to
  the CloudDog integration lane, NOT this doc. All flags below are documented from the
  tools' real manpages/options, so the SOP is copy-paste ready the moment they land.

## Step 0 — Get the direct URL and the cookies

1. **Direct URL.** The browser transfer tool is out of the loop. The download URL comes from
   the source's own page/API (TeraBox share page, archive.org metadata API, host's "direct
   link" button), or from a resolver: `yt-dlp -g` / `gallery-dl -g` (see section 4), or the
   AList TeraBox driver (`[[ALIST-TERABOX-WEBDAV-EVALUATION]]`, owner-gated).
2. **Cookies.** From the signed-in browser (local-only add-ons only — "Get cookies.txt LOCALLY"
   for Chrome, "Export Cookies" for Firefox — never remote-export extensions):
   save as `/tmp/cookies-<source>.txt` (Netscape/Mozilla format). `chmod 600` it.
   aria2c reads Firefox/Mozilla/Chromium cookie files without modification (aria2c manpage).
3. **Never commit cookies.** They live in `/tmp` or come through the Secure Vault flow.
   Delete after the lane finishes. Cookies expire on logout / password change / inactivity
   (TeraBox behavior) — treat "401/403 on first byte" as "refresh cookies", not a tool bug.

## Step 1 — aria2c (primary: segmented, resume-capable)

`--load-cookies`, `-c`, `-x`, `-s`, `-k`, `-m`, `--retry-wait`, `--dry-run` all verified in the
aria2c manpage (manpages.ubuntu.com, focal).

```bash
# 0. Sanity: is the session still alive? (dry-run checks availability, downloads nothing)
aria2c --dry-run=true --load-cookies=/tmp/cookies-terabox.txt \
  "https://<direct-download-url>"

# 1. The download. 16 conns/server, 16-way split, resume on, retry 10x w/ 5s wait,
#    no splits smaller than 10M, fail fast on HTTP errors handled by -m/--retry-wait.
aria2c \
  -c \
  -x16 -s16 \
  --min-split-size=10M \
  -m 10 --retry-wait=5 \
  --connect-timeout=30 --timeout=120 \
  --load-cookies=/tmp/cookies-terabox.txt \
  -d /tmp/tbpull \
  -o target-name.blend \
  "https://<direct-download-url>"
```

Behavior notes (all from the manpage):

- `-c/--continue` resumes a partially downloaded file; the `.aria2` control file tracks byte
  ranges across runs. It also resumes downloads started by a web browser.
- `-x/--max-connection-per-server` (default 1) × `-s/--split` (default 5): splits only take
  effect per `-k/--min-split-size` (default 20M, range 1M-1024M). A 100MB file with
  `-s16 -k10M` yields ~10 real segments; don't overshoot `-s` beyond what `-k` allows.
- `-m/--max-tries` default is 5; 0 = unlimited. `--retry-wait` applies between retries and
  triggers on HTTP 503.
- `-d/--dir` + `-o/--out`: `-o` is always relative to `-d`.
- Optional integrity check when you know the hash: `--checksum=sha-1=<hexdigest>` (the
  manpage's documented example is `sha-1=0192ba11...`). Run `aria2c -v` on the lane to see
  which hash types the build supports (sha-256 depends on the build).

Discover more: `aria2c --help=#http`, `--help=#cookie`, `--help=#all` (tag system verified).

## Step 2 — curl fallback (always available on this VM)

Flags verified against local `curl --help all` (curl 8.5.0):

```bash
# Auth probe: headers only, cookies attached, fail fast on HTTP errors
curl -sIL -f -b /tmp/cookies-terabox.txt "https://<direct-download-url>" | head -20

# The download: follow redirects, fail fast, auto-resume partials,
# retry 10x with 5s delay on transient errors
curl -L -f -C - \
  -b /tmp/cookies-terabox.txt \
  --retry 10 --retry-delay 5 --retry-all-errors \
  -o /tmp/tbpull/target-name.blend \
  "https://<direct-download-url>"
```

- `-C -` = auto resume from the existing local file's size. Safe on a fresh start too.
- `-f/--fail` fails fast with no output on HTTP errors (4xx/5xx) — without it curl happily
  saves an error page as your `.blend`.
- `--retry-all-errors` extends retries beyond transient network errors (use with judgment;
  it will also retry 4xx — for an auth-expired cookie you WANT the fail-fast signal, so
  watch the first failure's code).

## Step 3 — Verify bytes, then clear

```bash
cd /tmp/tbpull
sha256sum target-name.blend > target-name.blend.sha256   # record what you got
# If the source publishes an expected hash:
echo "<expected-sha256>  target-name.blend" | sha256sum -c -
stat -c '%s %n' target-name.blend                         # size sanity
```

Delete-as-you-go (owner 2026-10-19): once the blob verifies hash-identical on the store,
drop the local copy during upload — disk falls mid-download, not after.

## Worked example — the TeraBox .blend case that motivated this

```bash
export TB=/tmp/tbpull/madelyn-blends && mkdir -p "$TB"
chmod 600 /tmp/cookies-terabox.txt

# One share link, known file name, no browser tool anywhere in the loop:
aria2c -c -x16 -s16 --min-split-size=10M \
  -m 10 --retry-wait=5 \
  --load-cookies=/tmp/cookies-terabox.txt \
  -d "$TB" -o scene_a.blend \
  "https://<terabox-direct-download-url-for-scene_a.blend>"

sha256sum "$TB"/scene_a.blend
# -> push to GitHub release / TeraBox per store law, verify, then clear local
rm -f /tmp/cookies-terabox.txt   # cookies never outlive the lane
```

If the direct URL is a share page (not a file URL), resolve it first: AList TeraBox driver
(owner-gated, `[[ALIST-TERABOX-WEBDAV-EVALUATION]]`) or a site-specific resolver — then feed
the resolved URL into this recipe.

## 4. yt-dlp and gallery-dl: the direct-link lane standards

**Rule of thumb:** reach for these BEFORE any browser involvement, for every host that is
not TeraBox. Neither covers TeraBox (yt-dlp has no TeraBox extractor — verified in the
cluster research).

| Tool | Reach for it when | Don't use it for |
|---|---|---|
| `yt-dlp` | Video/audio/streaming hosts (1,000+ extractors), HLS/DASH manifests, playlists. `-g` prints the direct media URL to hand to aria2/curl. | TeraBox shares (no extractor). Sites needing JS-heavy auth flows. |
| `gallery-dl` | Image galleries / media collections (boorus, art sites, social galleries). `-g` dry-runs the direct URLs. | Video hosts (yt-dlp's territory), TeraBox. |

Verified commands (openSUSE yt-dlp manpage; gallery-dl upstream `docs/options.md`):

```bash
# --- yt-dlp: give me the direct link (no download) ---
yt-dlp --cookies /tmp/cookies-site.txt -g "https://<page-url>"
# -g/--get-url is --print urls; --cookies takes a Netscape-format file;
# --cookies-from-browser BROWSER works too (brave/chrome/chromium/edge/firefox/opera/safari/vivaldi/whale)

# --- yt-dlp: full authenticated pull, aria2c doing the bytes ---
yt-dlp --cookies /tmp/cookies-site.txt \
  -R 10 -N 16 \
  -o "/tmp/dl/%(title)s.%(ext)s" \
  --downloader aria2c \
  --downloader-args "aria2c:-c -x16 -s16" \
  "https://<page-url>"
# -R/--retries (default 10), -N/--concurrent-fragments, -o output template,
# --downloader aria2c (alias: --external-downloader), --downloader-args "NAME:ARGS"

# --- gallery-dl: dry-run the direct URLs ---
gallery-dl -g --cookies /tmp/cookies-site.txt "https://<gallery-url>"
# -g/--get-urls prints URLs instead of downloading; -G/--resolve-urls also
# resolves intermediaries; -C/--cookies is the short form of --cookies

# --- gallery-dl: authenticated gallery pull ---
gallery-dl --cookies /tmp/cookies-site.txt \
  -d /tmp/dl \
  -R 4 --download-archive /tmp/dl/archive.txt \
  "https://<gallery-url>"
# -d/--destination, -R/--retries, --download-archive skips already-grabbed files
```

Cookie rules from section 0 apply to both tools (local export only, `/tmp`, `chmod 600`,
delete after). `--cookies-from-browser firefox` is convenient on a lane VM with a browser
profile; on headless lanes prefer the exported `cookies.txt`.

## Lane checklist (copy into the runbook)

- [ ] Direct URL resolved (not a share page) — AList / `-g` dry-run / page source
- [ ] `cookies.txt` fresh, `chmod 600`, in `/tmp` only
- [ ] `--dry-run` / `curl -IL` auth probe green before the big pull
- [ ] aria2c: `-c -x16 -s16 --load-cookies` + retries; or curl: `-L -f -C - -b` + retries
- [ ] Hash verified (`sha256sum -c`), size sane
- [ ] Stored (GitHub/TeraBox), verified on store, local cleared per one-store rule
- [ ] Cookies deleted

**Index:** [[RESEARCH-PULLIN-INDEX]]
