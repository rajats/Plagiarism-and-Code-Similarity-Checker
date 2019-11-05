import random
import string
import os 

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


