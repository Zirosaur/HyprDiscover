from __future__ import annotations

import logging
import subprocess

log = logging.getLogger(__name__)


def reboot_system() -> None:
    """Request a system reboot via systemctl.

    The user must have Polkit authorization (hyprpolkitagent or similar).
    This calls systemctl reboot which triggers the polkit agent.
    """
    log.info("Requesting system reboot")
    subprocess.run(
        ["systemctl", "reboot"],
        check=False,
        timeout=30,
    )


def can_reboot() -> bool:
    """Check if the user appears to have authorization to reboot."""
    result = subprocess.run(
        ["systemctl", "reboot", "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
    )
    return result.returncode == 0
