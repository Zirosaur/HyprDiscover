from __future__ import annotations

from hyprdiscover.models.package import Package
from hyprdiscover.ui.widgets.package_list import PackageListView, PackageRow


class TestPackageRow:
    def test_stores_package_reference(self) -> None:
        pkg = Package(name="firefox", package_id="firefox-131.0.x86_64")
        row = PackageRow(pkg)
        assert row.package is pkg
        assert row.package.name == "firefox"

    def test_selected_defaults_to_false(self) -> None:
        pkg = Package(name="test", package_id="test-1.0")
        row = PackageRow(pkg)
        assert row.selected is False

    def test_selected_toggle(self) -> None:
        pkg = Package(name="test", package_id="test-1.0")
        row = PackageRow(pkg)
        row.selected = True
        assert row.selected is True
        row.selected = False
        assert row.selected is False


class TestPackageListView:
    def test_get_checked_empty(self) -> None:
        view = PackageListView()
        view.set_packages([])
        assert view.get_checked_packages() == []
        assert view.get_checked_count() == 0

    def test_set_packages_resets_selection(self) -> None:
        pkg = Package(name="firefox", package_id="firefox-131.0.x86_64")
        view = PackageListView()

        view.set_packages([pkg])
        store = view._store
        row: PackageRow = store.get_item(0)
        row.selected = True

        view.set_packages([pkg])
        new_store = view._store
        new_row: PackageRow = new_store.get_item(0)
        assert new_row.selected is False

    def test_get_checked_returns_selected_packages(self) -> None:
        pkg_a = Package(name="firefox", package_id="firefox-131.0.x86_64")
        pkg_b = Package(name="vim", package_id="vim-9.2.x86_64")
        pkg_c = Package(name="kernel", package_id="kernel-6.11.0.x86_64")
        view = PackageListView()

        view.set_packages([pkg_a, pkg_b, pkg_c])
        store = view._store

        store.get_item(0).selected = True
        store.get_item(2).selected = True

        checked = view.get_checked_packages()
        assert len(checked) == 2
        assert checked[0].name == "firefox"
        assert checked[1].name == "kernel"
        assert view.get_checked_count() == 2

    def test_selection_callback_fires_on_set_packages(self) -> None:
        call_counts: list[int] = []

        def cb(count: int) -> None:
            call_counts.append(count)

        pkg = Package(name="firefox", package_id="firefox-131.0.x86_64")
        view = PackageListView()
        view.set_selection_callback(cb)
        view.set_packages([pkg])
        assert call_counts == [0]
