from __future__ import annotations

import json
import sys
from datetime import datetime

from hyprdiscover.backends.packagekit import PackageKitBackend
from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.services.update_manager import UpdateManager


def format_status_text(
    count: int,
    security: int,
    bugfix: int,
    enhancement: int,
    other: int,
    last_checked: str | None,
) -> str:
    if count == 0:
        lines = ["System up to date"]
    else:
        lines = [
            f"Updates available: {count}",
            "",
            f"Security: {security}",
            f"Bug Fix: {bugfix}",
            f"Enhancement: {enhancement}",
            f"Other: {other}",
        ]

    if last_checked:
        lines.append("")
        lines.append(f"Last checked: {last_checked}")

    return "\n".join(lines)


def format_status_json(
    count: int,
    security: int,
    bugfix: int,
    enhancement: int,
    other: int,
    last_checked: str | None,
) -> str:
    payload: dict[str, object] = {
        "up_to_date": count == 0,
        "updates_available": count,
        "security": security,
        "bugfix": bugfix,
        "enhancement": enhancement,
        "other": other,
        "last_checked": last_checked,
    }
    return json.dumps(payload, ensure_ascii=False)


def _last_checked_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def _last_checked_human(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def run_status(json_output: bool = False) -> int:
    backend = PackageKitBackend()
    updater = UpdateManager(backend)
    updater.refresh()

    if updater.status == UpdateStatus.ERROR:
        print("Error: Unable to check for updates", file=sys.stderr)
        return 1

    last_checked_str: str | None = None
    if updater.last_checked:
        if json_output:
            last_checked_str = _last_checked_iso(updater.last_checked)
        else:
            last_checked_str = _last_checked_human(updater.last_checked)

    count = updater.update_count
    security = updater.security_count
    bugfix = updater.bugfix_count
    enhancement = updater.enhancement_count
    other = updater.other_count

    if json_output:
        output = format_status_json(count, security, bugfix, enhancement, other, last_checked_str)
    else:
        output = format_status_text(count, security, bugfix, enhancement, other, last_checked_str)

    print(output, file=sys.stdout)
    return 0
