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

from math import ceil
from math import floor

def calculateTotalVotes(votes, blankVotes=0, nullVotes=0):
    totalVotes = 0
        
    for party in votes:
        totalVotes = totalVotes + votes[party]
            
    totalVotes = totalVotes + blankVotes + nullVotes
        
    return totalVotes

def calculateValidVotes(totalVotes, nullVotes=0):
    return totalVotes - nullVotes

def calculateAbstention(census, totalVotes):
    abstention = census - totalVotes
    abstentionPercentage = round(100 * (float(abstention) / census), 2)
        
    return abstention, abstentionPercentage
        
def calculateVotePercentages(votes, totalVotes):
    votePercentages = {}

    for party in votes:
        votePercentages[party] = round(100 * (float(votes[party])/totalVotes), 2)
        
    return votePercentages

def calculateSeatPercentages(numSeats, seats):
    seatPercentages = {}

    for party in seats:
        seatPercentages[party] = round(100 * (float(seats[party])/numSeats), 2)
        
    return seatPercentages
            
def getDivisor(numSeats, method, MSLFD=1.4):
    if method == "D'hondt":
        return numSeats + 1
    elif method == "Sainte-Laguë":
        return 2 * numSeats + 1
    elif method == "Modified Sainte-Laguë":
        if numSeats == 0:
            return MSLFD
        else:
            return 2 * numSeats + 1
    elif method == "Imperiali": # The divisors are 2,3,4 etc
        return numSeats + 2
    else:
        print "ERROR: Unknown method"

def calculateLargestRemainder(votes, numSeats, method, threshold, votePercentages, validVotes):

    # I don't use threshold so far
    
    remainder = {}
    results = {}
    
    if method == "Hare Quota":
        quota = validVotes / numSeats # Integer or float???
    elif method == "Droop Quota":
        quota = 1 + (validVotes / (1 + numSeats))

    #print quota

    tempSeats = 0
    for party in votes:
        tempVQ = votes[party]/float(quota) # Calculate votes/quota
        results[party] = int(floor(tempVQ))  # Automatic seats
        remainder[party] = tempVQ - results[party]  # Remainder
        tempSeats = tempSeats + results[party]

    #sorted_remainder = sorted(remainder.iteritems(), key=(operator.itemgetter(1))
    for party in sorted(remainder, key=remainder.get, reverse=True):
        print party, remainder[party]
        if tempSeats < numSeats:
            results[party] = results[party] + 1
            tempSeats = tempSeats + 1
            
    return results
            
def calculateHighestAverage(votes, numSeats, method, threshold, votePercentages):
        
    lastQuot = {}
    nextSeat = {}
        
    # Initialize the results dictionary for the parties in votes
    results = {}
    for party in votes:
        results[party] = 0  # They start with 0 seats each
        
    # Calculate the number of seats for each party        
    for i in range(1, numSeats + 1):
        highest = 0 # Highest value in this round (reset it to 0 in each round)
        seatTo = "" # Who gets the seat in this round (reset it to "" in each round)
    
        for party in votes:
            if votePercentages[party] > threshold:
                quot = float(votes[party])/getDivisor(results[party], method) # Calculate the quot for this party in this round
                #print party, results[party], quot
                if quot > highest:  # If the quot is bigger than the highest value in this round:
                    seatTo = party  # the party becomes the candidate to get this seat
                    highest = quot  # save the quot to check it with the values for the rest of parties
                elif quot == highest: # If the quot is equal to the highest value in this round:
                    if votes[party] > votes[seatTo]: # the seat goes to the party that has more votes
                        seatTo = party
                        highest = quot
                # Save the last quots to calculate the number of extra votes needed to get the last seat
                if i == numSeats:
                    lastQuot[party] = quot
                    
        # The party with the highest quot gets another seat
        results[seatTo] = results[seatTo] + 1
        #print "----"
            
    #print "Last seat to:", seatTo
    for party in votes:
        # The party that got the last seat needs 0 votes to get the last vote
        if party == seatTo:
            nextSeat[party] = 0
            #print "*************", party, nextSeat[party], "************************"
        # The rest of parties need to get a bigger quot than the party that got the last seat
        else:
            nextSeat[party] = int(ceil(lastQuot[seatTo] * getDivisor(results[party], method)) - votes[party]) + 1# The difference between the votes needed to get the last seat minus the actual votes plus 1
            #print "lastQuot[seatTo]", lastQuot[seatTo], "getDivisor(results[party], method)", getDivisor(results[party], method)
            #print "ceil(lastQuot[seatTo] * getDivisor(results[party], method)", ceil(lastQuot[seatTo] * getDivisor(results[party], method))
            #print "ceil(lastQuot[seatTo] * getDivisor(results[party], method)) - votes[party]", ceil(lastQuot[seatTo] * getDivisor(results[party], method)) - votes[party]
            #print "int(ceil(lastQuot[seatTo] * getDivisor(results[party], method)) - votes[party])", int(ceil(lastQuot[seatTo] * getDivisor(results[party], method)) - votes[party])
            #print "+++++++++++++", party, nextSeat[party], "++++++++++++++++++++++++++"
    return results, nextSeat

