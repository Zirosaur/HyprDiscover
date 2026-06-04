from __future__ import annotations

from pathlib import Path

_AUTOSTART_DIR = Path.home() / ".config" / "autostart"
_AUTOSTART_FILE = _AUTOSTART_DIR / "hyprdiscover.desktop"

_AUTOSTART_CONTENT = """\
[Desktop Entry]
Type=Application
Name=HyprDiscover
Comment=Modern update manager for Fedora Hyprland
Exec=hyprdiscover
Icon=hyprdiscover
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""


def enable_autostart() -> None:
    _AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
    _AUTOSTART_FILE.write_text(_AUTOSTART_CONTENT)


def disable_autostart() -> None:
    _AUTOSTART_FILE.unlink(missing_ok=True)


def is_autostart_enabled() -> bool:
    return _AUTOSTART_FILE.exists()
