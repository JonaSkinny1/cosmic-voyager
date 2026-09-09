"""Local SIM-only ship tools HTTP API for Open WebUI (OpenAPI)."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict
from urllib.parse import urlparse

from .tools import TOOL_MAP, get_ship_status

HOST = "127.0.0.1"
PORT = 8767

PRESETS = [
    "ALERT_RED",
    "WARP_BLUE",
    "NEBULA_PURPLE",
    "STEALTH_DARK",
    "DEFAULT_WHITE",
]
ZONES = ["Bridge", "Observatory", "Cantina", "Tech Bay", "Cargo"]
ALERTS = ["nominal", "caution", "alert", "general_quarters"]
VIEWPORTS = ["offline", "sim", "space", "diagnostics"]


def _obj(props: dict, required: list | None = None) -> dict:
    schema: Dict[str, Any] = {"type": "object", "properties": props}
    if required:
        schema["required"] = required
    return schema


def _post(path: str, op: str, summary: str, schema: dict) -> dict:
    return {
        path: {
            "post": {
                "operationId": op,
                "summary": summary,
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": schema}},
                },
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    }
                },
            }
        }
    }


OPENAPI: Dict[str, Any] = {
    "openapi": "3.0.3",
    "info": {
        "title": "COSMOS Ship Tools (SIM)",
        "version": "0.1.0",
        "description": "Allowlisted Cosmic Voyager sim tools. No actuators/pours.",
    },
    "servers": [{"url": f"http://{HOST}:{PORT}"}],
    "paths": {},
}

OPENAPI["paths"].update(
    _post(
        "/get_ship_status",
        "get_ship_status",
        "Get full sim ship status",
        _obj({}),
    )
)
OPENAPI["paths"]["/get_ship_status"]["post"]["requestBody"]["required"] = False

OPENAPI["paths"].update(
    _post(
        "/set_lighting",
        "set_lighting",
        "Set global ship lighting",
        _obj(
            {
                "preset": {"type": "string", "enum": PRESETS},
                "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            ["preset", "brightness"],
        ),
    )
)
OPENAPI["paths"].update(
    _post(
        "/set_zone_lighting",
        "set_zone_lighting",
        "Set lighting for one zone",
        _obj(
            {
                "zone": {"type": "string", "enum": ZONES},
                "preset": {"type": "string", "enum": PRESETS},
                "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            ["zone", "preset", "brightness"],
        ),
    )
)
OPENAPI["paths"].update(
    _post(
        "/set_active_zone",
        "set_active_zone",
        "Set active zone focus",
        _obj({"zone": {"type": "string", "enum": ZONES}}, ["zone"]),
    )
)
OPENAPI["paths"].update(
    _post(
        "/set_alert_level",
        "set_alert_level",
        "Set ship alert level",
        _obj({"level": {"type": "string", "enum": ALERTS}}, ["level"]),
    )
)
OPENAPI["paths"].update(
    _post(
        "/set_viewport_mode",
        "set_viewport_mode",
        "Set viewport display mode (sim metadata)",
        _obj({"mode": {"type": "string", "enum": VIEWPORTS}}, ["mode"]),
    )
)


def _dispatch(path: str, body: Dict[str, Any]) -> Any:
    name = path.strip("/").split("/")[0]
    if name not in TOOL_MAP:
        return {"ok": False, "error": f"unknown tool {name}"}
    fn: Callable = TOOL_MAP[name]
    if name == "get_ship_status":
        return fn()
    if name == "set_lighting":
        return fn(body.get("preset", "DEFAULT_WHITE"), body.get("brightness", 60))
    if name == "set_zone_lighting":
        return fn(
            body.get("zone", "Bridge"),
            body.get("preset", "DEFAULT_WHITE"),
            body.get("brightness", 60),
        )
    if name == "set_active_zone":
        return fn(body.get("zone", "Bridge"))
    if name == "set_alert_level":
        return fn(body.get("level", "nominal"))
    if name == "set_viewport_mode":
        return fn(body.get("mode", "sim"))
    return {"ok": False, "error": "unhandled"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code: int, payload: Any) -> None:
        data = (
            payload
            if isinstance(payload, (bytes, bytearray))
            else json.dumps(payload).encode("utf-8")
        )
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        if code != 204:
            self.wfile.write(data)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, b"")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/openapi.json", "/"):
            self._send(200, OPENAPI)
            return
        if path == "/health":
            self._send(200, {"ok": True, "mode": "sim"})
            return
        if path == "/get_ship_status":
            self._send(200, get_ship_status())
            return
        self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send(400, {"ok": False, "error": "invalid json"})
            return
        if not isinstance(body, dict):
            body = {}
        try:
            result = _dispatch(path, body)
        except Exception as exc:  # noqa: BLE001
            self._send(500, {"ok": False, "error": str(exc)})
            return
        self._send(200, result)


def main() -> None:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"COSMOS tool server (SIM) http://{HOST}:{PORT}")
    print(f"OpenAPI: http://{HOST}:{PORT}/openapi.json")
    httpd.serve_forever()


if __name__ == "__main__":
    main()