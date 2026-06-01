# HyprDiscover Architecture

## Overview

HyprDiscover menggunakan arsitektur client-daemon.

Frontend GTK4 berkomunikasi dengan PackageKit melalui D-Bus untuk menjalankan transaksi sistem.

---

## High Level Architecture

User
↓
GTK4 + Libadwaita
↓
PackageKit D-Bus
↓
packagekitd
↓
RPM Database

---

## Components

### UI Layer

Technology:

* GTK4
* Libadwaita
* PyGObject

Responsibilities:

* Rendering UI
* Showing logs
* Showing progress
* User interaction

---

### Package Management Layer

Technology:

* PackageKit
* PackageKitGlib

Responsibilities:

* Query updates
* Download updates
* Install updates
* Offline update preparation

---

### Flatpak Layer

Technology:

* libflatpak

Responsibilities:

* Runtime updates
* Application updates

---

### System Integration Layer

Technology:

* systemd
* D-Bus
* Polkit

Responsibilities:

* Offline updates
* Authentication
* Reboot handling

---

### Waybar Integration

Technology:

* JSON output
* Systemd timer

Responsibilities:

* Background update checks
* Update count indicator
* Click-to-open integration

---

## Data Flow

Refresh Updates

User
→ HyprDiscover
→ PackageKit
→ packagekitd
→ Repository Metadata
→ UI

Install Updates

User
→ HyprDiscover
→ PackageKit
→ Polkit
→ packagekitd
→ RPM Transaction
→ UI

Offline Updates

User
→ HyprDiscover
→ PackageKit
→ /system-update
→ Reboot
→ system-update.target
→ Installation
→ Reboot
