def read_file(fn):
    with open(fn) as f:
        return [float(x) /1000000 for x in f.readlines()]

import sys
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('bmh')

orca = read_file("serverSim/responsiveness_orca.log")
bdw  = read_file("serverSim/responsiveness_bdw.log")

def plot(ax,name,data):
  ax.plot(x, data, '.', color='black')
  ax.set_xticks([], [])
  ax.set_title(name)


x = np.arange(0, len(orca))
f, (ax1, ax3) = plt.subplots(1, 2, sharey=True, figsize=(10, 3))
plot(ax1, "Orca", orca)
plot(ax3, "BDW",  bdw)

# plt.ylim(0, max(max(orca), max(bdw), max(nogc)))

plt.tight_layout()
plt.savefig('bdw_serverSim.png', format='png', pad_inches=0, bbox_inches='tight')