from datetime import datetime
from matplotlib import pyplot as plt

def create_int_list(size):
	int_arr = [0] * size
	sec1 = datetime.now()
	for i in xrange(64*1024*1024):
		int_arr[(i * 16) % size] *= 1
	sec2 = datetime.now()
	spent = (sec2 - sec1).microseconds
	del(int_arr)
	return spent


print size
print spent
print "justhere"
print "justhere"
print "justhere"
print "justhere"
print "justhere"