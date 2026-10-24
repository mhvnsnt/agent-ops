# TorBox BAD_TOKEN — Lane 5 All-Agents Review (2026-10-20)

Five coding agents were run on the same TorBox review prompt (tb_reqdl.py,
tb_mylist.py, tb_export.py, torbox_add_magnet.py, CONNECTOR.md, zip_extract.py).
Full verbatim outputs: `~/workspace/agent-ops/torbox-lane5-agents/` (local).

## Consensus root cause (Copilot CLI + Codex via Kilo gateway, independently)

`custom.torbox` is registered with **bearer_header** placement. The authd
surrogate (`hsurr:...`) is only substituted at approved egress points matching
that placement — i.e. in an `Authorization: Bearer` header. `tb_reqdl.py`
manually inserts the surrogate into `?token=`:

```python
surrogate = str(entry["surrogate"]).strip()
url = f"https://api.torbox.app/v1/api/torrents/requestdl?torrent_id={tid}&token={quote(surrogate, safe='')}"
```

TorBox receives the literal surrogate, not the real key -> `BAD_TOKEN`.
This also explains "fresh keys die as BAD_TOKEN": the request never contained
the fresh key at all.

## Additional bugs found

- `torbox_add_magnet.py`: imports `add_surrogate_to_request` but calls
  `url_with_surrogate_query_param(...)`, which is not imported/defined ->
  `NameError` before any request is sent (Copilot).
- `tb_mylist.py` / `tb_export.py` / `torbox_add_magnet.py` call
  `url_with_surrogate_query_param` on a bearer_header credential -> Codex
  (which read the dynamic_credentials module) predicts
  `DynamicCredentialError: credential is not query_param` at runtime.
- `tb_reqdl.py`: NoRedirect raises `RuntimeError`, but only `HTTPError` is
  caught -> redirect failures surface as tracebacks, not clean status/body.

## Fix options

- **A (preferred if requestdl accepts Bearer):** use
  `add_surrogate_to_request(req, "custom.torbox", allowed_hosts=["api.torbox.app"])`
  and drop `&token=` from the URL.
- **B (if requestdl truly requires ?token=):** register a second credential
  entry with query_param placement (`token`) and use
  `url_with_surrogate_query_param` consistently.

## Diagnostics (no key printed)

1. Print `dynamic_credential_entry("custom.torbox")["placement"]`.
2. Run `tb_mylist.py` — a DynamicCredentialError confirms placement mismatch.
3. Retry requestdl via `add_surrogate_to_request` (Bearer surrogate).
   Success -> Option A. BAD_TOKEN -> endpoint requires query placement -> Option B.

## Agent run status

- Copilot CLI 1.0.100 (reinstalled via npm): full review delivered.
- Codex 0.149.0: direct OpenAI lane = 401 login-required (recorded);
  via Kilo Code free gateway (`codex -p kilo-code`): full review delivered.
- Kilo CLI 7.8.15 (reinstalled via npm): native run blocked — default model
  requires Kilo sign-in; Kilo gateway contributed via the Codex profile above.
- OpenCode 1.19.3 (`~/.local/bin/opencode`): binary OK, `run` produced no
  completion within 110s on repeated attempts (recorded).
