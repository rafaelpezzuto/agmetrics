from model.graph import Edge, Graph, Node
from model.metrics import MetricsCalculator as mc
from model.patterns import PatternsCalculator as pc

import config
import time


start = time.time()

file_nodes = open(config.PATHS.get('FILE_IN_NODES'))
file_edges = open(config.PATHS.get('FILE_IN_EDGES'))
file_patterns = open(config.PATHS.get('FILE_OUT_PATTERNS'), 'w')

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

print('[4] calculating patterns')
file_patterns.write('id_random_graph,edges,in_degrees,out_degrees\n')
file_patterns.write('0' + ',' + str(sorted(g.edges)) + ',[')
file_patterns.write('-'.join([str(mc.in_degree(g, k)) for k in sorted(g.nodes)]))
file_patterns.write('],[')
file_patterns.write('-'.join([str(mc.out_degree(g, k)) for k in sorted(g.nodes)]))
file_patterns.write(']\n')
patterns = [pc.generate_null_model(g, 100) for i in range(100)]

print('[5] writing patterns on disc')
for index, i in enumerate(patterns):
	file_patterns.write(str(index+1) + ',' + str(sorted(i.edges)) + ',[')
	file_patterns.write('-'.join([str(mc.in_degree(i, k)) for k in sorted(i.nodes)]))
	file_patterns.write('],[')
	file_patterns.write('-'.join([str(mc.out_degree(i, k)) for k in sorted(i.nodes)]))
	file_patterns.write(']\n')
file_patterns.close()

end = time.time()
print('The calculation was performed in %.3f seconds' %(end - start))
