from __future__ import annotations

import logging
import subprocess
import threading
from datetime import datetime

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

from hyprdiscover.backends.packagekit import PackageKitBackend
from hyprdiscover.config import AppConfig
from hyprdiscover.models.enums import UpdateStatus
from hyprdiscover.models.package import UpdateProgress
from hyprdiscover.services.notifications import NotificationService
from hyprdiscover.services.reboot import reboot_system
from hyprdiscover.services.update_manager import UpdateManager
from hyprdiscover.ui.dialogs.about import show_about
from hyprdiscover.ui.dialogs.confirm import show_confirm
from hyprdiscover.ui.widgets.package_list import PackageListView
from hyprdiscover.ui.widgets.progress_bar import AnimatedProgressBar
from hyprdiscover.ui.widgets.summary_card import UpdateSummaryView
from hyprdiscover.ui.widgets.update_log import UpdateLogView

log = logging.getLogger(__name__)


class MainWindow(Gtk.ApplicationWindow):
    """Main application window.

    Layout (top to bottom):
      HeaderBar: title | [Open Discover] [About menu]
      Summary card: icon + headline + category breakdown
      Progress bar: visible only during updates
      Action bar: [Refresh] [Update All] [Reboot]
      Expander: Package Details (collapsed, contains list + logs)
    """

    _REFRESH_ICON = "\U000F0450"
    _UPDATE_ICON = "\U000F0196"
    _REBOOT_ICON = "\U000F0709"

    def __init__(self, application: Gtk.Application, config: AppConfig) -> None:
        super().__init__(application=application)
        self._config = config
        self._running = False
        self._pulse_source: int | None = None

        backend = PackageKitBackend()
        self._updater = UpdateManager(backend)
        self._notifier = NotificationService()

        self.set_title("HyprDiscover")
        self.set_default_size(config.window_width, config.window_height)
        self._build_header()
        self._build_ui()
        self._wire_signals()

        if config.check_on_startup:
            GLib.idle_add(self._async_refresh)

    # ── Header Bar ──────────────────────────────────────────────

    def _build_header(self) -> None:
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        discover_btn = Gtk.Button(label="Open Discover")
        discover_btn.connect("clicked", lambda b: self._open_discover())

        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")

        popover = Gtk.Popover()
        popover.set_parent(menu_btn)

        prefs_item = Gtk.Button(label="Preferences")
        prefs_item.add_css_class("flat")
        prefs_item.set_halign(Gtk.Align.START)
        prefs_item.connect("clicked", lambda b: (popover.popdown(), self._show_preferences()))

        about_item = Gtk.Button(label="About HyprDiscover")
        about_item.add_css_class("flat")
        about_item.set_halign(Gtk.Align.START)
        about_item.connect("clicked", lambda b: (popover.popdown(), show_about(self)))

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.append(prefs_item)
        box.append(about_item)
        popover.set_child(box)
        menu_btn.set_popover(popover)

        header.pack_end(menu_btn)
        header.pack_end(discover_btn)

    # ── UI Construction ─────────────────────────────────────────

    def _build_ui(self) -> None:
        self._summary = UpdateSummaryView()

        self._progress = AnimatedProgressBar()

        self._refresh_btn = Gtk.Button(
            label=f"  {self._REFRESH_ICON}  Refresh  "
        )
        self._refresh_btn.connect("clicked", lambda b: self._async_refresh())

        self._update_selected_btn = Gtk.Button(
            label=f"  {self._UPDATE_ICON}  Update Selected  "
        )
        self._update_selected_btn.connect("clicked", lambda b: self._async_install_selected())
        self._update_selected_btn.add_css_class("suggested-action")
        self._update_selected_btn.set_sensitive(False)

        self._update_btn = Gtk.Button(
            label=f"  {self._UPDATE_ICON}  Update All  "
        )
        self._update_btn.connect("clicked", lambda b: self._async_install_all())

        self._cancel_btn = Gtk.Button(
            label="  \U000F0156  Cancel  "
        )
        self._cancel_btn.connect("clicked", lambda b: self._cancel_operation())
        self._cancel_btn.set_sensitive(False)

        self._reboot_btn = Gtk.Button(
            label=f"  {self._REBOOT_ICON}  Reboot  "
        )
        self._reboot_btn.connect("clicked", lambda b: self._on_reboot())
        self._reboot_btn.add_css_class("destructive-action")
        self._reboot_btn.set_visible(False)

        action_bar = Gtk.Box(spacing=8)
        action_bar.set_halign(Gtk.Align.CENTER)
        action_bar.set_margin_top(8)
        action_bar.set_margin_bottom(4)
        action_bar.append(self._refresh_btn)
        action_bar.append(self._update_selected_btn)
        action_bar.append(self._update_btn)
        action_bar.append(self._cancel_btn)
        action_bar.append(self._reboot_btn)

        self._expander = Gtk.Expander(label="Package Details")
        self._expander.set_margin_top(8)

        self._expander_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self._expander_box.set_margin_top(6)
        self._expander_box.set_margin_start(8)
        self._expander_box.set_margin_end(8)
        self._expander_box.set_margin_bottom(8)

        self._package_list = PackageListView()
        self._package_list.set_vexpand(True)
        self._expander_box.append(self._package_list)

        self._log_view = UpdateLogView()
        self._log_view.set_visible(False)
        self._log_view.add_css_class("log-scroller")
        self._expander_box.append(self._log_view)

        self._expander.set_child(self._expander_box)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(18)
        main_box.set_margin_bottom(18)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)
        main_box.set_vexpand(True)

        main_box.append(self._summary)
        main_box.append(self._progress)
        main_box.append(action_bar)
        main_box.append(self._expander)

        self.set_child(main_box)

    def _wire_signals(self) -> None:
        self._updater.set_status_callback(self._on_status_changed)
        self._updater.set_progress_callback(self._on_progress)
        self._package_list.set_selection_callback(self._on_selection_changed)

    # ── Public API ──────────────────────────────────────────────

    def start_refresh(self) -> None:
        self._async_refresh()

    # ── Async Refresh ───────────────────────────────────────────

    def _async_refresh(self) -> None:
        self._summary.show_checking()
        self._refresh_btn.set_sensitive(False)
        thread = threading.Thread(target=self._refresh_in_thread, daemon=True)
        thread.start()

    def _refresh_in_thread(self) -> None:
        self._updater.refresh()

        GLib.idle_add(self._refresh_btn.set_sensitive, True)
        GLib.idle_add(
            self._summary.set_timestamp,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        count = self._updater.update_count
        if count > 0 and self._config.show_notifications:
            self._notifier.updates_available(count)

        GLib.idle_add(self._package_list.set_packages, self._updater.packages)

        total_size = self._updater.total_download_size
        if total_size > 0:
            GLib.idle_add(
                self._expander.set_label,
                f"Package Details ({self._format_size(total_size)})",
            )
        else:
            GLib.idle_add(
                self._expander.set_label,
                f"Package Details ({count} packages)" if count else "Package Details",
            )

    # ── Async Install ───────────────────────────────────────────

    def _async_install_all(self) -> None:
        count = self._updater.update_count
        if count == 0:
            return

        if self._config.confirm_update:
            confirmed = show_confirm(
                self, "Install Updates",
                f"{count} package{'s' if count != 1 else ''} will be updated.",
                primary_label="Install",
            )
            if not confirmed:
                return

        self._summary.show_updating()
        self._refresh_btn.set_sensitive(False)
        self._update_btn.set_sensitive(False)
        self._update_selected_btn.set_sensitive(False)
        self._cancel_btn.set_sensitive(True)
        self._reboot_btn.set_visible(False)
        self._expander.set_expanded(True)
        self._running = True

        self._log_view.clear()
        self._progress.show("Preparing update\u2026")
        self._pulse_source = GLib.timeout_add(100, self._pulse_tick)

        thread = threading.Thread(target=self._install_in_thread, daemon=True)
        thread.start()

    def _async_install_selected(self) -> None:
        packages = self._package_list.get_checked_packages()
        if not packages:
            return
        count = len(packages)

        if self._config.confirm_update:
            confirmed = show_confirm(
                self, "Install Selected Updates",
                f"{count} package{'s' if count != 1 else ''} will be updated.",
                primary_label="Install",
            )
            if not confirmed:
                return

        self._summary.show_updating()
        self._refresh_btn.set_sensitive(False)
        self._update_btn.set_sensitive(False)
        self._update_selected_btn.set_sensitive(False)
        self._cancel_btn.set_sensitive(True)
        self._reboot_btn.set_visible(False)
        self._expander.set_expanded(True)
        self._running = True

        self._log_view.clear()
        self._progress.show("Preparing update\u2026")
        self._pulse_source = GLib.timeout_add(100, self._pulse_tick)

        thread = threading.Thread(
            target=self._install_in_thread,
            kwargs={"packages": packages},
            daemon=True,
        )
        thread.start()

    def _install_in_thread(self, packages: object = None) -> None:
        result = self._updater.install_updates(packages=packages)

        GLib.idle_add(self._running_stop)
        GLib.idle_add(self._refresh_btn.set_sensitive, True)
        GLib.idle_add(self._update_btn.set_sensitive, True)
        GLib.idle_add(self._update_selected_btn.set_sensitive,
                      self._package_list.get_checked_count() > 0)
        GLib.idle_add(self._cancel_btn.set_sensitive, False)
        GLib.idle_add(self._progress.hide)

        if result.cancelled:
            self._updater.refresh()
            GLib.idle_add(self._package_list.set_packages, self._updater.packages)
            return

        if result.success:
            self._notifier.update_success()
            reboot = self._updater.status == UpdateStatus.REBOOT_REQUIRED
            GLib.idle_add(self._summary.show_success, reboot)
            if reboot:
                GLib.idle_add(self._reboot_btn.set_visible, True)
            self._updater.refresh()
            GLib.idle_add(self._package_list.set_packages, self._updater.packages)
        else:
            self._notifier.update_failed()
            GLib.idle_add(self._expander.set_expanded, True)

    # ── Progress ────────────────────────────────────────────────

    def _pulse_tick(self) -> bool:
        if self._running:
            self._progress.pulse()
            return True
        return False

    def _running_stop(self) -> None:
        self._running = False
        if self._pulse_source is not None:
            GLib.source_remove(self._pulse_source)
            self._pulse_source = None

    # ── Selection Callbacks ────────────────────────────────────

    def _on_selection_changed(self, count: int) -> None:
        if count == 0:
            self._update_selected_btn.set_sensitive(False)
            self._update_selected_btn.set_label(
                f"  {self._UPDATE_ICON}  Update Selected  "
            )
        else:
            self._update_selected_btn.set_sensitive(True)
            self._update_selected_btn.set_label(
                f"  {self._UPDATE_ICON}  Update Selected ({count})  "
            )

    # ── Progress Callbacks ─────────────────────────────────────

    def _on_progress(self, progress: UpdateProgress) -> None:
        if progress.percentage > 0 and self._pulse_source is not None:
            GLib.idle_add(self._running_stop)

        if progress.percentage >= 0:
            GLib.idle_add(self._progress.set_fraction, progress.percentage / 100.0)

        msg = progress.message or progress.status or ""
        if msg:
            GLib.idle_add(self._progress.set_label, msg)
            GLib.idle_add(self._log_view.append_text, msg + "\n")
            GLib.idle_add(self._log_view.set_visible, True)

    # ── Status Callbacks ────────────────────────────────────────

    def _on_status_changed(self, status: UpdateStatus) -> None:
        if status == UpdateStatus.UP_TO_DATE:
            GLib.idle_add(self._summary.show_up_to_date)

        elif status == UpdateStatus.UPDATES_AVAILABLE:
            GLib.idle_add(
                self._summary.show_updates_available,
                self._updater.update_count,
                self._updater.security_count,
                self._updater.bugfix_count,
                self._updater.enhancement_count,
                self._updater.other_count,
                self._updater.total_download_size,
            )

        elif status == UpdateStatus.REBOOT_REQUIRED:
            GLib.idle_add(self._summary.show_success, True)
            GLib.idle_add(self._reboot_btn.set_visible, True)
            self._notifier.reboot_reminder()

        elif status == UpdateStatus.SUCCESS:
            GLib.idle_add(self._summary.show_success, False)

        elif status == UpdateStatus.ERROR:
            GLib.idle_add(self._summary.show_error)
            GLib.idle_add(self._expander.set_expanded, True)

        elif status == UpdateStatus.CANCELLED:
            pass

    # ── Button Actions ──────────────────────────────────────────

    def _show_preferences(self) -> None:
        from hyprdiscover.ui.dialogs.preferences import PreferencesWindow
        PreferencesWindow(self, self._config).present()

    def _cancel_operation(self) -> None:
        self._updater.cancel()

    def _open_discover(self) -> None:
        subprocess.Popen(["plasma-discover"])

    def _on_reboot(self) -> None:
        if self._config.confirm_reboot:
            confirmed = show_confirm(
                self, "Reboot System",
                "The system will restart to complete updates.",
                primary_label="Reboot",
                destructive=True,
            )
            if not confirmed:
                return
        reboot_system()

    # ── Helpers ─────────────────────────────────────────────────

    @staticmethod
    def _format_size(byte_count: int) -> str:
        if byte_count < 1024:
            return f"{byte_count} B"
        elif byte_count < 1024 * 1024:
            return f"{byte_count / 1024:.0f} KB"
        elif byte_count < 1024 * 1024 * 1024:
            return f"{byte_count / (1024 * 1024):.0f} MB"
        else:
            return f"{byte_count / (1024 * 1024 * 1024):.1f} GB"
