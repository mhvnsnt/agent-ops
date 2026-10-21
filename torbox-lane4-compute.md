# Lane 4 — Free compute / cloud-to-cloud transfer layer

**Date:** 2026-10-20 · **Status:** prototype built + tested locally · **No real credential was used anywhere in this lane**

## The problem, restated

A ~350 GB zip sits behind a TorBox dashboard CDN link. Three walls:

1. **Local disk is dead** (96–97% full) — nothing more can stage here.
2. **TorBox's API path caps out** — API returns `BAD_TOKEN`; the Essential
   plan's API allowance (~200 GB) is smaller than the file (350 GB).
   Dashboard CDN links bypass the API cap, but…
3. **The link itself is a bearer credential**, and it is DLP-denylisted as
   a tool parameter — an agent literally cannot be handed the link through
   chat tooling.

## The architecture that dissolves all three walls

Put the compute where the secret can be typed into a **platform's own
secret store by a human in a browser**, and stream through it:

```
                 pasted ONCE into the platform's secret UI (browser)
                 never in chat / git / agent tool parameters
                                │
                                ▼
 TorBox CDN link ──HTTP Range──► FREE COMPUTE ──pipe──► uploads.github.com
 (350 GB zip,      (tail + CD,   (GHA runner /           ──► private GitHub
  never fully       then only    Kaggle kernel)              release assets
  downloaded)       wanted       RAM: a few MiB              (< 2 GiB each,
                    slices)      Disk: 0 bytes               hash-verified)
```

Why this works, mechanically:

- The proven local code already does the hard part.
  `hero-parts-pull/zip_extract.py` reads a Zip64 central directory over
  HTTP Range and fetches only wanted files' byte ranges;
  `hero-parts-pull/github_upload_stream.py` pipes a byte stream straight
  into an `uploads.github.com` POST and verifies size + head/mid/tail
  range hashes. Neither needs the whole file, ever.
- A runner/kernel only needs **a few MiB of RAM and zero disk** if the
  extraction is slice-streamed (the local extractor held each file whole
  in RAM; the prototype fixes that — 1 MiB slices, streaming zlib).
- The secret problem is a *routing* problem, not a cryptography problem:
  GitHub Actions secrets, Kaggle Secrets, Cloudflare secrets, and HF
  secrets are all entered through that platform's own UI. The value goes
  browser → platform secret store → runner environment. Chat, agents,
  and their DLP filters are simply not in the path.
- Resumability is by construction: release assets are named by content
  (file name, or `slice-<start>-<size>.bin`); a re-run skips assets that
  already exist at the exact size — the same pattern the local uploader
  uses with its manifest. If a CDN link expires mid-run, paste a fresh
  link into the secret and re-run; finished slices/files are not redone.

## Verdict table

