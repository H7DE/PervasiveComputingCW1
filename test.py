from sys import *
from random import *
from TOSSIM import *
from tinyos.tossim.TossimApp import *


#Command line arguments parsing
#TODO: Error handling
noNodes = int(sys.argv[1])
topologyFile = sys.argv[2]


n = NescApp()
t = Tossim(n.variables.variables())
r = t.radio()

t.addChannel("Boot", sys.stdout)
t.addChannel("App", sys.stdout)


print("Setting up network topology")

f = open(topologyFile, 'r')
for line in f:
    s = line.split()
    if s[0] == "gain":
        r.add(int(s[1]), int(s[2]), float(s[3]))

print("Setting up network noise model")
noise = open('meyer-heavy.txt', 'r')
for line in noise:
    s = line.strip()
    if s:
        val = int(s)
        for i in range(noNodes):
            t.getNode(i).addNoiseTraceReading(val)


#t.getNode(0).bootAtTime(1000);
for i in range(0,  noNodes):
    t.getNode(i).createNoiseModel()
    t.getNode(i).bootAtTime(i * 2351217 + 23542399)

"""
m = t.getNode(0)
simDone = m.getVariable('CollectionTreeC.SIM_DONE').getData()
while not simDone:
    t.runNextEvent()

"""
for i in range(100000):
    t.runNextEvent()

