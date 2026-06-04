# HyprDiscover Product Requirements Document (PRD)

## Vision

HyprDiscover helps Fedora users make correct software decisions
without needing to understand RPM, Flatpak, COPR, or any other
packaging system.

It recommends the right installation method, explains why, and
provides tools to install, update, and remove software securely.

---

## Problem Statement

The Linux packaging ecosystem is fragmented. On Fedora alone, users
encounter RPM repositories, Flatpak, COPR, AppImage, and more. Each
has different characteristics:

- RPM packages integrate with the system but can conflict
- Flatpak offers sandboxing but bundles entire runtimes
- COPR provides community packages but varies in trust and maintenance
- AppImage is portable but has no update mechanism

Fedora users are expected to understand these differences and make
informed decisions. Most cannot.

The result:

- Users install from the wrong source and encounter problems later
- Users cannot cleanly uninstall software they no longer need
- Users see update discrepancies between tools and don't know why
- Users follow terminal commands from blog posts without understanding them

---

## Target Users

### Primary Persona: The Fedora Beginner

A Fedora user who is comfortable using their computer but does not
understand Linux packaging. They want to install software safely and
keep it updated without becoming a system administrator.

Pain points:

- "I found this app — should I use Flatpak or RPM?"
- "What is COPR? Is it safe to install from there?"
- "Discover shows updates but HyprDiscover doesn't. Why?"
- "How do I remove this completely without leaving config files?"

### Secondary Persona: The Hyprland Enthusiast

An existing HyprDiscover user. Uses Hyprland as their daily driver.
Values lightweight tools, Waybar integration, CLI modes, and
background update checking. Wants control without complexity.

### Tertiary Persona: The Minimalist

A Fedora user who avoids GNOME Software and KDE Discover entirely.
Uses the terminal for most tasks but wants a lightweight GUI for
software management. Values speed, simplicity, and explanations
over catalogs and screenshots.

---

## Product Goals

### Goal 1: Source Intelligence

Help users understand where their software comes from and which
source is recommended for each package.

### Goal 2: Unified Management

Provide a single view for RPM, Flatpak, and COPR software — updates,
installation, and removal — without requiring users to switch between
tools.

### Goal 3: Guided Decisions

Recommend the correct installation method with plain-language
explanations. Users should not need to understand packaging systems
to make good choices.

### Goal 4: Clean Lifecycle

Support the full software lifecycle: discover → install → update →
remove. Clean uninstallation removes configuration and application
data, not just the package.

### Goal 5: Lightweight & Portable

Remain a lightweight GTK4 application that works on any Wayland
compositor or desktop environment on Fedora. No DE dependency.

---

## Guidance Philosophy

HyprDiscover recommends. You decide.

Every recommendation comes with an explanation. The system never
hides options — it presents the recommended choice alongside
alternatives, with clear reasoning for each.

HyprDiscover doesn't show you everything.
It shows you what matters.

---

## Non-Goals

HyprDiscover explicitly does NOT aim to be:

- **An app store catalog** — no browsing thousands of applications.
  HyprDiscover helps with the software you already know you want.

- **A screenshot gallery** — no rich media hosting. Guidance is
  text-based: explanations, not eye candy.

- **A ratings and reviews platform** — no user-generated content,
  no star ratings, no comment moderation.

- **A replacement for DNF or flatpak CLI** — complementary, not
  competitive. Power users can always drop to the terminal.

- **A cross-distribution tool** — Fedora only. The architecture
  supports other distributions via the `PackageManagerBackend` ABC,
  but the project ships and maintains Fedora backends only.

- **An AppImage repository** — no AppImageHub integration, no
  AppImage update management. HyprDiscover may detect installed
  AppImages and recommend alternatives (e.g., "Use the Flatpak
  version instead"), but will not manage AppImages directly.

- **A Snap manager** — Snap is Canonical-specific and not relevant
  to Fedora users.

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

The MVP (v0.1–v0.2) delivered basic update detection and execution.
See CHANGELOG.md for full release history.

---

## Roadmap

### v0.5 — Flatpak Integration (Foundation)

- Flatpak backend implementing `PackageManagerBackend` ABC
- Unified RPM + Flatpak update view
- Source column in package list (RPM / Flatpak / COPR)
- Multi-backend merge in `UpdateManager`

### v0.6 — Recommendation Engine (The Differentiator)

- Installation method recommendations (Flatpak vs RPM vs COPR)
- Explanation text for each recommendation
- COPR trust indicators
- Update discrepancy explanations between sources
- Update context (requires reboot, Flatpak runtime, advisory info)
- Native PackageKit D-Bus backend (real progress, structured errors)

### v0.7 — Software Discovery

- Package search across RPM + Flatpak
- "How to install" guidance with recommended method
- Install/uninstall via PackageKit + Flatpak backend
- Installed-software inventory with source annotations

### v0.8 — Software Lifecycle

- Clean uninstall (remove configs + application data)
- Package history/timeline
- Disk usage per application
- Export/import installed package list
- Offline updates via systemd

### v0.9 — Polish

- Internationalization (gettext, Weblate)
- Full accessibility compliance
- Keyboard-first navigation
- UI refinements (responsive, error states)
- Stability improvements

### v1.0 — Production Release

- Stable software guidance tool for Fedora
- Native PackageKit D-Bus integration
- Flatpak support with unified view
- COPR package repository
- Flathub submission
- Community documentation

---

## Success Criteria

Users can:

1. Open HyprDiscover and see available updates from all sources
2. Understand where each update comes from and why it matters
3. Receive a recommendation when multiple installation methods exist
4. Install software using the recommended method
5. Remove software cleanly, including configuration and data
6. Do all of the above without opening a terminal or reading documentation
