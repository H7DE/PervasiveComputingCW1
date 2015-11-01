from test import *
import matplotlib.pyplot as plt

resultsTable = [] #Table of number of nodes and packet transmitted(%)

#Generate a frequency table of (number of node in simulation, percentage of packets transmitted)
with sqlite3.connect("sample_db/uniform.db") as conn:
    cursor = conn.cursor()
    exprRootName="expr_topo_uniform_"
    for i in range(2, 8):
        numNodes = i
        amount_pkt = "select count(*) from readings where\
                readings.experiment_id = '{exprName}{exprNo}'".format(exprName=exprRootName, exprNo=numNodes)
        cursor.execute(amount_pkt)
        noPkts = cursor.fetchall()[0][0];

        maxExpect_pkts = "select experiments.expected_no_transmission_per_node \
                * (experiments.no_nodes - 1) from experiments\
        where experiments.experiment_id = '{exprName}{exprNo}'".format(exprName=exprRootName, exprNo=numNodes)

        cursor.execute(maxExpect_pkts)
        maxPkts = cursor.fetchall()[0][0];

        resultsTable.append((i*i, float(noPkts)/float(maxPkts)*100))


