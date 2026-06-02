# Contributing to HyprDiscover

Thank you for your interest in contributing to HyprDiscover.

## Development Environment

Requirements:

- Fedora Linux
- Python 3.12+
- GTK4 + Libadwaita
- PyGObject
- PackageKit
- libnotify
- Nerd Fonts (recommended, for icons)

Clone the repository:

```bash
git clone git@github.com:Zirosaur/HyprDiscover.git
cd HyprDiscover
```

Install in development mode:

```bash
pip install -e ".[dev]"
```

Run the application:

```bash
hyprdiscover              # GUI
python -m hyprdiscover    # Alternative
hyprdiscover --waybar     # Waybar JSON output mode
```

## Project Structure

```
HyprDiscover/
├── pyproject.toml           # Build configuration, dependencies, tool settings
├── src/hyprdiscover/        # Application package (PEP 517 src/ layout)
│   ├── __init__.py          # Version
│   ├── __main__.py          # Entry point (GUI / --waybar dispatch)
│   ├── config.py            # TOML configuration management
│   ├── logging.py           # Structured logging setup
│   ├── models/              # Pure data models (dataclasses, enums)
│   ├── backends/            # Package management backend ABC + implementations
│   ├── services/            # Business logic (UpdateManager, notifications, etc.)
│   └── ui/                  # GTK4 presentation layer
│       ├── application.py   # Gtk.Application lifecycle
│       ├── window.py        # Main window layout
│       ├── widgets/         # Reusable widgets
│       └── dialogs/         # Dialog boxes
├── tests/                   # Pytest test suite
├── scripts/                 # Shell launcher + systemd units
├── assets/                  # Desktop file, icons, CSS, screenshots
├── packaging/               # RPM spec, COPR config
└── .github/workflows/       # CI pipeline
```

## Running Tests

```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=hyprdiscover       # With coverage report
pytest tests/unit/test_backends.py  # Specific test file
```

## Linting and Type Checking

```bash
ruff check src/                 # Lint with ruff
ruff format src/                # Auto-format
mypy src/hyprdiscover/          # Type check
```

## Reporting Bugs

When reporting bugs please include:

- Fedora version
- Hyprland version
- Python version
- Error logs (from stderr)
- Steps to reproduce

## Feature Requests

Feature requests are welcome.

Before creating a request:

- Check existing issues
- Describe the use case
- Explain why the feature is useful

## Pull Requests

Before submitting a pull request:

1. Run tests: `pytest`
2. Run linting: `ruff check src/`
3. Keep commits focused
4. Follow existing coding style
5. Update documentation when needed

Example:

```bash
git checkout -b feature/my-feature
# ... make changes ...
pytest && ruff check src/
git commit -m "Add feature"
git push origin feature/my-feature
```

## Coding Guidelines

- Python 3.12+
- PEP 8 via ruff
- Prefer readability over clever code
- Keep dependencies minimal
- Avoid unnecessary root operations
- Follow the layered architecture:
  - `models/` — pure data, zero external imports
  - `backends/` — implement PackageManagerBackend ABC
  - `services/` — orchestrate backends, own business logic
  - `ui/` — presentation only, never imports backends directly

## Architecture

```
User → GTK4 UI (ui/application.py, ui/window.py)
         │
         ▼
     services/update_manager.py  (state machine, threading)
         │
         ▼
     backends/PackageManagerBackend (ABC)
         │
         ├── PackageKitBackend (pkcon subprocess, interim)
         ├── FlatpakBackend       (planned v0.5)
         └── DNF5Backend          (future)
         │
         ▼
     models/package.py  (dataclasses, enums)
```

The UI layer never imports backends directly. All business logic flows through
the `UpdateManager` service, which operates on the backend via its abstract
interface. This enables backend swapping without UI changes.

## Project Principles

HyprDiscover aims to be:

- Fedora-first
- Hyprland-first
- Lightweight
- Secure
- Open source
- Community-driven

## Code of Conduct

Be respectful.

Constructive discussion and collaboration are encouraged.

Harassment, discrimination, and abusive behavior will not be tolerated.
