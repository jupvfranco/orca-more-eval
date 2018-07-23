#!/usr/bin/env python
import sys
import math
import pylab
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('bmh') # ggplot

def cyclesToSec(x):
  return x/2299946000

def readFile(fn):
  with open(fn) as f:
    return f.readlines()

def parseNoGC(lines): 
  count = 0
  time = 0
  times = []
  for line in lines: 
    """size 10 :: iteration 5 :: 0.27 97512"""
    xyz=line.split(" :: ")
    time = time + float(xyz[2].split(" ")[0])
    count = count + 1 
    if (count == 10):
      times.append(time / 10) # average
      count = 0
      time = 0
  return times

def parseOrca(lines): 
  count = 0
  time = 0
  times = []
  scan = 0
  scans = []
  gc = 0
  gcs = []
  for line in lines:
    # "time_in_behaviour": 1217516916,
    # "time_in_gc": 451066165,
    # "time_in_send_scan": 46988856,
    # "time_in_recv_scan": 78329422
    # size 10 :: iteration 1 :: 0.58 9084 
    if "gc" in line: 
      gc = gc + float(line.split(":")[1])
    elif "send" in line: 
      scan = scan + float(line.split(":")[1])
    elif "rcv" in line: 
      scan = scan + float(line.split(":")[1])
    elif "size" in line: 
      xyz=line.split(" :: ")
      time = time + float(xyz[2].split(" ")[0])
      count = count + 1
      if (count == 10):
        times.append(time / 10) # average
        time = 0
        gcs.append(cyclesToSec(gc / 10))
        gc = 0
        scans.append(cyclesToSec(scan / 10))
        scan = 0
        count = 0
  return [times, gcs, scans]

sizes    = [ 10, 20, 30, 40, 50, 60 ]
nogc = parseNoGC(readFile("nbody/nogc.log"))
orca = [orcaTotal, orcaGC, orcaScan] = parseOrca(readFile("nbody/orca.log"))
print sizes
print nogc
print orcaTotal

# starts code for plotting 

colors = ['#79B6FF', '#4F76A6', '#2ca02c', '#C993FF', '#8A65AF', '#553E6C']
patterns = ['o', '\\', 'x', '.', '-', 'O', '*', '+']

N = 6 # sizes
ind = np.arange(0, 1.8, 0.30) #N)  # the x locations for the groups
width = 0.1       # the width of the bars

fig, ax = plt.subplots()
ponytotal = ax.bar(
  ind,
  orcaTotal,
  width,
  color=colors[0],
  edgecolor='black',
  hatch=patterns[0]
)
ponyscan = ax.bar(
  ind,
  orcaScan,
  width,
  color=colors[1],
  edgecolor='black',
  hatch=patterns[1]
)
ponygc = ax.bar(
  ind,
  orcaGC,
  width,
  color=colors[2],
  edgecolor='black',
  hatch=patterns[2],
  bottom=orcaScan
)

nogc = ax.bar(
  ind + width + 0.005,
  nogc,
  width,
  color=colors[3],
  edgecolor='black',
  hatch=patterns[3])

# add some text for labels, title and axes ticks
ax.set_ylabel('Time (seconds)', fontsize=16)
ax.set_xlabel('# Bodies', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(sizes)
ax.tick_params(labelsize=16)


plt.legend(
  (ponytotal[0], ponyscan[0], ponygc[0], nogc[0]),
  ('ORCA-total', 'ORCA-scan', 'ORCA-GC', 'NoGC-total'),
  loc='best') 

plt.tight_layout()
plt.savefig('nbody.pdf', format='pdf', pad_inches=0.1, bbox_inches='tight')


# # figlegend = pylab.figure(figsize=(1.9, 1.9)) #
# # figlegend.legend(
# #   (ponytotal[0], ponyscan[0], ponygc[0], erlangtotal[0], erlangcopy[0], c4total[0]),
# #   ('ORCA-total', 'ORCA-scan', 'ORCA-GC', 'Erlang-total','Erlang-copy', 'C4-total') ) #,
# # figlegend.savefig('legend.pdf', format='pdf', bbox_inches='tight')
