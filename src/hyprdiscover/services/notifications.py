from __future__ import annotations

import logging
import subprocess

log = logging.getLogger(__name__)


class NotificationService:
    """Desktop notification dispatcher.

    Abstracted behind a class so the UI and CLI (Waybar) paths can
    share the same notification logic. Silently degrades if notify-send
    is not available.
    """

    def __init__(self, app_name: str = "HyprDiscover") -> None:
        self._app_name = app_name

    def send(self, title: str, message: str, urgency: str | None = None) -> None:
        args = ["notify-send", title, message, "-a", self._app_name]
        if urgency:
            args.extend(["-u", urgency])

        try:
            subprocess.run(args, check=False, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            log.debug("notify-send unavailable or timed out")

    def updates_available(self, count: int) -> None:
        self.send("HyprDiscover", f"{count} updates available")

    def update_success(self) -> None:
        self.send("HyprDiscover", "System updated successfully")

    def update_failed(self, detail: str = "") -> None:
        msg = "Update failed"
        if detail:
            msg += f": {detail}"
        self.send("HyprDiscover", msg, urgency="critical")

    def reboot_reminder(self) -> None:
        self.send("HyprDiscover", "A reboot is required to complete updates", urgency="normal")
