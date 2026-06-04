from __future__ import annotations

from unittest.mock import MagicMock, patch

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

    def test_auto_start_toggle_calls_autostart(self) -> None:
        config = AppConfig()
        config.save = MagicMock()  # type: ignore[method-assign]

        with patch("hyprdiscover.services.autostart.enable_autostart") as mock_enable, \
             patch("hyprdiscover.services.autostart.is_autostart_enabled",
                   return_value=False):
            win = PreferencesWindow(None, config)
            win._auto_start_switch.set_active(True)

        assert config.auto_start is True
        config.save.assert_called()
        mock_enable.assert_called_once()

    def test_auto_start_toggle_calls_disable(self) -> None:
        config = AppConfig()
        config.save = MagicMock()  # type: ignore[method-assign]

        with patch("hyprdiscover.services.autostart.disable_autostart") as mock_disable, \
             patch("hyprdiscover.services.autostart.is_autostart_enabled",
                   return_value=True):
            win = PreferencesWindow(None, config)
            win._auto_start_switch.set_active(False)

        assert config.auto_start is False
        config.save.assert_called()
        mock_disable.assert_called_once()
