#!/usr/bin/env bash
set -e

echo "Installing HyprDiscover..."

APP_DIR="$HOME/.local/share/hyprdiscover"

mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
mkdir -p "$APP_DIR"

# Clean previous install
rm -rf "$APP_DIR"/*

# Copy source tree
cp -r src/hyprdiscover "$APP_DIR/"
cp pyproject.toml "$APP_DIR/"

# Copy wrapper entry point directly
cat > "$APP_DIR/hyprdiscover.py" << 'PYEOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, __import__("os").environ.get("HYPRDISCOVER_DIR",
    __import__("os").path.expanduser("~/.local/share/hyprdiscover")))
from hyprdiscover.__main__ import main
main()
PYEOF

# Clean pycache
find "$APP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Install launcher
install -m755 scripts/hyprdiscover ~/.local/bin/hyprdiscover

# Desktop entry
install -m644 assets/hyprdiscover.desktop ~/.local/share/applications/hyprdiscover.desktop
install -m644 assets/HyprDiscover.svg ~/.local/share/icons/hicolor/scalable/apps/hyprdiscover.svg

# CSS stylesheet
mkdir -p "$APP_DIR/styles"
install -m644 assets/styles/hyprdiscover.css "$APP_DIR/styles/"

# Update desktop database
update-desktop-database ~/.local/share/applications 2>/dev/null || true

echo "----------------------------------------"
echo "HyprDiscover installed successfully."
echo ""
echo "Launch with:"
echo "  hyprdiscover"
echo "  hyprdiscover --waybar"
echo "----------------------------------------"
