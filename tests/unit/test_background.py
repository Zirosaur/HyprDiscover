from __future__ import annotations

import io
from unittest.mock import MagicMock, patch

from hyprdiscover.config import AppConfig
from hyprdiscover.services.background import run_background_check


def _make_config(**overrides: object) -> AppConfig:
    config = AppConfig()
    for key, value in overrides.items():
        setattr(config, key, value)
    return config


class TestRunBackgroundCheck:
    def test_up_to_date_no_notification(self) -> None:
        mock_backend = MagicMock()
        mock_backend.get_updates.return_value = []
        mock_backend.refresh_cache.return_value = None
        config = _make_config(auto_refresh=True, show_notifications=True)

        with (
            patch("hyprdiscover.services.background.PackageKitBackend",
                  return_value=mock_backend),
            patch("hyprdiscover.services.background.load_config",
                  return_value=config),
            patch("hyprdiscover.services.background.NotificationService") as mock_notifier,
        ):
            exit_code = run_background_check()

        assert exit_code == 0
        mock_notifier.return_value.updates_available.assert_not_called()

    def test_with_updates_notification(self) -> None:
        mock_backend = MagicMock()
        mock_backend.refresh_cache.return_value = None
        from hyprdiscover.models.package import Package

        pkg = Package(
            name="firefox",
            package_id="firefox-131.0.x86_64",
            version_available="131.0-1.fc40",
            category="security",
        )
        mock_backend.get_updates.return_value = [pkg, pkg, pkg]
        config = _make_config(auto_refresh=True, show_notifications=True)

        with (
            patch("hyprdiscover.services.background.PackageKitBackend",
                  return_value=mock_backend),
            patch("hyprdiscover.services.background.load_config",
                  return_value=config),
            patch("hyprdiscover.services.background.NotificationService") as mock_notifier,
        ):
            exit_code = run_background_check()

        assert exit_code == 0
        mock_notifier.return_value.updates_available.assert_called_once_with(3)

    def test_notifications_disabled(self) -> None:
        mock_backend = MagicMock()
        mock_backend.refresh_cache.return_value = None
        from hyprdiscover.models.package import Package

        pkg = Package(
            name="firefox",
            package_id="firefox-131.0.x86_64",
            version_available="131.0-1.fc40",
            category="security",
        )
        mock_backend.get_updates.return_value = [pkg]
        config = _make_config(auto_refresh=True, show_notifications=False)

        with (
            patch("hyprdiscover.services.background.PackageKitBackend",
                  return_value=mock_backend),
            patch("hyprdiscover.services.background.load_config",
                  return_value=config),
            patch("hyprdiscover.services.background.NotificationService") as mock_notifier,
        ):
            exit_code = run_background_check()

        assert exit_code == 0
        mock_notifier.return_value.updates_available.assert_not_called()

    def test_auto_refresh_disabled(self) -> None:
        config = _make_config(auto_refresh=False)

        with (
            patch("hyprdiscover.services.background.load_config",
                  return_value=config),
            patch("hyprdiscover.services.background.PackageKitBackend") as mock_backend_class,
        ):
            exit_code = run_background_check()

        assert exit_code == 0
        mock_backend_class.assert_not_called()

    def test_error_returns_one(self) -> None:
        mock_backend = MagicMock()
        mock_backend.refresh_cache.side_effect = OSError("pkcon not found")
        config = _make_config(auto_refresh=True, show_notifications=True)

        with (
            patch("hyprdiscover.services.background.PackageKitBackend",
                  return_value=mock_backend),
            patch("hyprdiscover.services.background.load_config",
                  return_value=config),
            patch("sys.stderr", new_callable=io.StringIO) as fake_stderr,
        ):
            exit_code = run_background_check()

        assert exit_code == 1
        assert "Unable to check" in fake_stderr.getvalue()
