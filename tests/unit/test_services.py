from __future__ import annotations

from unittest.mock import MagicMock

from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.models.package import Package, UpdateProgress, UpdateResult
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

    def test_progress_callback_forwards_from_backend(self) -> None:
        backend = MagicMock()
        mgr = UpdateManager(backend)

        captured: list[UpdateProgress] = []
        mgr.set_progress_callback(captured.append)

        pkg = MagicMock(spec=Package)

        def fake_install(packages=None, progress_callback=None):
            progress_callback(UpdateProgress(status="Downloading", message=""))
            progress_callback(UpdateProgress(percentage=42))
            progress_callback(UpdateProgress(message="firefox-131.0.x86_64"))
            return UpdateResult(success=True, message="ok")

        backend.install_updates.side_effect = fake_install
        backend.get_updates.return_value = []
        mgr.install_updates(packages=[pkg])

        assert len(captured) == 3
        assert captured[0].status == "Downloading"
        assert captured[1].percentage == 42
        assert captured[2].message == "firefox-131.0.x86_64"

    def test_cancelled_preserves_cancelled_status(self) -> None:
        backend = MagicMock()
        backend.install_updates.return_value = UpdateResult(
            success=False, message="terminated", cancelled=True,
        )
        backend.get_updates.return_value = []
        mgr = UpdateManager(backend)

        mgr.cancel()
        assert mgr.status == UpdateStatus.CANCELLED

        result = mgr.install_updates()
        assert result.cancelled is True
        assert mgr.status == UpdateStatus.CANCELLED
