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

### UI / UX
- GTK4 + Libadwaita interface with HeaderBar
- Summary card with category breakdown (security, bug fix, enhancement, other)
- Sortable package table with checkboxes for selective updates
- Nerd Font category icons
- Expandable package details with transaction logs
- Real-time progress reporting via Popen streaming
- Confirmation dialogs for destructive actions
- CSS stylesheet for theming
- Accessibility labels on all interactive controls
- Tooltips on action buttons

### Package Management
- PackageKit integration via `pkcon` subprocess
- NEVRA-based package name/version/arch parsing
- PackageKit ID (`name;version;arch;repo`) for multi-arch environments
- Multi-word category detection ("Bug fix")
- Status line filtering
- Per-category update counts
- Selective package updates with checkbox column
- Cancel update operation with proper state handling
- Typed error classification (NETWORK, AUTH, LOCK, CONFLICT, INTERNAL)

### Desktop Integration
- Waybar JSON output mode (`--waybar`)
- CLI status output (`--status`, `--status --json`)
- Single-instance launcher with Hyprland window focus
- Desktop entry and SVG icon
- Desktop notifications (notify-send)
- Background update checking via systemd timer (`--check`)
- Autostart integration via Preferences
- Last checked timestamp

### Preferences & Configuration
- TOML configuration file
- Configuration GUI with instant-save (6 settings + Reset to Defaults)

### CLI
- Argparse command routing with `--help` support
- Waybar JSON mode, status text mode, status JSON mode, background check mode

### Testing & CI
- 86 unit tests covering models, enums, backends, services, CLI, UI, Unicode
- Test infrastructure with pytest + pytest-cov
- GitHub Actions: Ubuntu (3.12 + 3.13, ruff, mypy) + Fedora GTK container

---

## v0.4 — Desktop Integration ✅

Completed (2026-06-04):

- Background update checking via systemd timer
- Autostart `.desktop` file for session login
- Configuration GUI (preferences panel)
- Error classification (NETWORK, AUTH, LOCK, CONFLICT, INTERNAL)
- Accessibility pass (ATK labels, tooltips)
- Increased test coverage (19 → 86)

---

## v0.5 — Flatpak Integration

Foundation for multi-source awareness.

Planned:

- Flatpak backend implementing `PackageManagerBackend` ABC
- Unified RPM + Flatpak update view
- Source column in package list (RPM / Flatpak / COPR)
- Multi-backend merge in `UpdateManager`

Users will see where each update originates — the first step
toward informed software decisions.

---

## v0.6 — Recommendation Engine

The differentiator. Guidance becomes a feature.

Planned:

- Installation method recommendations (Flatpak vs RPM vs COPR)
- Explanation text for each recommendation
- COPR trust indicators
- Update discrepancy explanations between sources
- Update context (requires reboot, Flatpak runtime, advisory info)
- Native PackageKit D-Bus backend
  - Real progress signals (percentage, elapsed, remaining)
  - Structured error codes (no more text parsing)
  - Removes `pkcon` subprocess dependency

---

## v0.7 — Software Discovery

Builds on recommendation data to help users find software.

Planned:

- Package search across RPM + Flatpak
- "How to install" guidance with recommended method
- Install/uninstall via PackageKit + Flatpak backend
- Installed-software inventory with source annotations

---

## v0.8 — Software Lifecycle

Closes the loop: discover → install → update → remove.

Planned:

- Clean uninstall (remove configs + application data)
- Package history/timeline
- Disk usage per application
- Export/import installed package list
- Offline updates via systemd
- Reboot-and-install workflow

---

## v0.9 — Polish

Planned:

- Internationalization (gettext, Weblate)
- Full accessibility compliance
- Keyboard-first navigation
- UI refinements (responsive, error states)
- Stability improvements

---

## v1.0 — Production Release

Goals:

- Stable software guidance tool for Fedora
- Native PackageKit D-Bus integration
- Flatpak support with unified multi-source view
- Recommendation engine
- Full lifecycle: install, update, uninstall
- COPR package repository
- Flathub submission
- Community documentation

Long-term vision:

Help Fedora users make the right software decisions —
without becoming packaging experts.
