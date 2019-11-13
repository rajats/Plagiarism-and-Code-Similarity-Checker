import sys
def buildCoder(shift):
    dict={ 'a': 'a', 'c': 'c', 'b': 'b', 'e': 'e', 'd': 'd', 'g': 'g', 'f': 'f', 'i': 'i', 'h': 'h', 'k': 'k', 'j': 'j', 'm': 'm', 'l': 'l', 'o': 'o', 'n': 'n', 'q': 'q', 'p': 'p', 's': 's', 'r': 'r', 'u': 'u', 't': 't', 'w': 'w', 'v': 'v', 'y': 'y', 'x': 'x', 'z': 'z'}
    for keys in dict:
        if ord(keys)>=65 and ord(keys)<=90:
            ascii_value=ord(keys)
            new_ascii=shift+ascii_value
            if new_ascii>90:
                new_ascii=new_ascii+13
                new_ascii=new_ascii%26
                new_ascii += 65
            dict[keys]=chr(new_ascii)
                
        if ord(keys)>=97 and ord(keys)<=122:
            ascii_value=ord(keys)
            new_ascii=shift+ascii_value
            if new_ascii>122:
                new_ascii=new_ascii+7
                new_ascii=new_ascii%26
                new_ascii += 97
            dict[keys]=chr(new_ascii)
    return dict

def diff(x,y):
    d=0
    for i in range(len(x)):
        if x[i]!=y[i]:
            d+=1
    return d

t = int(raw_input().strip())
for a0 in xrange(t):
    P,E = raw_input().strip().split(' ')
    P,E = [str(P),str(E)]
    d=100
    for shift in range(26):
        get_map = buildCoder(shift)
        D=""
        for letter in P:
            D+=get_map[letter]
        if diff(D,E) < d:
            d=diff(D,E)
    print d
