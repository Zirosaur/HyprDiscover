# Changelog

All notable changes to HyprDiscover are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] — 2026-06-04

### Added

- **Configuration GUI** — Preferences window with 6 configurable settings
  and Reset to Defaults action. Launched from the HeaderBar menu.
- **Typed error classification** — `ErrorType` enum and `UpdateError`
  dataclass. pkcon failures are classified as NETWORK, AUTH, LOCK,
  CONFLICT, or INTERNAL. Typed error summaries are shown in the UI.
- **XDG autostart integration** — `~/.config/autostart/hyprdiscover.desktop`
  created via a "Start automatically on login" toggle in Preferences.
  Opt-in only; disabled by default.
- **Accessibility improvements** — `AccessibleProperty.LABEL` set on
  Switches, DropDowns, CheckButtons, the MenuButton, and ProgressBar.
  Tooltips added to all action buttons (Refresh, Update Selected,
  Update All, Cancel, Reboot, Open Discover).
- **Fedora GTK CI** — a `fedora:41` container job runs UI tests with
  `xvfb-run`. Ubuntu backend job tests both Python 3.12 and 3.13.

### Changed

- **Ruff lint** — 70 violations resolved. Per-file `E402` ignore for
  GTK UI files. Import blocks sorted, unused imports removed.
- **CI dependencies** — Ubuntu job installs `.[dev]` for ruff + mypy
  access. Fedora job uses native `python3-gobject` from dnf.

### Fixed

- **False refresh warning** — `pkcon get-updates` returns exit code 5
  when there are no updates. `get_updates()` now checks no-update
  markers before classifying non-zero return codes as errors.
- **F541** — extraneous f-string prefix on Cancel button label.

### Testing

- **86 unit tests** (up from 62 in v0.3.1) covering config,
  preferences, autostart, error classification, and accessibility.
  Test coverage at 44%.

---

## [0.3.1] — 2026-06-03

### Added

- **CLI status output** — `hyprdiscover --status` prints human-readable
  update summary; `--status --json` outputs machine-readable JSON with
  ISO-8601 timestamps.
- **Argparse command routing** — `hyprdiscover --help` shows all
  available options with descriptions.
- **Background update checking** — `hyprdiscover --check` mode for
  headless update checks via systemd user timer. Sends desktop
  notifications when updates are available.
- **Systemd timer** — `hyprdiscover-check.timer` and
  `hyprdiscover-check.service` units for periodic background checks.
- **Selective package updates** — checkbox column in the package list
  enables installing only selected packages. `Update Selected (N)` button
  shows count and installs the checked subset.
- **Real-time progress reporting** — `subprocess.Popen()` with line
  streaming replaces blocking `subprocess.run()`. Progress bar fraction,
  status label, and transaction log update in real time during updates.
- **Cancel update operation** — Cancel button stops an in-progress
  update via `process.terminate()`. Preserves `CANCELLED` status without
  showing failure notifications.
- **Package architecture tracking** — `arch` and `repo` fields added to
  `Package` model. PackageKit IDs (`name;version;arch;repo`) used for
  unambiguous package identification in multi-arch environments.

### Changed

- **Shell wrapper** — `scripts/hyprdiscover` now bypasses single-instance
  enforcement for `--check` and `--status` CLI modes.
- **Backend install_updates** — uses `os.environ.copy()` for `LANG=C`
  instead of hardcoded `env` dict.

### Testing

- **62 unit tests** (up from 19) covering CLI status, argparse routing,
  background checking, package list selection, real-time progress
  streaming, cancel termination, and CANCELLED status preservation.

---

## [0.3.0] — 2026-06-02

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
