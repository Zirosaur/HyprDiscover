#!/usr/bin/env python3

import argparse
import sys

from hyprdiscover.services.background import run_background_check
from hyprdiscover.services.cli_status import run_status
from hyprdiscover.services.waybar import run_waybar
from hyprdiscover.ui.application import HyprDiscoverApplication


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hyprdiscover",
        description="Modern update manager for Fedora Hyprland",
    )
    parser.add_argument(
        "--waybar", "-w",
        action="store_true",
        help="Waybar JSON output mode",
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show update status summary",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (use with --status)",
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Background update check (for systemd timer)",
    )
    args, remaining = parser.parse_known_args()

    if args.waybar:
        run_waybar()
        return

    if args.status:
        sys.exit(run_status(json_output=args.json))

    if args.check:
        sys.exit(run_background_check())

    app = HyprDiscoverApplication()
    sys.exit(app.run([sys.argv[0]] + remaining))


if __name__ == "__main__":
    main()
