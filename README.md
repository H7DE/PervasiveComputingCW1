# PervasiveComputingCW1
##Installation
run the installation script by running 
$> chmod +x install.py
$> ./install.py

This will compile the nesc program and the LinkLayerModel.java

##Usage
###To run a single simulation 
python test.py {noNodes} {topologyType} {experimentName}
i.e python test.py 5 random random_top_exp

This will run the nesc program, with noNode - 1 sensor node and 1 base station node.
The results of the experiments will be saved to wsn.db an (sqllite database file).
Topology types are random, uniform, grid
See report for more details.

##To run multiple simulations
run the installation script by running 
$> chmod +x random_top_test_script.sh
$> ./random_top_test_script.sh


##Dependencies
Python 2.5+
May require the installation of (matplot lib)[http://matplotlib.org/users/installing.html]
jre 1.5+
