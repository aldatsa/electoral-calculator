#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class infoWindow(Gtk.Window):

    def __init__(self):        
    
        # Calculation method
        self.method = "D'hondt"
        
        # Create new GtkBuilder object
        self.builder = Gtk.Builder()
        
        # Load UI from file
        self.builder.add_from_file("infoWindow_0.5.3.glade")
        
        # Connect signal
        self.builder.connect_signals(self)
        
        # Get the info window pointer from UI
        self.infoWindow = self.builder.get_object("infoWindow")
        
        # Get lblInfo from UI
        self.lblInfo = self.builder.get_object("lblInfo")
        
        # Destroy builder, since we don't need it anymore
        del(self.builder)

        # Show window. All other widgets are automatically shown by GtkBuilder
        self.infoWindow.show()
                
    def on_rbtnDhondt_toggled(self, widget):
        self.method = "D'hondt"    
        
    def on_rbtnSainteLague_toggled(self, widget):
        self.method = "Sainte-Laguë"

    def on_rbtnModifiedSainteLague_toggled(self, widget):
        self.method = "Modified Sainte-Laguë"

    def on_rbtnImperiali_toggled(self, widget):
        self.method = "Imperiali" 

    def on_rbtnHareQuota_toggled(self, widget):
        self.method = "Hare Quota"

    def on_rbtnDroopQuota_toggled(self, widget):
        self.method = "Droop Quota"

    def on_infoWindow_quit(self, widget):
        self.infoWindow.destroy()
        
