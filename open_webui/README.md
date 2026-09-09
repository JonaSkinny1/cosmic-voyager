# Open WebUI + COSMOS tools

SIM-only ship tools for local Open WebUI on SpaceshipDesktop. No actuators, pumps, or F.R.A.N.K. pours.

**Full daily ops:** [`docs/COSMOS-RUNBOOK.md`](../docs/COSMOS-RUNBOOK.md)

## Fast path (SpaceshipDesktop)

```powershell
cd $env:USERPROFILE\Documents\cosmic-voyager
.\scripts\start-cosmos-stack.ps1
.\scripts\cosmos-health.ps1
```

Then http://127.0.0.1:8080 → model **`cosmos`** → enable **COSMOS Ship Tools** → chat.

## Prerequisites

- Ollama with model `cosmos` (`ollama create cosmos -f ship_core/Modelfile`)
- Open WebUI on `http://127.0.0.1:8080` (`WEBUI_AUTH=False` is fine)
- Repo at `Documents\cosmic-voyager`

## Register tools (first time)

### Option A — OpenAPI tool server (Integrations)

Admin → Settings → Integrations (or External Tools) → add:

| Field | Value |
|-------|--------|
| URL | `http://127.0.0.1:8767` |
| Path | `/openapi.json` |
| Auth | None |
| Name | COSMOS Ship Tools (SIM) |

Enable the connection. Health: http://127.0.0.1:8767/health · OpenAPI: http://127.0.0.1:8767/openapi.json

### Option B — Workspace Python tool

Workspace → Tools → create/import using `open_webui/cosmos_ship_tools.py` (same allowlisted ops; calls the local tool server).

## Allowlisted operations

- `get_ship_status`
- `set_lighting`
- `set_zone_lighting`
- `set_active_zone`
- `set_alert_level`
- `set_viewport_mode`

## Manual start (if not using scripts)

```powershell
cd $env:USERPROFILE\Documents\cosmic-voyager
python -m orchestrator.tool_server

# separate terminal
$env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
$env:WEBUI_AUTH = "False"
open-webui serve --host 127.0.0.1 --port 8080
```

## Safety

Sim state only. Do not wire pours, door actuators, or live MCU endpoints into this allowlist.