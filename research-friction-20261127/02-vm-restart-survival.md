# 02 — VM restart survival: process checkpoint/restore vs lane checkpoints

**Date:** 2026-11-28 ~04:10 UTC (2026-11-27 ~22:10 CST) · **Pass:** continuous-friction-research
**Index:** [[RESEARCH-PULLIN-INDEX]] · **Related:** [[CHECKPOINT_PROTOCOL]] · [[LANE-RESILIENCE-SOP]] ·
`CUT001R-6B-VM-RESTART-LOSS-20261115.md` · `FRICTION-RESEARCH-LOG.md` §2026-11-15 (tmpfs loss)

## 1. Problem statement

The VM restarts ~5×/day at irregular, unforecastable intervals — **17 restarts counted
Nov 26–27, 2026** (task brief), boots lasting ~1–2 h. Every restart kills all running
work outright:

- **Blender renders:** Bannon render lanes died repeatedly; CUT 001R 6B lost 69 rendered
  character frames on 2026-11-15 because output lived in `/var/tmp` (tmpfs)
  — see `CUT001R-6B-VM-RESTART-LOSS-20261115.md`. On 2026-11-21 a restart wiped the
  Pyrite checkpoint, worktree, 8 proof shots, capture driver, suite log, and Colosseum
  M2 extracts (all in `/tmp`) — see NO-TEMP-STORAGE LAW in `AGENTS.md`.
- **Multi-GB inflates:** `at-inflate2` died 3× at different offsets (task brief); VM
  restart #13 (~19:12Z Nov 27) killed `at-inflate2` pid 3352; restart #15 (17:31 CST
  Nov 27) killed it again — the longtail watchdog owns the relaunch.
- **Uploads / pulls:** the TeraBox pull died 19:15 CST Nov 27 (sign-in window expired,
  no file landed); restarts #10/#11/#12 (Nov 27) killed two #16 lanes outright and
  interrupted a third — all re-queued, zero work lost only because lane checkpoints
  existed.
- **Separate harness limit (NOT the reboot):** tracked background exec sessions die at
  ~51 min; a detached relaunch died in ~4 min (MEMORY.md, 2026-11-27/28). Any
  relaunch wiring must survive both the 51-min exec cap *and* the reboot.

**Already settled — do not re-research:** lane-level checkpoint/resume
(`CHECKPOINT_PROTOCOL.md`, `checkpoint.sh` fencing-epoch claims, `supervisor.sh`
STUCK bucket, nurse watchdogs that relaunch Blender drivers — all landed Oct 20,
pull-in 5/6 in `RESEARCH-PULLIN-INDEX.md` line 181). What does NOT exist is
**process-level survival across a reboot**, or a diagnosis of **why** the VM restarts.
This doc covers exactly those two gaps.

## 2. Candidate table

