"""Terminal simulation loop for COSMOS tool-calls."""

from __future__ import annotations

import json

from .tools import TOOL_MAP, ZONES, get_ship_status


BANNER = """
COSMOS // Cosmic Voyager // Deck 01 // SIM MODE
Zones: Bridge | Observatory | Cantina | Tech Bay | Cargo  (names only — ft splits unlocked)
Tools:
  set_lighting <PRESET> <0-100>
  set_zone_lighting <ZONE> <PRESET> <0-100>
  set_active_zone <ZONE>
  set_alert_level <nominal|caution|alert|general_quarters>
  set_viewport_mode <offline|sim|space|diagnostics>
  list_devices
  shutdown_device <device_id> confirm
  wake_device <device_id> confirm
  get_ship_status
  quit
Presets: ALERT_RED WARP_BLUE NEBULA_PURPLE STEALTH_DARK DEFAULT_WHITE
F.R.A.N.K.: dry-run only — no pours
Device power: DRY-RUN only — no WoL / HA / plugs / OS power
"""


def dispatch(line: str) -> str:
    parts = line.strip().split()
    if not parts:
        return ""
    cmd = parts[0]
    if cmd in ("quit", "exit", "q"):
        raise SystemExit(0)

    if cmd == "get_ship_status":
        return json.dumps(TOOL_MAP["get_ship_status"](), indent=2)

    if cmd == "set_lighting" and len(parts) >= 3:
        return json.dumps(TOOL_MAP["set_lighting"](parts[1], parts[2]), indent=2)

    if cmd == "set_zone_lighting" and len(parts) >= 4:
        zone = " ".join(parts[1:-2]) if len(parts) > 4 else parts[1]
        # Support Tech_Bay or "Tech Bay" via underscore; multi-word zone = all but last two tokens
        if len(parts) == 4:
            zone, preset, brightness = parts[1], parts[2], parts[3]
        else:
            zone = " ".join(parts[1:-2])
            preset, brightness = parts[-2], parts[-1]
        return json.dumps(
            TOOL_MAP["set_zone_lighting"](zone, preset, brightness), indent=2
        )

    if cmd == "set_active_zone" and len(parts) >= 2:
        zone = " ".join(parts[1:])
        return json.dumps(TOOL_MAP["set_active_zone"](zone), indent=2)

    if cmd == "set_alert_level" and len(parts) >= 2:
        return json.dumps(TOOL_MAP["set_alert_level"](parts[1]), indent=2)

    if cmd == "set_viewport_mode" and len(parts) >= 2:
        return json.dumps(TOOL_MAP["set_viewport_mode"](parts[1]), indent=2)

    if cmd == "list_devices":
        return json.dumps(TOOL_MAP["list_devices"](), indent=2)

    if cmd == "shutdown_device" and len(parts) >= 2:
        device_id = parts[1]
        confirm = len(parts) >= 3 and parts[2].lower() in ("confirm", "true", "yes")
        return json.dumps(
            TOOL_MAP["shutdown_device"](device_id, confirm, "dry-run"), indent=2
        )

    if cmd == "wake_device" and len(parts) >= 2:
        device_id = parts[1]
        confirm = len(parts) >= 3 and parts[2].lower() in ("confirm", "true", "yes")
        return json.dumps(
            TOOL_MAP["wake_device"](device_id, confirm, "dry-run"), indent=2
        )

    return (
        "Unknown command. Try: set_lighting ALERT_RED 40 | "
        "set_zone_lighting Cantina NEBULA_PURPLE 35 | "
        "set_active_zone Observatory | set_alert_level caution | "
        "set_viewport_mode space | list_devices | "
        "shutdown_device host_pc confirm | wake_device host_pc confirm | "
        "get_ship_status | quit"
        f"\nZones: {', '.join(ZONES)}"
    )


def main() -> None:
    print(BANNER.strip())
    print(json.dumps(get_ship_status(), indent=2))
    print()
    while True:
        try:
            line = input("cosmos> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        out = dispatch(line)
        if out:
            print(out)


if __name__ == "__main__":
    main()
