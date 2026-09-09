"""Allowlisted tool handlers (simulation only)."""

from __future__ import annotations

from typing import Any, Dict

SHIP_STATE = {
    "name": "Cosmic Voyager",
    "deck": "01",
    "lighting": {"preset": "DEFAULT_WHITE", "brightness": 60},
    "mode": "sim",
    "frank": "dry-run",
}


def set_lighting(preset: str, brightness: int) -> Dict[str, Any]:
    brightness = max(0, min(100, int(brightness)))
    SHIP_STATE["lighting"] = {"preset": preset, "brightness": brightness}
    return {"ok": True, "lighting": SHIP_STATE["lighting"]}


def get_ship_status() -> Dict[str, Any]:
    return dict(SHIP_STATE)


TOOL_MAP = {
    "set_lighting": set_lighting,
    "get_ship_status": get_ship_status,
}
