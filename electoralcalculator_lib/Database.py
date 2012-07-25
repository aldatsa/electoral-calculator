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

import os

# The path to the directory where the database will be stored:
# ~/.electoralcalculator/
db_dir = os.path.join(os.path.expanduser('~'), '.electoralcalculator')

# The path of the database
db_file_dir = os.path.join(db_dir, 'elections.db')

def check_db_dir_exists():
    '''Check if the directory where the database will be stored exists:
    ~/.electoralcalculator'''
    return os.path.exists(db_dir)

def create_db_dir():
    '''Create the directory where the database will be stored:
    ~/.electoralcalculator'''
    os.makedirs(db_dir)