| Candidate | Source | License | Verdict | Why |
|---|---|---|---|---|
| DMTCP | https://github.com/dmtcp/dmtcp | **LGPLv3+** (FAQ: "free software distributed under the terms of the Lesser GNU Public License (LGPL)… non-contagious"; man page: "License LGPLv3+") — http://dmtcp.sourceforge.net/FAQ.html, https://manpages.ubuntu.com/manpages/bionic/man1/dmtcp_checkpoint.1.html | **QUEUED — pilot only** | No root needed; checkpoint images are files that can live on `/home` (persistent) and be restarted after a reboot with `dmtcp_restart`. BUT: (1) sockets are restored only when **both endpoints run under DMTCP** (coordinated checkpoint; DMTCP drains sockets between checkpointed peers) — an upload to TeraBox/GitHub has an external peer, so the TCP connection dies with the reboot; DMTCP saves **compute state, not the socket**. (2) No GPU/OpenGL state — our Blender renders are EEVEE via SwiftShader/llvmpipe or Cycles CPU; DMTCP's CUDA support is the separate CRAC plugin, not Mesa/llvmpipe; EEVEE-under-DMTCP is unproven. (3) Checkpoint cost: a live Blender render holds ~1.4 GB RSS (pid 52418, observed 04:08 UTC Nov 28) — each DMTCP checkpoint writes a ~GB image, on an 83%-full disk under a quota wall. (4) Not installed; `apt-cache policy dmtcp` returns no candidate info (no apt lists). (5) It still needs the cron/watchdog relaunch wiring — it does not self-resume after boot. Pilot: checkpoint a small **CPU Cycles** render (not EEVEE), measure image size + checkpoint time + restart-after-reboot success. Only if the pilot passes is wiring worth it. |
| CRIU | https://github.com/checkpoint-restore/criu / https://criu.org | **GPLv2** (lib/ LGPLv2.1) — https://www.gitplanet.com/project/criu8405561275840351, https://prohoster.info/en/blog/news/criu-4-3-released-a-system-for-saving-and-restoring-process-state-in-linux | **SKIP** | Kernel side looks promising (`CONFIG_CHECKPOINT_RESTORE=y` in `/proc/config.gz`; `CAP_CHECKPOINT_RESTORE` + `CAP_SYS_ADMIN` present in our effective set — verified live, §3) but three hard blockers: (a) the man page requires `CAP_CHECKPOINT_RESTORE` **in the init user namespace** to read `/proc/pid/map_files`; we run as uid 0 mapped to host uid 131072 (`/proc/self/uid_map`: `0 131072 65536`) inside a systemd-nspawn container — our caps are container-local, not init-ns. (b) No binary installed; the task forbids installing as root and `apt-cache` has no package info. (c) CRIU does not checkpoint GPU/device state ("a task that has opened or mapped any character or block device" is excluded; "GPU workloads in general are not supported by CRIU, may just crash on restore" — https://cedana.com/blog/criu-gpu-checkpointing/). TCP restore needs same host + same IP **plus** a netfilter lock rule that must sit in the host tables between dump and restore (https://criu.org — "TCP connection"); across a full container reboot the rule, the net namespace, and (presumably) the IP are all gone and the peer sends RST. License is fine; the environment is not. |
| tmux / screen / nohup / setsid (detached survival) | tmux: https://webdocklab.horiamc.com/blog/tmux-for-remote-servers, https://linuxize.com/post/getting-started-with-tmux/ | tmux ISC, screen GPLv3, nohup/setsid coreutils GPLv3 | **SKIP — verified dead on reboot** | tmux survives SSH drops, not reboots: "tmux is an ordinary process. A kernel update reboot ends it, along with everything inside" / "tmux sessions live in memory and do not survive a restart of the machine." Verified live on this VM: `tmux ls` → `error connecting to /tmp/tmux-0/default (No such file or directory)` — no server running after the 03:08 UTC boot, because the tmux socket lives in `/tmp`, which is tmpfs (512 MB, wiped every boot). `screen` is not installed (`which screen` → nothing); `nohup`/`setsid` only detach from the terminal — they do nothing against a reboot, which kills every process by definition. `tmux-resurrect`/`continuum` restore *layout*, not running programs (program restore is opt-in whitelist only), and still need a post-boot trigger we do not have. Do not re-propose. |
| Cron-based continuation / watchdog relaunch from checkpoint (shop pattern) | `CHECKPOINT_PROTOCOL.md`, `supervisor.sh`, nurse watchdogs; this very research run is itself a scheduled cron job | n/a (shop scripts) | **PULL IN — this is the answer for reboot survival** | The trigger lives **outside** the VM (the Muse scheduler / hooks, e.g. `bannon-render-watch`), and state lives on `/home` (btrfs, persistent — §3). It is the only candidate whose two halves both survive a reboot. Gap, quantified in §4: in-flight partial work between checkpoints is lost; expected loss per restart is half the checkpoint interval. Fix the gap by shrinking the interval / chunk size, not by chasing process checkpointing. |
| systemd user units | — | n/a | **SKIP — already verified unavailable, Oct 2026** | "Failed to connect to bus" (cited from the task brief / prior verification; not re-tested per brief). Note for context only: PID 1 *is* systemd (`/proc/1/exe -> /usr/lib/systemd/systemd`, observed live) but there is no per-user systemd instance / D-Bus user bus for our session, so no user units, no `Restart=on-failure`, no `@reboot` from inside the VM. |

