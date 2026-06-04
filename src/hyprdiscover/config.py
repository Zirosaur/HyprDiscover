from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


def _config_dir() -> Path:
    xdg = Path.home() / ".config" / "hyprdiscover"
    xdg.mkdir(parents=True, exist_ok=True)
    return xdg


@dataclass
class AppConfig:
    auto_refresh: bool = True
    refresh_interval_minutes: int = 60
    show_notifications: bool = True
    show_reboot_button: bool = True
    check_on_startup: bool = True
    waybar_interval: int = 3600
    backend_preference: str = "packagekit"
    log_level: str = "INFO"
    enable_flatpak: bool = False
    confirm_reboot: bool = True
    confirm_update: bool = False
    window_width: int = 700
    window_height: int = 500
    dark_mode: bool | None = None  # None = follow system

    def save(self, path: Path | None = None) -> None:
        import tomllib
        del tomllib  # unused in save path
        path = path or _config_dir() / "config.toml"
        path.write_text(self._to_toml())

    def _to_toml(self) -> str:
        lines = ["[hyprdiscover]"]
        for f_name, _f_value in self.__dataclass_fields__.items():
            val = getattr(self, f_name)
            if val is None:
                lines.append(f"{f_name} = \"\"")
            elif isinstance(val, bool):
                lines.append(f"{f_name} = {str(val).lower()}")
            elif isinstance(val, int):
                lines.append(f"{f_name} = {val}")
            else:
                lines.append(f"{f_name} = \"{val}\"")
        return "\n".join(lines) + "\n"


def load_config(config_path: Path | None = None) -> AppConfig:
    path = config_path or _config_dir() / "config.toml"

    if not path.exists():
        config = AppConfig()
        config.save(path)
        return config

    try:
        raw = tomllib.loads(path.read_text())
    except Exception:
        return AppConfig()

    toml_conf = raw.get("hyprdiscover", {})
    kwargs = {}
    for field_name in AppConfig.__dataclass_fields__:
        if field_name in toml_conf:
            kwargs[field_name] = toml_conf[field_name]
    return AppConfig(**kwargs)
