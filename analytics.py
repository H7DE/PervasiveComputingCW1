from test import *
import time

#Script to run several test at a time and analyse the results
def runSims(topo):
    for i in range(3, 4):
        exp = "rand_topo_node_" + str(i)

        noNodes =  i
        res =  runSim(noNodes, topo)
        addSimResultsToDB(exp, topo, noNodes, EXPECTED_NO_TRANSMISSIONS, res)
        print "Sleeping to prevent I/O issues"
        time.sleep(1)
        """
        res =  runSim(i, topo)
        addSimResultsToDB(exp, topo, i, EXPECTED_NO_TRANSMISSIONS, res)
        """

runSims("random")
