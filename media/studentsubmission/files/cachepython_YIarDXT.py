from datetime import datetime
from matplotlib import pyplot as plt

def create_int_list(size):
	int_list = [0] * size
	start_time = datetime.now()
	for i in xrange(64*1024*1024):
		int_list[(i * 16) % size] *= 1
	end_time = datetime.now()
	elapsed = (end_time - start_time).microseconds
	del(int_list)
	return elapsed


print "approximating cache size using integer list"
#int size is 4B, so int list of 256 elements will make int list size 1024B or 1KB
size = 256
sizes_in_KB = []
time_elapsed = []
while(size <= 4 * 1024 * 1024):
	print "size ", (size/256),"KB"
	sizes_in_KB.append(size/256)
	time_elapsed.append(create_int_list(size))
	size *= 2

print sizes_in_KB
print time_elapsed
plt.plot(sizes_in_KB, time_elapsed)
plt.xlabel('Size in KB')
plt.ylabel('Execution time')
plt.show()