"""Allowlisted tool handlers (simulation only)."""

from __future__ import annotations

from typing import Any, Dict, List

# Working zone labels only — sector footages stay unlocked until posts are measured.
ZONES: List[str] = ["Bridge", "Observatory", "Cantina", "Tech Bay", "Cargo"]

LIGHTING_PRESETS = {
    "ALERT_RED",
    "WARP_BLUE",
    "NEBULA_PURPLE",
    "STEALTH_DARK",
    "DEFAULT_WHITE",
}

ALERT_LEVELS = {"nominal", "caution", "alert", "general_quarters"}
VIEWPORT_MODES = {"offline", "sim", "space", "diagnostics"}


def _default_zone_lighting() -> Dict[str, Dict[str, Any]]:
    return {
        zone: {"preset": "DEFAULT_WHITE", "brightness": 60} for zone in ZONES
    }


SHIP_STATE: Dict[str, Any] = {
    "name": "Cosmic Voyager",
    "deck": "01",
    "mode": "sim",
    "frank": "dry-run",
    "active_zone": "Bridge",
    "alert_level": "nominal",
    "viewport_mode": "sim",
    "lighting": {
        "global": {"preset": "DEFAULT_WHITE", "brightness": 60},
        "zones": _default_zone_lighting(),
    },
    # Sector length splits: KEEP UNLOCKED — measure support posts before locking ft bands.
    "layout_note": "zones named only; ft splits unlocked pending post survey",
    "power_mode": "dry-run",  # Phase 1 — no WoL / HA / plugs / OS power calls
    "devices": {
        "host_pc": {
            "label": "COSMOS host PC (RTX 3090)",
            "zone": "Tech Bay",
            "kind": "pc",
            "power": "on",
            "live_path": "none",
        },
        "ollama": {
            "label": "Ollama local LLM",
            "zone": "Tech Bay",
            "kind": "service",
            "power": "on",
            "live_path": "none",
        },
        "open_webui": {
            "label": "Open WebUI",
            "zone": "Tech Bay",
            "kind": "service",
            "power": "on",
            "live_path": "none",
        },
        "viewport_display": {
            "label": "Observatory 55-in viewport display",
            "zone": "Observatory",
            "kind": "display",
            "power": "on",
            "live_path": "none",
        },
        "cantina_lights": {
            "label": "Cantina zone lights (sim)",
            "zone": "Cantina",
            "kind": "lighting",
            "power": "on",
            "live_path": "none",
        },
        "frank_arm": {
            "label": "F.R.A.N.K. arm bus",
            "zone": "Cantina",
            "kind": "actuator_bus",
            "power": "standby",
            "live_path": "none",
        },
    },
}


def _clamp_brightness(brightness: Any) -> int:
    return max(0, min(100, int(brightness)))


def _normalize_zone(zone: str) -> str | None:
    cleaned = zone.strip().replace("_", " ")
    for name in ZONES:
        if cleaned.lower() == name.lower():
            return name
    return None


def set_lighting(preset: str, brightness: Any) -> Dict[str, Any]:
    """Set global (ship-wide) lighting; does not wipe per-zone overrides."""
    preset = preset.upper()
    if preset not in LIGHTING_PRESETS:
        return {
            "ok": False,
            "error": f"unknown preset {preset}",
            "presets": sorted(LIGHTING_PRESETS),
        }
    level = _clamp_brightness(brightness)
    SHIP_STATE["lighting"]["global"] = {"preset": preset, "brightness": level}
    return {"ok": True, "lighting": {"global": SHIP_STATE["lighting"]["global"]}}


def set_zone_lighting(zone: str, preset: str, brightness: Any) -> Dict[str, Any]:
    name = _normalize_zone(zone)
    if name is None:
        return {"ok": False, "error": f"unknown zone {zone}", "zones": ZONES}
    preset = preset.upper()
    if preset not in LIGHTING_PRESETS:
        return {
            "ok": False,
            "error": f"unknown preset {preset}",
            "presets": sorted(LIGHTING_PRESETS),
        }
    level = _clamp_brightness(brightness)
    SHIP_STATE["lighting"]["zones"][name] = {"preset": preset, "brightness": level}
    return {
        "ok": True,
        "zone": name,
        "lighting": SHIP_STATE["lighting"]["zones"][name],
    }


def set_active_zone(zone: str) -> Dict[str, Any]:
    name = _normalize_zone(zone)
    if name is None:
        return {"ok": False, "error": f"unknown zone {zone}", "zones": ZONES}
    SHIP_STATE["active_zone"] = name
    return {"ok": True, "active_zone": name}


