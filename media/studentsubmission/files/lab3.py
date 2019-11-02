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
    random_str = ''.join(random.choice(alphabets) for x in range(length))   #randomly choosing a string
    random_string_gen = random.randrange(1,50)
    #print (length)
    #print (random_str)
    #print (random_string_gen)
    string_gen = 1
    random_name = ""
    for name in permute(random_str,""):                     #not needed for extra randomness, choosing randomly a permutation as random name between 1 to 50 permutations of randomly chosen string
        random_name = name
        if string_gen == random_string_gen:
            break
        string_gen += 1
    print ("random name", random_name)
    return random_name

#create folder
dir_name = 'Lab3Dir'
try:
    os.mkdir(dir_name)
    print("Directory " , dir_name ,  " Created ") 
except FileExistsError:
    print("Directory " , dir_name ,  " already exists")

try:
    os.chdir(dir_name)
except:
    exit('Invalid Path')
for i in range(500):
    all_files = os.listdir()
    while (True):
        random_name = random_name_generator()+'.txt'
        #random_name = 'ENAgwiWbzWaXwS.txt'
        if random_name not in all_files:
            break    
        else:
            print("Filename already exists. Retrying!")
            #break
    open(random_name, 'a').close()

print ("Total files in Directory: ",len(os.listdir()))

