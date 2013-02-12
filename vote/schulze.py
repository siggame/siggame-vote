#!/usr/bin/env python
#
# Schulze Voting Scheme
# https://en.wikipedia.org/wiki/Schulze_method

# Input is an iterable of ballots
# All ballots must have the same candidates
# Each ballot must have all candidates
#
# A ballot is a list of candidates, with candidates occuring earlier
#  in the list being prefered over candidates occuring later in the list.
# Each candidate may only appear once per ballot.
# Example Ballot: ['Pete', 'Frank', 'Oliver', 'Bob']

# Output is the single winner chosen by the Schulze voting algorithm


def schulze(ballots):
    candidates = ballots[0]
    # d is the pairwise preference grid. d is a stupid name
    d = {(i, j): 0 for i in candidates for j in candidates}
    for b in ballots:
        for (x, y) in d.keys():
            if b.index(x) < b.index(y):
                d[(x, y)] += 1

    # p is the strengths of the strongest paths grid. p is also a stupid name
    p = dict()
    for i in candidates:
        for j in candidates:
            if i != j:
                if d[(i, j)] > d[(j, i)]:
                    p[(i, j)] = d[(i, j)]
                else:
                    p[(i, j)] = 0
    for i in candidates:
        for j in candidates:
            if i != j:
                for k in candidates:
                    if i != k and j != k:
                        p[(j, k)] = max(p[(j, k)],
                                        min(p[(j, i)], p[(i, k)]))

    # now find the candidate i for which:
    #  p[(i,j)] > p[(j,i)] for all j in candidates
    for i in candidates:
        winner = True
        for j in candidates:
            if i != j:
                if p[(i, j)] < p[(j, i)]:
                    winner = False
                    break
        if winner == True:
            return i


def test():
    ballots = [['A', 'C', 'B', 'E', 'D']] * 5 + \
              [['A', 'D', 'E', 'C', 'B']] * 5 + \
              [['B', 'E', 'D', 'A', 'C']] * 8 + \
              [['C', 'A', 'B', 'E', 'D']] * 3 + \
              [['C', 'A', 'E', 'B', 'D']] * 7 + \
              [['C', 'B', 'A', 'D', 'E']] * 2 + \
              [['D', 'C', 'E', 'B', 'A']] * 7 + \
              [['E', 'B', 'A', 'D', 'C']] * 8
    assert schulze(ballots) == 'E'
    print "PASS"

if __name__ == "__main__":
    test()
