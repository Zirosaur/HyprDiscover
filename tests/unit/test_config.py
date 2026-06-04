from __future__ import annotations

import tempfile
from pathlib import Path

from hyprdiscover.config import AppConfig, load_config


class TestAppConfig:
    def test_default_values(self) -> None:
        c = AppConfig()
        assert c.auto_refresh is True
        assert c.show_notifications is True
        assert c.check_on_startup is True
        assert c.confirm_update is False
        assert c.confirm_reboot is True
        assert c.log_level == "INFO"

    def test_save_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.toml"

            c = AppConfig()
            c.auto_refresh = False
            c.log_level = "DEBUG"
            c.confirm_update = True
            c.save(path)

            loaded = load_config(path)
            assert loaded.auto_refresh is False
            assert loaded.log_level == "DEBUG"
            assert loaded.confirm_update is True
            assert loaded.show_notifications is True  # unchanged default

    def test_missing_file_returns_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nonexistent.toml"
            loaded = load_config(path)
            assert loaded.auto_refresh is True
            assert loaded.log_level == "INFO"

    def test_corrupt_file_returns_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "corrupt.toml"
            path.write_text("this is not valid toml {{{")
            loaded = load_config(path)
            assert loaded.auto_refresh is True

    def test_auto_start_defaults_to_false(self) -> None:
        c = AppConfig()
        assert c.auto_start is False
