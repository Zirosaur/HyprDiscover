from __future__ import annotations

import logging

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from hyprdiscover.config import AppConfig
from hyprdiscover.services import autostart

log = logging.getLogger(__name__)

_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def _make_switch_row(label: str, active: bool, on_toggle: callable) -> Gtk.ListBoxRow:
    sw = Gtk.Switch()
    sw.set_active(active)
    sw.set_valign(Gtk.Align.CENTER)
    sw.update_property([Gtk.AccessibleProperty.LABEL], [label])
    sw.connect("notify::active", lambda s, _p: on_toggle(s.get_active()))

    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    box.set_margin_start(12)
    box.set_margin_end(12)
    box.set_margin_top(8)
    box.set_margin_bottom(8)

    lbl = Gtk.Label(label=label)
    lbl.set_xalign(0)
    lbl.set_hexpand(True)
    box.append(lbl)
    box.append(sw)

    row = Gtk.ListBoxRow()
    row.set_child(box)
    return row


def _make_dropdown_row(
    label: str,
    items: list[str],
    selected: int,
    on_change: callable,
) -> Gtk.ListBoxRow:
    model = Gtk.StringList.new(items)
    dd = Gtk.DropDown.new(model)
    dd.set_selected(selected)
    dd.set_valign(Gtk.Align.CENTER)
    dd.update_property([Gtk.AccessibleProperty.LABEL], [label])
    dd.connect("notify::selected", lambda d, _p: on_change(d.get_selected()))

    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    box.set_margin_start(12)
    box.set_margin_end(12)
    box.set_margin_top(8)
    box.set_margin_bottom(8)

    lbl = Gtk.Label(label=label)
    lbl.set_xalign(0)
    lbl.set_hexpand(True)
    box.append(lbl)
    box.append(dd)

    row = Gtk.ListBoxRow()
    row.set_child(box)
    return row


def _make_section_header(label: str) -> Gtk.Label:
    header = Gtk.Label(label=label)
    header.set_xalign(0)
    header.add_css_class("heading")
    header.set_margin_start(12)
    header.set_margin_end(12)
    header.set_margin_top(16)
    header.set_margin_bottom(2)
    return header


class PreferencesWindow(Gtk.Window):
    """Non-modal preferences window with instant-save behaviour."""

    def __init__(self, parent: Gtk.Window, config: AppConfig) -> None:
        super().__init__()
        self.set_title("Preferences")
        self.set_transient_for(parent)
        self.set_default_size(400, -1)

        self._config = config
        self._defaults = AppConfig()

        # ── HeaderBar ──────────────────────────────────────
        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)

        reset_btn = Gtk.Button(label="Reset to Defaults")
        reset_btn.connect("clicked", self._on_reset)
        header.pack_start(reset_btn)

        self.set_titlebar(header)

        # ── ListBox ────────────────────────────────────────
        list_box = Gtk.ListBox()
        list_box.add_css_class("rich-list")
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        # Updates section
        list_box.append(_make_section_header("Updates"))

        self._auto_refresh_switch: Gtk.Switch
        row = _make_switch_row(
            "Auto-refresh updates",
            config.auto_refresh,
            self._on_auto_refresh_toggled,
        )
        self._auto_refresh_switch = row.get_child().get_last_child()
        list_box.append(row)

        self._confirm_update_switch: Gtk.Switch
        row = _make_switch_row(
            "Confirm before updating",
            config.confirm_update,
            self._on_confirm_update_toggled,
        )
        self._confirm_update_switch = row.get_child().get_last_child()
        list_box.append(row)

        self._confirm_reboot_switch: Gtk.Switch
        row = _make_switch_row(
            "Confirm before reboot",
            config.confirm_reboot,
            self._on_confirm_reboot_toggled,
        )
        self._confirm_reboot_switch = row.get_child().get_last_child()
        list_box.append(row)

        # Notifications section
        list_box.append(_make_section_header("Notifications"))

        self._show_notifications_switch: Gtk.Switch
        row = _make_switch_row(
            "Desktop notifications",
            config.show_notifications,
            self._on_show_notifications_toggled,
        )
        self._show_notifications_switch = row.get_child().get_last_child()
        list_box.append(row)

        self._check_on_startup_switch: Gtk.Switch
        row = _make_switch_row(
            "Check for updates on startup",
            config.check_on_startup,
            self._on_check_on_startup_toggled,
        )
        self._check_on_startup_switch = row.get_child().get_last_child()
        list_box.append(row)

        # Startup section
        list_box.append(_make_section_header("Startup"))

        self._auto_start_switch: Gtk.Switch
        row = _make_switch_row(
            "Start automatically on login",
            autostart.is_autostart_enabled(),
            self._on_auto_start_toggled,
        )
        self._auto_start_switch = row.get_child().get_last_child()
        list_box.append(row)

        # Advanced section
        list_box.append(_make_section_header("Advanced"))

        self._log_level_dropdown: Gtk.DropDown
        try:
            selected = _LOG_LEVELS.index(config.log_level)
        except ValueError:
            selected = 1
        row = _make_dropdown_row(
            "Log level",
            list(_LOG_LEVELS),
            selected,
            self._on_log_level_changed,
        )
        self._log_level_dropdown = row.get_child().get_last_child()
        list_box.append(row)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_child(list_box)

        self.set_child(scroll)

    # ── Handlers ──────────────────────────────────────────

    def _save(self) -> None:
        self._config.save()

    def _on_auto_refresh_toggled(self, active: bool) -> None:
        self._config.auto_refresh = active
        self._save()

    def _on_confirm_update_toggled(self, active: bool) -> None:
        self._config.confirm_update = active
        self._save()

    def _on_confirm_reboot_toggled(self, active: bool) -> None:
        self._config.confirm_reboot = active
        self._save()

    def _on_show_notifications_toggled(self, active: bool) -> None:
        self._config.show_notifications = active
        self._save()

    def _on_check_on_startup_toggled(self, active: bool) -> None:
        self._config.check_on_startup = active
        self._save()

    def _on_log_level_changed(self, idx: int) -> None:
        self._config.log_level = _LOG_LEVELS[idx]
        self._save()

    def _on_auto_start_toggled(self, active: bool) -> None:
        self._config.auto_start = active
        self._save()
        if active:
            autostart.enable_autostart()
        else:
            autostart.disable_autostart()

    def _on_reset(self, _button: Gtk.Button) -> None:
        defaults = AppConfig()
        self._config.auto_refresh = defaults.auto_refresh
        self._config.show_notifications = defaults.show_notifications
        self._config.check_on_startup = defaults.check_on_startup
        self._config.confirm_update = defaults.confirm_update
        self._config.confirm_reboot = defaults.confirm_reboot
        self._config.log_level = defaults.log_level
        self._config.auto_start = defaults.auto_start
        self._save()

        if defaults.auto_start:
            autostart.enable_autostart()
        else:
            autostart.disable_autostart()

        # Update widget states
        self._auto_refresh_switch.set_active(defaults.auto_refresh)
        self._confirm_update_switch.set_active(defaults.confirm_update)
        self._confirm_reboot_switch.set_active(defaults.confirm_reboot)
        self._show_notifications_switch.set_active(defaults.show_notifications)
        self._check_on_startup_switch.set_active(defaults.check_on_startup)
        self._auto_start_switch.set_active(defaults.auto_start)
        try:
            self._log_level_dropdown.set_selected(
                _LOG_LEVELS.index(defaults.log_level)
            )
        except ValueError:
            self._log_level_dropdown.set_selected(1)
