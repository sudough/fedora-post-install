import gi
import os
import sys
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DialogDone(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Success!",transient_for=parent,flags=0)
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_default_size(150,100)
        label=Gtk.Label(label="Your Fedora is now ready to use! Click OK to close this application.")
        box=self.get_content_area()
        box.add(label)
        self.show_all()

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Better Fedora")
        Gtk.Window.set_default_size(self,500,400)
        self.exescript=Gtk.Button(label="Set up Fedora how it should be out of the box")
        self.exescript.connect("clicked",self.on_exescript_clicked)
        self.add(self.exescript)

    def on_exescript_clicked(self, widget):
        print("enable rpm fusion button clicked")
        urlnonfree="https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"
        urlfree="https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"
        sub = subprocess.Popen('pkexec dnf up -y && pkexec dnf in '+urlfree+' '+urlnonfree+' gnome-extensions-app gnome-tweaks -y && flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo && gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,close"',shell=True)
        sub.communicate()
        dialog =DialogDone(self)
        dialogresponse=dialog.run()
        if dialogresponse==Gtk.ResponseType.OK:
            sys.exit()
        



win=MainWindow()
win.connect("destroy",Gtk.main_quit)
win.show_all()
Gtk.main()