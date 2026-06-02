from __future__ import annotations

import logging

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository import Pango

log = logging.getLogger(__name__)


class UpdateLogView(Gtk.ScrolledWindow):
    """Scrollable, monospace text view for update transaction logs."""

    def __init__(self) -> None:
        super().__init__()
        self.set_vexpand(True)

        self._text_view = Gtk.TextView()
        self._text_view.set_editable(False)
        self._text_view.set_monospace(True)
        self._text_view.set_cursor_visible(False)
        self._text_view.add_css_class("log-view")

        self.set_child(self._text_view)

    def set_text(self, text: str) -> None:
        buf = self._text_view.get_buffer()
        buf.set_text(text)

    def append_text(self, text: str) -> None:
        buf = self._text_view.get_buffer()
        end = buf.get_end_iter()
        buf.insert(end, text)

    def clear(self) -> None:
        buf = self._text_view.get_buffer()
        buf.set_text("")
