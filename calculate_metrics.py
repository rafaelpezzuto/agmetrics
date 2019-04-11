#!/usr/bin/python3
from model.graph import Edge, Graph, Node
from model.metrics import MetricsCalculator as mc

import config
import time


start = time.time()

file_nodes = open(config.PATHS.get('FILE_IN_NODES'))
file_edges = open(config.PATHS.get('FILE_IN_EDGES'))
file_metrics = open(config.PATHS.get('FILE_OUT_METRICS'), 'w')

print('[1] reading nodes')
head_nodes = file_nodes.readline()
nodes = [v.strip().split(',') for v in file_nodes]

print('[2] reading edges')
head_edges = file_edges.readline()
edges = [e.strip().split(',') for e in file_edges]

print('[3] creating graph')
g = Graph()
for v in nodes:
	code = v[0]
	g.add_node(code)
for e in edges:
	source = e[0]
	target = e[1]
	g.add_edge(source, target)

print('[4] calculating metrics')
file_metrics.write('node_id,d+,d-,fc+,fc-,ft+,ft-,c+,c-,ge+,ge-,r+,r-,g\n')
metrics = []
for index, i in enumerate(g.nodes):
	print('%s of %s\r' %(index + 1, len(nodes)), end='')
	metrics.append(','.join([str(k) for k in [i, mc.descendants(g, i), mc.inverse_descendants(g, i), mc.fecundity(g, i), mc.inverse_fecundity(g, i), mc.fertility(g, i), mc.inverse_fertility(g, i), mc.cousins(g, i), mc.inverse_cousins(g, i), mc.generations(g, i), mc.inverse_generations(g, i), mc.relationships(g, i), mc.inverse_relationships(g, i), mc.genealogical_index(g, i)]]))

metrics = sorted(metrics, key=lambda x:int(x.split(',')[0]))

print('[5] writing metrics on disc')
for i in metrics:
	file_metrics.write(i)
	file_metrics.write('\n')
file_metrics.close()

end = time.time()
print('The calculation was performed in %.3f seconds' %(end - start))
