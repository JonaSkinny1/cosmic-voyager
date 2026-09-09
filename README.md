# Cosmic Voyager — Deck 01

Local-first ship OS stubs for Jonathan’s basement freighter (**Deck 01 / Cosmic Voyager**, Youngstown Outpost).

| Role | Name |
|------|------|
| Ship AI | **COSMOS** |
| Cantina bartender | **F.R.A.N.K.** (Friendly Robot Administering Nourishment & Knowledge) |

## Zones (working)

Bridge → Observatory → Cantina → Tech Bay → Cargo (open freighter flow; **ft splits unlocked** until posts measured).

## Stack (software-first)

Ollama + **Qwen3** (`qwen3:8b` start) · Faster-Whisper · Piper/Kokoro · MQTT / Home Assistant · ESP-NOW to ESP32 later.

MCU fleet (docs): 4× GIGA R1 · 1× UNO R4 WiFi · 6× Nano ESP32.


## LOCKED (2026-09-09)

Jonathan conflict triage — do not auto-merge Gemini vs Grok elsewhere.

| Topic | Status |
|-------|--------|
| Viewport Fresnel | **LOCKED** Disney long-f: 8–12 in gap, 1200–1300 mm f (~1250 preferred), ~15–24 in wall; 55-in target. Gemini multi-viewer + Grok short-stack superseded. |
| Ship AI host | **LOCKED** software-first on existing RTX 3090 — Ollama + `qwen3:8b`. Dell out. DGX Spark / other GPUs = future only. |
| Sector ft splits | **KEEP UNLOCKED** — measure support posts before locking zone length bands. |

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
```

Zones are **names only** (Bridge / Observatory / Cantina / Tech Bay / Cargo) — sector footages stay unlocked until posts are measured.

## Safety

- No unsupervised pours — F.R.A.N.K. stays dry-run until you unlock wet tests.
- Allowlisted JSON tools only; sim mode by default.
- Doors/locks must fail safe with manual egress (firmware later).
- Gemini vs Grok conflicts: confirm with Jonathan before locking numbers.

## Layout

- `docs/` — lore placeholders for COSMOS RAG
- `ship_core/` — Modelfile + identity
- `orchestrator/` — tool-call sim loop
- `frank/` — persona + pour schema (dry)
- `mqtt/` — topic map stub
- `firmware/` — ESP32 notes only

Owner: `JonaSkinny1`
