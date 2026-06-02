from __future__ import annotations

from hyprdiscover.models.enums import UpdateCategory


class TestEnums:
    def test_update_category_values(self) -> None:
        assert UpdateCategory.SECURITY.value == "security"
        assert UpdateCategory.BUGFIX.value == "bugfix"
        assert UpdateCategory.ENHANCEMENT.value == "enhancement"
        assert UpdateCategory.UNKNOWN.value == "unknown"

    def test_update_status_values(self) -> None:
        from hyprdiscover.models.enums import UpdateStatus
        assert UpdateStatus.CHECKING.value == "checking"
        assert UpdateStatus.SUCCESS.value == "success"

    def test_str_behavior(self) -> None:
        cat = UpdateCategory.SECURITY
        assert str(cat) == "security"
        assert cat == "security"
