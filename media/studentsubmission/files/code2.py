import sys

def check(a, b, s):
    count = 0
    for i in xrange(len(a)):
        k = ord(a[i]) + s
        if k > ord('z'):
            k = k + ord('a') - ord('z') - 1
        if k != ord(b[i]):
            count += 1
    return count

t = int(raw_input().strip())
for a0 in xrange(t):
    P,E = raw_input().strip().split(' ')
    P,E = [str(P),str(E)]
    checked = [False for i in xrange(26)]
    best = len(P)
    for i in xrange(len(P)):
        k = ord(E[i]) - ord(P[i])
        if k < 0:
            k += 26
        if not checked[k]:
            best = min(best, check(P, E, k))
            checked[k] = True
    print best
