from __future__ import annotations

import logging
import os
import re
import subprocess
from collections.abc import Callable

from hyprdiscover.backends.base import PackageManagerBackend
from hyprdiscover.models.enums import ErrorType, UpdateCategory
from hyprdiscover.models.package import (
    BackendInfo,
    Package,
    PackageDetail,
    UpdateError,
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

_REPO_RE = re.compile(r"\s*\(([^)]+)\)\s*$")

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


def _parse_nevra(nevra: str) -> tuple[str, str, str]:
    """Parse RPM NEVRA string into (name, version, arch).

    Handles both NEVRA format (name-ver-rel.arch) and PackageKit
    ID format (name;ver;arch;repo).
    """
    if ";" in nevra:
        parts = nevra.split(";")
        name = parts[0]
        version = parts[1] if len(parts) > 1 else ""
        arch = parts[2] if len(parts) > 2 else ""
        return name, version, arch

    m = _NEVRA_RE.match(nevra)
    if m:
        return m.group(1), m.group(2), m.group(4)

    return nevra, "", ""


def _parse_progress_line(line: str) -> UpdateProgress | None:
    """Parse a single pkcon output line into an UpdateProgress event.

    Recognised prefixes (LANG=C):

        Status:      → update_progress.status
        Package:     → update_progress.message (NEVRA)
        Percentage:  → update_progress.percentage (0-100)

    Returns None when the line does not carry progress information.
    """
    if not line or ":" not in line:
        return None

    key, _, value = line.partition("\t")
    key = key.strip().rstrip(":")
    value = value.strip()

    if key == "Status":
        return UpdateProgress(status=value)
    if key == "Package":
        return UpdateProgress(message=value)
    if key == "Percentage":
        try:
            return UpdateProgress(percentage=int(value))
        except ValueError:
            return None

    return None


_NO_UPDATES_MARKERS = (
    "No packages",
    "There are no updates",
    "Tak ada paket",
    "Tidak ada paket",
    "Keine Pakete",
    "Nessun pacchetto",
)


def _classify_error(returncode: int, output: str) -> UpdateError:
    if any(m in output for m in (
        "Could not connect",
        "Cannot connect",
        "Network",
        "resolve host",
        "timeout",
    )):
        return UpdateError(
            type=ErrorType.NETWORK,
            summary="Network unavailable",
            detail="PackageKit could not reach the repository",
            recoverable=True,
            raw_output=output,
        )

    if any(m in output for m in (
        "auth", "permission", "not authorized",
        "Authentication", "Authorisation",
    )):
        return UpdateError(
            type=ErrorType.AUTH,
            summary="Permission denied",
            detail="Administrative authorization is required",
            recoverable=True,
            raw_output=output,
        )

    if any(m in output for m in (
        "another transaction",
        "lock",
        "already running",
    )):
        return UpdateError(
            type=ErrorType.LOCK,
            summary="Another update is in progress",
            detail="Only one PackageKit transaction can run at a time",
            recoverable=True,
            raw_output=output,
        )

    if any(m in output for m in (
        "conflict", "dependency", "unresolved",
        "broken", "requires",
    )):
        return UpdateError(
            type=ErrorType.CONFLICT,
            summary="Package conflict detected",
            detail="Dependencies could not be resolved",
            recoverable=False,
            raw_output=output,
        )

    return UpdateError(
        type=ErrorType.INTERNAL,
        summary="Unexpected error",
        detail=f"pkcon exited with code {returncode}",
        recoverable=False,
        raw_output=output,
    )


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
        result = subprocess.run(
            ["pkcon", "refresh", "force"] if force else ["pkcon", "refresh"],
            capture_output=True,
            text=True,
            env={"LANG": "C"},
            check=False,
        )
        if result.returncode != 0:
            error = _classify_error(result.returncode, result.stdout + result.stderr)
            log.warning("Cache refresh failed: [%s] %s", error.type, error.summary)

    def get_updates(self) -> list[Package]:
        result = subprocess.run(
            ["pkcon", "get-updates"],
            capture_output=True,
            text=True,
            env={"LANG": "C"},
            check=False,
        )
        output = result.stdout + result.stderr
        if result.returncode != 0:
            if any(m in output for m in _NO_UPDATES_MARKERS):
                return []
            error = _classify_error(result.returncode, output)
            log.warning("Update check failed: [%s] %s", error.type, error.summary)
            return []
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
            pkg_ids = [f"{p.name};{p.version_available};{p.arch};{p.repo}" for p in packages]
            cmd = ["pkcon", "update"] + pkg_ids + ["-y"]
        else:
            cmd = ["pkcon", "update", "-y"]

        env = os.environ.copy()
        env["LANG"] = "C"

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )

        output_lines: list[str] = []
        for line in process.stdout:
            line = line.rstrip("\n")
            output_lines.append(line)

            if self._cancelled:
                process.terminate()
                break

            if progress_callback:
                ev = _parse_progress_line(line)
                if ev is not None:
                    progress_callback(ev)

        process.wait(timeout=30)
        output = "\n".join(output_lines)

        if self._cancelled:
            return UpdateResult(success=False, message=output, cancelled=True)

        if any(m in output for m in _NO_UPDATES_MARKERS):
            return UpdateResult(success=True, message=output, packages_updated=0)

        if process.returncode == 0:
            return UpdateResult(
                success=True,
                message=output,
                packages_updated=_count_updated_packages(output),
            )

        return UpdateResult(
            success=False,
            message=output,
            error_code=process.returncode,
            error=_classify_error(process.returncode, output),
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

        _status_prefixes = {
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
            if first_word in _status_prefixes:
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

            pkg_name, version, arch = _parse_nevra(nevra)
            if not pkg_name:
                continue

            repo_match = _REPO_RE.search(rest)
            repo = repo_match.group(1) if repo_match else ""

            pkg = Package(
                name=pkg_name,
                package_id=nevra,
                version_available=version,
                category=category,
                arch=arch,
                repo=repo,
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
