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

def calculateHighestAverage_doctest():
    """
    d'Hondt method
    Example from http://en.wikipedia.org/wiki/D%27Hondt_method#Allocation
    >>> calculateHighestAverage({'a':100000, 'b':80000, 'c':30000, 'd':20000}, 8, "D'hondt", 0, {'a':43.48, 'b':34.78, 'c':13.04, 'd':8.70})[0] == {'a': 4,'b': 3,'c': 1,'d': 0}
    True
    
    d'Hondt method
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "D'hondt", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 5, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 0, 'Pink': 0}
    True

    d'Hondt method
    Example from http://en.wikipedia.org/wiki/Talk:Highest_averages_method
    >>> calculateHighestAverage({'MA':6349, 'CT':3405, 'ME':1274, 'NH':1235, 'RI':1048, 'VT':608}, 8, "D'hondt", 0, {'MA':45.61, 'CT':24.46, 'ME':9.15, 'NH':8.87, 'RI':7.53, 'VT':4.37})[0] == {'MA':5, 'CT':2, 'ME':1, 'NH':0, 'RI':0, 'VT':0}
    True

    Sainte-Laguë method (unmodified)
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "Sainte-Laguë", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 4, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 1, 'Pink': 0}
    True

    Sainte-Laguë method (unmodified)
    Example from http://en.wikipedia.org/wiki/Talk:Highest_averages_method
    >>> calculateHighestAverage({'MA':6349, 'CT':3405, 'ME':1274, 'NH':1235, 'RI':1048, 'VT':608}, 8, "Sainte-Laguë", 0, {'MA':45.61, 'CT':24.46, 'ME':9.15, 'NH':8.87, 'RI':7.53, 'VT':4.37})[0] == {'MA':3, 'CT':2, 'ME':1, 'NH':1, 'RI':1, 'VT':0}
    True

    Sainte-Laguë method (unmodified)
    Example from the 2002 New Zealand election using Sainte-Laguë: http://www.electionresults.govt.nz/electionresults_2002/e9/html/e9_part2.html
    >>> calculateHighestAverage({'Labour Party':838219, 'National Party':425310, 'NZ First':210912, 'ACT':145078, 'Green Party':142250, 'United Future':135918, 'Progressive Coalition':34542}, 120, "Sainte-Laguë", 0, {'Labour Party':43.38, 'National Party':22.01, 'NZ First':10.92, 'ACT':7.51, 'Green Party':7.36, 'United Future':7.03, 'Progressive Coalition':1.79})[0] == {'Labour Party':52, 'National Party':27, 'NZ First':13, 'ACT':9, 'Green Party':9, 'United Future':8, 'Progressive Coalition':2}
    True
    
    Sainte-Laguë method (modified)
    Example from http://en.wikipedia.org/wiki/Highest_averages_method#Comparison_between_the_d.27Hondt_and_Sainte-Lagu.C3.AB_methods
    >>> calculateHighestAverage({'Yellow':47000, 'White':16000, 'Red':15900, 'Green':12000, 'Blue':6000, 'Pink':3100}, 10, "Modified Sainte-Laguë", 0, {'Yellow':47.00, 'White':16.00, 'Red':15.90, 'Green':12.00, 'Blue':6.00, 'Pink':3.10})[0] == {'Yellow': 5, 'White': 2, 'Red': 2, 'Green': 1, 'Blue': 0, 'Pink': 0}
    True
    """

def calculateLargestRemainder_doctest():
    """
    Hare quota:
    Example from http://en.wikipedia.org/wiki/Largest_remainder_method#Examples
    >>> calculateLargestRemainder({'Yellows':47000, 'Whites':16000, 'Reds':15800, 'Greens':12000, 'Blues':6100, 'Pinks':3100}, 10, "Hare Quota", 0, {'Yellows':47.00, 'Whites':16.00, 'Reds':15.80, 'Greens':12.00, 'Blues':6.10, 'Pinks':3.10}, 100000) == {'Yellows': 5, 'Whites': 2, 'Reds': 1, 'Greens': 1, 'Blues': 1, 'Pinks': 0}
    True

    Hare quota:
    Example from http://en.wikipedia.org/wiki/Largest_remainder_method#Technical_evaluation_and_paradoxes
    >>> calculateLargestRemainder({'A':1500, 'B':1500, 'C':900, 'D':500, 'E':500, 'F':200}, 25, "Hare Quota", 0, {'A':29.41, 'B':29.41, 'C':17.65, 'D':9.80, 'E':9.80, 'F':3.92}, 5100) == {'A':7, 'B':7, 'C':4, 'D':3, 'E':3, 'F':1}
    True

    Hare quota:
    Example from http://en.wikipedia.org/wiki/Largest_remainder_method#Technical_evaluation_and_paradoxes
    >>> calculateLargestRemainder({'A':1500, 'B':1500, 'C':900, 'D':500, 'E':500, 'F':200}, 26, "Hare Quota", 0, {'A':29.41, 'B':29.41, 'C':17.65, 'D':9.80, 'E':9.80, 'F':3.92}, 5100) == {'A':8, 'B':8, 'C':5, 'D':2, 'E':2, 'F':1}
    True

    Droop quota:
    Example from http://en.wikipedia.org/wiki/Largest_remainder_method#Examples
    >>> calculateLargestRemainder({'Yellows':47000, 'Whites':16000, 'Reds':15800, 'Greens':12000, 'Blues':6100, 'Pinks':3100}, 10, "Droop Quota", 0, {'Yellows':47.00, 'Whites':16.00, 'Reds':15.80, 'Greens':12.00, 'Blues':6.10, 'Pinks':3.10}, 100000) == {'Yellows': 5, 'Whites': 2, 'Reds': 2, 'Greens': 1, 'Blues': 0, 'Pinks': 0}
    True
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
