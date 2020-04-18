#!/bin/sh
for year in $(seq 1900 2019); do
    base='/home/rafael/Temp/thesis/subgraphs/ano_acumulado/'
    file_node=$base'nodes_1900_'$year'.csv'
    file_edge=$base'edges_1900_'$year'.csv'
    file_out=$base'metrics_1900_'$year'.csv'
    if [ -f "$file_node" ]; then
        ./calculate_metrics.py $file_node $file_edge $file_out 
    else
        echo "$year does not exist"
    fi
done
