#!/usr/bin/env bash

set -e

echo "Installing HyprDiscover..."

mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
mkdir -p ~/.local/share/hyprdiscover

install -m644 \
    hyprdiscover.py \
    ~/.local/share/hyprdiscover/hyprdiscover.py

install -m755 \
    scripts/hyprdiscover \
    ~/.local/bin/hyprdiscover

install -m644 \
    assets/hyprdiscover.desktop \
    ~/.local/share/applications/hyprdiscover.desktop

install -m644 \
    assets/HyprDiscover.svg \
    ~/.local/share/icons/hicolor/scalable/apps/hyprdiscover.svg

update-desktop-database \
    ~/.local/share/applications \
    2>/dev/null || true

echo "HyprDiscover installed successfully."
echo
echo "Launch with:"
echo "  hyprdiscover"