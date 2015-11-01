from test import *


freqTable = {} #Dictionary of number of nodes and packet transmitted(%)



#Import data from db
with sqlite3.connect("sample_db/grid_uniform.db") as conn:
    cursor = conn.cursor()
    for i in range(2, 9):
        results=[]
        amount_pkt = "select count(*) from readings where\
                readings.experiment_id = 'grid_topo_node_{exprNo}'".format(exprNo=i*i)
        cursor.execute(amount_pkt)
        noPkts = cursor.fetchall()[0][0];

        maxExpect_pkts = "select experiments.expected_no_transmission_per_node \
                * (experiments.no_nodes - 1) from experiments\
        where experiments.experiment_id = 'grid_topo_node_{exprNo}'".format(exprNo=i*i)

        cursor.execute(maxExpect_pkts)
        maxPkts = cursor.fetchall()[0][0];

        print float(noPkts)/float(maxPkts)*100;

"""
    for i in range(2, 54):
        cursor.execute("select count(*),\
                        (select sum(experiments.no_nodes) from experiments where experiments.experiment_id\
                        in (select distinct experiments.experiment_id from experiments where\
                        experiments.no_nodes ={noNodes} and experiments.topology_type='{etype}') ) * 100\
                        as expectedPkt from readings\
                        where readings.experiment_id\
                            in (select distinct experiments.experiment_id from experiments\
                            where experiments.no_nodes = {noNodes} and experiments.topology_type='{etype}')".format(noNodes=4, etype="random"))
    for
        print cursor.fetchall()
    """

    #Generate freq table

#Plot tables
"""
values = [list(t) for t in zip(*result)]
print (values)
import matplotlib.pyplot as plt
plt.plot([sum(values[1])/expectNoPkts])
plt.ylabel('Pkt loss')
#plt.set_ylim([0, 100])
plt.show()
"""
