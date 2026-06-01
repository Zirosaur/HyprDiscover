# HyprDiscover Product Requirements Document (PRD)

## Vision

HyprDiscover adalah update manager modern untuk Fedora Hyprland yang menyediakan pengalaman pembaruan sistem yang ringan, aman, cepat, dan terintegrasi tanpa memerlukan KDE Plasma atau GNOME Software.

Tujuan utama proyek adalah memberikan pengalaman pembaruan sistem yang setara dengan Discover atau GNOME Software, namun dirancang khusus untuk pengguna Hyprland.

---

## Problem Statement

Pengguna Fedora Hyprland saat ini harus:

* Menggunakan terminal untuk melakukan update sistem
* Mengingat perintah PackageKit atau DNF
* Membuka KDE Discover yang membawa dependensi KDE besar
* Tidak memiliki update manager native yang terintegrasi dengan Waybar dan Hyprland

---

## Target Users

### Primary Users

* Pengguna Fedora Hyprland
* Pengguna Waybar
* Pengguna PackageKit

### Secondary Users

* Pengguna Sway
* Pengguna River
* Pengguna Niri
* Pengguna compositor Wayland lainnya

---

## Product Goals

### Goal 1

Menyediakan antarmuka grafis untuk pembaruan RPM Fedora.

### Goal 2

Menyediakan integrasi Flatpak.

### Goal 3

Menyediakan offline updates yang aman.

### Goal 4

Terintegrasi dengan Waybar dan Hyprland.

### Goal 5

Menjadi update manager standar untuk Fedora Hyprland.

---

## Non Goals

HyprDiscover tidak bertujuan menjadi:

* App Store
* Software Center umum
* Pengganti penuh KDE Discover
* Pengganti DNF

Fokus utama adalah pembaruan sistem.

---

## MVP Features

### Update Detection

* Scan update PackageKit
* Menampilkan jumlah update

### Update Execution

* Menjalankan update sistem
* Menampilkan log transaksi

### Status Management

* Up To Date
* Updates Available
* Updating
* Update Completed
* Update Failed

### Reboot Integration

* Reboot setelah update selesai

---

## Future Features

### v0.2

* Better UI
* Scrollable logs
* Better error handling

### v0.3

* Package list view

### v0.4

* Waybar integration

### v0.5

* Flatpak support

### v0.6

* Native D-Bus PackageKit integration

### v0.7

* Offline updates

### v1.0

* Production-ready Fedora Hyprland Update Manager

---

## Success Criteria

Pengguna dapat:

1. Membuka HyprDiscover
2. Melihat update tersedia
3. Menginstal update
4. Melakukan reboot

Tanpa membuka terminal.