## 3. Restart-cause diagnosis (read-only, 2026-11-28 ~04:08–04:10 UTC)

**Bottom line up front: the cause is NOT diagnosable from inside the guest, and the
evidence shows the restarts are host-imposed, not a guest crash.** The VM/container is
rebuilt from scratch each boot; only `/home` persists. No in-guest log survives a
reboot, so no OOM/panic trace can ever be retrieved after the fact.

### 3.1 Exact commands run and their output

```
$ date; uptime; journalctl --list-boots
Sat Nov 28 04:08:18 UTC 2026
 04:08:18 up  1:00,  0 user,  load average: 13.76, 13.06, 11.52
IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
  0 70533955f1f648ceb70cfd8280ed3485 Sat 2026-11-28 03:08:29 UTC Sat 2026-11-28 04:07:44 UTC
```
Only ONE boot in the journal. Current boot started 03:08:29 UTC Nov 28 — consistent
with the MEMORY record of a reboot ~01:15 UTC Nov 28 and one ~23:31 UTC Nov 27
(boots last ~1–2 h).

```
$ dmesg | tail -30
dmesg: read kernel buffer failed: Operation not permitted
$ journalctl -b -p err --no-pager
-- No entries --
$ journalctl -b --no-pager | grep -iE 'oom|killed process|out of memory|reboot|shutdown|watchdog|panic'
Nov 28 03:08:29 htch-runtime systemd[1]: Starting systemd-update-utmp.service ...
Nov 28 03:08:29 htch-runtime systemd[1]: Finished systemd-update-utmp.service ...
```
No errors in the current boot's journal (214 lines total, boot noise only). No OOM,
panic, or shutdown line — but the journal only ever holds the current boot, so a
previous boot's crash, if any, is unrecoverable from here.

```
$ ls -l /var/log/syslog /var/log/kern.log /var/log/messages
ls: cannot access '/var/log/syslog': No such file or directory
ls: cannot access '/var/log/kern.log': No such file or directory
ls: cannot access '/var/log/messages': No such file or directory
$ ls -la /var/log/journal/ ; du -sh /var/log/journal/*
... e5215e448f204747bd525a1d0d8c94f4   (dated Nov 28 03:08 — created at this boot)
8.0M  /var/log/journal/e5215e448f204747bd525a1d0d8c94f4
$ last reboot
reboot   system boot  7.0.0-44-generic Sat Nov 28 03:08   still running
wtmp begins Sat Nov 28 03:08:29 2026
```
No syslog/kern.log/messages. `wtmp` begins at this boot — no reboot history survives.

```
$ mount | grep -E ' / | /home|tmpfs'   (abridged)
overlay on / type overlay (rw,relatime,lowerdir=/sysroot,upperdir=/run/hatch/overlay/upper,...)
tmpfs on /tmp type tmpfs (rw,...,size=524288k)
tmpfs on /run type tmpfs (rw,...,size=1624980k)
$ stat -f -c '%T %n' / /tmp /home/hatch
overlayfs /
tmpfs /tmp
btrfs /home/hatch
```
**This is the smoking gun.** Root `/` is an overlay whose upper layer is
`/run/hatch/overlay/upper` — and `/run` is tmpfs. Everything outside `/home` is
ephemeral by construction: `/`, `/var/log`, `/run`, the journal, `wtmp`, `/tmp`
(512 MB tmpfs) are all recreated at every boot. Only `/home/hatch` (btrfs, 150G)
persists. That is why `journalctl --list-boots` shows one boot, why `last` has no
history, and why no crash evidence can ever survive a restart: the evidence lives on
a filesystem that is wiped by the restart itself.

