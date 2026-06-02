# HyprDiscover Security Model

## Security Philosophy

HyprDiscover never runs as root.

All administrative operations are delegated to PackageKit and Polkit.

---

## Authentication

### Authorization Flow

```
HyprDiscover
  → PackageKit
    → Polkit
      → hyprpolkitagent (or other polkit agent)
        → User Authentication
          → Authorization Granted
```

---

## Privilege Separation

### User Space

HyprDiscover runs as a regular user process.

It has no direct access to:

- RPM database
- System packages
- Root filesystem

### Privileged Space

The PackageKit daemon (`packagekitd`) runs with system privileges.

Only the daemon is authorized to:

- Install packages
- Remove packages
- Prepare offline updates

---

## Offline Update Security

HyprDiscover is designed to use Fedora's official offline update mechanism:

- PackageKit Offline Updates
- `system-update.target`
- `systemd-system-update-generator`

Benefits:

- Avoids in-place library replacement while the system is running
- Prevents compositor crashes during updates
- Reduces the risk of system instability

Note: Offline update workflow is planned for v0.7. Currently updates are
installed online via `pkcon update`.

---

## Polkit Requirements

At least one of the following polkit authentication agents must be available:

- hyprpolkitagent
- polkit-kde-agent
- lxqt-policykit
- mate-polkit

If no agent is found:

- A warning may be displayed
- Administrative operations requiring authentication will be blocked

---

## Threat Model

### Protected Against

- Accidental privilege escalation
- Unauthorized package installation
- Package tampering through the UI

### Not Intended to Protect Against

- Root compromise
- Malicious repositories
- Supply-chain attacks

Package security ultimately depends on Fedora's infrastructure, RPM, and
GPG signature verification.

---

## Secure Coding Principles

- No shell injection
- No root execution
- PackageKit-mediated system operations (pkcon subprocess; native D-Bus planned)
- Thread-safe UI updates via `GLib.idle_add()`
- Principle of least privilege
