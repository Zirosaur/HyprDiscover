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

## Current Features (v0.3.0-dev)

Beyond the MVP, the following features have been implemented:

- Summary card with category breakdown (security, bug fix, enhancement, other)
- Sortable four-column package table (icon, type, package, version)
- NEVRA-based package name/version parsing
- Configuration management (TOML)
- Waybar JSON output mode
- Desktop notifications
- Single-instance launcher with Hyprland window focus
- Test infrastructure (19 unit tests)
- CI pipeline (pytest, ruff, mypy)
- RPM packaging spec

---

## Future Features

### v0.4

- Background update checking (systemd timer)
- Autostart support
- Configuration GUI
- Error classification

### v0.5

- Flatpak support
- Unified RPM + Flatpak update view

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
