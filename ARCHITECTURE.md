# HyprDiscover Architecture

## Overview

HyprDiscover uses a **layered architecture** with strict dependency direction:

```
models → backends → services → ui
```

Each layer only depends on layers to its left. The UI never imports backends
directly. All business logic flows through services.

## Directory Structure

```
src/hyprdiscover/
├── __init__.py              # __version__
├── __main__.py              # Entry point (GUI / --waybar)
├── config.py                # TOML configuration (AppConfig)
├── logging.py               # Structured logging
│
├── models/                  # Pure data — zero external imports
│   ├── enums.py             # UpdateCategory, UpdateStatus, BackendType
│   └── package.py           # Package, UpdateResult, UpdateProgress dataclasses
│
├── backends/                # Package manager abstraction
│   ├── base.py              # PackageManagerBackend (ABC)
│   └── packagekit.py        # PackageKitBackend (pkcon subprocess, interim)
│
├── services/                # Business logic orchestration
│   ├── update_manager.py    # UpdateManager (state machine, threading)
│   ├── notifications.py     # NotificationService (notify-send wrapper)
│   ├── reboot.py            # reboot_system() helper
│   └── waybar.py            # CLI JSON output for Waybar
│
└── ui/                      # GTK4 presentation — never imports backends
    ├── application.py       # HyprDiscoverApplication (lifecycle, D-Bus)
    ├── window.py            # MainWindow (widget assembly)
    ├── widgets/
    │   ├── summary_card.py  # UpdateSummaryView (icon + headline + category grid)
    │   ├── package_list.py  # PackageListView (sortable ColumnView with PackageRow adapter)
    │   ├── update_log.py    # UpdateLogView (scrolled monospace text)
    │   ├── progress_bar.py  # AnimatedProgressBar
    │   └── status_header.py # StatusHeader (legacy, kept for compatibility)
    └── dialogs/
        ├── about.py         # Gtk.AboutDialog
        └── confirm.py       # Gtk.MessageDialog confirmation
```

## Layer Responsibilities

### Models (`models/`)

Pure Python data. Zero GTK imports, zero backend imports. Can be tested with
plain `pytest` — no display needed.

- `Package` — dataclass: name, package_id, version, category, summary, size
- `UpdateResult` — dataclass: success, message, requires_reboot, packages_updated
- `UpdateProgress` — dataclass: status, percentage, package, message
- `UpdateCategory` — StrEnum: security, bugfix, enhancement, blocked, unknown
- `UpdateStatus` — StrEnum: checking, up_to_date, updates_available, updating, success, failed, reboot_required, cancelled, error

### Backends (`backends/`)

Implements `PackageManagerBackend` ABC. Each backend is a swappable data
source for package operations.

Current implementations:
- **PackageKitBackend** — Uses `pkcon` subprocess (interim). Parses
  space-aligned `pkcon get-updates` output with NEVRA regex. Handles
  Security, Bug Fix, Enhancement, and Available categories.

Planned:
- **FlatpakBackend** — Using `gi.repository.Flatpak` (v0.5)
- **PackageKitNativeBackend** — Using `gi.repository.PackageKitGlib` (v0.6)
- **DNF5Backend** — Direct DNF5 integration (future)

### Services (`services/`)

Orchestrates backends. Owns the update lifecycle state machine.

- **UpdateManager** — Thread-safe state machine. Manages refresh/install
  lifecycle. Exposes category counts (security_count, bugfix_count, etc.)
  and package list. Emits status change callbacks for the UI.

- **NotificationService** — Sends desktop notifications via `notify-send`.
  Degrades silently if not available.

- **Waybar module** — CLI handler for `--waybar` flag. Uses backend directly
  (not UpdateManager) to minimize startup time. Never imports GTK.

### UI (`ui/`)

GTK4 + Libadwaita widgets. Presentation only — never calls backends.

