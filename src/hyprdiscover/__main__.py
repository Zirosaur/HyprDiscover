#!/usr/bin/env python3

import sys

from hyprdiscover.services.cli_status import run_status
from hyprdiscover.services.waybar import run_waybar
from hyprdiscover.ui.application import HyprDiscoverApplication


def main() -> None:
    if "--waybar" in sys.argv or "-w" in sys.argv:
        run_waybar()
        return

    if "--status" in sys.argv or "-s" in sys.argv:
        json_output = "--json" in sys.argv
        sys.exit(run_status(json_output=json_output))

    app = HyprDiscoverApplication()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
