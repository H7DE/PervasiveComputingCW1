from test import *


def runSims(topo):
    for i in range(2, 64):
        exp = "rand_topo_node_" + str(i)
        res =  runSim(i, topo)
        addSimResultsToDB(exp, topo, i, EXPECTED_NO_TRANSMISSIONS, res)
runSims("random")
