
import sys
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('bmh')

def read_file(fn):
    with open(fn) as f:
        return f.readlines()

def parse(lines):
	result = []
	for line in lines: 
		"""(32,8,4305)"""
		x = line.replace("(", "").replace(")", "").split(",")[2]
		total_i = float(x)/1000000
		result.append(total_i)
	return result

def plot(ax,name,data):
  ax.plot(x, data, '.', color='black')
  ax.set_xticks([], [])
  ax.set_title(name)

prefix = sys.argv[1]
ys = parse(read_file(prefix + "/linear.log"))
xs = np.arange(0, len(ys))

f, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 5))
ax.plot(xs, ys, '.')

ax.set_ylabel('total(i)', fontsize=16)
ax.set_xlabel('i', fontsize=16)
ax.tick_params(labelsize=16)


plt.tight_layout()
plt.savefig(prefix + '_1server.pdf', format='pdf', pad_inches=0, bbox_inches='tight')