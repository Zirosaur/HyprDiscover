#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib
import subprocess
import threading


class HyprDiscover(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="com.hyprdiscover.app")

    def do_activate(self):
        self.win = Gtk.ApplicationWindow(application=self)
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

        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", self.refresh)

        update_btn = Gtk.Button(label="Update")
        update_btn.connect("clicked", self.update_system)

        discover_btn = Gtk.Button(label="Open Discover")
        discover_btn.connect("clicked", self.open_discover)

        self.reboot_btn = Gtk.Button(label="Reboot")
        self.reboot_btn.connect("clicked", self.reboot_system)
        self.reboot_btn.set_visible(False)

        buttons = Gtk.Box(spacing=10)
        buttons.append(refresh_btn)
        buttons.append(update_btn)
        buttons.append(discover_btn)
        buttons.append(self.reboot_btn)

        box.append(self.label)
        box.append(self.progress)
        box.append(buttons)
        box.append(self.text)

        self.win.set_child(box)

        self.refresh(None)

        self.win.present()

    def refresh(self, button):
        try:
            output = subprocess.check_output(
                ["pkcon", "get-updates"],
                text=True
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

            self.label.set_text(
                f"󰚰 {count} updates available"
            )

            buf = self.text.get_buffer()
            buf.set_text(output)

        except Exception as e:
            self.label.set_text(str(e))

    def open_discover(self, button):
        subprocess.Popen(["plasma-discover"])

    def update_system(self, button):
        self.progress.set_visible(True)
        self.progress.set_fraction(0.0)
        self.reboot_btn.set_visible(False)

        self.label.set_text("Updating packages...")
        self.running = True

        GLib.timeout_add(
            100,
            self.pulse
        )

        thread = threading.Thread(
            target=self.run_update,
            daemon=True
        )

        thread.start()

    def pulse(self):
        if self.running:
            self.progress.pulse()
            return True

        return False

    def run_update(self):
        try:
            result = subprocess.run(
                ["pkexec", "pkcon", "update"],
                capture_output=True,
                text=True
            )

            output = (
                result.stdout +
                result.stderr
            )

            print(output)

            if (
                "Tak ada paket" in output
                or "Tidak ada paket" in output
                or "No packages" in output
            ):
                self.running = False

                GLib.idle_add(
                    self.label.set_text,
                    "System already up to date"
                )

                GLib.idle_add(
                    self.progress.set_visible,
                    False
                )

                return

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
            print(e)

            GLib.idle_add(
                self.update_finished,
                False
            )

    def update_finished(self, success):
        self.running = False

        self.progress.set_fraction(1.0)
        self.progress.set_visible(False)

        if success:
            self.label.set_text(
                "Update completed successfully"
            )

            self.reboot_btn.set_visible(True)

            self.refresh(None)

        else:
            self.label.set_text(
                "Update failed"
            )

    def reboot_system(self, button):
        subprocess.Popen([
            "systemctl",
            "reboot"
        ])


app = HyprDiscover()
app.run()