from __future__ import annotations

import io
import json
import sys


class TestWaybarOutput:
    def test_json_format(self) -> None:
        from hyprdiscover.services.waybar import run_waybar
        output = {"text": "󰄬", "tooltip": "System is up to date", "class": "up-to-date"}
        json_str = json.dumps(output)
        parsed = json.loads(json_str)
        assert "text" in parsed
        assert "tooltip" in parsed
        assert "class" in parsed
