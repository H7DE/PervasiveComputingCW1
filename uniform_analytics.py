from test import *
import matplotlib.pyplot as plt

resultsTable = [] #Table of number of nodes and packet transmitted(%)

#Generate a frequency table of (number of node in simulation, percentage of packets transmitted)
with sqlite3.connect("sample_db/grid_uniform.db") as conn:
    cursor = conn.cursor()
    for i in range(2, 9):
        numNodes = i*i
        amount_pkt = "select count(*) from readings where\
                readings.experiment_id = 'uniform_topo_node_{exprNo}'".format(exprNo=numNodes)
        cursor.execute(amount_pkt)
        noPkts = cursor.fetchall()[0][0];

        maxExpect_pkts = "select experiments.expected_no_transmission_per_node \
                * (experiments.no_nodes - 1) from experiments\
        where experiments.experiment_id = 'uniform_topo_node_{exprNo}'".format(exprNo=numNodes)

        cursor.execute(maxExpect_pkts)
        maxPkts = cursor.fetchall()[0][0];

        resultsTable.append((numNodes, float(noPkts)/float(maxPkts)*100))


#Create plot
plt.plot(*zip(*resultsTable))
plt.title("Comparing WSN network size with % pkt loss")
plt.xlabel('Number of node in simulation')
plt.ylabel('% of Pkts successfully transmitted')
plt.show()
