"""Terminal simulation loop for COSMOS tool-calls."""

from __future__ import annotations

import json

from .tools import TOOL_MAP, get_ship_status


BANNER = """
COSMOS // Cosmic Voyager // Deck 01 // SIM MODE
Tools: set_lighting <PRESET> <0-100> | get_ship_status | quit
Presets: ALERT_RED WARP_BLUE NEBULA_PURPLE STEALTH_DARK DEFAULT_WHITE
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
        result = TOOL_MAP["set_lighting"](parts[1], parts[2])
        return json.dumps(result, indent=2)
    return "Unknown command. Try: set_lighting ALERT_RED 40 | get_ship_status | quit"


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
