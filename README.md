![GitHub release](https://img.shields.io/github/v/release/Zirosaur/HyprDiscover)
![License](https://img.shields.io/github/license/Zirosaur/HyprDiscover)
![GitHub stars](https://img.shields.io/github/stars/Zirosaur/HyprDiscover)

# HyprDiscover

A modern update manager for Fedora Hyprland.

HyprDiscover provides a lightweight graphical interface for managing system
updates on Fedora-based Hyprland systems without requiring KDE Plasma or
GNOME Software.

---

## Screenshot

![HyprDiscover](assets/main-window1.png)

---

## Features

- **GTK4 + Libadwaita** graphical interface
- **Summary card** — total updates, security, bug fixes, enhancements at a glance
- **Sortable package table** — four-column view (icon, type, package, version)
- **Category icons** — Nerd Font glyphs for security, bug fix, enhancement, other
- **PackageKit integration** — update detection and installation
- **Update log viewer** — expandable transaction details
- **Progress bar** — pulse animation during updates
- **Reboot button** — appears after successful updates
- **About dialog**
- **KDE Discover launcher** — fallback to Plasma's update tool
- **Waybar integration** — JSON output mode (`--waybar`) with update count indicator
- **Single-instance launcher** — shell wrapper with Hyprland focuswindow
- **Desktop notifications** — via `notify-send`
- **Configuration file** — TOML at `~/.config/hyprdiscover/config.toml`
- **Structured logging** — Python stdlib logging to stderr
- **Desktop entry** — application menu integration
- **SVG icon** — scalable application icon
- **CSS stylesheet** — GTK4 CSS provider for theming
- **Installation script** — quick user-space install to `~/.local/`

---

## Why HyprDiscover?

Fedora users running Hyprland often rely on:

- Terminal commands
- KDE Discover
- GNOME Software

HyprDiscover aims to provide a dedicated update manager designed specifically
for Hyprland environments.

The project focuses on:

- Simplicity
- Performance
- Fedora integration
- Hyprland integration
- Security

---

## Technology Stack

### User Interface

- Python 3.12+
- GTK4
- Libadwaita
- PyGObject

### Package Management

- PackageKit (via `pkcon` subprocess; native D-Bus planned for v0.6)

### System Integration

- systemd
- Polkit
- notify-send

### Desktop Integration

- Hyprland
- Waybar

---

## Installation

### Quick install (user-space)

```bash
git clone https://github.com/Zirosaur/HyprDiscover.git
cd HyprDiscover
chmod +x install.sh
./install.sh
```

Launch:

```bash
hyprdiscover
```

### Development install (pip)

```bash
git clone https://github.com/Zirosaur/HyprDiscover.git
cd HyprDiscover
pip install -e ".[dev]"
```

Run:

```bash
hyprdiscover              # GUI
hyprdiscover --waybar     # Waybar JSON output
hyprdiscover --status     # CLI status summary
hyprdiscover --status --json  # CLI status (JSON output)
python -m hyprdiscover    # Alternative entry point
```

Dependencies: `python3-gobject`, `gtk4`, `libadwaita`, `PackageKit`,
`libnotify`, `nerd-fonts` (or any font with Nerd Font glyphs for icons).

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
pkill waybar && waybar &
```

HyprDiscover provides a native Waybar output mode with JSON-formatted
update counts and does not require external update scripts.

---

## CLI Status Output

Check for available updates from the command line:

```bash
hyprdiscover --status
```

Example output:

```
Updates available: 12

Security: 2
Bug Fix: 5
Enhancement: 3
Other: 2

Last checked: 2026-06-03 12:45
```

Up-to-date systems show:

```
System up to date
Last checked: 2026-06-03 12:45
```

For automated scripts and integrations, use JSON output:

```bash
hyprdiscover --status --json
```

```json
{"up_to_date": false, "updates_available": 12, "security": 2, "bugfix": 5, "enhancement": 3, "other": 2, "last_checked": "2026-06-03T12:45:00"}
```

Exit codes:

- `0` — successful check (updates found or system up to date)
- `1` — error (unable to check for updates)

---

## Background Update Checking

HyprDiscover can periodically check for updates in the background using
a systemd user timer. When updates are available, a desktop notification
is sent.

### Enable the timer

```bash
# Install the systemd units
mkdir -p ~/.config/systemd/user/
cp assets/systemd/hyprdiscover-check.service ~/.config/systemd/user/
cp assets/systemd/hyprdiscover-check.timer ~/.config/systemd/user/
systemctl --user daemon-reload

# Enable and start the timer
systemctl --user enable --now hyprdiscover-check.timer
```

### Check timer status

```bash
systemctl --user status hyprdiscover-check.timer
systemctl --user list-timers
```

### Configuration

Background checking respects the following settings in
`~/.config/hyprdiscover/config.toml`:

```toml
[hyprdiscover]
auto_refresh = true            # Enable background checks
refresh_interval_minutes = 60  # Sync with timer OnUnitActiveSec
show_notifications = true      # Show desktop notifications
```

The timer runs every 60 minutes by default. To change the interval,
edit the timer unit:

```bash
systemctl --user edit hyprdiscover-check.timer
```

---

## Security

HyprDiscover never runs as root.

Administrative operations are delegated to:

- PackageKit
- Polkit
- systemd Offline Updates (planned)

This follows Fedora's recommended update workflow and minimizes privilege
escalation risks.

For more information see:

- SECURITY.md
- ARCHITECTURE.md

---

## Project Documentation

Additional documentation is available:

- PRD.md — product requirements
- ARCHITECTURE.md — architecture overview
- SECURITY.md — security model
- ROADMAP.md — planned releases
- CONTRIBUTING.md — contribution guide

---

## Target Platforms

### Primary Target

- Fedora Linux
- Hyprland

### Future Compatibility

- Sway
- Niri
- River
- Other Wayland compositors

---

## Status

Current development stage: **v0.3.0-dev**

Implemented:

- GTK4 interface with HeaderBar
- Summary card with category breakdown
- Sortable four-column package table
- PackageKit integration (pkcon backend)
- Update detection with NEVRA parsing
- Update installation with progress
- Transaction log viewer (expandable)
- Reboot integration with confirmation dialog
- About dialog, desktop entry, SVG icon
- Waybar JSON output mode
- Single-instance launcher
- Desktop notifications
- Configuration file (TOML)
- Structured logging
- CSS stylesheet for theming
- Test infrastructure (19 unit tests)
- CI pipeline (pytest, ruff, mypy)
- RPM packaging spec
- Modular architecture (models → backends → services → ui)

### Planned Features

#### v0.4

- Background update checking (systemd timer)
- Autostart support
- Configuration GUI panel
- Error classification

#### v0.5

- Flatpak support
- Multi-backend update merging

#### v0.6

- Native PackageKit D-Bus integration
- Real progress signals
- Cancellable transactions

#### v0.7

- Offline updates (systemd)
- Reboot-and-install workflow

#### v1.0

- Production-ready Fedora Hyprland update manager

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

This project is inspired by the simplicity of modern Linux update managers
while focusing specifically on the needs of Fedora Hyprland users.

HyprDiscover aims to provide a lightweight, native update experience without
requiring a full desktop environment.
