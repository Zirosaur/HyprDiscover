from gi.repository import Gtk


def show_about(parent):

    dialog = Gtk.AboutDialog()

    dialog.set_transient_for(parent)

    dialog.set_modal(True)

    dialog.set_program_name(
        "HyprDiscover"
    )

    dialog.set_version(
        "0.2.1-dev"
    )

    dialog.set_comments(
        "Modern update manager for Fedora Hyprland"
    )

    dialog.set_website(
        "https://github.com/Zirosaur/HyprDiscover"
    )

    dialog.set_authors([
        "Zirosaur"
    ])

    dialog.present()