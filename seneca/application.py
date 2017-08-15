# application.py
#
# Copyright (C) 2017 Eddy Castillo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from .window import ApplicationWindow
from .dialogs import AboutDialog, InfoDialog

class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 #application_id='com.github.dyskette.seneca',
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN)

        GLib.set_application_name('Seneca')
        GLib.set_prgname('seneca')

        self.window = None
        # self.settings = Gio.Settings.new('com.github.dyskette.seneca')

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('about')
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit')
        action.connect('activate', self.on_quit)
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = ApplicationWindow(application=self)
        self.window.present()

    def do_shutdown(self):
        if self.window:
            self.window.settings.save()
        Gtk.Application.do_shutdown(self)

    def do_open(self, files, n_files, hint):
        if not self.window:
            self.window = ApplicationWindow(application=self)

        first = False
        for giofile in files:
            if self.is_supported(giofile):
                if first is False and self.window.book.get_doc() is None:
                    self.window.open_file(giofile)
                    first = True
                else:
                    # TODO: Spawn processes of this program with the file as argument
                    cmd = 'seneca'
                    flags = Gio.AppInfoCreateFlags.SUPPORTS_STARTUP_NOTIFICATION
                    appinfo = Gio.AppInfo.create_from_commandline(cmd, 'seneca', flags)
                    # launch = appinfo.launch([giofile], None)
                    # if not launch:
                    #     print('Something went wrong!')

        self.activate()

    def is_supported(self, giofile):
        try:
            ftype = giofile.query_info(Gio.FILE_ATTRIBUTE_STANDARD_CONTENT_TYPE,
                                       Gio.FileQueryInfoFlags.NONE,
                                       None)
        except Exception as e:
            return False
        else:
            if ftype.get_content_type() == 'application/epub+zip':
                return True
            else:
                return False

    def on_about(self, action, param):
        dialog = AboutDialog(self.get_active_window())
        dialog.about.present()

    def on_quit(self, action, param):
        self.quit()