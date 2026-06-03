from __future__ import annotations

import io
import json
from unittest.mock import MagicMock, patch

from hyprdiscover.services.cli_status import (
    format_status_json,
    format_status_text,
    run_status,
)


class TestFormatStatusText:
    def test_with_updates(self) -> None:
        result = format_status_text(12, 2, 5, 3, 2, "2026-06-03 12:45")

        assert "Updates available: 12" in result
        assert "Security: 2" in result
        assert "Bug Fix: 5" in result
        assert "Enhancement: 3" in result
        assert "Other: 2" in result
        assert "Last checked: 2026-06-03 12:45" in result
        lines = result.split("\n")
        assert lines[1] == ""

    def test_up_to_date(self) -> None:
        result = format_status_text(0, 0, 0, 0, 0, "2026-06-03 12:45")

        assert result.startswith("System up to date")
        assert "Updates available" not in result
        assert "Last checked: 2026-06-03 12:45" in result

    def test_no_last_checked(self) -> None:
        result = format_status_text(5, 1, 2, 1, 1, None)

        assert "Updates available: 5" in result
        assert "Last checked" not in result

    def test_up_to_date_no_timestamp(self) -> None:
        result = format_status_text(0, 0, 0, 0, 0, None)

        assert result == "System up to date"


class TestFormatStatusJson:
    def test_with_updates(self) -> None:
        result = format_status_json(12, 2, 5, 3, 2, "2026-06-03T12:45:00")

        data = json.loads(result)
        assert data["up_to_date"] is False
        assert data["updates_available"] == 12
        assert data["security"] == 2
        assert data["bugfix"] == 5
        assert data["enhancement"] == 3
        assert data["other"] == 2
        assert data["last_checked"] == "2026-06-03T12:45:00"

    def test_up_to_date(self) -> None:
        result = format_status_json(0, 0, 0, 0, 0, "2026-06-03T12:45:00")

        data = json.loads(result)
        assert data["up_to_date"] is True
        assert data["updates_available"] == 0

    def test_no_last_checked(self) -> None:
        result = format_status_json(3, 1, 1, 0, 1, None)

        data = json.loads(result)
        assert data["last_checked"] is None

    def test_valid_json_utf8(self) -> None:
        result = format_status_json(0, 0, 0, 0, 0, None)

        data = json.loads(result)
        assert isinstance(data, dict)
        assert "up_to_date" in data


class TestRunStatus:
    def test_returns_zero_when_up_to_date(self) -> None:
        mock_backend = MagicMock()
        mock_backend.get_updates.return_value = []
        mock_backend.refresh_cache.return_value = None

        with patch(
            "hyprdiscover.services.cli_status.PackageKitBackend",
            return_value=mock_backend,
        ), patch("sys.stdout", new_callable=io.StringIO) as fake_stdout:
            exit_code = run_status()

        assert exit_code == 0
        assert "System up to date" in fake_stdout.getvalue()

    def test_returns_zero_with_updates(self) -> None:
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

        with patch(
            "hyprdiscover.services.cli_status.PackageKitBackend",
            return_value=mock_backend,
        ), patch("sys.stdout", new_callable=io.StringIO) as fake_stdout:
            exit_code = run_status()

        assert exit_code == 0
        assert "Updates available: 3" in fake_stdout.getvalue()

    def test_returns_one_on_error(self) -> None:
        mock_backend = MagicMock()
        mock_backend.refresh_cache.side_effect = OSError("pkcon not found")

        with patch(
            "hyprdiscover.services.cli_status.PackageKitBackend",
            return_value=mock_backend,
        ), patch("sys.stdout", new_callable=io.StringIO), patch(
            "sys.stderr", new_callable=io.StringIO
        ) as fake_stderr:
            exit_code = run_status()

        assert exit_code == 1
        assert "Unable to check" in fake_stderr.getvalue()

    def test_json_output_flag(self) -> None:
        mock_backend = MagicMock()
        mock_backend.get_updates.return_value = []
        mock_backend.refresh_cache.return_value = None

        with patch(
            "hyprdiscover.services.cli_status.PackageKitBackend",
            return_value=mock_backend,
        ), patch("sys.stdout", new_callable=io.StringIO) as fake_stdout:
            exit_code = run_status(json_output=True)

        assert exit_code == 0
        data = json.loads(fake_stdout.getvalue())
        assert data["up_to_date"] is True
        assert data["updates_available"] == 0

    def test_json_with_updates(self) -> None:
        mock_backend = MagicMock()
        mock_backend.refresh_cache.return_value = None
        from hyprdiscover.models.package import Package

        pkg = Package(
            name="kernel",
            package_id="kernel-6.11.0.x86_64",
            version_available="6.11.0-1.fc40",
            category="security",
        )
        mock_backend.get_updates.return_value = [pkg, pkg]

        with patch(
            "hyprdiscover.services.cli_status.PackageKitBackend",
            return_value=mock_backend,
        ), patch("sys.stdout", new_callable=io.StringIO) as fake_stdout:
            exit_code = run_status(json_output=True)

        assert exit_code == 0
        data = json.loads(fake_stdout.getvalue())
        assert data["up_to_date"] is False
        assert data["updates_available"] == 2
        assert data["security"] == 2
        assert "last_checked" in data
        assert data["last_checked"] is not None
        assert "T" in data["last_checked"]
