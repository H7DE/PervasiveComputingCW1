#!/bin/bash
expr_name='expr_topo_uniform_'
for i in `seq 2 9 `;
do
    name=$expr_name$i
    numNodes=$(($i*$i))
    python test.py $numNodes uniform $name
done 
