# HyprDiscover Roadmap

## Current Status

**v0.4.0**

Implemented:

### Architecture
- Layered architecture: models → backends → services → ui
- `src/hyprdiscover/` layout (PEP 517)
- Backend abstraction (PackageManagerBackend ABC)
- Service layer (UpdateManager state machine)
- `pyproject.toml` build system
- TOML configuration file
- Structured logging
- RPM packaging spec (COPR-ready)
- CI pipeline (pytest, ruff, mypy)

### UI / UX
- GTK4 + Libadwaita interface with HeaderBar
- Summary card with category breakdown (security, bug fix, enhancement, other)
- Sortable four-column package table (icon, type, package, version)
- Nerd Font category icons
- Expandable package details with transaction logs
- Animated progress bar during updates
- Confirmation dialogs for destructive actions
- CSS stylesheet for theming

### Package Management
- PackageKit integration via `pkcon` subprocess
- NEVRA-based package name/version parsing
- Multi-word category detection ("Bug fix")
- Status line filtering
- Per-category update counts

### Desktop Integration
- Waybar JSON output mode (`--waybar`)
- CLI status output (`--status`, `--status --json`)
- Single-instance launcher with Hyprland window focus
- Desktop entry and SVG icon
- Desktop notifications (notify-send)
- Background update checking via systemd timer (`--check`)
- Autostart integration via Preferences
- Last checked timestamp

### Package Management
- PackageKit integration via `pkcon` subprocess
- NEVRA-based package name/version/arch parsing
- PackageKit ID (`name;version;arch;repo`) for multi-arch environments
- Multi-word category detection ("Bug fix")
- Status line filtering
- Per-category update counts
- Selective package updates with checkbox column
- Real-time progress reporting via Popen streaming
- Cancel update operation with proper state handling
- Typed error classification (NETWORK, AUTH, LOCK, CONFLICT, INTERNAL)

### Preferences & Configuration
- TOML configuration file
- Configuration GUI with instant-save (6 settings + Reset to Defaults)
- Accessibility labels on all interactive controls
- Tooltips on action buttons

### CLI
- Argparse command routing with `--help` support
- Waybar JSON mode, status text mode, status JSON mode, background check mode

### Testing & CI
- 86 unit tests covering models, enums, backends, services, CLI, UI, Unicode
- Test infrastructure with pytest + pytest-cov
- GitHub Actions: Ubuntu (3.12 + 3.13, ruff, mypy) + Fedora GTK container
- RPM packaging spec (COPR-ready)

---

## v0.4 — Desktop Integration ✅

Completed (2026-06-04):

- Background update checking via systemd timer
- Autostart `.desktop` file for session login
- Configuration GUI (preferences panel)
- Error classification (NetworkError, AuthError, LOCK, CONFLICT, INTERNAL)
- Accessibility pass (ATK labels, tooltips)
- Increased test coverage (19 → 86)

---

## v0.5 — Flatpak Support

Planned:

- Flatpak backend implementing `PackageManagerBackend` ABC
- Unified RPM + Flatpak update view
- Multi-backend merge in `UpdateManager`
- Flatpak package list with source column

---

## v0.6 — Native Backend

Planned:

- `PackageKitNativeBackend` using `gi.repository.PackageKitGlib`
- Real progress signals (percentage, elapsed, remaining)
- Cancellable transactions
- Structured error codes (no more text parsing)
- Remove `pkcon` subprocess dependency
- Online update mode with restart-required detection

---

## v0.7 — Offline Updates

Planned:

- PackageKit `PrepareOffline` workflow
- Systemd offline update service integration
- Reboot-and-install UI flow
- Update preparation status reporting

---

## v0.8 — Polish

Planned:

- Internationalization (gettext, Weblate)
- Full accessibility compliance
- UI refinements (responsive, error states)
- Package history and rollback (via PackageKit)
- Stability improvements

---

## v1.0 — Production Release

Goals:

- Stable update manager for Fedora Hyprland
- Native PackageKit D-Bus integration
- Flatpak support
- Offline updates
- Waybar + desktop integration
- COPR package repository
- Flathub submission
- Community documentation

Long-term vision:

Become the preferred update manager for Fedora Hyprland users.
