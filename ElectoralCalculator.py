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

from collections import defaultdict

from infoWindow import infoWindow

from calculations import *
from Methods import Methods

def isListStoreEmpty(listStore):
    # get_iter_first() returns a Gtk.TreeIter instance pointing to the first iterator in the tree (the one at the path “0”) or None if the tree is empty.
    # Is there a better way to know if a listStore is empty???
    if listStore.get_iter_first() == None:
        return True
    return False

class pydhondt(Gtk.Window):
    
    def __init__(self):

        # Calculation method
        self.method = Methods.DHONDT
        
        # Votes for each party
        self.votes = {}        
        
        # The model and treeIter of the selected item in tvwCandidatures
        self.tvwCandidaturesModel = None
        self.tvwCandidaturesTreeIter = None
                
        # Create new GtkBuilder object
        self.builder = Gtk.Builder()
        
        # Load UI from file
        self.builder.add_from_file("gui.glade")
        
        # Connect signal
        self.builder.connect_signals(self)
        
        # Get the main window pointer from UI
        self.mainWindow = self.builder.get_object("mainWindow")
        
        # Get txtSeats from the UI
        self.txtSeats = self.builder.get_object("txtSeats")
        
        # Get the optional data text entries from UI
        self.txtCensus = self.builder.get_object("txtCensus")
        self.txtBlankVotes = self.builder.get_object("txtBlankVotes")
        self.txtNullVotes = self.builder.get_object("txtNullVotes")
        self.txtThreshold = self.builder.get_object("txtThreshold")
        
        # Get txtParty from the UI
        self.txtParty = self.builder.get_object("txtParty")
        
        # Get txtVotes from the UI
        self.txtVotes = self.builder.get_object("txtVotes")
        
        # Get tvwCandidatures from the UI
        self.tvwCandidatures = self.builder.get_object("tvwCandidatures")
        
        # Get btnCalculate from the UI
        self.btnAddCandidature = self.builder.get_object("btnAddCandidature")
        
        # Get the lsvwResults TreeView from UI
        self.lsvwResults = self.builder.get_object("lsvwResults")
        
        # Get lblAbstention from the UI
        self.lblAbstention = self.builder.get_object("lblAbstention")
        
        # Destroy builder, since we don't need it anymore
        del(self.builder)
        
        # Create a ListStore for the candidatures
        self.listStoreCandidatures = Gtk.ListStore(str, str)
        
        # Create the TreeViewColumns to display the list of candidatures
        self.tvwcolParty = Gtk.TreeViewColumn('Party')
        self.tvwcolVotes = Gtk.TreeViewColumn('Votes')
        
        # Add the TreeViewColumns to tvwCandidatures
        self.tvwCandidatures.append_column(self.tvwcolParty)
        self.tvwCandidatures.append_column(self.tvwcolVotes)

        # Create a CellRenderer to render the candidatures
        self.cellCandidatures = Gtk.CellRendererText()
        self.cellCandidatures.set_property('xalign', 0.5)

        # Add cellCandidatures to the tvw columns and allow it to expand
        self.tvwcolParty.pack_start(self.cellCandidatures, True)
        self.tvwcolVotes.pack_start(self.cellCandidatures, True)

        # add the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvwcolParty.add_attribute(self.cellCandidatures, 'text', 0)
        self.tvwcolVotes.add_attribute(self.cellCandidatures, 'text', 1)        

        self.listStoreCandidatures.append(["-", "-"])
        
        # Attache the model to the treeview
        self.tvwCandidatures.set_model(self.listStoreCandidatures)
        
        # Get a reference to a selection object and connect to the "changed" signal
        # to manage the user's clicks on tvwCandidatures
        select = self.tvwCandidatures.get_selection()
        select.connect("changed", self.on_tvwCandidatures_selection_changed)
        
        # Create a ListStore for the results
        self.liststore = Gtk.ListStore(str, str, str, str, str, str)
            
        # Create the TreeViewColumn to display the data
        self.tvcolParty = Gtk.TreeViewColumn('Party')
        self.tvcolSeats = Gtk.TreeViewColumn('Seats')
        self.tvcolSeatsPercent = Gtk.TreeViewColumn('% of seats')
        self.tvcolVotes = Gtk.TreeViewColumn('Votes')
        self.tvcolVotesPercent = Gtk.TreeViewColumn('% of votes')
        self.tvcolVotesForNextSeat = Gtk.TreeViewColumn('Votes for next seat')
        
        # Add tv columns to treeview
        self.lsvwResults.append_column(self.tvcolParty)
        self.lsvwResults.append_column(self.tvcolSeats)
        self.lsvwResults.append_column(self.tvcolSeatsPercent)
        self.lsvwResults.append_column(self.tvcolVotes)
        self.lsvwResults.append_column(self.tvcolVotesPercent)
        self.lsvwResults.append_column(self.tvcolVotesForNextSeat)

        # Create a CellRenderer to render the data
        self.cell = Gtk.CellRendererText()
        self.cell.set_property('xalign', 0.5)
        
        # Add the cell to the tv columns and allow it to expand
        self.tvcolParty.pack_start(self.cell, True)
        self.tvcolSeats.pack_start(self.cell, True)
        self.tvcolSeatsPercent.pack_start(self.cell, True)
        self.tvcolVotes.pack_start(self.cell, True)
        self.tvcolVotesPercent.pack_start(self.cell, True)
        self.tvcolVotesForNextSeat.pack_start(self.cell, True)
        
        # add the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolParty.add_attribute(self.cell, 'text', 0)
        self.tvcolSeats.add_attribute(self.cell, 'text', 1)        
        self.tvcolSeatsPercent.add_attribute(self.cell, 'text', 2)
        self.tvcolVotes.add_attribute(self.cell, 'text', 3)        
        self.tvcolVotesPercent.add_attribute(self.cell, 'text', 4)
        self.tvcolVotesForNextSeat.add_attribute(self.cell, 'text', 5)        

        self.liststore.append(["-", "-", "-", "-", "-", "-"])
        
        # Attache the model to the treeview
        self.lsvwResults.set_model(self.liststore)
            
        # Show window. All other widgets are automatically shown by GtkBuilder
        self.mainWindow.show()
        # Maximize the main window
        self.mainWindow.maximize()

    def show_info_message(self, widget, infoText):
        msgDlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, infoText)
        msgDlg.run()
        msgDlg.destroy()

    def on_btnCalculate_clicked(self, widget):        
            
        MSL_FirstDivisor = 1.4
        
        numSeats = 0
        census = 0
        blankVotes = 0
        nullVotes = 0
        totalVotes = 0
        validVotes = 0
        abstention = 0
        abstentionPercentage = 0.00
        threshold = 0
        results = {}
        nextSeat = {}
        seatPercentages = {}        
        
        try:
            numSeats = int(self.txtSeats.get_text())
        except:
            self.show_info_message(self, "The number of seats must be an integer value")
            self.txtSeats.set_text("")
            self.txtSeats.grab_focus()
            return 1
                    
        try:
            census = int(self.txtCensus.get_text())
        except:
            if self.txtCensus.get_text() != "":
                self.show_info_message(self, "The census value is not an integer value, so it's impossible to calculate the abstention")
            census = 0
        
        try:
            blankVotes = int(self.txtBlankVotes.get_text())
        except:
            if self.txtBlankVotes.get_text() != "":
                self.show_info_message(self, "The number of blank votes must be an integer value, it won't be used in the calculation of the abstention")
            blankVotes = 0
            
        try:
            nullVotes = int(self.txtNullVotes.get_text())
        except:
            if self.txtNullVotes.get_text() != "":
                self.show_info_message(self, "The number of null votes must be an integer value, it won't be used in the calculation of the abstention")        
            nullVotes = 0            
        
        try:
            threshold = float(self.txtThreshold.get_text())
        except:
            if self.txtThreshold.get_text() != "":
                self.show_info_message(self, "The threshold must be a number, it won't be used in the calculation of the results")
            threshold = 0
            
        self.liststore.clear()
        
        totalVotes = calculateTotalVotes(self.votes, blankVotes, nullVotes)
        validVotes = calculateValidVotes(totalVotes, nullVotes)
        votePercentages = calculateVotePercentages(self.votes, totalVotes)
        
        if census != 0:
            (abstention, abstentionPercentage) = calculateAbstention(census, totalVotes)
            self.lblAbstention.set_text('Abstention: %i (%d%%)' % (abstention, abstentionPercentage))
        else:
            self.lblAbstention.set_text("Abstention: N/A")
        
        if self.method in (Methods.DHONDT, Methods.SAINTE_LAGUE, Methods.MODIFIED_SAINTE_LAGUE, Methods.IMPERIALI):
            (results, nextSeat) = calculateHighestAverage(self.votes, numSeats, self.method, threshold, votePercentages)
        elif self.method in (Methods.HARE_QUOTA, Methods.DROOP_QUOTA):
            results = calculateLargestRemainder(self.votes, numSeats, self.method, threshold, votePercentages, validVotes)
            for party in results:
                nextSeat[party] = "-"
        else:
            print "Incorrect method name or not implemented method"
                            
        seatPercentages = calculateSeatPercentages(numSeats, results)
        
        print results
        print nextSeat
        print "Total votes: ", totalVotes
        print "Valid votes: ", validVotes
        print "Abstention: " + str(abstention) + " (" + str(abstentionPercentage) + "%)"
        print votePercentages
        print seatPercentages
        print "-------------------------------"
        
        # Add the results to the listStore: [party, seats, %seats, votes, %votes, votesForNextSeat]
        for party in self.votes:
            self.liststore.append([party, str(results[party]), str(seatPercentages[party]), str(self.votes[party]), str(votePercentages[party]), str(nextSeat[party])])
        
        self.txtParty.grab_focus()
    
    def on_btnAddCandidature_clicked(self, widget):
        try:
            self.votes[self.txtParty.get_text()] = int(self.txtVotes.get_text())
        except:
            if self.txtParty.get_text() == "":
                self.show_info_message(self, "The name of the party can't be empty")
                self.txtParty.grab_focus()
                return 1
                
            else:
                self.show_info_message(self, "The number of votes must be an integer value")
                self.txtVotes.set_text("")
                self.txtVotes.grab_focus()
                return 1

        # If this candidature is the first one, delete the "-" from the liststore
        if self.listStoreCandidatures[0][0] == "-":
            self.listStoreCandidatures.clear()
            
        # Add the new candidature to listStoreCandidatures: [party, votes]
        self.listStoreCandidatures.append([self.txtParty.get_text(), self.txtVotes.get_text()])

        self.txtParty.set_text("")
        self.txtVotes.set_text("")

        self.txtParty.grab_focus()
    
    def on_btnEditSelection_clicked(self, widget):
        print "Not implemented yet"    
    
    def on_btnDeleteSelection_clicked(self, widget):
        try:
            msgDlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "Do you want to delete the party " + self.tvwCandidaturesModel[self.tvwCandidaturesTreeIter][0] + "?")
            response = msgDlg.run()
            msgDlg.destroy()
            if response == Gtk.ResponseType.YES:
                # Delete the selected party from the dictionary votes
                del self.votes[self.tvwCandidaturesModel[self.tvwCandidaturesTreeIter][0]]
                # Delete the selected party from listStoreCandidatures
                self.listStoreCandidatures.remove(self.tvwCandidaturesTreeIter)
        except:
            self.show_info_message(self, "You have to select a candidature first")

        if isListStoreEmpty(self.listStoreCandidatures) == True:
            self.listStoreCandidatures.append(["-", "-"])

    def on_btnClear_clicked(self, widget):
        try:
            msgDlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "Do you want to clear the list of candidatures?")
            response = msgDlg.run()
            msgDlg.destroy()
            if response == Gtk.ResponseType.YES:
                # Clear the dictionary votes
                self.votes.clear()
                # Clear the listStoreCandidatures
                self.listStoreCandidatures.clear()
                self.listStoreCandidatures.append(["-", "-"])
        except:
            self.show_info_message(self, "The list of candidatures is already empty")

    def on_tvwCandidatures_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]
        self.tvwCandidaturesModel = model
        self.tvwCandidaturesTreeIter = treeiter
        
    def on_rbtnDhondt_toggled(self, widget):
        self.method = "D'hondt"    
    
    def on_rbtnSainteLague_toggled(self, widget):
        self.method = Methods.SAINTE_LAGUE
        
    def on_rbtnModifiedSainteLague_toggled(self, widget):
        self.method = Methods.MODIFIED_SAINTE_LAGUE
    
    def on_rbtnImperiali_toggled(self, widget):
        self.method = Methods.IMPERIALI
        
    def on_rbtnHareQuota_toggled(self, widget):
        self.method = Methods.HARE_QUOTA
    
    def on_rbtnDroopQuota_toggled(self, widget):
        self.method = Methods.DROOP_QUOTA
    
    def on_mainWindow_quit(self, widget):
        Gtk.main_quit()

    def on_edit_copy_clicked(self, widget):
        print "Ezin dut asmatu nola egin!!!!!!!!!!!!!!!!!!!!!!!!!"

    def on_help_info_methods_clicked(self, widget):
        infoMethods = infoWindow()
        #infoMethods.show()
                
    def on_help_about_clicked(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("Electoral Calculator")
        about.set_version("0.5.3")
        about.set_copyright("© 2012 Asier Iturralde Sarasola")
        about.set_comments("Electoral Calculator can calculate seat distributions using\nHighest averages methods (D'hondt, Sainte-Laguë, Modified Sainte-Laguë, Imperialli)\nand Largest remainder methods (Hare quota, Droop quota)")
        about.set_website("https://launchpad.net/electoralcalculator")
        #about.set_logo(Gdk.pixbuf_new_from_file("election.jpeg"))
        about.run()
        about.destroy()
    
def main():

    # Create a new pydhondt object
    dhondt = pydhondt()
    
    # Start main loop
    Gtk.main()
    
if __name__ == '__main__':
    main()    
