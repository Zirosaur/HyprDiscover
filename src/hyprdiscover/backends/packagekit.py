from __future__ import annotations

import logging
import re
import subprocess
from collections.abc import Callable

from hyprdiscover.backends.base import PackageManagerBackend
from hyprdiscover.models.enums import UpdateCategory
from hyprdiscover.models.package import (
    BackendInfo,
    Package,
    PackageDetail,
    UpdateProgress,
    UpdateResult,
)

log = logging.getLogger(__name__)

# NOTE: This backend uses `pkcon` subprocess calls as an interim solution.
# The target architecture (v0.6) replaces this with native D-Bus via
# gi.repository.PackageKitGlib.

_NEVRA_RE = re.compile(
    r"^(.+)-((\d+:)?\d[\w.+]*?-[\w.+~]+)\.(\w+)$"
)

_CATEGORY_NAMES: dict[str, UpdateCategory] = {
    "Security": UpdateCategory.SECURITY,
    "Bug fix": UpdateCategory.BUGFIX,
    "Bugfix": UpdateCategory.BUGFIX,
    "Bug": UpdateCategory.BUGFIX,
    "Enhancement": UpdateCategory.ENHANCEMENT,
    "Blocked": UpdateCategory.BLOCKED,
    "Available": UpdateCategory.UNKNOWN,
    "Unknown": UpdateCategory.UNKNOWN,
}


def _parse_nevra(nevra: str) -> tuple[str, str]:
    """Parse RPM NEVRA string into (name, version).

    Handles both NEVRA format (name-ver-rel.arch) and PackageKit
    ID format (name;ver;arch;repo).
    """
    if ";" in nevra:
        parts = nevra.split(";")
        return parts[0], parts[1] if len(parts) > 1 else ""

    m = _NEVRA_RE.match(nevra)
    if m:
        return m.group(1), m.group(2)

    return nevra, ""


class PackageKitBackend(PackageManagerBackend):
    """PackageKit backend using pkcon subprocess (interim implementation)."""

    def __init__(self) -> None:
        self._cancelled = False

    def get_backend_info(self) -> BackendInfo:
        return BackendInfo(
            backend_type="packagekit",
            name="PackageKit (pkcon)",
            available=True,
        )

    def refresh_cache(self, force: bool = False) -> None:
        subprocess.run(
            ["pkcon", "refresh", "force"] if force else ["pkcon", "refresh"],
            capture_output=True,
            text=True,
            env={"LANG": "C"},
            check=False,
        )

    def get_updates(self) -> list[Package]:
        result = subprocess.run(
            ["pkcon", "get-updates"],
            capture_output=True,
            text=True,
            env={"LANG": "C"},
            check=False,
        )
        return self._parse_update_list(result.stdout)

    def get_update_count(self) -> int:
        return len(self.get_updates())

    def install_updates(
        self,
        packages: list[Package] | None = None,
        progress_callback: Callable[[UpdateProgress], None] | None = None,
    ) -> UpdateResult:
        self._cancelled = False

        if packages:
            cmd = ["pkcon", "update"] + [p.name for p in packages] + ["-y"]
        else:
            cmd = ["pkcon", "update", "-y"]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout + result.stderr

        if progress_callback:
            progress_callback(UpdateProgress(
                status="finished",
                percentage=100,
                message="Update transaction complete",
            ))

        no_updates_markers = (
            "No packages",
            "There are no updates",
            "Tak ada paket",
            "Tidak ada paket",
            "Keine Pakete",
            "Nessun pacchetto",
        )
        if any(m in output for m in no_updates_markers):
            return UpdateResult(success=True, message=output, packages_updated=0)

        if result.returncode == 0:
            return UpdateResult(
                success=True,
                message=output,
                packages_updated=_count_updated_packages(output),
            )

        return UpdateResult(
            success=False,
            message=output,
            error_code=result.returncode,
        )

    def search_packages(self, query: str) -> list[PackageDetail]:
        return []

    def get_package_details(self, package_id: str) -> PackageDetail | None:
        return None

    def cancel(self) -> None:
        self._cancelled = True

    def prepare_offline_update(self) -> None:
        subprocess.run(
            ["pkcon", "update", "prepare"],
            capture_output=True,
            text=True,
            check=False,
        )

    def get_reboot_required(self) -> bool:
        result = subprocess.run(
            ["pkcon", "get-distro-upgrades"],
            capture_output=True,
            text=True,
            env={"LANG": "C"},
            check=False,
        )
        return "RebootRequired" in (result.stdout + result.stderr)

    def _parse_update_list(self, output: str) -> list[Package]:
        packages: list[Package] = []

        _STATUS_PREFIXES = {
            "Transaction",
            "Status",
            "Results",
            "Getting",
            "Waiting",
            "Starting",
            "Finished",
            "Loading",
            "Downloading",
            "Resolving",
            "Testing",
            "Running",
            "Querying",
            "Refreshing",
        }

        for line in output.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            first_word = stripped.split(None, 1)[0].rstrip(":")
            if first_word in _STATUS_PREFIXES:
                continue

            matched = False
            category = UpdateCategory.UNKNOWN
            rest = ""

            for label, cat in _CATEGORY_NAMES.items():
                if stripped.startswith(label) and (
                    len(stripped) == len(label)
                    or stripped[len(label)] in (" ", "\t")
                ):
                    category = cat
                    rest = stripped[len(label):].strip()
                    matched = True
                    break

            if not matched:
                if ":" in first_word:
                    continue
                parts = stripped.split(None, 2)
                if len(parts) < 2:
                    continue
                category = UpdateCategory.UNKNOWN
                rest = " ".join(parts[1:])

            nevra = rest.split(None, 1)[0] if rest else ""
            if not nevra or not any(c.isdigit() for c in nevra):
                continue

            pkg_name, version = _parse_nevra(nevra)
            if not pkg_name:
                continue

            pkg = Package(
                name=pkg_name,
                package_id=nevra,
                version_available=version,
                category=category,
            )
            packages.append(pkg)

        log.debug("Parsed %d packages from update list", len(packages))
        return packages


def _count_updated_packages(output: str) -> int:
    count = 0
    for line in output.splitlines():
        stripped = line.strip()
        if any(
            stripped.startswith(prefix)
            for prefix in ("Installing", "Updating", "Removing", "Installed", "Updated")
        ):
            count += 1
    return count
