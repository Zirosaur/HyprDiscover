from __future__ import annotations

import logging

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

log = logging.getLogger(__name__)


def show_confirm(
    parent: Gtk.Window,
    title: str,
    message: str,
    primary_label: str = "Confirm",
    destructive: bool = False,
) -> bool:
    """Show a confirmation dialog. Returns True if user confirmed."""
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        modal=True,
        message_type=Gtk.MessageType.WARNING if destructive else Gtk.MessageType.QUESTION,
        buttons=Gtk.ButtonsType.NONE,
        text=title,
        secondary_text=message,
    )
    dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)

    button = dialog.add_button(primary_label, Gtk.ResponseType.OK)
    if destructive:
        button.add_css_class("destructive-action")

    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.OK
