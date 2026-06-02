from __future__ import annotations

import json


class TestUnicodeIcons:
    """Verify all icon strings use valid Unicode (no surrogate code points)."""

    def test_all_icons_encode_to_utf8(self) -> None:
        icons: list[str] = [
            # summary_card.py
            "\U000F0B30",
            "\U000F0330",
            "\U000F06B0",
            "\U000F012C",
            "\U000F0482",
            "\U000F0190",
            "\U000F0020",
            "\U000F0820",
            # window.py action icons
            "\U000F0450",
            "\U000F0196",
            "\U000F0709",
            # BMP chars
            "\u2713",
            "\u26A0",
            "\u2014",
            "\u2026",
        ]
        for icon in icons:
            b = icon.encode("utf-8")
            assert len(b) > 0, f"Icon {icon!r} encoded to empty bytes"

    def test_codepoints_above_ffff_are_not_surrogates(self) -> None:
        for icon in [
            "\U000F0B30",
            "\U000F0330",
            "\U000F06B0",
            "\U000F012C",
            "\U000F0482",
            "\U000F0190",
            "\U000F0020",
            "\U000F0820",
            "\U000F0450",
            "\U000F0196",
            "\U000F0709",
        ]:
            assert len(icon) == 1, f"Icon U+{ord(icon):05X} has length {len(icon)}, expected 1"

    def test_json_serialization_produces_valid_utf8(self) -> None:
        text = "\U000F06B0 5"
        output = {"text": text, "tooltip": "5 updates available"}
        json_str = json.dumps(output, ensure_ascii=False)
        json_str.encode("utf-8")
        parsed = json.loads(json_str)
        assert parsed["text"] == text
