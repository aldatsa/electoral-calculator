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

class partyEditor():

    def __init__(self, party, votes, function, treeIter):
        
        # The function used to update the values of the liststore tvwCandidatures from the main window (ElectoralCalculator.py)
        self.setTreeElement = function
        
        # The tree iterator that points to the currently selected item in the liststore tvwCandidatures from the main window (ElectoralCalculator.py)
        self.treeIter = treeIter

        # Create new GtkBuilder object
        self.builder = Gtk.Builder()
        
        # Load UI from file
        self.builder.add_from_file("partyEditor.glade")
        
        # Connect signal
        self.builder.connect_signals(self)
        
        # Get the info window pointer from UI
        self.partyEditor = self.builder.get_object("partyEditor")
        
        # Connect the delete event to the function delete_event to destroy the window
        self.partyEditor.connect('delete-event', self.delete_event)
        
        # Get txtVotes from the UI
        self.txtParty = self.builder.get_object("txtParty")

        # Set in the entry object txtParty the name of the party passed in to this window
        self.txtParty.set_text(party)
        self.txtParty.grab_focus()

        # Get txtVotes from the UI
        self.txtVotes = self.builder.get_object("txtVotes")

        # Set in the entry object txtVotes the nunmber of votes of the party passed in to this window
        self.txtVotes.set_text(votes)

        # Destroy builder, since we don't need it anymore
        del(self.builder)

    def run(self):
        self.partyEditor.show_all()

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def on_btnAccept_clicked(self, widget):
        # Update the list store tvwCandidatures from the main window (ElectoralCalculator.py)
        self.setTreeElement(self.txtParty.get_text(), self.txtVotes.get_text(), self.treeIter)
            
        # Destroy the window
        self.partyEditor.destroy()

    def on_partyEditor_quit(self, widget):
        self.partyEditor.destroy()
