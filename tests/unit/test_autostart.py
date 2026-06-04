from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from hyprdiscover.services.autostart import (
    disable_autostart,
    enable_autostart,
    is_autostart_enabled,
)


class TestAutostart:
    def test_enable_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "hyprdiscover.desktop"
            with patch("hyprdiscover.services.autostart._AUTOSTART_FILE", file_path):
                enable_autostart()
            assert file_path.exists()
            content = file_path.read_text()
            assert "Exec=hyprdiscover" in content
            assert "Type=Application" in content
            assert "StartupNotify=false" in content
            assert "NoDisplay=true" not in content

    def test_disable_removes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "hyprdiscover.desktop"
            file_path.write_text("test")
            with patch("hyprdiscover.services.autostart._AUTOSTART_FILE", file_path):
                disable_autostart()
            assert not file_path.exists()

    def test_disable_when_not_enabled_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.desktop"
            with patch("hyprdiscover.services.autostart._AUTOSTART_FILE", file_path):
                disable_autostart()

    def test_is_enabled_reflects_file_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.desktop"
            with patch("hyprdiscover.services.autostart._AUTOSTART_FILE", file_path):
                assert is_autostart_enabled() is False
                enable_autostart()
                assert is_autostart_enabled() is True
                disable_autostart()
                assert is_autostart_enabled() is False

    def test_enable_twice_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "idem.desktop"
            with patch("hyprdiscover.services.autostart._AUTOSTART_FILE", file_path):
                enable_autostart()
                content_first = file_path.read_text()
                enable_autostart()
                content_second = file_path.read_text()
                assert content_first == content_second
