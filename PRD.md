# HyprDiscover Product Requirements Document (PRD)

## Vision

HyprDiscover is a modern update manager for Fedora Hyprland that provides a
lightweight, secure, fast, and integrated system update experience without
requiring KDE Plasma or GNOME Software.

The primary goal is to deliver an update experience comparable to Discover
or GNOME Software, but designed specifically for Hyprland users.

---

## Problem Statement

Fedora Hyprland users currently must:

- Use the terminal to perform system updates
- Remember PackageKit or DNF commands
- Install KDE Discover (which pulls in large KDE dependencies)
- Go without a native update manager integrated with Waybar and Hyprland

---

## Target Users

### Primary Users

- Fedora Hyprland users
- Waybar users
- PackageKit users

### Secondary Users

- Sway users
- River users
- Niri users
- Other Wayland compositor users

---

## Product Goals

### Goal 1

Provide a graphical interface for Fedora RPM updates.

### Goal 2

Provide Flatpak integration.

### Goal 3

Provide secure offline updates.

### Goal 4

Integrate with Waybar and Hyprland.

### Goal 5

Become the standard update manager for Fedora Hyprland.

---

## Non-Goals

HyprDiscover is not intended to be:

- An app store
- A general software center
- A full replacement for KDE Discover
- A replacement for DNF

The core focus is system updates.

---

## MVP Features

### Update Detection

- Scan for PackageKit updates
- Display the number of available updates

### Update Execution

- Install system updates
- Display transaction logs

### Status Management

- Up to date
- Updates available
- Updating
- Update completed
- Update failed

### Reboot Integration

- Reboot after update completion

---

## Current Features (v0.4.0)

- GTK4 + Libadwaita graphical interface
- Summary card with category breakdown (security, bug fix, enhancement, other)
- Sortable package table with checkboxes for selective updates
- Real-time progress streaming during updates
- Cancel update operation
- Configuration GUI (Preferences window with instant-save)
- XDG autostart integration (opt-in)
- Typed error classification (Network, Auth, Lock, Conflict, Internal)
- Accessibility labels on all interactive controls
- Tooltips on action buttons
- NEVRA-based package name/version/arch parsing
- Background update checking via systemd timer
- CLI status output (--status, --status --json)
- Waybar JSON output mode
- Desktop notifications
- Single-instance launcher with Hyprland window focus
- Configuration management (TOML)
- Test infrastructure (86 unit tests, 44% coverage)
- CI pipeline: Ubuntu (pytest, ruff, mypy) + Fedora GTK container
- RPM packaging spec (COPR-ready)

---

## Future Features

### v0.5

- Flatpak support
- Unified RPM + Flatpak update view
- Multi-backend merge

### v0.6

- Native PackageKit D-Bus integration
- Real progress signals
- Cancellable transactions

### v0.7

- Offline updates via systemd
- Reboot-and-install workflow

### v1.0

- Production-ready Fedora Hyprland update manager in COPR and Flathub

---

## Success Criteria

Users can:

1. Open HyprDiscover
2. View available updates
3. Install updates
4. Reboot when required

All without opening a terminal.