| Platform | Verdict | Why (evidence below) |
|---|---|---|
| **GitHub Actions** | ✅ **PRIMARY — prototype built** | Public-repo standard runners: free, no minute cap. Private: 2,000 min/mo free. 14 GB disk is irrelevant (streaming uses 0). 6 h/job cap solved by matrix fan-out (20 concurrent on Free). Secret store is exactly the DLP bypass needed. Same destination platform as the upload target — when target = same repo, not even a PAT is needed. |
| **Kaggle kernels** | ✅ **STRONG FALLBACK — variant included** | Internet-capable kernels, ~9 h sessions, CPU kernels don't touch the 30 GPU-h/week quota, Kaggle Secrets is a real secret store (`UserSecretsClient`). ~20 GB working cap is irrelevant when streaming out. Weaker than GHA only in automation (kernel push/run is clunkier) and session model. |
| **Google Colab** | ⚠️ Manual fallback only | Free runtimes up to 12 h, but idle timeouts (~90 min), no headless trigger, no durable unattended run. Fine if a human is already sitting in the notebook; wrong tool for a 350 GB unattended transfer. Has a Secrets pane (`google.colab.userdata`) in current Colab — verify in UI. |
| **Hugging Face Spaces** | ⚠️ Workable, awkward | Free CPU Basic: 2 vCPU / 16 GB / 50 GB *non-persistent* disk, secrets as env vars. But a Space is a long-running web app that sleeps, not a batch job — you'd expose a trigger endpoint and babysit it. No advantage over GHA for this job. |
| **Cloudflare Workers (free)** | ❌ Not an engine; ✅ optional proxy | Free: 100k req/day but **10 ms CPU/invocation, 128 MB RAM, 50 subrequests**. Any Zip64 parsing / zlib / hashing blows the CPU cap. A *pure pass-through* Range proxy survives (CPU isn't charged while waiting on the network; response body size unenforced) — useful only as URL laundering in front of a real engine. Prototype included, untested live (no CF account wired in this lane). |
| **Oracle Always Free ARM** | 🚩 Owner decision — **not recommended by this lane** | Technically the best always-on free VM (Ampere A1 + 200 GB block). But signup **requires a real credit/debit card** for identity verification (no prepaid/virtual), home region is permanent, free ARM capacity is frequently unavailable, and idle instances get reclaimed. Spending/identity step = owner's call only, per the brief. |
| **MultCloud / cloud-to-cloud services** | ❌ Dead end for this target | Supports ~30–40 clouds (Drive, Dropbox, OneDrive, MEGA, FTP/SFTP, WebDAV, S3…) — **no TorBox / debrid source, and no GitHub (let alone GitHub Releases) as a target**. Its URL "remote upload" lands in a cloud drive, not a release; the obvious free target (Drive, 15 GB) is two orders too small anyway. |

## Platform evidence

### GitHub Actions

- **Minutes:** "GitHub Actions usage is free for standard GitHub-hosted
  runners in **public repositories**"; private repos get a plan allowance
  — **2,000 min/mo on Free**, 3,000 Pro/Team, 50,000 Enterprise Cloud.
  ([GitHub plans doc](https://docs.github.com/en/enterprise-cloud@latest/get-started/learning-about-github/githubs-plans);
  [billing summary](https://www.codetalenthub.io/github-actions-free-tier/))
- **Runner:** Linux standard runner = 14 GB SSD (2 vCPU/8 GB private,
  4 vCPU/16 GB public per the current runner table). Our streaming peak
  disk is the checkout (< 1 MB) — the 14 GB never binds.
  ([runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners))
- **Job cap:** each job max **6 hours** execution; `timeout-minutes` max
  360. **Concurrency:** Free plan = **20 concurrent jobs**.
  ([Actions limits](https://docs.github.com/en/enterprise-server@3.18/actions/reference/limits))
  → Fan-out math (scenarios, not measurements — runner bandwidth was not
  benchmarked in this lane): one job must move its share in < 6 h, i.e.
  sustain ≥ share/21,600 s. A full 350 GB mirror split 20 ways = 17.5 GB
  per job ≈ 0.81 MB/s floor per job — a very low bar. The *selective*
  pull (the ~5 GB actually wanted in past pulls of this kind) is a
  single short job at any plausible speed.
- **Release asset cap:** each release file must be **< 2 GB** (2 GiB).
  The workflow defaults to the owner's **100 MB** asset standard
  (`slice_size=100000000`) and accepts anything < 2 GiB.
  ([storage limits write-up](https://gitprotect.io/blog/github-storage-limits/);
  [gh-large-releases, built around the same 2 GB limit](https://deepwiki.com/ading2210/gh-large-releases))
- **Secrets:** entered in repo Settings → Secrets and variables →
  Actions; injected as env; GitHub masks exact secret values in logs.
  This prototype additionally never prints the URL (scheme + host +
  path only, query redacted) and never puts it on a command line.
- **The unlimited-minutes shape:** make the *runner* repo public (code
  only — it contains no data and no secrets in git) and the *target*
  repo private, reached with a fine-grained PAT stored as a secret in
  the runner repo (scope: that one repo, Contents: Read and write,
  short expiry). Public minutes are free; the assets land private.
  If the target release may live in the runner repo itself, skip the
  PAT entirely — the built-in `GITHUB_TOKEN` with
  `permissions: contents: write` suffices.
- **⚠️ Terms flag (read before the first big run):** GitHub's Actions
  terms restrict uses unrelated to the repo's own software project
  (bulk file-hosting / distribution abuse is the classic enforcement
  case). This lane's honest read: streaming *this project's own assets*
  into *this project's own releases* is project-scoped CI-shaped work,
  and the selective pull is small. A repeated wholesale 350 GB mirror
  through a public repo is greyer and higher-profile. Keep runs
  project-scoped and modest, prefer the private-repo/2,000-min path
  when the job fits it, and treat any GitHub warning as a stop signal.
  This is a judgement call for the owner, surfaced — not hidden.

### Kaggle

- Kernels: CPU notebooks (4 cores / ~16 GB in secondary sources),
  GPU quota **30 h/week** (owner-known), sessions up to **~9 h**,
  saved output capped ~**20 GB**, internet is a notebook setting that
  must be ON. ([Kaggle constraints summary](https://deepwiki.com/hahuyhoang411/SmolDLM/5.2-kaggle-notebooks);
  [notebook resource notes](https://www.scribd.com/document/738541657/Data-Analysis-and-Machine-Learning-With-Kaggle-How-to-Win-Competitions-On-Kaggle-and-Build-a-Successful-Career-in-Data-Science-1801817472-978180181747))
- Secrets: Add-ons → Secrets; read with
  `from kaggle_secrets import UserSecretsClient` /
  `UserSecretsClient().get_secret("SOURCE_URL")` — same DLP bypass shape
  as GHA. ([GitGuardian on notebook secrets](https://blog.gitguardian.com/how-to-handle-secrets-in-jupyter-notebooks/))
- Use **CPU** kernels for byte moving; GPU quota is for renders.
  Variant script: `torbox-gha-prototype/kaggle/kaggle_kernel.py`.

### Cloudflare Workers

- Free plan, from Cloudflare's own docs: **100,000 requests/day,
  10 ms CPU time, 128 MB memory, 50 subrequests/request, 6 simultaneous
  outgoing connections**; request body cap 100 MB on the Free zone plan;
  **response body size not enforced**.
  ([Workers limits](https://developers.cloudflare.com/workers/platform/limits/);
  [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/))
- Conclusion drawn from those numbers: a Worker can *proxy* a Range
  stream (I/O wait is not CPU time) but cannot *be* the engine — parsing
  a central directory, inflating deflate streams, and SHA-256 over
  gigabytes inside 10 ms CPU slices is not a thing. Optional proxy
  prototype: `torbox-gha-prototype/cloudflare-worker/worker.js`.

### Colab / HF Spaces

- Colab free: notebooks run **at most 12 hours**, idle timeouts apply,
  availability varies. ([Colab FAQ](https://research.google.com/colaboratory/faq.html))
- HF Spaces free CPU Basic: **2 vCPU, 16 GB RAM, 50 GB non-persistent
  disk**; secrets configured per-Space and exposed as env vars; free
  Spaces sleep when idle. ([Spaces overview](https://huggingface.co/docs/hub/spaces-overview))

### Oracle Always Free

- Ampere A1 ARM + 200 GB block storage, always-free — but signup states,
  in every current guide: **a valid credit card is required for identity
  verification; virtual/prepaid cards are not accepted**; a small
  temporary hold is placed; the home region chosen at signup is
  permanent for Always Free resources.
  ([setup guide](https://www.techeia.com/blog/how-to-create-always-free-vm-in-oracle);
  [2026 limits write-up](https://site2us.com/en/servers/oracle-cloud-free-tier))
- **Flagged, not recommended.** If the owner ever chooses to create the
  account himself, an always-on ARM box becomes the cleanest engine of
  all (no 6 h cap, no minute accounting) — the same `range_list.py`
  runs there unchanged. Nobody else should make that signup call.

### MultCloud

- Supported set is mainstream cloud drives + FTP/SFTP/WebDAV/NAS/S3
  (~30–40 services). TorBox is not among them; GitHub is not among
  them. ([MultCloud supported clouds](https://www.multcloud.com/tutorials/access-all-your-clouds-with-one-login.html);
  [MultCloud intro, supported list](https://www.aomeitech.com/s-preview?f=pdf%2FMultCloud.pdf))
- No source, no target → no path. Closed.

### One more dead end, stated plainly

**Magnet-direct is not viable at 350 GB on any free tier above.** A
torrent client must land the bytes *somewhere* before re-chunking them;
every free disk here is 14–50 GB. The only shapes that work at this
size are (a) Range-selective extraction of wanted files, and (b)
Range re-chunking of the raw archive — both need the HTTP/CDN link,
which is exactly what the secret-store architecture delivers. (For a
*small* wanted subset, torrent file-selection on Kaggle's ~20 GB would
fit — fallback B, only if no CDN link can be obtained at all.)

## The prototype

`~/workspace/agent-ops/torbox-gha-prototype/` — README, workflow,
`range_list.py` (stdlib only), Kaggle variant, Worker proxy, test
evidence. Design deltas vs the local originals:

- CD parsed **incrementally** (8 MiB fetches, carry buffer) — no
  whole-CD or whole-file RAM residency anywhere.
- `extract-one` **verifies CRC32** against the central directory
  (the local script never checked).
- `slice` mode is a **stdout generator** for raw re-chunking:
  `range_list.py slice <start> <size> | curl --data-binary @- …uploads…`
- URL only from `SOURCE_URL` env; logs print scheme+host+path with the
  query redacted; size discovery falls back from HEAD to a `bytes=0-0`
  probe for signed links that reject HEAD.

### Test evidence (local, public file, 2026-10-20)

Target: the archive.org **Zip64** zip `OK KO.zip`,
7,910,137,932 bytes — previously parsed by the local pipeline
(`hero-parts-pull/okko-ia-centraldir.json`), so results cross-check.

| Test | Result |
|---|---|
| `list` | **476 entries / 428 files / 12.046 GB uncompressed** — matches the earlier independent parse (476 entries, 7,910,137,932 bytes) exactly |
| `extract-one ENID_01_RGB.ai` | 444,118 bytes streamed out; `size_ok=True`; **CRC32 computed `4843a44f` == CD CRC `4843a44f`**; sha256 `2245c7c3…a973a` |
| `slice 1000000 4194304` | sha256 `b8103775…c519` — **byte-identical to an independent `curl -L -r` fetch of the same range** |

Logs: `torbox-gha-prototype/test-output/` (`list-run.log`,
`extract-one-run.log`, `slice-crosscheck.txt`, `okko-manifest.json`).
YAML and both Python files pass syntax checks; `worker.js` passes
`node --check`.

**Not tested (needs the parent/browser lane):** an actual Actions run,
and Range behaviour of a real TorBox CDN link. Both are first-run smoke
items, deliberately sequenced: `mode=list` costs only ~70 KB + the CD
bytes and answers "does this link honour Range after redirects?" before
a single big byte moves.

## Runbook for the parent / browser lane

1. Create the runner repo with this prototype's code (public for
   unlimited minutes, or private if the job fits 2,000 min/mo and you
   prefer it — selective pulls fit easily). Push via the normal
   branch → PR → merge path. **No secrets in git, ever.**
2. In that repo: **Settings → Secrets and variables → Actions** —
   add secret `SOURCE_URL` (paste the TorBox dashboard CDN link in the
   browser), and, for a separate private target repo, secret
   `TARGET_PAT` + variables `TARGET_REPO`, `RELEASE_TAG`.
3. **Actions → torbox-range → Run workflow → `mode=list`.** Expect the
   manifest artifact + entry count in the log. If Range fails here, the
   link/CDN is the problem — nothing else was spent.
4. Then `mode=extract-one` per wanted file, or `mode=slice-upload`
   with the JSON offset list for a whole-archive mirror
   (100 MB assets by default; 20-way matrix max).
5. Verify per the workflow's built-in checks (upload size-exact; the
   extract pass prints CRC OK before the upload pass runs).
6. **Cleanup:** delete `SOURCE_URL` / revoke `TARGET_PAT` when done.
   Bearer link + PAT are spent once the transfer lands.

## Open questions / risks

- TorBox CDN link lifetime and Range-after-redirect behaviour: unproven
  until runbook step 3. Mitigation is built in (resumable assets,
  cheap smoke test first).
- GHA bandwidth from runner → TorBox CDN and runner → uploads endpoint
  was not benchmarked here; the 6 h math has huge headroom at 20-way
  fan-out, but the first real run should record its own throughput in
  the run log for the next plan.
- Actions terms flag (above) — owner's call on public-vs-private
  runner repo for the big mirror; selective pulls are low-profile
  either way.
- Kaggle internet-on kernels and the Colab Secrets pane are
  settings-level facts from secondary sources — confirm in the UI at
  setup time; neither blocks the GHA primary path.
