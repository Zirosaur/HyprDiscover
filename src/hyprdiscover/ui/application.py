from __future__ import annotations

import logging
from pathlib import Path

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import Gtk

from hyprdiscover import __version__
from hyprdiscover.config import AppConfig, load_config
from hyprdiscover.logging import setup_logging

log = logging.getLogger(__name__)

APP_ID = "com.hyprdiscover.app"


class HyprDiscoverApplication(Gtk.Application):
    """Main GTK4 Application.

    Owns the application lifecycle, single-instance enforcement via D-Bus,
    configuration loading, and window management. Does NOT own business
    logic — that's handled by the UpdateManager service.
    """

    def __init__(self) -> None:
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.config = load_config()
        self._window: Gtk.ApplicationWindow | None = None

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)

        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        setup_logging(level)

        log.info("HyprDiscover %s starting", __version__)

        self._setup_actions()
        self._setup_css()

    def do_activate(self) -> None:
        if self._window is not None:
            self._window.present()
            return

        from hyprdiscover.ui.window import MainWindow
        self._window = MainWindow(self, self.config)
        self._window.present()

    def do_shutdown(self) -> None:
        log.info("HyprDiscover shutting down")
        Gtk.Application.do_shutdown(self)

    def _setup_actions(self) -> None:
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *a: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Control>q", "<Control>w"])

        refresh_action = Gio.SimpleAction.new("refresh", None)
        refresh_action.connect("activate", self._on_refresh_action)
        self.add_action(refresh_action)
        self.set_accels_for_action("app.refresh", ["<Control>r"])

    def _on_refresh_action(self, action: Gio.SimpleAction, param: None) -> None:
        if self._window is not None:
            self._window.start_refresh()

    def _setup_css(self) -> None:
        possible_paths = [
            # Source tree (development)
            Path(__file__).parent.parent.parent.parent / "assets" / "styles" / "hyprdiscover.css",
            # Installed location
            Path.home() / ".local" / "share" / "hyprdiscover" / "styles" / "hyprdiscover.css",
            # System install
            Path("/usr/share/hyprdiscover/styles/hyprdiscover.css"),
        ]
        for path in possible_paths:
            if path.exists():
                provider = Gtk.CssProvider()
                provider.load_from_path(str(path))
                Gtk.StyleContext.add_provider_for_display(
                    Gdk.Display.get_default(),
                    provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
                )
                log.debug("Loaded CSS from %s", path)
                return
        log.debug("No custom CSS found in any search path")
