from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from hyprdiscover.__main__ import main


class TestMainRouting:
    def test_waybar_flag(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "--waybar"]),
            patch("hyprdiscover.__main__.run_waybar") as mock_waybar,
        ):
            main()
        mock_waybar.assert_called_once()

    def test_waybar_short_flag(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "-w"]),
            patch("hyprdiscover.__main__.run_waybar") as mock_waybar,
        ):
            main()
        mock_waybar.assert_called_once()

    def test_status_text(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "--status"]),
            patch("hyprdiscover.__main__.run_status") as mock_status,
            pytest.raises(SystemExit),
        ):
            main()
        mock_status.assert_called_once_with(json_output=False)

    def test_status_short_flag(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "-s"]),
            patch("hyprdiscover.__main__.run_status") as mock_status,
            pytest.raises(SystemExit),
        ):
            main()
        mock_status.assert_called_once_with(json_output=False)

    def test_status_json(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "--status", "--json"]),
            patch("hyprdiscover.__main__.run_status") as mock_status,
            pytest.raises(SystemExit),
        ):
            main()
        mock_status.assert_called_once_with(json_output=True)

    def test_launches_gtk_when_no_flags(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover"]),
            patch(
                "hyprdiscover.__main__.HyprDiscoverApplication"
            ) as mock_app_class,
            pytest.raises(SystemExit),
        ):
            main()
        mock_app_class.assert_called_once()
        mock_app_class.return_value.run.assert_called_once()

    def test_help_exits_zero(self) -> None:
        with (
            patch.object(sys, "argv", ["hyprdiscover", "--help"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()
        assert exc_info.value.code == 0
