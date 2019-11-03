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


print sizes_in_KB
print time_elapsed
plt.plot(sizes_in_KB, time_elapsed)
plt.xlabel('Size in KB')
plt.ylabel('Execution time')
plt.show()