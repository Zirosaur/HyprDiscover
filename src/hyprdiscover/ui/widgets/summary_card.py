from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Pango


class UpdateSummaryView(Gtk.Box):
    """Prominent summary card showing update counts by category.

    Replaces the old flat StatusHeader with a visually structured
    overview that makes critical information immediately visible.
    """

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("summary-card")

        self._icon_label = Gtk.Label(label="\U000F012C")
        self._icon_label.add_css_class("summary-icon")
        self._icon_label.set_halign(Gtk.Align.CENTER)

        self._headline = Gtk.Label(label="Ready")
        self._headline.add_css_class("summary-headline")
        self._headline.set_halign(Gtk.Align.CENTER)
        self._headline.set_ellipsize(Pango.EllipsizeMode.END)
        self._headline.set_wrap(True)
        self._headline.set_justify(Gtk.Justification.CENTER)

        self._timestamp = Gtk.Label(label="Last checked: Never")
        self._timestamp.add_css_class("caption")
        self._timestamp.set_halign(Gtk.Align.CENTER)

        self._grid = Gtk.Grid()
        self._grid.set_halign(Gtk.Align.CENTER)
        self._grid.set_column_spacing(48)
        self._grid.set_row_spacing(4)
        self._grid.set_visible(False)
        self._grid.add_css_class("summary-grid")

        self._rows: list[tuple[str, Gtk.Label, Gtk.Label]] = []

        self.append(self._icon_label)
        self.append(self._headline)
        self.append(self._timestamp)
        self.append(self._grid)

    @property
    def headline(self) -> Gtk.Label:
        return self._headline

    @property
    def timestamp_label(self) -> Gtk.Label:
        return self._timestamp

    def show_up_to_date(self) -> None:
        self._icon_label.set_text("\U000F012C")
        self._icon_label.remove_css_class("summary-icon-warning")
        self._icon_label.add_css_class("summary-icon-ok")
        self._headline.set_text("Your system is up to date")
        self._headline.remove_css_class("warning-label")
        self._headline.add_css_class("success-label")
        self._grid.set_visible(False)
        self._clear_rows()

    def show_updates_available(
        self,
        total: int,
        security: int,
        bugfix: int,
        enhancement: int,
        other: int,
        download_size: int = 0,
    ) -> None:
        self._icon_label.set_text("\U000F06B0")
        self._icon_label.remove_css_class("summary-icon-ok")
        self._icon_label.add_css_class("summary-icon-warning")
        self._headline.set_text(f"{total} update{'s' if total != 1 else ''} available")
        self._headline.remove_css_class("success-label")
        self._headline.add_css_class("warning-label")
        self._rebuild_grid(security, bugfix, enhancement, other, download_size)

    def show_checking(self) -> None:
        self._icon_label.set_text("\U000F0330")
        self._icon_label.remove_css_class("summary-icon-ok")
        self._icon_label.remove_css_class("summary-icon-warning")
        self._icon_label.add_css_class("dim-label")
        self._headline.set_text("Checking for updates\u2026")
        self._headline.remove_css_class("success-label")
        self._headline.remove_css_class("warning-label")
        self._grid.set_visible(False)
        self._clear_rows()

    def show_error(self, message: str = "An error occurred") -> None:
        self._icon_label.set_text("\u26A0")
        self._icon_label.remove_css_class("summary-icon-ok")
        self._icon_label.add_css_class("summary-icon-warning")
        self._headline.set_text(message)
        self._headline.remove_css_class("success-label")
        self._headline.add_css_class("error-label")
        self._grid.set_visible(False)
        self._clear_rows()

    def show_updating(self) -> None:
        self._icon_label.set_text("\U000F0330")
        self._icon_label.remove_css_class("summary-icon-ok")
        self._icon_label.remove_css_class("summary-icon-warning")
        self._icon_label.add_css_class("dim-label")
        self._headline.set_text("Updating packages\u2026")
        self._headline.remove_css_class("success-label")
        self._headline.remove_css_class("warning-label")
        self._grid.set_visible(False)
        self._clear_rows()

    def show_success(self, reboot_required: bool = False) -> None:
        self._icon_label.set_text("\u2713")
        self._icon_label.remove_css_class("summary-icon-warning")
        self._icon_label.add_css_class("summary-icon-ok")
        if reboot_required:
            self._headline.set_text("Updates installed \u2014 reboot required")
        else:
            self._headline.set_text("Updates installed successfully")
        self._headline.remove_css_class("warning-label")
        self._headline.add_css_class("success-label")
        self._grid.set_visible(False)
        self._clear_rows()

    def set_timestamp(self, text: str) -> None:
        self._timestamp.set_text(f"Last checked: {text}")

    def _rebuild_grid(
        self,
        security: int,
        bugfix: int,
        enhancement: int,
        other: int,
        download_size: int,
    ) -> None:
        self._clear_rows()
        items = [
            ("security", "\U000F0482  Security", security),
            ("bugfix", "\U000F0190  Bug fixes", bugfix),
            ("enhancement", "\U000F0020  Enhancements", enhancement),
            ("other", "\U000F0820  Other", other),
        ]
        self._grid.set_visible(True)

        for idx, (_, label_text, count) in enumerate(items):
            row = idx
            icon_label = Gtk.Label(label=label_text)
            icon_label.set_halign(Gtk.Align.START)
            icon_label.add_css_class("summary-category-label")
            count_label = Gtk.Label(label=str(count))
            count_label.set_halign(Gtk.Align.START)
            count_label.add_css_class("summary-category-count")
            self._grid.attach(icon_label, 0, row, 1, 1)
            self._grid.attach(count_label, 1, row, 1, 1)
            self._rows.append((_, icon_label, count_label))

    def _clear_rows(self) -> None:
        for _, icon_label, count_label in self._rows:
            self._grid.remove(icon_label)
            self._grid.remove(count_label)
        self._rows.clear()