- **HyprDiscoverApplication** — Gtk.Application subclass. Handles lifecycle,
  D-Bus single-instance enforcement, CSS loading, keyboard accelerators.

- **MainWindow** — Gtk.ApplicationWindow with HeaderBar. Layout:
  ```
  ┌─ HeaderBar: title | [Open Discover] [Menu] ─┐
  ├─ Summary card (icon, headline, category grid)┤
  ├─ Progress bar (hidden → visible during update)┤
  ├─ Action bar: [Refresh] [Update All] [Reboot] ┤
  └─ Expander: Package Details (collapsed)       ┘
  ```

- **UpdateSummaryView** — Card with large Nerd Font icon, headline text,
  and two-column category grid (Security/Bug Fix | Enhancement/Other).

- **PackageListView** — Sortable four-column ColumnView with separate
  SignalListItemFactory per column. Uses PackageRow GObject adapter to
  bridge dataclasses into Gio.ListStore.

## Data Flow

### Refresh Updates

```
User clicks Refresh
  → MainWindow._async_refresh()  [background thread]
    → UpdateManager.refresh()
      → PackageKitBackend.refresh_cache()
      → PackageKitBackend.get_updates()
        → subprocess: pkcon get-updates
        → _parse_update_list()  [NEVRA regex + category matching]
        → List[Package]
    → UpdateManager._set_status(UPDATES_AVAILABLE or UP_TO_DATE)
    → callback → MainWindow._on_status_changed()
      → GLib.idle_add(UpdateSummaryView.show_updates_available())
      → GLib.idle_add(PackageListView.set_packages())
```

### Install Updates

```
User clicks Update All
  → MainWindow._async_install()  [confirmation dialog if configured]
    → summary: show_updating()
    → progress: visible + pulse animation
    → background thread:
      → UpdateManager.install_updates()
        → PackageKitBackend.install_updates()
          → subprocess: pkcon update -y
          → UpdateResult
      → GLib.idle_add: stop progress, update summary
      → GLib.idle_add: log_view.set_text() if message
      → GLib.idle_add: reboot_btn.set_visible() if reboot required
```

### Waybar Mode

```
hyprdiscover --waybar
  → __main__.py: run_waybar()
    → PackageKitBackend.get_update_count()  [no GTK import, fast startup]
    → json.dumps({"text": "󰚰 N", "tooltip": "...", "class": "..."})
    → stdout
```

## PackageKit Backend: pkcon Parsing

The interim backend runs `pkcon get-updates` (LANG=C) and parses
space-aligned output:

```
Security     samba-2:4.24.3-1.fc44.x86_64     (updates)
Bug fix      cracklib-2.10.3-1.fc44.x86_64    (updates)
Enhancement  at-spi2-atk-2.60.4-1.fc44.x86_64 (updates)
Available    aquamarine-0.12.0-1.fc44.x86_64  (copr:...:hyprland)
```

The parser:
1. Matches category labels as line prefixes (handles multi-word "Bug fix")
2. Extracts NEVRA string (name-version-release.arch)
3. Uses regex to split NEVRA into `name` and `version` components
4. Filters status/transaction lines (Status:, Transaction:, etc.)
5. Classifies categories: Security, Bug Fix, Enhancement, Other

## Threading Model

All PackageKit operations run on background `threading.Thread` (daemon).
GTK UI updates are dispatched via `GLib.idle_add()` to ensure thread safety.

Progress bar uses `GLib.timeout_add(100, pulse)` for animation during updates.
The pulse source is stopped when the update completes.

## Configuration

User configuration is stored at `~/.config/hyprdiscover/config.toml`:

```toml
[hyprdiscover]
auto_refresh = true
refresh_interval_minutes = 60
show_notifications = true
show_reboot_button = true
check_on_startup = true
enable_flatpak = false
confirm_reboot = true
confirm_update = false
window_width = 700
window_height = 500
```

Default values are used if the file doesn't exist. The file is created
automatically on first run.
