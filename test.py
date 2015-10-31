from sys import *
from random import *
from TOSSIM import *
from tinyos.tossim.TossimApp import *

import os
import sqlite3
import StringIO

from genTopology import *
#Command line arguments parsing
#TODO: Error handling


db_filename = 'wsn.db'
schema_filename = 'db_schema.sql'
EXPECTED_NO_TRANSMISSIONS=100


#Runs the CollectionTree tinyos program
#Returns a list of tuples containing (node_id, transmission_round_of_pkt)
def runSim(noNodes, topologyType):
    #Init tossim
    n = NescApp()
    t = Tossim(n.variables.variables())
    r = t.radio()

    log_file = "tmp/output.txt"
    if os.path.exists(log_file):
        os.remove(log_file)

    output=open(log_file, 'w+')

    #Uncomment for verbose output from simulation
    #t.addChannel("Boot", sys.stdout)
    #t.addChannel("App", sys.stdout)
    t.addChannel("App", output)

    topology = getTopology(noNodes, topologyType)
    for (n1, n2, gain) in topology:
        r.add(n1, n2, gain)

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

    print("Running sim")
    timer_ticks = 10000 * noNodes;

    for i in range(timer_ticks):
        t.runNextEvent()


    #Parse output file for results
    output.seek(0,0)
    resultsList = []


    #Position vars for regex
    NODE_ID = 4
    NODE_TRANSMISSION_ROUND = 6

    for line in output:
        match = re.search(r'(\w+) (\S+) (\w+): (\S+), (\w+): (\S+)', line)
        resultsList.append((match.group(NODE_ID),
                            int(match.group(NODE_TRANSMISSION_ROUND))))
    return resultsList


#Read output file into db
def addSimResultsToDB(noNodes, resultsList):
    db_exist = os.path.exists(db_filename)
    with sqlite3.connect(db_filename) as conn:
        with open(schema_filename, 'rt') as f:
            if not db_exist:
                schema = f.read()
                conn.executescript(schema)

        cursor = conn.cursor()
        #Add each node that participated in simulation
        for i in range(0 , noNodes):
            cursor.execute('insert or ignore into node values (?)', (str(i)))
        #Add node readings
        for x in resultsList:
            cursor.execute('insert or ignore into readings values (? , ?)', x)

        cursor.execute('SELECT node.node_id, COUNT(transmission_round) FROM node JOIN readings ON(node.node_id = readings.node_id) GROUP BY node.node_id')
        result = cursor.fetchall()
        print result
        conn.commit()
        os.remove(db_filename)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: test.py <numNodes> <topologyType>")
        exit()
    noNodes =  int(sys.argv[1])
    topo = sys.argv[2]
    res =  runSim(noNodes, topo)
    addSimResultsToDB(noNodes, res)




"""
noNodes = int(sys.argv[1])
topologyFile = sys.argv[2]
expectNoPkts = int(sys.argv[3]) #Small hack as variable inspect in tossim doesnt work on lab machines

#Constants
db_filename = 'wsn.db'
schema_filename = 'db_schema.sql'

#Simulation files

#outFile = open(log_file, 'w+')



print("Creating simulation for ",  noNodes, "nodes")




print("Setting up network topology")
"""
"""
#Parse results file


#Add result to db
db_exist = os.path.exists(db_filename)
with sqlite3.connect(db_filename) as conn:
    with open(schema_filename, 'rt') as f:
        if not db_exist:
            schema = f.read()
            conn.executescript(schema)

    cursor = conn.cursor()
    #Add each node that participated in simulation
    for i in range(0 , noNodes):
        cursor.execute('insert or ignore into node values (?)', (str(i)))
    #Add node readings
    for x in resultsList:
        cursor.execute('insert or ignore into readings values (? , ?)', x)

    cursor.execute('SELECT node.node_id, COUNT(transmission_round) FROM node JOIN readings ON(node.node_id = readings.node_id) GROUP BY node.node_id')
    result = cursor.fetchall()
    print result
    conn.commit()

    os.remove(db_filename)
"""


"""
values = [list(t) for t in zip(*result)]
print (values)
import matplotlib.pyplot as plt
plt.plot([sum(values[1])/expectNoPkts])
plt.ylabel('Pkt loss')
#plt.set_ylim([0, 100])
plt.show()
"""
#Perform analytics

#Topologies
#MATPLOT LIB
#Star
#Grid
#Random
#Optimisation
#Attributes

#outFile.close()
"""
"""
