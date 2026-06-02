# Changelog

All notable changes to HyprDiscover are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0-dev] — Unreleased

### Architecture

- **Layered architecture** — migrated from flat `core/` + `ui/` to
  `models/` → `backends/` → `services/` → `ui/` with strict dependency
  direction. The UI never imports backends directly.
- **PEP 517 `src/` layout** — moved application code to
  `src/hyprdiscover/` with `pyproject.toml` build system.
- **Backend abstraction** — introduced `PackageManagerBackend` ABC,
  enabling future Flatpak, native D-Bus, and DNF5 backends without UI
  changes.
- **Service layer** — extracted business logic into `UpdateManager`
  state machine with thread-safe status transitions and callback
  notifications.
- **Configuration management** — TOML-based user config at
  `~/.config/hyprdiscover/config.toml` with auto-creation on first run.
- **Structured logging** — Python stdlib logging to stderr replacing
  ad-hoc `print()` calls.

### Frontend

- **Summary card** — `UpdateSummaryView` widget with large Nerd Font
  icon, headline text, and two-column category grid showing security,
  bug fix, enhancement, and other counts at a glance.
- **Sortable package table** — four-column `Gtk.ColumnView` (icon,
  type, package, version) with `Gtk.StringSorter` and
  `Gtk.NumericSorter` per column. Separate `SignalListItemFactory` per
  column eliminates `gtk_widget_set_parent` CRITICAL warnings.
- **`PackageRow` GObject adapter** — bridges Python `Package`
  dataclasses into `Gio.ListStore` for the column view.
- **`Gtk.HeaderBar`** — window title, Open Discover button, and About
  menu moved into the header bar following GNOME HIG.
- **`Gtk.Expander`** — package details and transaction logs moved into
  a collapsible expander, collapsed by default to reduce visual
  clutter.
- **CSS stylesheet** — GTK4 CSS provider at `assets/styles/` with
  styled summary card, expander, log view, and button variants.

### Backend

- **NEVRA parsing** — new regex-based parser extracts package name and
  version from RPM `name-version-release.arch` strings in `pkcon
  get-updates` output.
- **Multi-word category detection** — handles `"Bug fix"` as a
  two-word category label in space-aligned pkcon output, fixing 24
  previously dropped packages.
- **Status line filtering** — filters pkcon progress messages
  (Transaction, Status, Waiting, Starting, Finished, etc.) from the
  parsed package list.
- **Per-category counts** — `UpdateManager` exposes `security_count`,
  `bugfix_count`, `enhancement_count`, `other_count`, and
  `total_download_size` properties.
- **Locale-independent parsing** — uses `LANG=C` environment variable
  for consistent pkcon output format.

### Integration

- **Reboot confirmation dialog** — `Gtk.MessageDialog` with destructive
  action styling before `systemctl reboot`, respecting
  `config.confirm_reboot` setting.
- **Update confirmation dialog** — optional pre-install confirmation
  with package count, respecting `config.confirm_update` setting.
- **Log view visibility** — transaction log view hidden when empty,
  shown only during install success/failure.
- **Waybar JSON output** — `ensure_ascii=False` for clean UTF-8 output
  avoiding surrogate pair JSON escapes.
- **Nerd Font icons** — consistent icon set across summary card,
  package table, and action buttons.

### Fixed

- **Unicode surrogate pair bug** — replaced `\uDB80\uDF30` surrogate
  pair with proper `\U000F0330` code point, fixing `UnicodeEncodeError`
  on UTF-8 encoding in GTK labels.
- **Shared factory warning** — replaced single shared
  `Gtk.SignalListItemFactory` across columns with three independent
  factories, eliminating `gtk_widget_set_parent` CRITICAL assertions.
- **Orphaned widgets** — removed unused `menu_box` and missing
  `expander.set_child()` call that left the expander content
  unrendered.
- **Summary card spacers** — replaced empty `Gtk.Label` spacers with
  CSS margins.
- **Log view minimum height** — removed forced `min-height: 80px` that
  created large empty areas.

### Testing

- **19 unit tests** covering models, enums, backends (including
  NEVRA parsing), services (UpdateManager state machine, status
  callbacks), Unicode icon encoding, and Waybar JSON output.
- **Test infrastructure** — `pytest` with `pytest-cov` for coverage
  reporting.
- **Continuous integration** — GitHub Actions workflow running pytest,
  ruff linting, and mypy type checking on push to main.

### Documentation

- **README.md** — updated to v0.3.0-dev with current features,
  installation instructions, and technology stack.
- **ARCHITECTURE.md** — complete rewrite documenting the layered
  architecture, directory structure, data flow, threading model, and
  pkcon parsing details.
- **CONTRIBUTING.md** — updated with pip dev install, test/lint
  commands, project structure, and architecture diagram.
- **ROADMAP.md** — updated with completed v0.3 items and revised
  v0.4–v1.0 plans.
- **SECURITY.md** — translated from Indonesian to English.
- **PRD.md** — translated from Indonesian to English, added current
  features list.
- **CHANGELOG.md** — this file.

### Packaging

- **RPM spec** — `packaging/fedora/hyprdiscover.spec` with
  `%pyproject_wheel` build, desktop entry, icon, and CSS stylesheet
  installation.
- **CI pipeline** — `.github/workflows/test.yml` for automated testing.

---

## [0.2.1] — 2026-06-01

### Added

- Desktop notifications via `notify-send` for updates available,
  success, and failure states.
- Last checked timestamp display in the status area.
- Waybar JSON output mode (`--waybar` flag) with update count and
  tooltip.
- Single-instance launcher script with `pgrep` detection and Hyprland
  `focuswindow` reuse.

### Changed

- Install script copies `core/` and `ui/` modules and cleans
  `__pycache__` from the target directory.

---

## [0.2.0] — 2026-06-01

### Added

- GTK4 graphical interface with status label, progress bar, and action
  buttons.
- PackageKit integration via `pkcon` subprocess for update detection
  and installation.
- Refresh button to query available updates.
- Update button to install updates with pulse progress animation.
- Reboot button appearing after successful updates (`systemctl reboot`).
- Open Discover button as KDE Discover fallback.
- About dialog.
- Scrollable update log viewer.
- Desktop entry file for application menu integration.
- SVG application icon.
- Waybar JSON output mode (basic).
- GPLv3 license.

---

## [0.1.0] — 2026-06-01

### Added

- Initial release with core PackageKit update detection and CLI output.
- Basic GTK4 window with update count display.
