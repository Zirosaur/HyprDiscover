# HyprDiscover Security Model

## Security Philosophy

HyprDiscover tidak pernah berjalan sebagai root.

Semua operasi administratif dilakukan melalui PackageKit dan Polkit.

---

## Authentication

### Authorization Flow

HyprDiscover
→ PackageKit
→ Polkit
→ hyprpolkitagent
→ User Authentication
→ Authorization Granted

---

## Privilege Separation

### User Space

HyprDiscover berjalan sebagai user biasa.

Tidak memiliki akses langsung ke:

* RPM Database
* System Packages
* Root Filesystem

### Privileged Space

PackageKit daemon berjalan dengan hak akses sistem.

Hanya daemon yang diperbolehkan melakukan:

* Install package
* Remove package
* Offline update

---

## Offline Update Security

HyprDiscover menggunakan mekanisme resmi Fedora:

* PackageKit Offline Updates
* system-update.target
* systemd-system-update-generator

Keuntungan:

* Menghindari library replacement saat runtime
* Menghindari compositor crash
* Mengurangi risiko sistem tidak stabil

---

## Polkit Requirements

Minimal salah satu agent berikut harus tersedia:

* hyprpolkitagent
* polkit-kde-agent
* lxqt-policykit
* mate-polkit

Jika tidak ditemukan:

* Warning akan ditampilkan
* Operasi administratif akan diblokir

---

## Threat Model

### Protected Against

* Accidental privilege escalation
* Unauthorized package installation
* Package tampering through UI

### Not Intended To Protect Against

* Root compromise
* Malicious repositories
* Supply-chain attacks

Keamanan paket tetap bergantung pada Fedora, RPM, dan GPG signature verification.

---

## Secure Coding Principles

* No shell injection
* No root execution
* D-Bus based communication
* Asynchronous operations
* Principle of least privilege
