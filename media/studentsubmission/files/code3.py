import sys
import operator

def possible_encryption(P, E):
    shifts = dict()
    n = len(P)

    for i in xrange(n):
        cnt = shifts.get((ord(E[i]) - ord(P[i]))%26, 0)
        shifts[(ord(E[i]) - ord(P[i]))%26] =  cnt + 1
    max_shift = max(shifts.iteritems(), key=operator.itemgetter(1))[1]
    return n - max_shift
     
if __name__ == "__main__":
    t = int(raw_input().strip())
    for a0 in xrange(t):
        P,E = raw_input().strip().split(' ')
        P,E = [str(P),str(E)]
        print possible_encryption(P, E)
