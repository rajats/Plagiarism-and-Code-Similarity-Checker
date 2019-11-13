import sys

def shiftByOne(P):
  lp=list(P)
  retP=[]
  for x in lp:
    #newX=''
    if x=='z':
      newX='a'
    else:
      newX=chr(ord(x)+1)
    retP.append(newX)
  return retP

def compare(P,E):
  ret=0
  for k in xrange(len(P)):
    if P[k]!=E[k]: 
      ret+=1
  return ret

t = int(raw_input().strip())
for a0 in xrange(t):
    P,E = raw_input().strip().split(' ')
    P,E = [str(P),str(E)]
    diff=101
    for _ in xrange(26):
      P=shiftByOne(P)
      V=compare(P,E)
      #print P,V
      diff=min(diff,V)
    print diff
