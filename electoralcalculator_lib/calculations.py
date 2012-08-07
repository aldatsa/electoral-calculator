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


from math import ceil, floor

from Methods import Methods


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
        votePercentages[party] = round(100 *
                                       (float(votes[party]) / totalVotes), 2)

    return votePercentages


def calculateSeatPercentages(numSeats, seats):
    seatPercentages = {}

    for party in seats:
        seatPercentages[party] = round(100 *
                                       (float(seats[party]) / numSeats), 2)

    return seatPercentages


def getDivisor(numSeats, method, MSLFD=1.4):
    if method == Methods.DHONDT:
        return numSeats + 1
    elif method == Methods.SAINTE_LAGUE:
        return 2 * numSeats + 1
    elif method == Methods.MODIFIED_SAINTE_LAGUE:
        if numSeats == 0:
            return MSLFD
        else:
            return 2 * numSeats + 1
    elif method == Methods.IMPERIALI:  # The divisors are 2,3,4 etc
        return numSeats + 2
    else:
        print "ERROR: Unknown method"


def calculateLargestRemainder(votes, numSeats, method, threshold,
                              votePercentages, validVotes):

    # I don't use threshold so far

    remainder = {}
    results = {}

    # The largest remainder method requires the numbers of votes for each party
    # to be divided by a quota representing the number of votes required for a
    # seat (i.e. usually the total number of votes cast divided by the number
    # of seats, or some similar formula). The result for each party will
    # usually consist of an integer part plus a fractional remainder.

    # Calculate the quota for the current method
    if method == Methods.HARE_QUOTA:
        quota = validVotes / numSeats  # Integer or float???
    elif method == Methods.DROOP_QUOTA:
        quota = 1 + (validVotes / (1 + numSeats))

    #print quota

    # Each party is first allocated a number of seats equal to their integer.
    # This will generally leave some seats unallocated.
    tempSeats = 0
    for party in votes:
        tempVQ = votes[party] / float(quota)        # Calculate votes/quota
        results[party] = int(floor(tempVQ))         # Automatic seats
        remainder[party] = tempVQ - results[party]  # Remainder
        tempSeats = tempSeats + results[party]

    # The parties are then ranked on the basis of the fractional remainders,
    # and the parties with the largest remainders are each allocated one
    # additional seat until all the seats have been allocated.
    # This gives the method its name.
    for party in sorted(remainder, key=remainder.get, reverse=True):
        #print party, remainder[party]
        if tempSeats < numSeats:
            results[party] = results[party] + 1
            tempSeats = tempSeats + 1

    return results


def calculateHighestAverage(votes, numSeats, method,
                            threshold, votePercentages):

    lastQuot = {}
    nextSeat = {}

    # Initialize the results dictionary for the parties in votes
    results = {}
    for party in votes:
        results[party] = 0  # They start with 0 seats each

    # Calculate the number of seats for each party
    for i in range(1, numSeats + 1):
        # Highest value in this round (reset it to 0 in each round)
        highest = 0

        # Who gets the seat in this round (reset it to "" in each round)
        seatTo = ""

        for party in votes:
            if votePercentages[party] > threshold:
                # Calculate the quot for this party in this round
                quot = float(votes[party]) / getDivisor(results[party],
                                                        method)
                # If the quot is bigger than the highest value in this round:
                if quot > highest:
                    # the party becomes the candidate to get this seat
                    seatTo = party
                    # save the quot to check it with the values
                    # for the rest of parties
                    highest = quot
                # If the quot is equal to the highest value in this round:
                elif quot == highest:
                    # the seat goes to the party that has more votes
                    if votes[party] > votes[seatTo]:
                        seatTo = party
                        highest = quot
                # Save the last quots to calculate the number of
                # extra votes needed to get the last seat
                if i == numSeats:
                    lastQuot[party] = quot

        # The party with the highest quot gets another seat
        results[seatTo] = results[seatTo] + 1

    for party in votes:
        # The party that got the last seat needs 0 votes to get the last vote
        if party == seatTo:
            nextSeat[party] = 0
        # The rest of parties need to get a bigger quot
        # than the party that got the last seat
        else:
            nextSeat[party] = int(ceil(lastQuot[seatTo] *
                                       getDivisor(results[party], method)) -
                                  votes[party])
            if (lastQuot[seatTo] == votes[party] + nextSeat[party] or
            lastQuot[seatTo] == (votes[party] + nextSeat[party]) /
                                     getDivisor(results[party], method) and
            votes[seatTo] > votes[party]):
                nextSeat[party] += 1
    return results, nextSeat
