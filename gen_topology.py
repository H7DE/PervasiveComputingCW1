#Class for generating topologies using tinyos' linklayermodel
import os



filePath = "tmp/tmp.cfg" #topology file path


#Topology configs
#GRID = "1"
#UNIFORM = "2"
#RANDOM = "3"

def createTopologyConfig(topology, noNodes):
    #Make topology file for linklayermodel
    if os.path.exists(filePath):
        os.remove(filePath)
    with open("tmp/tmp.cfg", "w") as config:
        config.write("PATH_LOSS_EXPONENT = 2.0;\n\
        SHADOWING_STANDARD_DEVIATION = 3.2;\n\
        D0 = 1.0;\n\
        PL_D0 = 55.0;\n\
        NOISE_FLOOR = -105.0;\n\
        S11 = 3.7;\n\
        S12 = -3.3;\n\
        S21 = -3.3;\n\
        S22 = 6.0;\n\
        WHITE_GAUSSIAN_NOISE = 4;\n\
        TOPOLOGY = {tp};\n\
        GRID_UNIT = 1.0;\n\
        TOPOLOGY_FILE = topologyFile;\n\
        NUMBER_OF_NODES = {tp};\n\
        TERRAIN_DIMENSIONS_X = 100.0;\n\
        TERRAIN_DIMENSIONS_Y = 100.0;\n".format(tp=topology, nodes=noNodes))


def createLinkGainFile():
    os.system('cd linklayer; java LinkLayerModel ../{fp}'.format(fp=filePath))

if __name__ == "__main__":
    createTopologyConfig(3, 3)
    createLinkGainFile()
