from __future__ import annotations

from hyprdiscover.backends.packagekit import PackageKitBackend


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
