#!/bin/sh
for year in $(seq 1932 2016); do
    base='/home/rafael/Temp/2017-08-acacia-aglattes-1.1/subgrafos/anos/'
    file_node=$base'nodes_1932_'$year'.gdf'
    file_edge=$base'edges_1932_'$year'.gdf'
    file_out=$base'metrics_1932_'$year'.csv'
    if [ -f "$file_node" ]; then
        ./calculate_metrics.py $file_node $file_edge $file_out 
    else
        echo "$year does not exist"
    fi
done
