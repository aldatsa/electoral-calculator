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

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('electoralcalculator')

from gi.repository import Gtk # pylint: disable=E0611

from electoralcalculator import ElectoralcalculatorWindow

from electoralcalculator_lib import set_up_logging, get_version

from electoralcalculator_lib.Database import check_db_dir_exists, create_db_dir

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs electoralcalculator_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'
    parse_options()

    # Check if the database dir exists, if it doesn't create it
    if not check_db_dir_exists():
        create_db_dir()

    # Run the application.    
    window = ElectoralcalculatorWindow.ElectoralcalculatorWindow()
    window.show()
    Gtk.main()
