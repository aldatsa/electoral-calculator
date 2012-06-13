#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Asier Iturralde Sarasola
#
# This file is part of Electoral Calculator.
#
# Electoral Calculator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Electoral Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk

from Methods import Methods

class infoWindow(Gtk.Window):

    def __init__(self):

        # Calculation method
        self.method = Methods.DHONDT

        # Create new GtkBuilder object
        self.builder = Gtk.Builder()

        # Load UI from file
        self.builder.add_from_file("infoWindow.glade")

        # Connect signal
        self.builder.connect_signals(self)

        # Get the info window pointer from UI
        self.infoWindow = self.builder.get_object("infoWindow")

        # Get lblInfo from UI
        self.lblInfo = self.builder.get_object("lblInfo")

        # Show info about the current method
        self.show_info(self.method)

        # Destroy builder, since we don't need it anymore
        del(self.builder)

        # Show window. All other widgets are automatically shown by GtkBuilder
        self.infoWindow.show()

        # Maximize the main window
        self.infoWindow.maximize()

    def show_info(self, method):
        label_text = "<b>Selected method: " + str(method) + "</b>"
        self.lblInfo.set_markup(label_text)

    def on_rbtnDhondt_toggled(self, widget):
        self.method = Methods.DHONDT
        self.show_info(self.method)

    def on_rbtnSainteLague_toggled(self, widget):
        self.method = Methods.SAINTE_LAGUE
        self.show_info(self.method)

    def on_rbtnModifiedSainteLague_toggled(self, widget):
        self.method = Methods.MODIFIED_SAINTE_LAGUE
        self.show_info(self.method)

    def on_rbtnImperiali_toggled(self, widget):
        self.method = Methods.IMPERIALI
        self.show_info(self.method)

    def on_rbtnHareQuota_toggled(self, widget):
        self.method = Methods.HARE_QUOTA
        self.show_info(self.method)

    def on_rbtnDroopQuota_toggled(self, widget):
        self.method = Methods.DROOP_QUOTA
        self.show_info(self.method)

    def on_infoWindow_quit(self, widget):
        self.infoWindow.destroy()
