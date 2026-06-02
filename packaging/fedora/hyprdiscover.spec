%global pypi_name hyprdiscover
%global app_id com.hyprdiscover.app

Name:           %{pypi_name}
Version:        0.3.0
Release:        1%{?dist}
Summary:        Modern update manager for Fedora Hyprland

License:        GPL-3.0-only
URL:            https://github.com/Zirosaur/HyprDiscover
Source0:        https://github.com/Zirosaur/HyprDiscover/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

Requires:       python3 >= 3.12
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       PackageKit
Requires:       libnotify

%description
HyprDiscover is a modern, lightweight update manager for Fedora Linux
running the Hyprland Wayland compositor. It provides a native GTK4-based
GUI for managing system package updates via PackageKit.

Features:
- GTK4 + Libadwaita graphical interface
- PackageKit integration for RPM updates
- Waybar JSON output mode
- Desktop notifications
- Offline update preparation (planned)
- Flatpak support (planned)

%prep
%autosetup -n HyprDiscover-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

# Desktop integration
mkdir -p %{buildroot}%{_datadir}/applications
install -m644 assets/hyprdiscover.desktop %{buildroot}%{_datadir}/applications/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m644 assets/HyprDiscover.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

# CSS stylesheet
mkdir -p %{buildroot}%{_datadir}/%{pypi_name}/styles
install -m644 assets/styles/hyprdiscover.css %{buildroot}%{_datadir}/%{pypi_name}/styles/

%check
%pytest

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_datadir}/applications/hyprdiscover.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/%{pypi_name}/styles/hyprdiscover.css

%changelog
* Tue Jun 02 2026 HyprDiscover Team - 0.3.0-1
- Architecture restructure: src/ layout, models/backends/services/ui layers
- Backend ABC (PackageManagerBackend) with PackageKit implementation
- Summary card with category breakdown (security, bug fix, enhancement, other)
- Sortable four-column package table with separate column factories
- NEVRA-based package name/version parsing
- TOML configuration management
- Structured logging (Python stdlib)
- 19-unit test suite with pytest
- CI pipeline (GitHub Actions: pytest, ruff, mypy)
- GTK4 CSS stylesheet for theming
- Updated installation script

* Sun Jun 01 2026 HyprDiscover Team - 0.2.1-1
- Initial RPM packaging
