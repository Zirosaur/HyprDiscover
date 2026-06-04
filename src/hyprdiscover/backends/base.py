from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from hyprdiscover.models.package import (
    BackendInfo,
    Package,
    PackageDetail,
    UpdateProgress,
    UpdateResult,
)


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
        packages: list[Package] | None = None,
        progress_callback: Callable[[UpdateProgress], None] | None = None,
    ) -> UpdateResult:
        ...

    @abstractmethod
    def search_packages(self, query: str) -> list[PackageDetail]:
        ...

    @abstractmethod
    def get_package_details(self, package_id: str) -> PackageDetail | None:
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
