# COSMOS Runbook (SpaceshipDesktop)

Daily ops for the local COSMOS stack: Ollama + tool server + Open WebUI.

**Safety:** SIM only. No actuators, door locks, pumps, or F.R.A.N.K. pours. Allowlisted ship tools update in-memory sim state only.

**Backlog:** Device power control (list/shutdown/wake) — see [`BACKLOG-device-power.md`](BACKLOG-device-power.md). Dry-run first; no live power until Jonathan unlocks a phase.

## Ports

| Service     | Port  | Health / probe                                      |
|-------------|-------|----------------------------------------------------|
| Ollama      | 11434 | `http://127.0.0.1:11434/api/tags`                  |
| Tool server | 8767  | `http://127.0.0.1:8767/health`                     |
| Open WebUI  | 8080  | `http://127.0.0.1:8080/health`                     |

Repo root on PC: `%USERPROFILE%\Documents\cosmic-voyager`

## Daily start

```powershell
cd $env:USERPROFILE\Documents\cosmic-voyager
.\scripts\start-cosmos-stack.ps1
.\scripts\cosmos-health.ps1
```

What `start-cosmos-stack.ps1` does:

1. Verifies Ollama on `:11434` (exits if down — start the Ollama app first)
2. Starts `python -m orchestrator.tool_server` on `:8767` if needed
3. Starts `open-webui serve` on `:8080` if needed (`OLLAMA_BASE_URL`, `WEBUI_AUTH=False`)

Then:

1. Open http://127.0.0.1:8080
2. Select model **`cosmos`** (or `cosmos:latest`)
3. Enable **COSMOS Ship Tools** (tools picker / `+`)
4. Chat, e.g. `Set Cantina to NEBULA_PURPLE at 40` or `What's the ship status?`

## Health check

```powershell
.\scripts\cosmos-health.ps1
```

Expect: Ollama / ToolServer / OpenWebUI all **OK**, plus a one-line ship sim status and listed models.

Manual probes:

```powershell
Invoke-WebRequest http://127.0.0.1:11434/api/tags -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8767/health -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8080/health -UseBasicParsing
```

## Open WebUI — enable ship tools

### First-time: register the tool server

Admin → Settings → Integrations (or External Tools) → add:

| Field | Value |
|-------|--------|
| URL   | `http://127.0.0.1:8767` |
| Path  | `/openapi.json` |
| Auth  | None |
| Name  | COSMOS Ship Tools (SIM) |

Enable the connection. OpenAPI: http://127.0.0.1:8767/openapi.json

### Alternate: Workspace Python tool

Workspace → Tools → import `open_webui/cosmos_ship_tools.py` (calls the same local tool server).

### Per chat

Select model **`cosmos`**, then enable **COSMOS Ship Tools** on that chat before asking for lighting / status changes.

### Allowlisted ops

`get_ship_status` · `set_lighting` · `set_zone_lighting` · `set_active_zone` · `set_alert_level` · `set_viewport_mode`

## Troubleshooting

### Ollama DOWN (`:11434`)

- Start the **Ollama** desktop app / service.
- Confirm model exists: `ollama list` — need `cosmos` (create with `ollama create cosmos -f ship_core/Modelfile`).
- Firewall / VPN rarely blocks loopback; stick to `127.0.0.1`.

### Tool server DOWN (`:8767`)

- From repo root: `python -m orchestrator.tool_server`
- Port in use: find and stop the old process, or check something else bound to 8767.
- Python / deps: `pip install -r requirements.txt` from repo root.
- OpenAPI must load: http://127.0.0.1:8767/openapi.json

### Open WebUI DOWN (`:8080`)

```powershell
$env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
$env:WEBUI_AUTH = "False"
open-webui serve --host 127.0.0.1 --port 8080
```

- If `open-webui` not found: install/reinstall the Open WebUI CLI and refresh PATH.
- Cold start can take ~30–60s — wait for `/health`.
- Port conflict: stop other listeners on 8080.

### Chat ignores tools / no lighting change

- Confirm tool server **OK** and tools enabled on **this** chat.
- Model must be `cosmos`, not a generic base model without tool use.
- Re-check Integrations entry points at `http://127.0.0.1:8767`.
- Probe sim: `POST http://127.0.0.1:8767/get_ship_status` with body `{}`.

### After reboot

Run `start-cosmos-stack.ps1` again. Ollama often auto-starts; tool server and Open WebUI usually do not.

## Related

- [`open_webui/README.md`](../open_webui/README.md) — tool registration details
- [`AFTER-WORK-CHECKLIST.md`](../AFTER-WORK-CHECKLIST.md) — Deck 01 measure + optional COSMOS check
- [`ship_core/Modelfile`](../ship_core/Modelfile) — COSMOS identity