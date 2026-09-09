# Open WebUI + COSMOS tools

SIM-only ship tools for local Open WebUI on SpaceshipDesktop. No actuators, pumps, or F.R.A.N.K. pours.

## Prerequisites

- Ollama running with model `cosmos` (from `ship_core/Modelfile`)
- Open WebUI on `http://127.0.0.1:8080` (`WEBUI_AUTH=False` is fine)
- This repo checked out (e.g. `Documents\cosmic-voyager`)

## 1. Start the tool server

```powershell
cd $env:USERPROFILE\Documents\cosmic-voyager
python -m orchestrator.tool_server
```

- Health: http://127.0.0.1:8767/health
- OpenAPI: http://127.0.0.1:8767/openapi.json

Leave this terminal open.

## 2. Register tools in Open WebUI

### Option A — OpenAPI tool server (Integrations)

Admin → Settings → Integrations (or External Tools) → add:

| Field | Value |
|-------|--------|
| URL | `http://127.0.0.1:8767` |
| Path | `/openapi.json` |
| Auth | None |
| Name | COSMOS Ship Tools (SIM) |

Enable the connection.

### Option B — Workspace Python tool

Workspace → Tools → create/import using `open_webui/cosmos_ship_tools.py` (same allowlisted ops; calls the local tool server).

## 3. Chat

1. Open http://127.0.0.1:8080
2. Select model **`cosmos`** (or `cosmos:latest`)
3. Enable **COSMOS Ship Tools** on the chat (tools picker / `+`)
4. Ask e.g. `Set Cantina to NEBULA_PURPLE at 40` or `What's the ship status?`

## Allowlisted operations

- `get_ship_status`
- `set_lighting`
- `set_zone_lighting`
- `set_active_zone`
- `set_alert_level`
- `set_viewport_mode`

## Restart cheat sheet (SpaceshipDesktop)

```powershell
# Ollama usually runs as a service after install

# Tool server
cd $env:USERPROFILE\Documents\cosmic-voyager
python -m orchestrator.tool_server

# Open WebUI (separate terminal)
$env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
$env:WEBUI_AUTH = "False"
open-webui serve --host 127.0.0.1 --port 8080
```

## Safety

Sim state only. Do not wire pours, door actuators, or live MCU endpoints into this allowlist.