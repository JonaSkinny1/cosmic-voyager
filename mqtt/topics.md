# MQTT topic map (stub)

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `ship/control/lighting` | orchestrator → HA | lighting presets |
| `ship/control/alert` | orchestrator → HA | alert scenes |
| `ship/status` | nodes → orchestrator | telemetry |
| `frank/order` | UI → orchestrator | drink orders (confirm required) |
| `frank/telemetry` | arm → orchestrator | pour progress (future) |

Broker: local Mosquitto later. Auth required before any actuator topic goes live.
