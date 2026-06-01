#!/usr/bin/env python3

import sys

from core.waybar import run_waybar
from ui.main_window import HyprDiscover


def main():

    if "--waybar" in sys.argv:
        run_waybar()
        return

    app = HyprDiscover()
    app.run()


if __name__ == "__main__":
    main()