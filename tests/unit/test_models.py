from __future__ import annotations

from hyprdiscover.models.enums import UpdateCategory
from hyprdiscover.models.package import Package


class TestPackage:
    def test_creation(self) -> None:
        pkg = Package(
            name="firefox",
            package_id="firefox;131.0;x86_64;fedora",
            version_installed="130.0",
            version_available="131.0",
            category=UpdateCategory.SECURITY,
            summary="Mozilla Firefox Web browser",
        )
        assert pkg.name == "firefox"
        assert pkg.category == UpdateCategory.SECURITY
        assert pkg.display_name == "firefox"

    def test_display_name_truncation(self) -> None:
        pkg = Package(
            name="firefox;131.0;x86_64;fedora",
            package_id="firefox;131.0;x86_64;fedora",
            category=UpdateCategory.ENHANCEMENT,
        )
        assert pkg.display_name == "firefox"

    def test_defaults(self) -> None:
        pkg = Package(name="test", package_id="test")
        assert pkg.category == UpdateCategory.UNKNOWN
        assert pkg.size == 0
        assert pkg.summary == ""
