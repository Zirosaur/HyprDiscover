# HyprDiscover

A modern update manager for Fedora Hyprland.

HyprDiscover provides a lightweight graphical interface for managing system updates on Fedora-based Hyprland systems without requiring KDE Plasma or GNOME Software.

The goal of this project is to deliver a native, simple, and efficient update experience tailored specifically for Hyprland users.

---

## Features

### Current Features

* GTK4-based graphical interface
* PackageKit integration
* Check available system updates
* Install updates directly from the GUI
* Update status reporting
* Transaction log viewer
* Reboot button after successful updates
* KDE Discover integration
* Waybar integration support

---

## Planned Features

### v0.2

* Improved user interface
* Scrollable update logs
* Better error handling
* Button state management during updates

### v0.3

* Package list view
* Update categories
* Update size information

### v0.4

* Native Waybar integration
* Desktop notifications

### v0.5

* Flatpak update support

### v0.6

* Native PackageKit D-Bus integration
* Removal of pkcon dependency

### v0.7

* Offline updates

### v1.0

* Production-ready Fedora Hyprland update manager

---

## Screenshot

![HyprDiscover](assets/main-window.png)

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

* README.md
* PRD.md
* ARCHITECTURE.md
* SECURITY.md

---

## Target Platforms

Primary target:

* Fedora Linux
* Hyprland

Future compatibility:

* Sway
* River
* Niri
* Other Wayland compositors

---

## Status

Current development stage:

**MVP (Minimum Viable Product)**

Implemented:

* Update checking
* Update installation
* Status reporting
* Reboot integration

Development is active and new features are being added regularly.

---

## ## License

HyprDiscover is licensed under the GNU General Public License v3.0 (GPLv3).

See the [LICENSE](LICENSE) file for the full license text.

---

## Project Documentation

Additional documentation is available:

* [PRD.md](PRD.md) – Product Requirements Document
* [ARCHITECTURE.md](ARCHITECTURE.md) – System architecture and design
* [SECURITY.md](SECURITY.md) – Security model and privilege management
* [ROADMAP.md](ROADMAP.md) – Development roadmap
* [CONTRIBUTING.md](CONTRIBUTING.md) – Contribution guidelines

---

## Status

Current development stage:

**v0.1.0 – MVP (Minimum Viable Product)**

Implemented:

* Update detection
* Update installation
* Transaction logging
* PackageKit integration
* Reboot integration
* KDE Discover integration
* Waybar integration support

Development is active and new features are planned for upcoming releases.

---

## Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

---

## Acknowledgements

This project is inspired by the simplicity of modern Linux update managers while focusing specifically on the needs of Fedora Hyprland users.

HyprDiscover aims to provide a lightweight, native update experience without requiring a full desktop environment.
