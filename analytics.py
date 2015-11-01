from test import *
import time

#Script to run several test at a time and analyse the results
def runSims(name, topo, noNodes):
        exp = name
        res =  runSim(noNodes, topo)
        addSimResultsToDB(exp, topo, noNodes, EXPECTED_NO_TRANSMISSIONS, res)
        print "Simulation complete"

runSims("exp1", "random", 30)
