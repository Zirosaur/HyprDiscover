from __future__ import annotations

from enum import StrEnum


class UpdateCategory(StrEnum):
    SECURITY = "security"
    BUGFIX = "bugfix"
    ENHANCEMENT = "enhancement"
    UNKNOWN = "unknown"
    BLOCKED = "blocked"


class BackendType(StrEnum):
    PACKAGEKIT = "packagekit"
    FLATPAK = "flatpak"
    DNF5 = "dnf5"


class UpdateStatus(StrEnum):
    CHECKING = "checking"
    UP_TO_DATE = "up_to_date"
    UPDATES_AVAILABLE = "updates_available"
    UPDATING = "updating"
    SUCCESS = "success"
    FAILED = "failed"
    REBOOT_REQUIRED = "reboot_required"
    CANCELLED = "cancelled"
    ERROR = "error"


class PackageStatus(StrEnum):
    INSTALLED = "installed"
    AVAILABLE = "available"
    UPDATING = "updating"
    INSTALLING = "installing"
    REMOVING = "removing"


class ErrorType(StrEnum):
    NETWORK = "network"
    AUTH = "auth"
    LOCK = "lock"
    CONFLICT = "conflict"
    INTERNAL = "internal"
