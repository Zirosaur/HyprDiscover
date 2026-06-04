from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from hyprdiscover.models.enums import UpdateStatus

_CLASS_MAP = {
    UpdateStatus.CHECKING: ("checking-label", "Checking for updates..."),
    UpdateStatus.UP_TO_DATE: ("success-label", "System is up to date"),
    UpdateStatus.UPDATES_AVAILABLE: ("warning-label", ""),
    UpdateStatus.UPDATING: ("progress-label", "Updating packages..."),
    UpdateStatus.SUCCESS: ("success-label", "Updates installed successfully"),
    UpdateStatus.FAILED: ("error-label", "Update failed"),
    UpdateStatus.REBOOT_REQUIRED: ("success-label", "Updates installed — reboot required"),
    UpdateStatus.CANCELLED: ("dim-label", "Cancelled"),
    UpdateStatus.ERROR: ("error-label", "An error occurred"),
}


class StatusHeader(Gtk.Box):
    """Status display with icon label and optional timestamp."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        self._status_label = Gtk.Label(label="Ready")
        self._status_label.add_css_class("title-3")

        self._timestamp_label = Gtk.Label(label="Last checked: Never")
        self._timestamp_label.add_css_class("caption")

        self.append(self._status_label)
        self.append(self._timestamp_label)

    @property
    def status_label(self) -> Gtk.Label:
        return self._status_label

    @property
    def timestamp_label(self) -> Gtk.Label:
        return self._timestamp_label

    def set_status(self, status: UpdateStatus) -> None:
        css_class, text = _CLASS_MAP.get(status, ("", str(status)))
        self._status_label.remove_css_class("success-label")
        self._status_label.remove_css_class("warning-label")
        self._status_label.remove_css_class("error-label")
        self._status_label.remove_css_class("progress-label")
        self._status_label.remove_css_class("dim-label")
        self._status_label.add_css_class(css_class)
        self._status_label.set_text(text)

    def set_timestamp(self, timestamp_text: str) -> None:
        self._timestamp_label.set_text(f"Last checked: {timestamp_text}")
