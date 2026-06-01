#!/usr/bin/env bash

set -e

echo "Installing HyprDiscover..."

# 1. Membuat direktori yang dibutuhkan
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
mkdir -p ~/.local/share/hyprdiscover

# 2. Bersihkan instalasi lama jika ada (agar tidak bentrok)
rm -rf ~/.local/share/hyprdiscover/*

# 3. Menyalin modul utama dan seluruh foldernya (core & ui)
install -m644 hyprdiscover.py ~/.local/share/hyprdiscover/hyprdiscover.py
cp -r core ~/.local/share/hyprdiscover/
cp -r ui ~/.local/share/hyprdiscover/

# Bersihkan __pycache__ hasil build lokal agar tidak mengotori system user
find ~/.local/share/hyprdiscover/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 4. Menyalin script executable pembungkus ke local bin
install -m755 scripts/hyprdiscover ~/.local/bin/hyprdiscover

# 5. Menyalin file Desktop Entry dan Icon Launcher
install -m644 assets/hyprdiscover.desktop ~/.local/share/applications/hyprdiscover.desktop
install -m644 assets/HyprDiscover.svg ~/.local/share/icons/hicolor/scalable/apps/hyprdiscover.svg

# 6. Update database desktop environment agar aplikasi langsung muncul di menu/launcher
update-desktop-database ~/.local/share/applications 2>/dev/null || true

echo "----------------------------------------"
echo "HyprDiscover installed successfully. 🎉"
echo
echo "Launch with:"
echo "  hyprdiscover"
echo "----------------------------------------"