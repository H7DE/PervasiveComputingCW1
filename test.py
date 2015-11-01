import sys
from random import *
from TOSSIM import *

import math
import os
import sqlite3
import StringIO
import re
import random

from genTopology import *


db_filename = 'wsn.db'
schema_filename = 'db_schema.sql'
EXPECTED_NO_TRANSMISSIONS=100


#Runs the CollectionTree tinyos program
#Returns a list of tuples containing (node_id, transmission_round_of_pkt)
def runSim(noNodes, topologyType):
    #Init tossim
    t = Tossim([])
    r = t.radio()

    log_file = "tmp/output.txt"
    if os.path.exists(log_file):
        os.remove(log_file)

    with open(log_file, 'w+') as output:

        #Uncomment/comment for verbose output from simulation
        #t.addChannel("Boot", sys.stdout)
        t.addChannel("App", sys.stdout)
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

        #Boot motes and randomised times to minimise radio interference
        for i in range(0,  noNodes):
            t.getNode(i).createNoiseModel()
            t.getNode(i).bootAtTime(long(i * 1000 * random.uniform(1, 10)))

        print("Running sim(may take a long time)")
        #We need a sufficiently long time to run simulation
        #This formula has been experimentally test to do well
        if noNodes <= 20:
            timer_ticks = long(10000 * math.pow(noNodes, 2));
        else:
            timer_ticks = long(1000 * math.pow(noNodes,  3));

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
        output.flush()
        output.close()
    return resultsList


def addSimResultsToDB(experimentId, experimentType, noNodes, expNoNodeTransmission, resultsList):
    db_exist = os.path.exists(db_filename)
    with sqlite3.connect(db_filename) as conn:
        with open(schema_filename, 'rt') as f:
            if not db_exist:
                schema = f.read()
                conn.executescript(schema)

        cursor = conn.cursor()
        #Add each node that participated in simulation
        cursor.execute('insert or ignore into experiments values (?,?,?,?)', (experimentId, noNodes, experimentType, expNoNodeTransmission))
        #Add node readings
        for n, t in resultsList:
            cursor.execute('insert or ignore into readings values (?,?,?)', (experimentId, n, t))
        conn.commit()


#No nodes includes sensor nodes
#Grid/Uniform must be square no
#Runs a single experiment
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: test.py <numNodes> <topologyType> <experimentName>")
        exit()
    noNodes =  int(sys.argv[1])
    topo = sys.argv[2]
    expName = sys.argv[3]
    res =  runSim(noNodes, topo)
    addSimResultsToDB(expName, topo, noNodes, EXPECTED_NO_TRANSMISSIONS, res)
    print ("Experiment: " + expName +" saved to wsn.db")


