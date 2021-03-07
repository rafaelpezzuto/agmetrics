#!/usr/bin/env python3
import os
import sys


BASE_FOLDER = '/home/rafael/Temp/2017-08-acacia-aglattes-1.1/subgrafos/anos/cum/metrics/'

files = os.listdir(BASE_FOLDER)
metric_files = [f for f in files if f.startswith('metrics')]

idlattes2metrics = {}

for f in sorted(metric_files):
    year = f.split('.')[0].split('_')[-1]
    if int(year) > 1907 and int(year) < 2017:
        rows = [e.strip().split(',') for e in open(BASE_FOLDER + f)]
        header = rows.pop(0)
        for r in rows:
            node_id = r[0]
            if node_id not in idlattes2metrics:
                idlattes2metrics[node_id] = {year: r[1:]}
            else:
                idlattes2metrics[node_id][year] = r[1:]

file_results = open(BASE_FOLDER + 'ids_metrics_by_year.csv', 'w')
file_results.write(','.join(['node_id', 'year'] + header[1:]) + '\n')

for idlattes in sorted(idlattes2metrics):
    years2metrics = idlattes2metrics[idlattes]
    for y in sorted(years2metrics):
        file_results.write(','.join([idlattes, y] + years2metrics[y]))
        file_results.write('\n')