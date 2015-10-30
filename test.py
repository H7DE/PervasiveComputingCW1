from sys import *
from random import *
from TOSSIM import *
from tinyos.tossim.TossimApp import *

import os
import sqlite3

#Command line arguments parsing
#TODO: Error handling
noNodes = int(sys.argv[1])
topologyFile = sys.argv[2]


#Constants
db_filename = 'wsn.db'
schema_filename = 'db_schema.sql'

#Simulation files
log_file = "output.txt"
if os.path.exists(log_file):
    outFile = open(log_file, 'r+')
else:
    outFile = open(log_file, 'w+')



print("Creating simulation for ",  noNodes, "nodes")


#Init tossim
n = NescApp()
t = Tossim(n.variables.variables())
r = t.radio()

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
timer_ticks = 100000;
for i in range(timer_ticks):
    t.runNextEvent()

#Read output file into db
NODE_ID = 4
NODE_TRANSMISSION_ROUND = 6


#Parse results file
outFile.seek(0,0)
resultsList = []
for line in outFile:
    match = re.search(r'(\w+) (\S+) (\w+): (\S+), (\w+): (\S+)', line)
    resultsList.append((match.group(NODE_ID), int(match.group(NODE_TRANSMISSION_ROUND))))


#Add result to db
db_exist = os.path.exists(db_filename)
with sqlite3.connect(db_filename) as conn:
    with open(schema_filename, 'rt') as f:
        if not db_exist:
            schema = f.read()
            conn.executescript(schema)

    cursor = conn.cursor()
    cursor.execute('insert into node values (?)', ("1"))
    #Add each node that participated in simulation
    for i in range(0 , noNodes):
        cursor.execute('insert or ignore into node values (?)', (str(i)))
    #Add node readings
    for x in resultsList:
        cursor.execute('insert or ignore into readings values (? , ?)', x)

    cursor.execute('SELECT * FROM readings')
    print cursor.fetchall()
    conn.commit()
    os.remove(db_filename)

#Perform analytics

#Calculate pkt loss


outFile.close()


