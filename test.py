from sys import *
from random import *
from TOSSIM import *
from tinyos.tossim.TossimApp import *


#Command line arguments parsing
#TODO: Error handling
noNodes = int(sys.argv[1])
topologyFile = sys.argv[2]


print("Creating simulation for ",  noNodes, "nodes")



n = NescApp()
t = Tossim(n.variables.variables())
r = t.radio()



outFile = open('output.txt', 'r+')

t.addChannel("Boot", sys.stdout)
t.addChannel("App", sys.stdout)
t.addChannel("App", outFile)

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


for i in range(0,  noNodes):
    t.getNode(i).createNoiseModel()
    t.getNode(i).bootAtTime(i * 100000)

"""
m = t.getNode(0)
simDone = m.getVariable('CollectionTreeC.SIM_DONE').getData()
while not simDone:
    t.runNextEvent()

"""
print("Running sim")
for i in range(100000):
    t.runNextEvent()

#Read output file into db
NODE_ID = 4
NODE_TRANSMISSION_ROUND = 6

resultsList = []
for line in outFile:
    match = re.search(r'(\w+) (\S+) (\w+): (\S+), (\w+): (\S+)', line)
    resultsList.append((match.group(NODE_ID), match.group(NODE_TRANSMISSION_ROUND)))

print resultsList
#Calculate pkt loss

import os
import sqlite3

db_filename = 'wsn.db'
with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT SQLITE_VERSION()')
    data = cursor.fetchone()
    print 'SQLite version: ', data

outFile.close()



