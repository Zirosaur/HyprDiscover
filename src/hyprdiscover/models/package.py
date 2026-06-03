from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from hyprdiscover.models.enums import PackageStatus, UpdateCategory


@dataclass
class Package:
    name: str
    package_id: str
    version_installed: str = ""
    version_available: str = ""
    size: int = 0
    category: UpdateCategory = UpdateCategory.UNKNOWN
    summary: str = ""
    source: str = ""
    arch: str = ""
    repo: str = ""

    @property
    def display_name(self) -> str:
        return self.name.split(";")[0] if ";" in self.name else self.name


@dataclass
class PackageDetail:
    package_id: str
    name: str
    summary: str = ""
    size: int = 0
    license: str = ""
    url: str = ""
    status: PackageStatus = PackageStatus.INSTALLED


@dataclass
class UpdateResult:
    success: bool
    message: str
    requires_reboot: bool = False
    packages_updated: int = 0
    error_code: Optional[int] = None
    cancelled: bool = False


@dataclass
class BackendInfo:
    backend_type: str
    name: str
    version: str = ""
    available: bool = True
    error: Optional[str] = None


@dataclass
class UpdateProgress:
    status: str = ""
    percentage: int = 0
    package: Optional[Package] = None
    message: str = ""
    elapsed: float = 0.0
    remaining: float = 0.0
