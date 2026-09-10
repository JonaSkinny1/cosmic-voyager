# Backlog — COSMOS device power control

**Filed:** 2026-09-10 (Jonathan request via CoS)  
**Status:** BACKLOG — do **not** implement live power until Jonathan asks for a phase.  
**Owner:** Spaceship Build / `orchestrator/tool_server.py` + future soft targets

## Goal

COSMOS gains **device power control** — shut down and start/wake devices — so ship ops can power-cycle or sleep gear from the allowlisted tool path.

## Phased plan

### Phase 1 — Software dry-run (safe to build when greenlit)
Allowlisted SIM tools only (in-memory / log `would_power`):

| Tool | Intent |
|------|--------|
| `list_devices` | Inventory known devices + reported power state (sim) |
| `shutdown_device` | Request shutdown / sleep for a device id (dry-run) |
| `wake_device` | Request wake for a device id (dry-run) |

**Rules for Phase 1:**
- Forced dry-run / SIM — no OS calls, no WoL packets, no HA/MQTT actuator publishes
- Explicit **confirm** required on shutdown/wake
- Allowlisted device ids only; reject unknown
- Run [F.R.A.N.K. / COSMOS safety pass](../ — skill on Spaceship Build) before any later live enablement
- Wire into `tool_server` OpenAPI only when Phase 1 is explicitly requested

### Phase 2 — Soft targets (live, gated)
When Jonathan unlocks:

- **PC** sleep/shutdown when SpaceshipDesktop / COSMOS stack is online
- **Home Assistant / smart plugs** for switched loads
- **ESP32 nodes** (fleet already locked: 4× GIGA, 1× UNO R4, 6× Nano ESP32) — software commands only after dry-run proves UX

### Phase 3 — Wake / mains
- **WoL** for PC wake
- **Smart-plug mains** for dumb gear

## Safety (hard)

- Real power / motors / plugs: **confirm + e-stop** path required
- No unsupervised power-off of safety-critical or egress-related gear
- Separate logic vs actuator rails when MCU/plug control lands
- F.R.A.N.K. pours stay dry-run until separately unlocked (orthogonal but same safety skill)
- Do **not** enable live actuators from this backlog entry alone

## Non-goals (now)

- Implementing Phase 1–3 code in this filing
- Ordering smart plugs or WoL NIC changes
- Touching F.R.A.N.K. wet path

## Suggested next ask

Jonathan: “Build Phase 1 dry-run device power tools” → extend `orchestrator/tools.py` + `tool_server` OpenAPI with `list_devices` / `shutdown_device` / `wake_device` (sim only).
