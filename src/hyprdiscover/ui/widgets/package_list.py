from __future__ import annotations

import logging

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

from hyprdiscover.models.package import Package

log = logging.getLogger(__name__)

_ICONS: dict[str, str] = {
    "security": "\U000F0482",
    "bugfix": "\U000F0190",
    "enhancement": "\U000F0020",
}

_LABELS: dict[str, str] = {
    "security": "Security",
    "bugfix": "Bug Fix",
    "enhancement": "Enhancement",
    "blocked": "Blocked",
    "unknown": "Other",
}

_CATEGORY_SORT: dict[str, int] = {
    "security": 0,
    "bugfix": 1,
    "enhancement": 2,
    "blocked": 3,
    "unknown": 4,
}

_DEFAULT_ICON = "\U000F0820"
_DEFAULT_LABEL = "Other"


class PackageRow(GObject.Object):
    """GObject adapter for Gio.ListStore / Gtk.ColumnView.

    Properties are exposed for Gtk.PropertyExpression-based sorters.
    """

    icon = GObject.Property(type=str, default=_DEFAULT_ICON)
    category = GObject.Property(type=str, default=_DEFAULT_LABEL)
    sort_key = GObject.Property(type=int, default=4)
    name = GObject.Property(type=str, default="")
    version = GObject.Property(type=str, default="")
    package_id = GObject.Property(type=str, default="")

    def __init__(self, package: Package) -> None:
        super().__init__()
        cat_val = package.category.value
        self.icon = _ICONS.get(cat_val, _DEFAULT_ICON)
        self.category = _LABELS.get(cat_val, _DEFAULT_LABEL)
        self.sort_key = _CATEGORY_SORT.get(cat_val, 4)
        self.name = package.display_name
        self.version = package.version_available or ""
        self.package_id = package.package_id


def _make_factory(
    setup_cb: callable,
    bind_cb: callable,
) -> Gtk.SignalListItemFactory:
    factory = Gtk.SignalListItemFactory()
    factory.connect("setup", setup_cb)
    factory.connect("bind", bind_cb)
    factory.connect("teardown", _on_teardown)
    return factory


def _on_label_setup(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    label = Gtk.Label()
    label.set_xalign(0)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    item.set_child(label)


def _bind_icon(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    row: PackageRow = item.get_item()
    if row is not None:
        item.get_child().set_text(row.icon)


def _bind_category(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    row: PackageRow = item.get_item()
    if row is not None:
        item.get_child().set_text(row.category)


def _bind_name(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    row: PackageRow = item.get_item()
    if row is not None:
        item.get_child().set_text(row.name)


def _bind_version(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    row: PackageRow = item.get_item()
    if row is not None:
        item.get_child().set_text(row.version)


def _on_teardown(factory: Gtk.ListItemFactory, item: Gtk.ListItem) -> None:
    label = item.get_child()
    if label is not None:
        label.set_text("")


def _prop_expr(prop_name: str) -> Gtk.PropertyExpression:
    return Gtk.PropertyExpression.new(PackageRow, None, prop_name)


class PackageListView(Gtk.Box):
    """Scrollable, sortable ColumnView of packages.

    Columns (left to right):
      Icon (Nerd Font glyph per category)
      Type (Security / Bug Fix / Enhancement / Other — sortable)
      Package (name, sortable A-Z)
      Version (sortable A-Z)
    """

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self._store = Gio.ListStore.new(PackageRow)
        self._selection = Gtk.SingleSelection(model=self._store)

        self._column_view = Gtk.ColumnView(model=self._selection)
        self._column_view.set_hexpand(True)
        self._column_view.set_vexpand(True)
        self._column_view.add_css_class("rich-list")

        # ── Icon column (unsorted) ──────────────────────────
        icon_factory = _make_factory(_on_label_setup, _bind_icon)
        col_icon = Gtk.ColumnViewColumn.new("", icon_factory)
        col_icon.set_fixed_width(40)
        col_icon.set_resizable(False)
        self._column_view.append_column(col_icon)

        # ── Type column (sorted by priority) ────────────────
        type_factory = _make_factory(_on_label_setup, _bind_category)
        col_type = Gtk.ColumnViewColumn.new("Type", type_factory)
        col_type.set_fixed_width(110)
        col_type.set_resizable(True)
        col_type.set_sorter(
            Gtk.NumericSorter.new(_prop_expr("sort_key"))
        )
        self._column_view.append_column(col_type)

        # ── Package column (sorted A-Z) ─────────────────────
        name_factory = _make_factory(_on_label_setup, _bind_name)
        col_name = Gtk.ColumnViewColumn.new("Package", name_factory)
        col_name.set_expand(True)
        col_name.set_resizable(True)
        col_name.set_sorter(
            Gtk.StringSorter.new(_prop_expr("name"))
        )
        self._column_view.append_column(col_name)

        # ── Version column (sorted A-Z) ─────────────────────
        ver_factory = _make_factory(_on_label_setup, _bind_version)
        col_ver = Gtk.ColumnViewColumn.new("Version", ver_factory)
        col_ver.set_fixed_width(180)
        col_ver.set_resizable(True)
        col_ver.set_sorter(
            Gtk.StringSorter.new(_prop_expr("version"))
        )
        self._column_view.append_column(col_ver)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_child(self._column_view)
        self.append(scroll)

    def set_packages(self, packages: list[Package]) -> None:
        new_store = Gio.ListStore.new(PackageRow)
        for pkg in packages:
            new_store.append(PackageRow(pkg))
        self._store = new_store
        self._selection.set_model(self._store)
