from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional

from hyprdiscover.models.package import (
    BackendInfo,
    PackageDetail,
    UpdateProgress,
    UpdateResult,
)
from hyprdiscover.models.package import Package


class PackageManagerBackend(ABC):
    """Abstract backend for package management operations.

    All backends (PackageKit, Flatpak, DNF5) implement this interface.
    The service layer never imports concrete backends directly.
    """

    @abstractmethod
    def get_backend_info(self) -> BackendInfo:
        ...

    @abstractmethod
    def refresh_cache(self, force: bool = False) -> None:
        ...

    @abstractmethod
    def get_updates(self) -> list[Package]:
        ...

    @abstractmethod
    def get_update_count(self) -> int:
        ...

    @abstractmethod
    def install_updates(
        self,
        packages: Optional[list[Package]] = None,
        progress_callback: Optional[Callable[[UpdateProgress], None]] = None,
    ) -> UpdateResult:
        ...

    @abstractmethod
    def search_packages(self, query: str) -> list[PackageDetail]:
        ...

    @abstractmethod
    def get_package_details(self, package_id: str) -> Optional[PackageDetail]:
        ...

    @abstractmethod
    def cancel(self) -> None:
        ...

    @abstractmethod
    def prepare_offline_update(self) -> None:
        ...

    @abstractmethod
    def get_reboot_required(self) -> bool:
        ...
