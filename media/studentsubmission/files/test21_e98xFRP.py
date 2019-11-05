import random
import string
import os
def permute(s, chosen):
#    print s,chosen
    if not s:
        #perms.append(chosen)
        #print chosen
        yield chosen
    else:
        for i in range(0, len(s)):
            #print "i",s,chosen
            selected_char = s[i]
            chosen += selected_char      #putting a char in chosen
            s = s[:i]+s[i+1:]	#remove that char from string
            yield from permute(s,chosen)
            #permute(s, chosen)
            #unchoose char for backtrack
            s = s[:i]+ selected_char +s[i:]
            chosen = chosen[:-1]
 

def random_name_generator():
    name_lengths = [i+1 for i in range(20)]             #max lentgth of name can be 20 chars
    length = random.choice(name_lengths)                #choosing randomly a length from 1 to 20
    alphabets = string.ascii_lowercase + string.ascii_uppercase         #all alphabets upper and lower case
    random_str = ''.join(random.choice(alphabets) for x in range(length))   
    random_string_gen = random.randrange(1,50)
    string_gen = 1
    random_name = ""
    for name in permute(random_str,""):                    
        random_name = name
        if string_gen == random_string_gen:
            break
        string_gen += 1
    print ("random name", random_name)
    return random_name