```
$ systemd-detect-virt
systemd-nspawn
$ uname -r; zgrep CONFIG_CHECKPOINT_RESTORE /proc/config.gz
7.0.0-44-generic
CONFIG_CHECKPOINT_RESTORE=y
$ id; cat /proc/self/uid_map; readlink /proc/self/ns/user /proc/1/ns/user
uid=0(root) gid=0(root) groups=0(root)
         0     131072      65536
user:[4026532494]   (both self and PID 1 — same container user namespace)
$ python3 -c "cap=int('000001ffffb7cfff',16); ..."
CAP_SYS_ADMIN True
CAP_CHECKPOINT_RESTORE True
CAP_SYS_PTRACE False
CAP_NET_ADMIN False
$ cat /proc/sys/kernel/yama/ptrace_scope
1
$ which criu dmtcp tmux screen setsid nohup systemd-run
/usr/bin/tmux
/usr/bin/setsid
/usr/bin/nohup
/usr/bin/systemd-run
```
(neither `criu` nor `dmtcp` nor `screen` is installed; `apt-cache policy dmtcp criu`
returned no candidate info — no apt lists on this image.)

```
$ free -m; cat /proc/loadavg; df -h / /home/hatch
Mem: 7934 total, 5001 used, 168 free, 2932 available; Swap: 1023 total, 372 used
15.14 13.35 11.62  (load at 04:09 UTC, two Blender renders running)
overlay 7.5G 143M 7.4G 2% / ; /dev/mapper/rv 150G 124G 26G 83% /home/hatch
$ ps aux (observed only, nothing signalled)
root 40829 ... blender -b --python render_pair.py -- --pair data/animit_55256__100.json ... --out frames/55256_100_wide
root 52418 ... blender -b --python render_pair.py -- --pair data/animit_2k26_suplex_8.json ... --out frames/4022_nr
```
Live Bannon render lanes running at check time (observed via `ps` only, per brief —
no signals sent). Load 13–15 with 2.9 GB available and 372 MB swap used is busy
but is not OOM evidence, and there is no OOM trace in the current boot's journal.

### 3.2 What could and could not be checked

| Check | Result | Meaning |
|---|---|---|
| `journalctl --list-boots` | 1 boot only | Journal does not persist across boots (root is ephemeral overlay on tmpfs). |
| `journalctl -b -p err` | No entries | Current boot is clean; says nothing about prior boots. |
| `dmesg` | `Operation not permitted` | Kernel log is blocked in this container; kernel-level crash evidence is unreachable in-guest. |
| `/var/log/{syslog,kern.log,messages}` | Do not exist | No persistent text logs at all. |
| `last reboot` / `wtmp` | Begins at this boot | No reboot history survives. |
| `uptime` | 1:00 at 04:08 UTC; boot 03:08 UTC | Confirms the ~2 h boot cadence recorded in MEMORY (reboots ~23:31 UTC Nov 27, ~01:15 UTC Nov 28). |
| `mount` / `stat -f` | `/` overlay upper on tmpfs `/run`; `/home` btrfs | Only `/home` survives a reboot — by design, not by accident. |
| `systemd-detect-virt` | `systemd-nspawn` | We are a container, not a full VM; the "VM restart" is the host runtime recreating the container (hostname `htch-runtime`). |
| OOM-killer traces | None found, none retrievable | No evidence of guest OOM; also no mechanism by which such evidence could survive. |
| `CONFIG_CHECKPOINT_RESTORE`, caps | Kernel `=y`; caps present in container user ns; uid 0 → host 131072 | CRIU's init-ns requirement (§2) is not met despite the caps looking present. |

