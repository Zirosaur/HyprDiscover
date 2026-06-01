import json

from core.updates import get_updates


def run_waybar():

    try:

        count, output = get_updates()

        if count > 0:

            print(json.dumps({
                "text": f"󰚰 {count}",
                "tooltip": f"{count} updates available"
            }))

        else:

            print(json.dumps({
                "text": "󰄬",
                "tooltip": "System up to date"
            }))

    except Exception:

        print(json.dumps({
            "text": "⚠",
            "tooltip": "Unable to check updates"
        }))