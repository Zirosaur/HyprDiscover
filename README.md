# HyprDiscover

A modern update manager for Fedora Hyprland.

HyprDiscover provides a lightweight graphical interface for managing system updates on Fedora-based Hyprland systems without requiring KDE Plasma or GNOME Software.

The goal of this project is to deliver a native, simple, and efficient update experience tailored specifically for Hyprland users.

---

## Features

### Current Features

* GTK4-based graphical interface
* PackageKit integration
* Update detection
* Update installation
* Transaction log viewer
* Scrollable update logs
* Update status reporting
* Button state management during updates
* Reboot button after successful updates
* About dialog
* KDE Discover integration
* Native Waybar integration
* Waybar JSON output mode (`--waybar`)
* Single-instance launcher

---

## Screenshot

![HyprDiscover](assets/main-window.png)

---

## Why HyprDiscover?

Fedora users running Hyprland often rely on:

* Terminal commands
* KDE Discover
* GNOME Software

HyprDiscover aims to provide a dedicated update manager designed specifically for Hyprland environments.

The project focuses on:

* Simplicity
* Performance
* Fedora integration
* Hyprland integration
* Security

---

## Technology Stack

### User Interface

* Python
* GTK4
* PyGObject

### Package Management

* PackageKit

### System Integration

* systemd
* Polkit

### Desktop Integration

* Hyprland
* Waybar

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Zirosaur/HyprDiscover.git
cd HyprDiscover
```

Install launcher:

```bash
./install.sh
```

Launch application:

```bash
hyprdiscover
```

---

## Waybar Integration

Add the following module to your Waybar configuration:

```json
"custom/updates": {
    "exec": "hyprdiscover --waybar",
    "return-type": "json",
    "format": "{}",
    "on-click": "hyprdiscover",
    "interval": 3600,
    "tooltip": true
}
```

Reload Waybar:

```bash
pkill waybar
waybar &
```

---

## Security

HyprDiscover never runs as root.

Administrative operations are delegated to:

* PackageKit
* Polkit
* systemd Offline Updates

This follows Fedora's recommended update workflow and minimizes privilege escalation risks.

For more information see:

* SECURITY.md
* ARCHITECTURE.md

---

## Project Documentation

Additional documentation is available:

* PRD.md
* ARCHITECTURE.md
* SECURITY.md
* ROADMAP.md
* CONTRIBUTING.md

---

## Target Platforms

### Primary Target

* Fedora Linux
* Hyprland

### Future Compatibility

* Sway
* Niri
* River
* Other Wayland compositors

---

## Status

Current development stage:

**v0.2.0-dev**

Implemented:

* Update detection
* Update installation
* Transaction logging
* PackageKit integration
* Reboot integration
* About dialog
* Native Waybar integration
* Single-instance launcher
* Installation script

Development is active and new features are planned for future releases.

---

## Planned Features

### v0.3

* Package list view
* Update categories
* Package size information
* Better package details

### v0.4

* Desktop notifications
* Automatic update checks
* Background refresh

### v0.5

* Flatpak support
* Unified update view

### v0.6

* Native PackageKit D-Bus integration
* Removal of pkcon dependency

### v0.7

* Offline updates
* Reboot-and-install workflow

### v1.0

* Production-ready Fedora Hyprland update manager

---

## License

HyprDiscover is licensed under the GNU General Public License v3.0 (GPLv3).

See the LICENSE file for the full license text.

---

## Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

Please read CONTRIBUTING.md before submitting changes.

---

## Acknowledgements

This project is inspired by the simplicity of modern Linux update managers while focusing specifically on the needs of Fedora Hyprland users.

HyprDiscover aims to provide a lightweight, native update experience without requiring a full desktop environment.
