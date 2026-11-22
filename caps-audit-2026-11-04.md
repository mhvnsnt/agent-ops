# Free-Tier Caps Audit — 2026-11-04 (READ-ONLY)

Owner approved this audit on 2026-11-04 and will personally approve every deletion afterward.
**Nothing was deleted, no budget was changed, no plan was changed, no card was touched.**
All figures below were measured live during this audit (2026-11-04 ~18:10–18:25 CST).

---

## Section 1 — Vercel: Deployment Storage, team `orion-enterprises-llc`

**Situation (from Vercel's 2026-11-03 email):** 100% of included Deployment Storage used — 10 GB of 10 GB.

**What the connector can see:** The Vercel connector is signed in as mhvnsnt (fmmg.mars@gmail.com), plan: Hobby, default team `team_mVloBIMoIfJSbcOwzZFcLsWU` = scope `orion-enterprises-llc`. The team has exactly **ONE project: `physics-playground-pwa`** — it is the only thing consuming this team's deployment storage.

**Deployment inventory (complete, paged through all of them): 122 deployments, all created in a ~30-hour window** (oldest 2026-11-03 12:35 CST, newest 2026-11-04 18:06 CST):

| Kind | Count | Notes |
|---|---|---|
| Production, READY | 42 | Only the newest 3 are protected by Hobby retention |
| Production, CANCELED | 1 | Dead build, protects nothing |
| Preview, READY | 41 | Branch/PR previews, none are production |
| Preview, CANCELED | 38 | Dead builds |
| **Total** | **122** | |

**Current production (KEEP, untouchable):** `dpl_X2tdLaQk8jy3VZjwgj3T7psZf2Hj`, created 2026-11-04 18:06 CST, commit `8959a8a3` ("Land clean-UI layout rules"). Second and third newest production (also inside Hobby's automatic keep-set): `dpl_8VnjHv1mLS4vVdDpzRQLGqEmAtNf` (2026-11-04 10:15 CST) and `dpl_Fg2PVfdTNruK5JqYfXopakquvRWg` (2026-11-04 08:07 CST).

### Per-deployment sizes: NOT obtainable — exact blocker

Vercel's deployment list exposes **no size field**, and the two endpoints that could show file-level detail are blocked for this connection:

- `get_deployment` / `list_deployment_files` require team scope → **403 "Not authorized: Trying to access resource under scope orion-enterprises-llc. You must re-authenticate to this scope."** The API's suggested recovery (`authorize_team_access`) is **not among the tools this connector exposes**, so the re-auth link cannot be generated from here.
- `list_billing_charges` → **404 `costs_not_found`** (Hobby plan has no charges data).

So no per-deployment sizes are listed below — inventing them would be guessing. The only size fact is Vercel's own total: **10 GB stored across these 122 deployments.**

### Vercel deletion candidates

| Candidate | Count | What it is | Recommendation |
|---|---|---|---|
| Preview deployments, CANCELED | 38 | Dead branch builds from the Nov 3–4 CI storm, never served | **DELETE** — zero risk, they are not running anywhere |
| Preview deployments, READY | 41 | Branch/PR preview builds, all ≤36 hours old, none is production | **DELETE** — previews are disposable and rebuilt on the next push |
| Production deployments, CANCELED | 1 | One canceled production build | **DELETE** — never went live |
| Production READY older than the newest 3 | 39 | Superseded production builds (Nov 3 12:35 CST – Nov 4 08:07 CST) | **DELETE** — Hobby only guarantees keeping the newest 3 production anyway; current production is not in this set |
| Newest 3 production deployments | 3 | Current production + 2 rollback points | **KEEP** — current production stays intact |

**Vercel total freed if all 116 candidates are approved:** the full stored set is 10 GB across 122 deployments; deleting 116 of 122 removes the overwhelming majority of it. A precise GB figure per group cannot be stated because per-deployment sizes are blocked (above). If deployments were uniform in size — they are not, this is only a scale estimate — 116/122 ≈ **~9.5 GB of the 10 GB**.

**Root cause worth knowing:** 122 deployments in ~30 hours means every CI run and push is creating a full new deployment that is kept. The cap will refill at the same speed unless old deployments are pruned regularly.

---

## Section 2 — GitHub: Actions storage, account `mhvnsnt`

**Situation (from GitHub's 2026-11-04 email):** 0.48 GB used / 0.5 GB included (90%), resets 2026-12-01; overage billed "unless a $0 budget is set."

**$0 budget check: NOT verifiable.** `gh api users/mhvnsnt/settings/billing/actions` returns **403 "Resource not accessible by personal access token"** (token scope) — retested during this audit, same result. Whether a $0 spending budget is set **cannot be confirmed from here**; it can only be checked on GitHub's website under Settings → Billing. This matters: the live artifact total measured below is far above the included 0.5 GB.

**Why the email says 0.48 GB but the live total is ~9.9 GB:** GitHub's storage figure is a billing-period (GB-hour averaged) number as of the email's timestamp (2026-11-04 02:01Z), and a large share of the artifacts below were created in the CI runs since. Both numbers are real; the live point-in-time total is what deletion acts on.

### Artifact inventory by repo (live API, complete via pagination)

| Repo | Artifacts | Live size | Expired |
|---|---|---|---|
| mhvnsnt/western-heart | 2,227 | **9,070.0 MB** | 0 |
| mhvnsnt/physics-playground-pwa | 155 | **797.4 MB** | 0 |
| mhvnsnt/cape-jones | 0 | 0 | — |
| mhvnsnt/agent-ops | 0 | 0 | — |
| mhvnsnt/game-reverse-engineering | 0 | 0 | — |
| mhvnsnt/Mochiichao-Crystal-Version-2d | 0 | 0 | — |

**Nothing is expired anywhere** — every artifact is live and counting until its retention date (mostly 2027-02-01/02, i.e. the default 90 days).

### GitHub deletion candidates

| # | Candidate | Size | Age / expiry | What it is | Recommendation |
|---|---|---|---|---|---|
| G1 | western-heart `menu-touch-shots` — 1,181 artifacts | **8,435.6 MB** | Created on every CI run; expire 2027-02 | Screenshot sets (~7.45 MB each) uploaded by the menu-touch-e2e check on every western-heart PR run. The proof copies that matter are committed in the repo under docs/proof/; these are duplicate CI outputs. | **DELETE (all, or all but the newest few)** — this one item is ~85% of the entire account's artifact storage and it regenerates on every CI run |
| G2 | physics-playground-pwa `public-dist-preflight` — 2 artifacts | **431.4 MB** (233.2 + 198.1) | Created 2026-11-03 16:31 CST and 2026-11-03 19:55 CST, branch `fix/ci-deploy-allowlist-startup-entry`; expire 2027-02-01/02 | Full preflight dist snapshots from a fix-branch deploy effort | **DELETE** — branch work snapshots, not needed once the fix landed; biggest single win in this repo |
| G3 | physics-playground-pwa `e2e-screenshots` — 153 artifacts | **366.0 MB** | Created across Nov 3–4 CI runs; expire 2027-02 | Per-run e2e screenshot outputs (~0.04–1.6 MB each) from the overnight CI/deploy runs | **DELETE older ones** (keep the newest handful if he wants a recent reference) — regenerated every run |
| G4 | western-heart `github-pages` — 1 artifact | **630.0 MB** | Created 2026-11-04 05:45Z, **expires on its own 2026-11-05 05:44Z** (1-day retention) | The Pages deployment artifact for the live Western Heart build | **DO NOT DELETE — let it expire** (hours away); it is tied to the live site deploy |
| G5 | western-heart `material-gate` — 1,041 artifacts | 4.3 MB total | Ongoing; expire 2027-02 | Near-empty gate-result outputs (~4 KB each) | **Optional** — deleting frees almost nothing (4.3 MB); only worth it as tidiness |
| G6 | western-heart `test-output`, `checkout-debug`, `test-debug-979` — 4 artifacts | ~0 MB | — | Debug outputs | **Ignore** — zero size |

### Actions cache (separate pool — does NOT count toward the 0.5 GB artifact storage)

Cache has its own 10 GB-per-repo limit and auto-evicts; it is reported here only for completeness:

| Repo | Active caches | Size |
|---|---|---|
| western-heart | 916 | 1,169.3 MB |
| Mochiichao-Crystal-Version-2d | 1 | 78.6 MB |
| All other audited repos | 0 | 0 |

**Recommendation: no cache action needed** — under its own limit, self-managing, and not part of the billed artifact figure.

### GitHub totals

- **Recommended deletion set (G1 + G2 + G3): ~9,233 MB (~9.0 GB) freed** — takes live artifact storage from ~9,867 MB down to ~634 MB, of which 630 MB (G4) self-expires on 2026-11-05 anyway, leaving ~4 MB.
- Optional tidiness (G5): +4.3 MB.

---

## Blockers and unverifiable items (stated plainly)

1. **Vercel per-deployment sizes:** blocked — team-scope 403 on the detail endpoints, and the connector does not expose the `authorize_team_access` recovery tool. Only the account-level total (10 GB, from Vercel's own email) and the full deployment inventory were obtainable.
2. **GitHub $0 budget status:** blocked — billing endpoint 403 (personal-access-token scope), retested this audit. Checkable only on github.com under Settings → Billing.
3. Everything else in both sections was read live from the APIs during this audit.

## What was NOT done

No deletions, no budget changes, no plan changes, no card activity, no settings changes of any kind. This report is the candidate list for the owner's per-item approval.