**Diagnosis:** the restarts are host-side lifecycle events of the `htch-runtime`
container (recreate from image, fresh ephemeral root, `/home` re-attached). They are
not a guest kernel panic or OOM that we can fix from inside — there is no in-guest
lever to pull, no setting to change (and the brief forbids changing system settings
anyway). The correct response is to design for them (see §4), not to diagnose them
further from inside. If the host ever exposes a restart reason, that comes from the
runtime operator, not from this guest.

## 4. The checkpoint-interval tradeoff (quantified)

Restarts are uniformly random within any interval, so expected rework per restart =
interval ÷ 2. At the observed rate (17 restarts / 2 days ≈ **8.5 restarts/day**):

| Checkpoint / chunk interval | Expected loss per restart | Expected rework per day |
|---|---|---|
| 5 min | 2.5 min | ~21 min |
| 15 min | 7.5 min | ~64 min |
| 30 min | 15 min | ~2.1 h |
| 60 min | 30 min | ~4.3 h |
| 2 h (a full boot's work, no checkpoint) | 60 min | ~8.5 h |

Two costs bound the interval from below: (a) checkpoint write cost — a DMTCP image
of a ~1.4 GB Blender process, or a `git push` of a render batch, is itself seconds
to minutes and competes with the quota wall at 83% disk; (b) the 51-min exec-session
cap means a single foreground session cannot even hold a 60-min chunk. The sweet
spot for this shop is **5–15 min per checkpoint, with work already structured as
per-frame / per-file units**:

- **Renders:** per-frame output on `/home` IS the checkpoint (each frame ~40–160 s
  at the recorded 001R pace). Never batch frames only in memory; never write frames
  to `/tmp` or `/var/tmp` (both tmpfs — the Nov 15 and Nov 21 losses). Stage finished
  frames to the repo branch as they land (stage-as-it-lands, already the shop rule).
- **Inflates / extracts:** `at-inflate2` died 3× at different offsets because it
  restarts from zero. Use a resumable extractor: extract file-by-file with a manifest
  of completed files on `/home`, or split the input into per-part archives so a
  restart resumes at the next part, not the beginning. (No new tool needed — this is
  a driver change, not a pull-in.)
- **Uploads / downloads:** use resumable transfers with control state on `/home` —
  `aria2` (`.aria2` control files, already decided in prior research), `curl -C -`,
  or `rclone` with retries. A plain `curl`/`scp` upload has no resume point: a
  restart at 99% costs 99%. **No checkpointing tool saves an upload's socket** —
  DMTCP and CRIU both lose external TCP connections across a reboot (§2) — so
  resume-at-the-transfer-layer is the only answer for uploads, full stop.
- **Relaunch wiring:** the relaunch trigger must live outside the VM — the Muse
  scheduler (crons) and hooks (e.g. `bannon-render-watch`), which already relaunch
  lanes today. Inside the VM there is no `@reboot`, no systemd user unit, and no
  surviving daemon to do it. Every long job's driver must be **idempotent and
  resume-from-manifest on a cold start**, because a cold start after reboot is the
  normal path, not the exception.

## 5. Recommendation

1. **Do not pull in CRIU.** License is fine (GPLv2) but the environment defeats it:
   container user namespace (no init-ns caps), no binary, no GPU/device state, TCP
   restore impossible across a container recreate. Verdict: SKIP, do not re-propose.
2. **Do not pull in DMTCP now; queue a narrow pilot.** LGPLv3+ is fine and it is
   the only candidate that can, in principle, save in-flight compute across a
   reboot (checkpoint image on `/home` + `dmtcp_restart` after boot). But it saves
   compute, not sockets; EEVEE-under-DMTCP is unproven; each checkpoint is ~GB on
   an 83%-full disk; and it still needs the cron/watchdog relaunch. Pilot (one
   lane, one afternoon): build DMTCP from source or apt, checkpoint a small
   **CPU Cycles** Blender render, reboot, `dmtcp_restart`, verify the frame
   completes. If the pilot fails or the image/checkpoint cost exceeds ~10% of the
   chunk, drop DMTCP and stay with lane checkpoints. Tracked as QUEUED in
   [[RESEARCH-PULLIN-INDEX]].
3. **The shop answer is the one already built: cron/hook relaunch + lane
   checkpoints + small chunks.** Standardize it as a rule for every long job:
   - No unit of work longer than **15 min** without a durable checkpoint on `/home`.
   - Renders: per-frame files, staged to the branch as they land.
   - Inflates: per-file manifest resume, never restart-from-zero.
   - Transfers: resumable (`aria2` / `curl -C -` / `rclone`), control files on `/home`.
   - Drivers: idempotent, resume-from-manifest on cold start; the relaunch trigger
     is an external cron/hook, never a long-lived exec session (51-min cap) and
     never a daemon inside the VM (dies with the reboot).
4. **Stop diagnosing the restarts from inside the guest.** The cause is host-side
   container recreation; in-guest evidence is wiped by design each boot. Log each
   restart's time + what it killed in the lane checkpoint (already the practice —
   restarts #10–#15 are all recorded in MEMORY), and spend the effort on
   chunking, not forensics.
5. **Open question (not answered by this pass):** why a *detached* relaunch died
   in ~4 min (MEMORY, Nov 27/28) when the exec-session cap is ~51 min. That is a
   runtime-harness behavior, not a VM reboot, and it matters because the watchdog
   relaunch path depends on detached processes surviving. Worth one focused check
   by whoever owns the nurse/watchdog wiring — observe, do not kill live lanes.

## 6. Sources

- DMTCP repo: https://github.com/dmtcp/dmtcp (README: user-level, no kernel modules)
- DMTCP FAQ (license LGPL, no root, supported apps incl. Python):
  http://dmtcp.sourceforge.net/FAQ.html
- DMTCP man page (LGPLv3+): https://manpages.ubuntu.com/manpages/bionic/man1/dmtcp_checkpoint.1.html
- DMTCP socket behavior (external sockets need both endpoints under DMTCP; blacklist
  or run peer under DMTCP): https://sourceforge.net/p/dmtcp/mailman/message/35052145/
- DMTCP design paper (socket draining / coordinated checkpoint):
  http://dmtcp.github.io/papers/dmtcp.pdf
- DMTCP + CUDA via CRAC plugin (GPU is plugin-only, CUDA-only):
  https://www.slideshare.net/slideshow/checkpointing-the-uncheckpointable/240116265
- CRIU man page — NON-ROOT section (CAP_SYS_ADMIN or CAP_CHECKPOINT_RESTORE minimum;
  init-ns requirement for `/proc/pid/map_files`; `--unprivileged`):
  https://manpages.debian.org/unstable/criu/criu.8.en.html
- CRIU TCP connection (TCP_REPAIR, netfilter lock rule between dump and restore,
  same-IP requirement): https://criu.org/index.php?title=TCP_connection
- CRIU GPU limits ("GPU workloads in general are not supported… may just crash on
  restore"; CUDA plugin via `cuda-checkpoint`, same-GPU-type restore):
  https://cedana.com/blog/criu-gpu-checkpointing/
- CRIU license GPLv2: https://www.gitplanet.com/project/criu8405561275840351
- tmux vs reboot: https://webdocklab.horiamc.com/blog/tmux-for-remote-servers
  ("tmux survives SSH drops, not reboots… Sessions are gone after a reboot");
  https://linuxize.com/post/getting-started-with-tmux/ ("tmux sessions live in
  memory and do not survive a restart of the machine")
- Live command outputs: §3.1 above (all run 2026-11-28 ~04:08–04:10 UTC, read-only;
  live lanes observed via `ps` only, nothing signalled, nothing installed, nothing
  changed).
