# I am considering the first email id in "to" field as receiver email id

import re
header_details = {}
previous_header = ''
input_header_to = []          #for reply all, if there are multiple email ids in "to" field then we need all email ids except first one(receiver's id)
print "Enter file name"
file_name = raw_input()
input_header = open(file_name, 'r').read()  #all file contents to string
#print input_header

for line in input_header.split('\n'):       #split string by new line, it will give list whose each element in one line of string
	if ':' in line:
		splitted_line = line.split(':')     #split line by ":", left side will become key and right will be added as key
		header_details[splitted_line[0]] = splitted_line[1]
		previous_header = splitted_line[0]
	else:
		header_details[previous_header] += line  #if there's no ":" in line then add that line as value to previous key

input_header_to = header_details['to'].split(',')  #splitting the received to by "," to count number of email ids in to field
try:
	if len(input_header_to) > 10:				   #if number of email ids in "to" exceeds 10 then throw error
		raise Error()
except:
	exit("max email ids in to field can be 10")

print "select 1)reply 2)reply all"
choice = int(raw_input())

to, cc, sub, body = '', '', '', ''
try:
	to = header_details['from'].lstrip()         #using try to avoid key error in dictonary
except:
	exit("error no to field found")
try:
	sub = header_details['subject'].lstrip()
except:
	sub = ''                                    #if no subject then leave it as empty
if choice == 1:
	sub = 'Reply '+sub                         #append reply before subject
if choice == 2:                                #for reply all we need all email ids in "cc" and in "to" (if there are more than one email id in "to")
	if len(input_header_to) > 1:               #if there are multiple email ids in "to", then for reply all except for first one(which is of receiver) keep the rest in "to" field
		to += ','+','.join(input_header_to[1:])
	try:
		cc = header_details['cc'].lstrip()
	except:
		cc = ''
	try:
		if len(cc.split(',')) > 10:          #if number of email ids in cc exceeds 10 then throw error 
			raise Error()
	except:
		exit("max email ids in cc can be 10")
	sub = 'Reply all '+sub                  #append reply all before subject
reply_header = 'to: '+to+'\n'+'cc: '+cc+'\n'+'subject:  '+sub+'\n'
if re.match(r'[A-Za-z]', to):               #checking if name preceeds the email id then add "Hi <name>," in template
	body = "Hi "+to[:to.find('<')].rstrip()+",\n"
else:
	body = "Hi,\n"
reply_header += body
output_header = open("output_header.txt",'w')
output_header.write(reply_header)
output_header.close()

