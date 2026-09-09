"""COSMOS LLM bridge: Ollama cosmos model -> allowlisted sim tools."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from typing import Any

from .tools import TOOL_MAP, get_ship_status

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def _extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and "tool" in obj:
            return obj
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[^{}]*\"tool\"[^{}]*\}", text, re.DOTALL)
    if not m:
        m = re.search(r"\{.*\"tool\".*\}", text, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and "tool" in obj:
                return obj
        except json.JSONDecodeError:
            return None
    return None


def ask_cosmos(prompt: str, model: str = "cosmos") -> str:
    body = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    return (data.get("response") or "").strip()


def run_tool(call: dict[str, Any]) -> Any:
    name = call.get("tool")
    args = call.get("args") or {}
    if name not in TOOL_MAP:
        return {"ok": False, "error": f"tool not allowlisted: {name}"}
    fn = TOOL_MAP[name]
    if name == "get_ship_status":
        return fn()
    if name == "set_lighting":
        return fn(args.get("preset", "DEFAULT_WHITE"), args.get("brightness", 60))
    if name == "set_zone_lighting":
        return fn(
            args.get("zone", "Bridge"),
            args.get("preset", "DEFAULT_WHITE"),
            args.get("brightness", 60),
        )
    if name == "set_active_zone":
        return fn(args.get("zone", "Bridge"))
    if name == "set_alert_level":
        return fn(args.get("level", "nominal"))
    if name == "set_viewport_mode":
        return fn(args.get("mode", "sim"))
    return {"ok": False, "error": "unhandled tool"}


def handle_user(line: str) -> str:
    reply = ask_cosmos(line)
    call = _extract_json(reply)
    if not call:
        return f"COSMOS: {reply}"
    result = run_tool(call)
    return (
        f"COSMOS tool call:\n{json.dumps(call, indent=2)}\n\n"
        f"SIM result:\n{json.dumps(result, indent=2)}"
    )


def main() -> None:
    print("COSMOS // Ollama bridge // SIM tools only // type quit to exit")
    print(json.dumps(get_ship_status(), indent=2))
    print()
    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"quit", "exit", "q"}:
            break
        try:
            print(handle_user(line))
        except Exception as exc:  # noqa: BLE001
            print(f"error: {exc}", file=sys.stderr)
        print()


if __name__ == "__main__":
    main()
