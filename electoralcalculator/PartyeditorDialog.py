# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from gi.repository import Gtk # pylint: disable=E0611

from electoralcalculator_lib.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('electoralcalculator')

class PartyeditorDialog(Gtk.Dialog):
    __gtype_name__ = "PartyeditorDialog"

    def __new__(cls, party='', votes=''):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated PartyeditorDialog object.
        """
        builder = get_builder('PartyeditorDialog')
        new_object = builder.get_object('partyeditor_dialog')
        new_object.finish_initializing(builder, party, votes)
        return new_object

    def finish_initializing(self, builder, party, votes):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a PartyeditorDialog object with it in order to
        finish initializing the start of the new PartyeditorDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)
        self.entryParty = builder.get_object("entryParty")
        self.entryVotes = builder.get_object("entryVotes")
        self.entryParty.set_text(party)
        self.entryVotes.set_text(votes)

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        pass

    def get_party(self):
        return self.entryParty.get_text()

    def get_votes(self):
        return self.entryVotes.get_text()

if __name__ == "__main__":
    dialog = PartyeditorDialog()
    dialog.show()
    Gtk.main()
