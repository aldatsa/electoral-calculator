# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Asier Iturralde Sarasola <asier.iturralde@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('electoralcalculator')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('electoralcalculator')

from electoralcalculator_lib import Window
from electoralcalculator.AboutElectoralcalculatorDialog import AboutElectoralcalculatorDialog
from electoralcalculator.PreferencesElectoralcalculatorDialog import PreferencesElectoralcalculatorDialog
from electoralcalculator_lib.Methods import Methods
from electoralcalculator_lib.calculations import *
from electoralcalculator.PartyeditorDialog import PartyeditorDialog

def isListStoreEmpty(listStore):
    # get_iter_first() returns a Gtk.TreeIter instance pointing to
    # the first iterator in the tree (the one at the path “0”)
    # or None if the tree is empty.
    # Is there a better way to know if a listStore is empty???
    if listStore.get_iter_first() == None:
        return True
    return False

def areThereCandidatures(listStore):
    if listStore[0][0] == '-':
        return False
    return True

# See electoralcalculator_lib.Window.py for more details about how this
# class works
class ElectoralcalculatorWindow(Window):
    __gtype_name__ = "ElectoralcalculatorWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(ElectoralcalculatorWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutElectoralcalculatorDialog
        self.PreferencesDialog = PreferencesElectoralcalculatorDialog

        # Code for other initialization actions should be added here.
        
        # Calculation method
        self.method = Methods.DHONDT

        # Votes for each party
        self.votes = {}

        # The model and treeIter of the selected item in tvwCandidatures
        self.tvwCandidaturesModel = None
        self.tvwCandidaturesTreeIter = None

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

        # Get the toolbar Open button from the UI
        self.toolbuttonOpen = self.builder.get_object("toolbuttonOpen")

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

        # Get a reference to a selection object and connect to
        # the "changed" signal to manage the user's clicks on tvwCandidatures
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

    def show_info_message(self, widget, infoText):
        msgDlg = Gtk.MessageDialog(self,
                                   0,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   infoText)
        msgDlg.run()
        msgDlg.destroy()

    def showNoCandidaturesMsg(self):
        msgText = "There are no candidatures"
        self.show_info_message(self, msgText)

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

        # Check if the list of parties is empty
        if (isListStoreEmpty(self.listStoreCandidatures) == True or
        areThereCandidatures(self.listStoreCandidatures) == False):
            self.showNoCandidaturesMsg()
            self.txtParty.grab_focus()
            return 1

        try:
            numSeats = int(self.txtSeats.get_text())
        except:
            msgText = "The number of seats must be an integer value."
            self.show_info_message(self, msgText)
            self.txtSeats.set_text("")
            self.txtSeats.grab_focus()
            return 1

        try:
            census = int(self.txtCensus.get_text())
        except:
            msgText = ("The census value is not an integer value,\n"
                       "so it's impossible to calculate the abstention.")
            if self.txtCensus.get_text() != "":
                self.show_info_message(self, msgText)
            census = 0

        try:
            blankVotes = int(self.txtBlankVotes.get_text())
        except:
            msgText = ("The number of blank votes must be an integer value.\n"
                       "It won't be used to calculate the abstention.")
            if self.txtBlankVotes.get_text() != "":
                self.show_info_message(self, msgText)
            blankVotes = 0

        try:
            nullVotes = int(self.txtNullVotes.get_text())
        except:
            msgText = ("The number of null votes must be an integer value.\n"
                       "It won't be used to calculate the abstention.")
            if self.txtNullVotes.get_text() != "":
                self.show_info_message(self, msgText)
            nullVotes = 0

        try:
            threshold = float(self.txtThreshold.get_text())
        except:
            msgText = ("The threshold must be a number.\n"
                      "It won't be used to calculate the results.")
            if self.txtThreshold.get_text() != "":
                self.show_info_message(self, msgText)
            threshold = 0

        self.liststore.clear()

        totalVotes = calculateTotalVotes(self.votes, blankVotes, nullVotes)
        validVotes = calculateValidVotes(totalVotes, nullVotes)
        votePercentages = calculateVotePercentages(self.votes, totalVotes)

        if census != 0:
            (abstention,
             abstentionPercentage) = calculateAbstention(census,
                                                         totalVotes)
            self.lblAbstention.set_text('Abstention: %i (%d%%)' %
                                        (abstention, abstentionPercentage))
        else:
            self.lblAbstention.set_text("Abstention: N/A")

        if self.method in (Methods.DHONDT,
                            Methods.SAINTE_LAGUE,
                            Methods.MODIFIED_SAINTE_LAGUE,
                            Methods.IMPERIALI):
            (results, nextSeat) = calculateHighestAverage(self.votes,
                                                          numSeats,
                                                          self.method,
                                                          threshold,
                                                          votePercentages)
        elif self.method in (Methods.HARE_QUOTA, Methods.DROOP_QUOTA):
            results = calculateLargestRemainder(self.votes, numSeats,
                                                self.method, threshold,
                                                votePercentages, validVotes)
            for party in results:
                nextSeat[party] = "-"
        else:
            print "Incorrect method name or not implemented method"

        seatPercentages = calculateSeatPercentages(numSeats, results)

        print results
        print nextSeat
        print "Total votes: ", totalVotes
        print "Valid votes: ", validVotes
       #print "Abstention: " + str(abstention) +
        #" (" + str(abstentionPercentage) + "%)"
        print "Abstention: %d (%d%%)" % (abstention, abstentionPercentage)
        print votePercentages
        print seatPercentages
        print "-------------------------------"

        # Add the results to the listStore:
        # [party, seats, %seats, votes, %votes, votesForNextSeat]
        for party in self.votes:
            self.liststore.append([party,
                                  str(results[party]),
                                  str(seatPercentages[party]),
                                  str(self.votes[party]),
                                  str(votePercentages[party]),
                                  str(nextSeat[party])])

        self.txtParty.grab_focus()

    def on_btnAddCandidature_clicked(self, widget):
        # The name of the party can't be a empty string
        if self.txtParty.get_text() == "":
            msgText = "The name of the party can't be empty"
            self.show_info_message(self, msgText)
            self.txtParty.grab_focus()
            return 1

        try:
            self.votes[self.txtParty.get_text()] = \
            int(self.txtVotes.get_text())
        except:
            msgText = "The number of votes must be an integer value"
            self.show_info_message(self, msgText)
            self.txtVotes.set_text("")
            self.txtVotes.grab_focus()
            return 1

        # If this candidature is the first one,
        # delete the "-" from the liststore
        if self.listStoreCandidatures[0][0] == "-":
            self.listStoreCandidatures.clear()

        # Add the new candidature to listStoreCandidatures: [party, votes]
        self.listStoreCandidatures.append([self.txtParty.get_text(),
                                           self.txtVotes.get_text()])

        self.txtParty.set_text("")
        self.txtVotes.set_text("")

        self.txtParty.grab_focus()

    def setTreeElement(self, partyName, partyVotes, treeIter):
        self.tvwCandidaturesModel[treeIter][0] = partyName
        self.tvwCandidaturesModel[treeIter][1] = partyVotes

    def on_btnEditSelection_clicked(self, widget):
        try:
            party = self.tvwCandidaturesModel[self.tvwCandidaturesTreeIter][0]
            votes = self.tvwCandidaturesModel[self.tvwCandidaturesTreeIter][1]

            if party == '-':
                self.showNoCandidaturesMsg()
                return 1

            #PartyEditor = partyEditor(party,
            #                          votes,
            #                          self.setTreeElement,
            #                          self.tvwCandidaturesTreeIter)
            PartyEditor = PartyeditorDialog()
            
            PartyEditor.run()
            
        except:
            if areThereCandidatures(self.listStoreCandidatures) == False:
                self.showNoCandidaturesMsg()
                return 1

            msgText = "You have to select a candidature first"
            self.show_info_message(self, msgText)

    def on_btnDeleteSelection_clicked(self, widget):
        try:
            party = self.tvwCandidaturesModel[self.tvwCandidaturesTreeIter][0]

            if party == '-':
                self.showNoCandidaturesMsg()
                return 1

            msgText = ("Do you want to delete the party " +
                      party +
                      "?")
            msgDlg = Gtk.MessageDialog(self,
                                       0,
                                       Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.YES_NO,
                                       msgText)
            response = msgDlg.run()
            msgDlg.destroy()
            if response == Gtk.ResponseType.YES:
                treeIter = self.tvwCandidaturesTreeIter
                party = self.tvwCandidaturesModel[treeIter][0]
                # Delete the selected party from the dictionary votes
                del self.votes[party]
                # Delete the selected party from listStoreCandidatures
                self.listStoreCandidatures.remove(self.tvwCandidaturesTreeIter)
        except:
            if areThereCandidatures(self.listStoreCandidatures) == False:
                self.showNoCandidaturesMsg()
                return 1

            msgText = "You have to select a candidature first"
            self.show_info_message(self, msgText)

        if isListStoreEmpty(self.listStoreCandidatures) == True:
            self.listStoreCandidatures.append(["-", "-"])

    def on_btnClear_clicked(self, widget):
        try:
            if areThereCandidatures(self.listStoreCandidatures) == False:
                self.showNoCandidaturesMsg()
                return 1

            msgText = "Do you want to clear the list of candidatures?"
            msgDlg = Gtk.MessageDialog(self,
                                       0,
                                       Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.YES_NO,
                                       msgText)
            response = msgDlg.run()
            msgDlg.destroy()
            if response == Gtk.ResponseType.YES:
                # Clear the dictionary votes
                self.votes.clear()
                # Clear the listStoreCandidatures
                self.listStoreCandidatures.clear()
                self.listStoreCandidatures.append(["-", "-"])
        except:
            msgText = "The list of candidatures is already empty."
            self.show_info_message(self, msgText)

    def on_tvwCandidatures_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]
        self.tvwCandidaturesModel = model
        self.tvwCandidaturesTreeIter = treeiter

    def on_rbtnDhondt_toggled(self, widget):
        self.method = Methods.DHONDT

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

    def on_toolbutton_open_clicked(self, widget):
        print "Open toolbutton pressed"
        
