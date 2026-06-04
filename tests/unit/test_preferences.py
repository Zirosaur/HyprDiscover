from __future__ import annotations

from unittest.mock import MagicMock

from hyprdiscover.config import AppConfig
from hyprdiscover.ui.dialogs.preferences import PreferencesWindow


class TestPreferencesWindow:
    def test_widgets_reflect_config(self) -> None:
        config = AppConfig()
        config.auto_refresh = False
        config.log_level = "DEBUG"
        config.confirm_update = True

        win = PreferencesWindow(None, config)

        assert win._auto_refresh_switch.get_active() is False
        assert win._confirm_update_switch.get_active() is True
        assert win._confirm_reboot_switch.get_active() is True
        assert win._show_notifications_switch.get_active() is True
        assert win._check_on_startup_switch.get_active() is True
        assert win._log_level_dropdown.get_selected() == 0  # DEBUG is index 0

    def test_toggle_saves_config(self) -> None:
        config = AppConfig()
        config.save = MagicMock()  # type: ignore[method-assign]

        win = PreferencesWindow(None, config)
        win._auto_refresh_switch.set_active(False)

        assert config.auto_refresh is False
        config.save.assert_called()

    def test_reset_restores_defaults(self) -> None:
        config = AppConfig()
        config.auto_refresh = False
        config.log_level = "ERROR"
        config.confirm_update = True
        config.save = MagicMock()  # type: ignore[method-assign]

        win = PreferencesWindow(None, config)
        win._on_reset(None)

        assert config.auto_refresh is True
        assert config.log_level == "INFO"
        assert config.confirm_update is False
        config.save.assert_called()

        assert win._auto_refresh_switch.get_active() is True
        assert win._log_level_dropdown.get_selected() == 1  # INFO is index 1
