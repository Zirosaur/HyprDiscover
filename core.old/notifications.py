import subprocess


def send_notification(title, message):

    subprocess.run(
        [
            "notify-send",
            title,
            message,
            "-a",
            "HyprDiscover"
        ],
        check=False
    )


def updates_available(count):

    send_notification(
        "HyprDiscover",
        f"{count} updates available"
    )


def update_success():

    send_notification(
        "HyprDiscover",
        "System updated successfully"
    )


def update_failed():

    send_notification(
        "HyprDiscover",
        "Update failed"
    )    