# WH fixable-PRs work log — 2026-10-23 (conflict-resolution worker)

## PR #841 — Submenu: versus setup rebuilt from Tekken 7 GAME OPTION (worker-submenus/versus-setup-v2)
- State at start: DIRTY (mergeable_state=dirty), head f914b60c, base ba25f89.
- Contamination check: PASS — tree carries only versus-setup work (game/js/versus-setup.js,
  rules.js, submenus.css, docs/decisions/2026-10-23-submenu-versus-setup.md,
  teardown/tekken7/ui/GAME-OPTION-VS-MENU.md, proof shots, e2e test). No foreign files (#832's flaw absent).
- Conflicts vs main@06d3361b (PR #903): 2 — game/index.html (stylesheet link:
  branch submenus.css vs main t7-skin.css → kept BOTH), game/ui_sources.json
  (branch screen-vssetup entry vs main hud-fight entry → kept BOTH; JSON validated).
- Merge commit 05a08e5b pushed. CI: instruction-gate/deletion-guard/clobber-guard/
  ui-sources/canon-names/rig-guard/game-unit-tests GREEN; menu-touch-e2e RED.
- e2e root cause (verified locally with Playwright 1.64.1 against merged tree):
  openVersusSetup() adds .active to #screen-vssetup, but main.js show() only
  clears the `screens` map — vssetup was never in the map, so show('select')
  left it covering screen-select; the .char-card tap then timed out (90s).
  Trusted click fired fine; screen-select WAS display:block underneath.
- Fix: added `vssetup: document.getElementById('screen-vssetup')` to the screens
  map in game/js/main.js (additive, one entry). Verified locally: after the
  CHOOSE FIGHTERS tap, vssetup hidden + select shown.
- Commit 498d1fd4 pushed → CI re-running. Merge pending green e2e.
- Status: IN PROGRESS (awaiting CI on 498d1fd4)

## PR #701 — FIGHT-LOOP CRASH REPAIR (worker54/fight-loop-repair-20261022)
- State at start: DIRTY, head dab69f72, base 5697af6a.
- Conflicts vs main@2221237b: 2 — game/index.html (branch integration.js script
  tag vs main menu-fallback-binder block → kept BOTH), game/js/game.js (2 KO
  hunks: branch restored hitfx.spawn('ko') + feel tuning vs main's
  rage/xray/stageBreaks hooks → kept BOTH; main's _spawnImpact call dropped in
  those two hunks only — it is now a shim over hitfx.spawn, would double-spawn).
- Merge commit 781816fc pushed. CI re-running.
- Status: IN PROGRESS (awaiting CI on 781816fc)

## RUN INTERRUPTED (cron timeout ~00:40Z) — final state
- #841: merge 05a08e5b + e2e fix 498d1fd4 pushed. CI ran on 05a08e5b (all green
  except menu-touch-e2e, root-caused + fixed). NO CI runs have materialized for
  498d1fd4 (~18 min). NOT merged. Next: confirm CI green on 498d1fd4 (or
  empty-commit re-trigger if synchronize event is lost), then merge + verify on main.
- #701: merge 781816fc pushed. NO CI runs materialized yet. NOT merged. Next:
  wait CI green, then merge + verify on main.
- #498: NOT STARTED (conflicts unknown).
- Open question: pushes via this token are not firing pull_request/synchronize
  workflow runs (first push did; last two did not). Other PRs' events flow fine.

## CONTINUED 2026-10-24 ~00:45-01:15Z (overnight pipeline, resumed after cron-timeout interruption)
- #701: MERGED via API (merge 4757df4d1d083515db0b78ab8fa1d1d5cc650098). Deletion-guard had been cancelled by concurrency at 00:49:54Z (no visible superseding run; branch head unchanged) — verified locally: 1 added + 4 modified + 0 removed → guard passes. Payloads verified on main: game/js/game.js 34,071B, 8× hitfx.spawn + 1× new HitFX. LANDED-VERIFIED.
- #841: Git Data API empty commit (82cbd8ab) did NOT fire synchronize (API ref updates don't emit push webhooks — root cause of the "pushes not firing CI" pattern). Real `git push` of an empty commit now in flight to fire CI. Merge pending green.
- #498: body edit at 00:47:47Z applied but NO instruction-gate run fired for the `edited` event (stale 2026-10-22 failure still attached to head). Local run of the gate's own comparison: method sections EQUAL → passes. Merge blocked by REAL 405 conflicts (WORKLOG.md append/append). Resolved keep-both-sides via Git Data API merge commit 32495cfc: main's WORKLOG.md kept (main already carries the verbatim Pantera entry at lines 1066+, restored 2026-10-22 — branch section byte-identical per diff, no content lost); pantera.glb + reskin script from branch. PR mergeable=true → MERGED via API (a46838460b9ddccb70c2f6d987aadd33ef4db55d). Payloads verified on main: pantera.glb 7,625,912B, reskin_pantera_weights.py 15,877B, WORKLOG.md 217,868B. LANDED-VERIFIED.
