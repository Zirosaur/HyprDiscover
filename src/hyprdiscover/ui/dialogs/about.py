from __future__ import annotations

import logging

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from hyprdiscover import __version__

log = logging.getLogger(__name__)


def show_about(parent: Gtk.Window) -> None:
    dialog = Gtk.AboutDialog()
    dialog.set_transient_for(parent)
    dialog.set_modal(True)

    dialog.set_program_name("HyprDiscover")
    dialog.set_version(__version__)
    dialog.set_comments("Modern update manager for Fedora Hyprland")
    dialog.set_website("https://github.com/Zirosaur/HyprDiscover")
    dialog.set_license_type(Gtk.License.GPL_3_0)
    dialog.set_authors(["Zirosaur"])
    dialog.set_copyright("Zirosaur")

    dialog.present()
