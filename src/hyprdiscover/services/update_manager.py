from __future__ import annotations

import logging
import threading
from datetime import datetime
from typing import Callable, Optional

from hyprdiscover.backends.base import PackageManagerBackend
from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.models.package import Package, UpdateProgress, UpdateResult

log = logging.getLogger(__name__)


class UpdateManager:
    """Orchestrates package update operations across backends.

    Owns the update lifecycle state machine. The UI layer observes this
    service through callbacks rather than calling backends directly.
    """

    def __init__(self, backend: PackageManagerBackend) -> None:
        self._backend = backend
        self._status = UpdateStatus.UP_TO_DATE
        self._packages: list[Package] = []
        self._last_checked: Optional[datetime] = None
        self._lock = threading.Lock()

        self._on_status_changed: Optional[Callable[[UpdateStatus], None]] = None
        self._on_progress: Optional[Callable[[UpdateProgress], None]] = None

    @property
    def status(self) -> UpdateStatus:
        return self._status

    @property
    def packages(self) -> list[Package]:
        return list(self._packages)

    @property
    def update_count(self) -> int:
        return len(self._packages)

    @property
    def security_count(self) -> int:
        return sum(1 for p in self._packages if p.category == "security")

    @property
    def bugfix_count(self) -> int:
        return sum(1 for p in self._packages if p.category == "bugfix")

    @property
    def enhancement_count(self) -> int:
        return sum(1 for p in self._packages if p.category == "enhancement")

    @property
    def other_count(self) -> int:
        excluded = {"security", "bugfix", "enhancement", "blocked"}
        return sum(1 for p in self._packages if p.category not in excluded)

    @property
    def blocked_count(self) -> int:
        return sum(1 for p in self._packages if p.category == "blocked")

    @property
    def total_download_size(self) -> int:
        return sum(p.size for p in self._packages)

    @property
    def last_checked(self) -> Optional[datetime]:
        return self._last_checked

    @property
    def backend(self) -> PackageManagerBackend:
        return self._backend

    def set_status_callback(self, callback: Optional[Callable[[UpdateStatus], None]]) -> None:
        self._on_status_changed = callback

    def set_progress_callback(self, callback: Optional[Callable[[UpdateProgress], None]]) -> None:
        self._on_progress = callback

    def refresh(self) -> None:
        self._set_status(UpdateStatus.CHECKING)
        log.info("Refreshing update cache")

        try:
            self._backend.refresh_cache()
            self._packages = self._backend.get_updates()
            self._last_checked = datetime.now()

            if self._packages:
                log.info("Found %d updates (%d security)", len(self._packages), self.security_count)
                self._set_status(UpdateStatus.UPDATES_AVAILABLE)
            else:
                log.info("System is up to date")
                self._set_status(UpdateStatus.UP_TO_DATE)

        except Exception:
            log.exception("Failed to refresh updates")
            self._packages = []
            self._set_status(UpdateStatus.ERROR)

    def install_updates(
        self,
        packages: Optional[list[Package]] = None,
    ) -> UpdateResult:
        self._set_status(UpdateStatus.UPDATING)
        log.info("Starting update installation")

        try:
            result = self._backend.install_updates(
                packages=packages,
                progress_callback=self._on_progress,
            )

            if result.success:
                if result.requires_reboot:
                    self._set_status(UpdateStatus.REBOOT_REQUIRED)
                else:
                    self._set_status(UpdateStatus.SUCCESS)
                log.info("Updates installed successfully: %d packages", result.packages_updated)
            else:
                self._set_status(UpdateStatus.FAILED)
                log.warning("Update failed: %s", result.message[:200])

            return result

        except Exception:
            log.exception("Update installation crashed")
            self._set_status(UpdateStatus.ERROR)
            return UpdateResult(success=False, message="Internal error during update")

    def cancel(self) -> None:
        log.info("Cancelling update operation")
        self._backend.cancel()
        self._set_status(UpdateStatus.CANCELLED)

    def _set_status(self, status: UpdateStatus) -> None:
        with self._lock:
            old = self._status
            self._status = status
        if old != status and self._on_status_changed:
            self._on_status_changed(status)

    def get_update_log(self) -> str:
        if not self._packages:
            return "No updates available."
        lines = []
        for pkg in self._packages:
            lines.append(
                f"{pkg.category.value:>12}  {pkg.display_name:<40}  {pkg.version_available}"
            )
        return "\n".join(lines)
