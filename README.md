# Cosmic Voyager — Deck 01

Local-first ship OS stubs for Jonathan’s basement freighter (**Deck 01 / Cosmic Voyager**, Youngstown Outpost).

| Role | Name |
|------|------|
| Ship AI | **COSMOS** |
| Cantina bartender | **F.R.A.N.K.** (Friendly Robot Administering Nourishment & Knowledge) |

## Zones (working)

Bridge → Observatory → Cantina → Tech Bay → Cargo (open freighter flow).

## Stack (software-first)

Ollama + **Qwen3** (`qwen3:8b` start) · Faster-Whisper · Piper/Kokoro · MQTT / Home Assistant · ESP-NOW to ESP32 later.

MCU fleet (docs): 4× GIGA R1 · 1× UNO R4 WiFi · 6× Nano ESP32.

## Run the sim

```bash
python3 -m orchestrator.sim
```

Type a fake tool call, e.g. `set_lighting ALERT_RED 40` or `get_ship_status`.

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
