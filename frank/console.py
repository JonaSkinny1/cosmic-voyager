"""F.R.A.N.K. dry-run order console — sim only, no actuators."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from .drinks import DRINKS, list_drinks

SCHEMA_PATH = Path(__file__).with_name("pour_schema.json")
ALLOWED_MODES = {"dry-run"}
# Face / RFID must never be collected or retained in this slice.
FORBIDDEN_KEYS = {"face", "rfid", "biometrics", "camera", "identity"}

BANNER = """
F.R.A.N.K. // Friendly Robot Administering Nourishment & Knowledge
Deck 01 Cantina // DRY-RUN ONLY — no pumps, motors, GPIO, or MQTT publishes
Commands:
  menu                         list allowlisted bottle/can drinks
  order <drink_id>             stage an order (still needs confirm)
  confirm                      confirm staged order → print would_pour JSON
  cancel                       clear staged order
  status                       show mode + staged order
  help
  quit
Rejects: missing confirm, unknown drink, supervised-wet, face/RFID fields
"""


def load_schema() -> Dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text())


def validate_order(payload: Dict[str, Any]) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "order must be a JSON object"
    # order_id is console-internal; not part of the pour schema allowlist.
    public_keys = {"drink_id", "confirm", "mode", "gesture", "notes"}
    for key in payload:
        if key == "order_id":
            continue
        if key in FORBIDDEN_KEYS:
            return False, f"rejected: {key} not allowed (no face/RFID retention)"
        if key not in public_keys:
            return False, f"rejected: unknown property '{key}' (allowlisted schema only)"
    if "drink_id" not in payload:
        return False, "rejected: drink_id required"
    drink_id = payload["drink_id"]
    if drink_id not in DRINKS:
        return False, f"rejected: unknown drink_id '{drink_id}'"
    if "mode" not in payload:
        return False, "rejected: mode required"
    mode = payload["mode"]
    if mode == "supervised-wet":
        return False, "rejected: supervised-wet is not live — dry-run only"
    if mode not in ALLOWED_MODES:
        return False, f"rejected: mode must be dry-run (got {mode})"
    if payload.get("confirm") is not True:
        return False, "rejected: confirm must be true (explicit confirm required)"
    return True, "ok"


def build_would_pour(order: Dict[str, Any]) -> Dict[str, Any]:
    drink = DRINKS[order["drink_id"]]
    return {
        "ok": True,
        "bartender": "F.R.A.N.K.",
        "mode": "dry-run",
        "order_id": order.get("order_id") or str(uuid.uuid4()),
        "order": {
            "drink_id": order["drink_id"],
            "label": drink["label"],
            "confirm": True,
            "mode": "dry-run",
            "gesture": order.get("gesture"),
            "notes": order.get("notes"),
        },
        "would_pour": drink["would_pour"],
        "hardware": {
            "executed": False,
            "pumps": [],
            "gpio": [],
            "mqtt_published": [],
        },
        "message": f"DRY-RUN: would dispense {drink['label']} — no hardware moved.",
    }


class FrankConsole:
    def __init__(self) -> None:
        self.mode = "dry-run"
        self.staged: Optional[Dict[str, Any]] = None

    def cmd_menu(self) -> str:
        lines = ["Allowlisted drinks (bottle/can lean):"]
        for sku, label in list_drinks().items():
            lines.append(f"  {sku:18}  {label}")
        return "\n".join(lines)

    def cmd_order(self, drink_id: str) -> str:
        drink_id = drink_id.strip()
        if drink_id not in DRINKS:
            return f"Unknown drink_id '{drink_id}'. Type 'menu'."
        self.staged = {
            "drink_id": drink_id,
            "confirm": False,
            "mode": "dry-run",
            "order_id": str(uuid.uuid4()),
        }
        label = DRINKS[drink_id]["label"]
        return (
            f"Staged: {label} ({drink_id}) [mode=dry-run, confirm=false]\n"
            "Type 'confirm' to print would_pour JSON, or 'cancel'."
        )

    def cmd_confirm(self) -> str:
        if not self.staged:
            return "Nothing staged. Use: order <drink_id>"
        payload = dict(self.staged)
        payload["confirm"] = True
        payload["mode"] = "dry-run"  # forced
        ok, reason = validate_order(payload)
        if not ok:
            return reason
        result = build_would_pour(payload)
        self.staged = None
        return json.dumps(result, indent=2)

    def cmd_cancel(self) -> str:
        self.staged = None
        return "Staged order cleared."

    def cmd_status(self) -> str:
        return json.dumps(
            {
                "bartender": "F.R.A.N.K.",
                "mode": self.mode,
                "supervised_wet_live": False,
                "staged": self.staged,
            },
            indent=2,
        )

    def dispatch(self, line: str) -> str:
        parts = line.strip().split()
        if not parts:
            return ""
        cmd = parts[0].lower()
        if cmd in ("quit", "exit", "q"):
            raise SystemExit(0)
        if cmd in ("help", "?"):
            return BANNER.strip()
        if cmd == "menu":
            return self.cmd_menu()
        if cmd == "order":
            if len(parts) < 2:
                return "Usage: order <drink_id>"
            return self.cmd_order(parts[1])
        if cmd == "confirm":
            return self.cmd_confirm()
        if cmd == "cancel":
            return self.cmd_cancel()
        if cmd == "status":
            return self.cmd_status()
        # Allow pasting a full JSON order (must include confirm:true)
        if line.strip().startswith("{"):
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                return f"Invalid JSON: {exc}"
            # Force dry-run even if caller asked otherwise after validation message
            ok, reason = validate_order(payload)
            if not ok:
                return reason
            payload = dict(payload)
            payload["mode"] = "dry-run"
            payload["order_id"] = payload.get("order_id") or str(uuid.uuid4())
            return json.dumps(build_would_pour(payload), indent=2)
        return "Unknown command. Type 'help'."


def main() -> None:
    console = FrankConsole()
    print(BANNER.strip())
    print(console.cmd_status())
    print()
    while True:
        try:
            line = input("frank> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        out = console.dispatch(line)
        if out:
            print(out)


if __name__ == "__main__":
    main()
