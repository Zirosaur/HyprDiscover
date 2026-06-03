from __future__ import annotations

import logging
import sys

from hyprdiscover.backends.packagekit import PackageKitBackend
from hyprdiscover.config import load_config
from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.services.notifications import NotificationService
from hyprdiscover.services.update_manager import UpdateManager

log = logging.getLogger(__name__)


def run_background_check() -> int:
    config = load_config()

    if not config.auto_refresh:
        return 0

    backend = PackageKitBackend()
    updater = UpdateManager(backend)
    updater.refresh()

    if updater.status == UpdateStatus.ERROR:
        print("Error: Unable to check for updates", file=sys.stderr)
        return 1

    count = updater.update_count

    if count > 0 and config.show_notifications:
        notifier = NotificationService()
        notifier.updates_available(count)

    log.info("Background check: %d updates available", count)
    return 0
