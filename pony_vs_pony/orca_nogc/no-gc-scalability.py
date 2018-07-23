
import sys
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('bmh')
cores = [4, 8, 16, 32, 64]


def plot(ax, orca, nogc, name):
  ax.plot(cores, orca, 'ro-', label="orca")
  ax.plot(cores, nogc, 'g^-', label="no-gc")
  # ax.plot(cores, bdw, 'b*-', label="bdw")
  # ax.set_title(name)
  ax.set_xlabel('cores', fontsize=16)

def finalisePlot(name):
  plt.legend(loc='best', shadow=True, fontsize=16)
  plt.savefig(name + '_scalability.pdf', format='pdf', pad_inches=0, bbox_inches='tight') 

def read_file(fn):
  with open(fn) as f:
    return f.readlines()

def newRun(d, cores, time):
  t = d.get(cores, -1)
  if t == -1:
    d[cores] = time
  else: 
    d[cores] = t + time

def parse(fn): 
  d = {}
  for line in read_file(fn): 
    """4 cores :: iteration 1 :: 2.40"""
    xyz=line.split(" :: ")
    cores=int(xyz[0].replace(" cores", ""))
    time=float(xyz[2])
    newRun(d, cores, time)
  times = []
  c=4
  while c <= 64:
    times.append(d.get(c)/10)
    c = c*2
  return times

def parseAndPlot(name, i):
  orca=parse(name + '/orca.scalability.log')
  nogc=parse(name + '/nogc.scalability.log')
  # bdw =parse(name + '/bdw.scalability.log')
  plot(i, orca, nogc, name)
  finalisePlot(name)

name = sys.argv[1]
f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=False, figsize=(20, 5))
f, ax = plt.subplots()
ax.set_ylabel('time (s)', fontsize=16)
parseAndPlot(name, ax)
# parseAndPlot('trees', ax1)
# parseAndPlot('trees2', ax2)
# parseAndPlot('rings', ax3)
# parseAndPlot('mailbox', ax4)


