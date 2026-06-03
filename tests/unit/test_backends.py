from __future__ import annotations

import io
from unittest.mock import MagicMock, patch

from hyprdiscover.backends.packagekit import (
    PackageKitBackend,
    _parse_progress_line,
)
from hyprdiscover.models.package import Package, UpdateProgress


def _make_popen_mock(stdout_text: str, returncode: int = 0) -> MagicMock:
    stdout = io.StringIO(stdout_text)
    mock_proc = MagicMock()
    mock_proc.stdout = stdout
    mock_proc.returncode = returncode
    mock_proc.wait = MagicMock()
    mock_proc.terminate = MagicMock()
    return mock_proc


class TestParseProgressLine:
    def test_status_line(self) -> None:
        ev = _parse_progress_line("Status:\tDownloading packages")
        assert ev is not None
        assert ev.status == "Downloading packages"

    def test_package_line(self) -> None:
        ev = _parse_progress_line("Package:\tfirefox-131.0.x86_64")
        assert ev is not None
        assert ev.message == "firefox-131.0.x86_64"

    def test_percentage_line(self) -> None:
        ev = _parse_progress_line("Percentage:\t42")
        assert ev is not None
        assert ev.percentage == 42

    def test_unknown_line_returns_none(self) -> None:
        assert _parse_progress_line("Results:") is None
        assert _parse_progress_line("") is None
        assert _parse_progress_line("Some random text") is None


class TestPackageKitBackend:
    def test_get_backend_info(self) -> None:
        backend = PackageKitBackend()
        info = backend.get_backend_info()
        assert info.backend_type == "packagekit"
        assert info.name == "PackageKit (pkcon)"
        assert info.available is True

    def test_parse_empty_output(self) -> None:
        backend = PackageKitBackend()
        packages = backend._parse_update_list("")
        assert packages == []

    def test_parse_with_categories(self) -> None:
        backend = PackageKitBackend()
        output = (
            "Available\tfirefox-131.0.x86_64\t131.0-1.fc40\tBrowser\n"
            "Security\tkernel-6.11.0.x86_64\t6.11.0-1.fc40\tLinux Kernel\n"
            "Bugfix\tvim-9.2.x86_64\t9.2-1.fc40\tText editor\n"
            "Enhancement\tnautilus-47.0.x86_64\t47.0-1.fc40\tFile manager\n"
        )
        packages = backend._parse_update_list(output)
        assert len(packages) == 4
        assert packages[0].category.value == "unknown"
        assert packages[1].category.value == "security"
        assert packages[2].category.value == "bugfix"
        assert packages[3].category.value == "enhancement"

    def test_install_all_packages(self) -> None:
        backend = PackageKitBackend()
        mock_proc = _make_popen_mock("Status:\tRunning\nPercentage:\t100\nStatus:\tFinished\n")
        with patch("hyprdiscover.backends.packagekit.subprocess.Popen",
                   return_value=mock_proc) as mock_popen:
            result = backend.install_updates(packages=None)
        assert result.success
        call_args = mock_popen.call_args[0][0]
        assert call_args == ["pkcon", "update", "-y"]

    def test_install_selected_packages(self) -> None:
        backend = PackageKitBackend()
        pkg_a = Package(
            name="firefox", package_id="firefox-131.0.x86_64",
            version_available="131.0-1.fc40", arch="x86_64", repo="updates",
        )
        pkg_b = Package(
            name="vim", package_id="vim-9.2.x86_64",
            version_available="9.2-1.fc40", arch="x86_64", repo="updates",
        )
        mock_proc = _make_popen_mock("Status:\tRunning\n")
        with patch("hyprdiscover.backends.packagekit.subprocess.Popen",
                   return_value=mock_proc):
            result = backend.install_updates(packages=[pkg_a, pkg_b])
        assert result.success

    def test_install_streams_progress_callbacks(self) -> None:
        backend = PackageKitBackend()
        stdout_lines = (
            "Status:\tDownloading packages\n"
            "Package:\tfirefox-131.0.x86_64\n"
            "Percentage:\t50\n"
            "Percentage:\t100\n"
            "Status:\tFinished\n"
        )
        mock_proc = _make_popen_mock(stdout_lines)
        callbacks: list[UpdateProgress] = []

        with patch("hyprdiscover.backends.packagekit.subprocess.Popen",
                   return_value=mock_proc):
            backend.install_updates(progress_callback=callbacks.append)

        assert len(callbacks) == 5
        assert callbacks[0].status == "Downloading packages"
        assert callbacks[1].message == "firefox-131.0.x86_64"
        assert callbacks[2].percentage == 50
        assert callbacks[3].percentage == 100
        assert callbacks[4].status == "Finished"

    def test_install_cancelled_terminates_process(self) -> None:
        backend = PackageKitBackend()
        stdout_lines = (
            "Status:\tDownloading packages\n"
            "Percentage:\t10\n"
        )
        mock_proc = _make_popen_mock(stdout_lines)

        def check_cancel(*_args: object) -> None:
            backend._cancelled = True

        with patch("hyprdiscover.backends.packagekit.subprocess.Popen",
                   return_value=mock_proc):
            result = backend.install_updates(progress_callback=check_cancel)

        mock_proc.terminate.assert_called_once()
        assert result.cancelled is True
        assert result.success is False

    def test_install_failure_returncode(self) -> None:
        backend = PackageKitBackend()
        mock_proc = _make_popen_mock("Error\n", returncode=1)
        with patch("hyprdiscover.backends.packagekit.subprocess.Popen",
                   return_value=mock_proc):
            result = backend.install_updates()
        assert not result.success
        assert result.error_code == 1
