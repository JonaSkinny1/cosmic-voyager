# Cosmic Voyager â€” Deck 01

Local-first ship OS stubs for Jonathanâ€™s basement freighter (**Deck 01 / Cosmic Voyager**, Ohio Outpost // Sol-3).

| Role | Name |
|------|------|
| Ship AI | **COSMOS** |
| Cantina bartender | **F.R.A.N.K.** (Friendly Robot Administering Nourishment & Knowledge) |

## Zones (working)

Bridge â†’ Observatory â†’ Cantina â†’ Tech Bay â†’ Cargo (open freighter flow; **ft splits unlocked** until posts measured).

## Stack (software-first)

Ollama + **Qwen3** (`qwen3:8b` start) Â· Faster-Whisper Â· Piper/Kokoro Â· MQTT / Home Assistant Â· ESP-NOW to ESP32 later.

MCU fleet (docs): 4Ã— GIGA R1 Â· 1Ã— UNO R4 WiFi Â· 6Ã— Nano ESP32.


## LOCKED (2026-09-09)

Jonathan conflict triage â€” do not auto-merge Gemini vs Grok elsewhere.

| Topic | Status |
|-------|--------|
| Viewport Fresnel | **LOCKED** Disney long-f: 8â€“12 in gap, 1200â€“1300 mm f (~1250 preferred), ~15â€“24 in wall; 55-in target. Gemini multi-viewer + Grok short-stack superseded. |
| Ship AI host | **LOCKED** software-first on existing RTX 3090 â€” Ollama + `qwen3:8b`. Dell out. DGX Spark / other GPUs = future only. |
| Sector ft splits | **KEEP UNLOCKED** â€” measure support posts before locking zone length bands. |

Details: [`docs/deck_layout.md`](docs/deck_layout.md).

## Run the sim

```bash
python3 -m orchestrator.sim
```

Type a fake tool call, e.g.:

```text
set_lighting ALERT_RED 40
set_zone_lighting Cantina NEBULA_PURPLE 35
set_active_zone Observatory
set_alert_level caution
set_viewport_mode space
get_ship_status
list_devices
shutdown_device  # needs confirm via tool_server JSON
wake_device
```

Zones are **names only** (Bridge / Observatory / Cantina / Tech Bay / Cargo) â€” sector footages stay unlocked until posts are measured.


## Run F.R.A.N.K. dry-run console

```bash
python3 -m frank
```

```text
menu
order root_beer
confirm
```

Forced **dry-run** only: explicit `confirm` required; prints `would_pour` JSON; no pumps/GPIO/MQTT. `supervised-wet` is rejected. No face/RFID retention.


## Device power (Phase 1 — dry-run)

Allowlisted tools: `list_devices`, `shutdown_device`, `wake_device`.

- **SIM / dry-run only** — updates in-memory device power state and prints `would_power`
- **No** OS shutdown, Wake-on-LAN, Home Assistant, smart plugs, GPIO, or MQTT actuator publishes
- `shutdown_device` / `wake_device` require `"confirm": true` (CLI: `shutdown_device host_pc confirm`)
- Live power is backlog Phase 2+ — see [`docs/BACKLOG-device-power.md`](docs/BACKLOG-device-power.md)

Via tool server (Open WebUI): POST `/list_devices`, `/shutdown_device`, `/wake_device` on `:8767`.

## Safety

- No unsupervised pours â€” F.R.A.N.K. stays dry-run until you unlock wet tests.
- Allowlisted JSON tools only; sim mode by default.
- Doors/locks must fail safe with manual egress (firmware later).
- Gemini vs Grok conflicts: confirm with Jonathan before locking numbers.

## Layout

- `docs/` â€” lore placeholders for COSMOS RAG
- `ship_core/` â€” Modelfile + identity
- `orchestrator/` â€” tool-call sim loop
- `frank/` â€” persona + pour schema + dry-run console (`python3 -m frank`)
- `mqtt/` â€” topic map stub
- `firmware/` â€” ESP32 notes only

Owner: `JonaSkinny1`

## COSMOS desktop stack (SpaceshipDesktop)

Daily start + health + Open WebUI tools: [`docs/COSMOS-RUNBOOK.md`](docs/COSMOS-RUNBOOK.md)

```powershell
cd $env:USERPROFILE\Documents\cosmic-voyager
.\scripts\start-cosmos-stack.ps1
.\scripts\cosmos-health.ps1
```

After-work measure + optional check: [`AFTER-WORK-CHECKLIST.md`](AFTER-WORK-CHECKLIST.md)