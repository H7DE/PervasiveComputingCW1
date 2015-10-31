#Class for generating topologies using tinyos' linklayermodel
import os



#Topology configs
#GRID = "1"
#UNIFORM = "2"
#RANDOM = "3"

def createTopology(topology, noNodes):
    #Make topology file for linklayermodel
    filePath = "tmp/tmp.cfg"
    if os.path.exists(filePath):
        os.remove(filePath)
    with open("tmp/tmp.cfg", "w") as config:
        config.write("PATH_LOSS_EXPONENT = 2.0;\
        SHADOWING_STANDARD_DEVIATION = 3.2;\
        D0 = 1.0;\
        PL_D0 = 55.0;NOISE_FLOOR = -105.0;\
        S11 = 3.7;\
        S12 = -3.3;\
        S21 = -3.3;\
        S22 = 6.0;\
        WHITE_GAUSSIAN_NOISE = 4;\
        TOPOLOGY = {tp};\
        GRID_UNIT = 1.0;\
        TOPOLOGY_FILE = topologyFile;\
        NUMBER_OF_NODES = {nodes};\
        TERRAIN_DIMENSIONS_X = 100.0;\
        TERRAIN_DIMENSIONS_Y = 100.0;".format(tp=topology, nodes=noNodes))

if __name__ == "__main__":
    createTopology(3, 3)
