from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class AnimatedProgressBar(Gtk.Box):
    """Progress bar with optional pulse animation and status label."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        self._bar = Gtk.ProgressBar()
        self._bar.set_visible(False)
        self._bar.set_hexpand(True)

        self._label = Gtk.Label()
        self._label.set_visible(False)
        self._label.add_css_class("caption")

        self.append(self._bar)
        self.append(self._label)

    @property
    def bar(self) -> Gtk.ProgressBar:
        return self._bar

    def show(self, label: str = "") -> None:
        self._bar.set_visible(True)
        self._bar.set_fraction(0.0)
        if label:
            self._label.set_text(label)
            self._label.set_visible(True)

    def hide(self) -> None:
        self._bar.set_visible(False)
        self._label.set_visible(False)

    def pulse(self) -> None:
        self._bar.pulse()

    def set_fraction(self, fraction: float) -> None:
        self._bar.set_fraction(fraction)

    def set_label(self, text: str) -> None:
        self._label.set_text(text)
        self._label.set_visible(True)
