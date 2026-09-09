"""Allowlisted bottle/can drinks for F.R.A.N.K. dry-run."""

from __future__ import annotations

from typing import Any, Dict

# SKU -> human label + dry-run dispense plan (no hardware).
DRINKS: Dict[str, Dict[str, Any]] = {
    "root_beer": {
        "label": "Root Beer (can)",
        "container": "can",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "root_beer",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
    "cola": {
        "label": "Cola (can)",
        "container": "can",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "cola",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
    "ginger_ale": {
        "label": "Ginger Ale (can)",
        "container": "can",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "ginger_ale",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
    "sparkling_water": {
        "label": "Sparkling Water (bottle)",
        "container": "bottle",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "sparkling_water",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
    "still_water": {
        "label": "Still Water (bottle)",
        "container": "bottle",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "still_water",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
    "orange_soda": {
        "label": "Orange Soda (can)",
        "container": "can",
        "would_pour": {
            "action": "dispense_sealed",
            "sku": "orange_soda",
            "qty": 1,
            "arm": "idle_sim",
            "pumps": [],
            "gpio": [],
            "mqtt_topics": [],
        },
    },
}


def list_drinks() -> Dict[str, str]:
    return {sku: meta["label"] for sku, meta in DRINKS.items()}
