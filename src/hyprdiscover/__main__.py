#!/usr/bin/env python3

import sys

from hyprdiscover.services.waybar import run_waybar
from hyprdiscover.ui.application import HyprDiscoverApplication


def main() -> None:
    if "--waybar" in sys.argv or "-w" in sys.argv:
        run_waybar()
        return

    app = HyprDiscoverApplication()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
