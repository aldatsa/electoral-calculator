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

from calculations import *

def calculateLargestRemainder_doctest():
    """
    d'Hondt method
    Example from http://en.wikipedia.org/wiki/D%27Hondt_method#Allocation
    >>> calculateHighestAverage({'a':100000, 'b':80000, 'c':30000, 'd':20000}, 8, "D'hondt", 0, {'a':43.48, 'b':34.78, 'c':13.04, 'd':8.70})[0] == {'a': 4,'b': 3,'c': 1,'d': 0}
    True
    
    d'Hondt method
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "D'hondt", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 5, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 0, 'Pink': 0}
    True
    
    Sainte-Laguë method (unmodified)
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "Sainte-Laguë", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 4, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 1, 'Pink': 0}
    True
    
    Sainte-Laguë method (modified)
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "Modified Sainte-Laguë", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 5, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 0, 'Pink': 0}
    True
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
