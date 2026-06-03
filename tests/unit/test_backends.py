from __future__ import annotations

from unittest.mock import patch

from hyprdiscover.backends.packagekit import PackageKitBackend
from hyprdiscover.models.package import Package


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
        with patch("hyprdiscover.backends.packagekit.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Updated\tsuccess"
            mock_run.return_value.stderr = ""
            result = backend.install_updates(packages=None)
        assert result.success
        mock_run.assert_called_once_with(
            ["pkcon", "update", "-y"],
            capture_output=True, text=True, check=False,
        )

    def test_install_selected_packages(self) -> None:
        backend = PackageKitBackend()
        pkg_a = Package(name="firefox", package_id="firefox-131.0.x86_64")
        pkg_b = Package(name="vim", package_id="vim-9.2.x86_64")
        with patch("hyprdiscover.backends.packagekit.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Updated\tfirefox\nUpdated\tvim"
            mock_run.return_value.stderr = ""
            result = backend.install_updates(packages=[pkg_a, pkg_b])
        assert result.success
        mock_run.assert_called_once_with(
            ["pkcon", "update", "firefox", "vim", "-y"],
            capture_output=True, text=True, check=False,
        )
