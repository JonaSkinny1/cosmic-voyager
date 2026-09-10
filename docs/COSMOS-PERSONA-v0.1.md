# COSMOS persona v0.1 (Jarvis-leaning)

**Status:** Draft for Jonathan — lore still unlocked; this is voice + behavior, not locked ship history.

## Goal
Make local COSMOS (Ollama `cosmos` from `ship_core/Modelfile`) feel closer to a trusted freighter AI: warm, concise, capable with tools — not a sterile chatbot.

## What’s in the Modelfile
- Warm / dry humor voice; short answers by default
- Ohio Outpost // Sol-3 · CV-OH-01 place chrome
- Explicit **lore unlocked** — do not invent backstory
- Tool discipline + Phase 1 dry-run device power allowlist
- F.R.A.N.K. dry-run only; no fake hardware claims

## Apply on SpaceshipDesktop
```bash
cd path\to\cosmic-voyager
git pull
ollama create cosmos -f ship_core/Modelfile
```
Then pick model `cosmos` in Open WebUI.

## Later (when Jonathan locks lore)
Add a short “LOCKED LORE” block to the SYSTEM prompt and/or a RAG notes file — do not bake unfinished story into the model now.

## Not this pass
- Cloud Grok Bot parity (separate stack)
- Live device power / WoL / HA
- Voice wake word / TTS personality pack
