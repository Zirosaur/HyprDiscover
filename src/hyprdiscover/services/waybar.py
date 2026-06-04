from __future__ import annotations

import json
import sys

from hyprdiscover.backends.packagekit import PackageKitBackend


def run_waybar() -> None:
    """CLI handler for Waybar JSON output mode.

    Uses the backend directly (not UpdateManager) to keep startup fast.
    Must NOT import GTK — this runs on every Waybar interval tick.
    """
    backend = PackageKitBackend()

    try:
        count = backend.get_update_count()

        if count > 0:
            text = f"󰚰 {count}"
            tooltip = f"{count} updates available"
        else:
            text = "󰄬"
            tooltip = "System is up to date"

        output = {
            "text": text,
            "tooltip": tooltip,
            "class": "updates-available" if count else "up-to-date",
        }

    except Exception:
        output = {"text": "⚠", "tooltip": "Unable to check for updates", "class": "error"}

    json.dump(output, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    sys.stdout.flush()
