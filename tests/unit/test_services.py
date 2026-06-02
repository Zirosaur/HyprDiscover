from __future__ import annotations

from unittest.mock import MagicMock

from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.models.package import Package, UpdateResult
from hyprdiscover.services.update_manager import UpdateManager


class TestUpdateManager:
    def test_initial_state(self) -> None:
        backend = MagicMock()
        backend.get_updates.return_value = []
        backend.get_update_count.return_value = 0
        mgr = UpdateManager(backend)
        assert mgr.status == UpdateStatus.UP_TO_DATE
        assert mgr.update_count == 0
        assert mgr.last_checked is None

    def test_refresh_no_updates(self) -> None:
        backend = MagicMock()
        backend.get_updates.return_value = []
        mgr = UpdateManager(backend)
        mgr.refresh()
        assert mgr.status == UpdateStatus.UP_TO_DATE
        assert mgr.update_count == 0
        assert mgr.last_checked is not None

    def test_refresh_with_updates(self) -> None:
        backend = MagicMock()
        pkg = MagicMock(spec=Package)
        pkg.category.value = "bugfix"
        backend.get_updates.return_value = [pkg, pkg]
        mgr = UpdateManager(backend)
        mgr.refresh()
        assert mgr.status == UpdateStatus.UPDATES_AVAILABLE
        assert mgr.update_count == 2
        assert mgr.security_count == 0

    def test_install_success(self) -> None:
        backend = MagicMock()
        backend.install_updates.return_value = UpdateResult(
            success=True,
            message="done",
            packages_updated=2,
        )
        backend.get_updates.return_value = []
        mgr = UpdateManager(backend)
        result = mgr.install_updates()
        assert result.success
        assert mgr.status == UpdateStatus.SUCCESS

    def test_install_failure(self) -> None:
        backend = MagicMock()
        backend.install_updates.return_value = UpdateResult(
            success=False,
            message="error",
            error_code=1,
        )
        backend.get_updates.return_value = []
        mgr = UpdateManager(backend)
        result = mgr.install_updates()
        assert not result.success
        assert mgr.status == UpdateStatus.FAILED

    def test_status_callback_fires(self) -> None:
        backend = MagicMock()
        backend.get_updates.return_value = []
        mgr = UpdateManager(backend)

        statuses: list[UpdateStatus] = []
        mgr.set_status_callback(lambda s: statuses.append(s))
        mgr.refresh()
        assert UpdateStatus.CHECKING in statuses
        assert UpdateStatus.UP_TO_DATE in statuses