def set_alert_level(level: str) -> Dict[str, Any]:
    cleaned = level.strip().lower().replace("-", "_").replace(" ", "_")
    if cleaned not in ALERT_LEVELS:
        return {
            "ok": False,
            "error": f"unknown alert level {level}",
            "levels": sorted(ALERT_LEVELS),
        }
    SHIP_STATE["alert_level"] = cleaned
    return {"ok": True, "alert_level": cleaned}


def set_viewport_mode(mode: str) -> Dict[str, Any]:
    cleaned = mode.strip().lower()
    if cleaned not in VIEWPORT_MODES:
        return {
            "ok": False,
            "error": f"unknown viewport mode {mode}",
            "modes": sorted(VIEWPORT_MODES),
        }
    SHIP_STATE["viewport_mode"] = cleaned
    return {"ok": True, "viewport_mode": cleaned}


def get_ship_status() -> Dict[str, Any]:
    return dict(SHIP_STATE)


def list_devices() -> Dict[str, Any]:
    """List allowlisted devices and sim power state (dry-run inventory)."""
    devices = SHIP_STATE.get("devices", {})
    return {
        "ok": True,
        "power_mode": SHIP_STATE.get("power_mode", "dry-run"),
        "live_power": False,
        "devices": {
            did: {
                "id": did,
                "label": meta.get("label"),
                "zone": meta.get("zone"),
                "kind": meta.get("kind"),
                "power": meta.get("power"),
                "live_path": meta.get("live_path", "none"),
            }
            for did, meta in devices.items()
        },
        "message": "DRY-RUN inventory only — no real power control.",
    }


def _require_dry_run_confirm(confirm: Any, mode: Any) -> Dict[str, Any] | None:
    if mode is not None and str(mode).strip().lower() not in ("", "dry-run", "sim"):
        return {
            "ok": False,
            "error": f"rejected: live/power mode '{mode}' not enabled — dry-run only",
            "power_mode": "dry-run",
            "live_power": False,
        }
    if confirm is not True:
        return {
            "ok": False,
            "error": "rejected: confirm must be true (explicit confirm required)",
            "power_mode": "dry-run",
            "live_power": False,
        }
    return None


def shutdown_device(device_id: str, confirm: Any = False, mode: Any = "dry-run") -> Dict[str, Any]:
    """Simulate shutdown/sleep for an allowlisted device. No OS/WoL/HA/plug calls."""
    gate = _require_dry_run_confirm(confirm, mode)
    if gate:
        return gate
    devices = SHIP_STATE.get("devices", {})
    did = (device_id or "").strip()
    if did not in devices:
        return {
            "ok": False,
            "error": f"unknown device_id '{device_id}'",
            "devices": sorted(devices),
        }
    prev = devices[did].get("power")
    devices[did]["power"] = "off"
    return {
        "ok": True,
        "power_mode": "dry-run",
        "live_power": False,
        "device_id": did,
        "previous": prev,
        "power": "off",
        "would_power": {
            "action": "shutdown",
            "device_id": did,
            "os_call": None,
            "wol": None,
            "ha": None,
            "smart_plug": None,
            "mqtt_published": [],
            "gpio": [],
        },
        "message": f"DRY-RUN: would shut down {devices[did]['label']} — no hardware/OS power changed.",
    }


def wake_device(device_id: str, confirm: Any = False, mode: Any = "dry-run") -> Dict[str, Any]:
    """Simulate wake/start for an allowlisted device. No WoL/HA/plug calls."""
    gate = _require_dry_run_confirm(confirm, mode)
    if gate:
        return gate
    devices = SHIP_STATE.get("devices", {})
    did = (device_id or "").strip()
    if did not in devices:
        return {
            "ok": False,
            "error": f"unknown device_id '{device_id}'",
            "devices": sorted(devices),
        }
    prev = devices[did].get("power")
    devices[did]["power"] = "on"
    return {
        "ok": True,
        "power_mode": "dry-run",
        "live_power": False,
        "device_id": did,
        "previous": prev,
        "power": "on",
        "would_power": {
            "action": "wake",
            "device_id": did,
            "os_call": None,
            "wol": None,
            "ha": None,
            "smart_plug": None,
            "mqtt_published": [],
            "gpio": [],
        },
        "message": f"DRY-RUN: would wake {devices[did]['label']} — no hardware/OS power changed.",
    }


TOOL_MAP = {
    "set_lighting": set_lighting,
    "set_zone_lighting": set_zone_lighting,
    "set_active_zone": set_active_zone,
    "set_alert_level": set_alert_level,
    "set_viewport_mode": set_viewport_mode,
    "get_ship_status": get_ship_status,
    "list_devices": list_devices,
    "shutdown_device": shutdown_device,
    "wake_device": wake_device,
}
