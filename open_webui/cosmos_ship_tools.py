"""
title: COSMOS Ship Tools
author: Cosmic Voyager
description: SIM-only ship tools via local tool_server (no actuators/pours).
version: 0.1.0
"""

from __future__ import annotations

import json
import urllib.request

BASE = "http://127.0.0.1:8767"


def _post(path: str, payload: dict | None = None) -> str:
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8")


class Tools:
    def get_ship_status(self) -> str:
        """Get full Cosmic Voyager sim ship status."""
        return _post("/get_ship_status", {})

    def set_lighting(self, preset: str, brightness: int) -> str:
        """Set global ship lighting preset and brightness (0-100)."""
        return _post("/set_lighting", {"preset": preset, "brightness": int(brightness)})

    def set_zone_lighting(self, zone: str, preset: str, brightness: int) -> str:
        """Set lighting for one zone (Bridge, Observatory, Cantina, Tech Bay, Cargo)."""
        return _post(
            "/set_zone_lighting",
            {"zone": zone, "preset": preset, "brightness": int(brightness)},
        )

    def set_active_zone(self, zone: str) -> str:
        """Set active zone focus."""
        return _post("/set_active_zone", {"zone": zone})

    def set_alert_level(self, level: str) -> str:
        """Set ship alert level: nominal, caution, alert, general_quarters."""
        return _post("/set_alert_level", {"level": level})

    def set_viewport_mode(self, mode: str) -> str:
        """Set viewport mode: offline, sim, space, diagnostics."""
        return _post("/set_viewport_mode", {"mode": mode})