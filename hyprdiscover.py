#!/usr/bin/env python3

import sys
import json
import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib
import subprocess
import threading


# ==========================================
# Waybar Mode
# ==========================================

if "--waybar" in sys.argv:
    try:
        result = subprocess.run(
            ["pkcon", "get-updates"],
            capture_output=True,
            text=True
        )

        output = result.stdout + result.stderr

        count = sum(
            1 for line in output.splitlines()
            if any(
                line.startswith(x)
                for x in [
                    "Tersedia",
                    "Keamanan",
                    "Perbaikan kutu",
                    "Enhancement"
                ]
            )
        )

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

    sys.exit(0)


# ==========================================
# GUI Application
# ==========================================

class HyprDiscover(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="com.hyprdiscover.app"
        )

    def do_activate(self):
        self.win = Gtk.ApplicationWindow(
            application=self
        )

        self.win.set_title("HyprDiscover")
        self.win.set_default_size(700, 500)

        self.running = False

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        self.label = Gtk.Label(
            label="Checking updates..."
        )

        self.progress = Gtk.ProgressBar()
        self.progress.set_visible(False)

        self.text = Gtk.TextView()
        self.text.set_editable(False)
        self.text.set_monospace(True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_child(self.text)

        self.refresh_btn = Gtk.Button(
            label="Refresh"
        )

        self.refresh_btn.connect(
            "clicked",
            self.refresh
        )

        self.update_btn = Gtk.Button(
            label="Update"
        )

        self.update_btn.connect(
            "clicked",
            self.update_system
        )

        discover_btn = Gtk.Button(
            label="Open Discover"
        )

        discover_btn.connect(
            "clicked",
            self.open_discover
        )

        about_btn = Gtk.Button(
            label="About"
        )

        about_btn.connect(
            "clicked",
            self.show_about
        )

        self.reboot_btn = Gtk.Button(
            label="Reboot"
        )

        self.reboot_btn.connect(
            "clicked",
            self.reboot_system
        )

        self.reboot_btn.set_visible(False)

        buttons = Gtk.Box(
            spacing=10
        )

        buttons.append(self.refresh_btn)
        buttons.append(self.update_btn)
        buttons.append(discover_btn)
        buttons.append(about_btn)
        buttons.append(self.reboot_btn)

        box.append(self.label)
        box.append(self.progress)
        box.append(buttons)
        box.append(scroll)

        self.win.set_child(box)

        self.refresh(None)

        self.win.present()

    def show_log(self, text):
        buf = self.text.get_buffer()
        buf.set_text(text)

    def refresh(self, button):
        try:
            result = subprocess.run(
                ["pkcon", "get-updates"],
                capture_output=True,
                text=True
            )

            output = (
                result.stdout +
                result.stderr
            )

            count = sum(
                1 for line in output.splitlines()
                if any(
                    line.startswith(x)
                    for x in [
                        "Tersedia",
                        "Keamanan",
                        "Perbaikan kutu",
                        "Enhancement"
                    ]
                )
            )

            if count == 0:
                self.label.set_text(
                    "✓ System is up to date"
                )
            else:
                self.label.set_text(
                    f"󰚰 {count} updates available"
                )

            self.show_log(output)

        except Exception as e:
            print(f"Refresh error: {e}")

            self.label.set_text(
                "Unable to check for updates"
            )

            self.show_log(
                f"Error:\n\n{e}"
            )

    def open_discover(self, button):
        subprocess.Popen(
            ["plasma-discover"]
        )

    def update_system(self, button):

        self.refresh_btn.set_sensitive(False)
        self.update_btn.set_sensitive(False)

        self.progress.set_visible(True)
        self.progress.set_fraction(0.0)

        self.reboot_btn.set_visible(False)

        self.label.set_text(
            "Updating packages..."
        )

        self.running = True

        GLib.timeout_add(
            100,
            self.pulse
        )

        threading.Thread(
            target=self.run_update,
            daemon=True
        ).start()

    def pulse(self):
        if self.running:
            self.progress.pulse()
            return True

        return False

    def run_update(self):
        try:
            result = subprocess.run(
                ["pkcon", "update"],
                capture_output=True,
                text=True
            )

            output = (
                result.stdout +
                result.stderr
            )

            if (
                "Tak ada paket" in output
                or "Tidak ada paket" in output
                or "No packages" in output
            ):
                self.running = False

                GLib.idle_add(
                    self.label.set_text,
                    "✓ System is up to date"
                )

                GLib.idle_add(
                    self.progress.set_visible,
                    False
                )

                GLib.idle_add(
                    self.refresh_btn.set_sensitive,
                    True
                )

                GLib.idle_add(
                    self.update_btn.set_sensitive,
                    True
                )

                GLib.idle_add(
                    self.show_log,
                    output
                )

                return

            GLib.idle_add(
                self.show_log,
                output
            )

            if result.returncode == 0:
                GLib.idle_add(
                    self.update_finished,
                    True
                )
            else:
                GLib.idle_add(
                    self.update_finished,
                    False
                )

        except Exception as e:
            print(f"Update error: {e}")

            GLib.idle_add(
                self.show_log,
                str(e)
            )

            GLib.idle_add(
                self.update_finished,
                False
            )

    def update_finished(self, success):

        self.running = False

        self.refresh_btn.set_sensitive(True)
        self.update_btn.set_sensitive(True)

        self.progress.set_visible(False)

        if success:

            self.label.set_text(
                "✓ Updates installed successfully"
            )

            self.reboot_btn.set_visible(True)

            self.refresh(None)

        else:

            self.label.set_text(
                "Update failed"
            )

    def show_about(self, button):

        dialog = Gtk.AboutDialog()

        dialog.set_transient_for(
            self.win
        )

        dialog.set_modal(True)

        dialog.set_program_name(
            "HyprDiscover"
        )

        dialog.set_version(
            "0.2.0-dev"
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

    def reboot_system(self, button):
        subprocess.Popen(
            ["systemctl", "reboot"]
        )


app = HyprDiscover()
app.run()