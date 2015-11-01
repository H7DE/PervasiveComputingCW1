#!/bin/bash
expr_name='expr_topo_rand_'
for i in `seq 2 40 `;
do
    name=$expr_name$i
    python test.py $i random $name
done 
