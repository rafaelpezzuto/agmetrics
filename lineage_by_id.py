#!/usr/bin/python3
from model.graph import Edge, Graph, Node
from model.metrics import MetricsCalculator as mc

import config
import time


start = time.time()

lineage_node_id = config.LINEAGE.get('LINEAGE_NODE_ID')
only_descendants = config.LINEAGE.get('ONLY_DESCENDANTS')
file_nodes = open(config.PATHS.get('FILE_IN_NODES'))
file_edges = open(config.PATHS.get('FILE_IN_EDGES'))
file_lineage = open(config.PATHS.get('FILE_OUT_LINEAGE'), 'w')

print('[1] reading nodes')
head_nodes = file_nodes.readline().strip().split(',')
nodes = []
for line in file_nodes:
	node = {}
	elements = line.strip().split(',')
	for i, element in enumerate(elements):
		node[head_nodes[i]] = element
	nodes.append(node)

print('[2] reading edges')
head_edges = file_edges.readline().strip().split(',')
edges = []
for line in file_edges:
	edge = {}
	elements = line.strip().split(',')
	for i, element in enumerate(elements):
		edge[head_edges[i]] = element
	edges.append(edge)

print('[3] creating graph')
g = Graph()
for v in nodes:
	code = v[head_nodes[0]]
	keys = [i for i in v.keys() if i != head_nodes[0]]
	g.add_node(code)
	for k in keys:
		g.nodes[code].other_attributes[k] = v[k]

for e in edges:
	source = e[head_edges[0]]
	target = e[head_edges[1]]
	keys = [i for i in e.keys() if i != head_edges[0] and i != head_edges[1]]
	other_attributes = {}
	for k in keys:
		other_attributes[k] = e[k]
	g.add_edge(source, target, other_attributes)

print('[4] calculating lineage of node %s' %lineage_node_id)
subg_nodes = []
subg_edges = []

node = g.nodes[lineage_node_id]
node.lineage = 'Origin'
node.lineage_distance = 0
subg_nodes.append(node)

if not only_descendants:
	node_ancestors = mc.inverse_generations(g, lineage_node_id, return_length=False)
	for k, gen in node_ancestors.items():
		for v in gen:
			d = k + 1
			v.lineage = 'Ancestor'
			v.lineage_distance = -d
			subg_nodes.append(v)

node_descendants = mc.generations(g, lineage_node_id, return_length=False)
for k, gen in node_descendants.items():
	for v in gen:
		d = k + 1
		v.lineage = 'Descendant'
		v.lineage_distance = d
		subg_nodes.append(v)

for e in g.edges:
	if e.source in subg_nodes and e.target in subg_nodes:
		subg_edges.append(e)

print('[5] calculating metrics')
subg_codes = [v.code for v in subg_nodes]
for v in g.nodes:
	if v in subg_codes:
		g.nodes[v].metrics['d+'] = mc.descendants(g, v)
		g.nodes[v].metrics['d-'] = mc.inverse_descendants(g, v)
		g.nodes[v].metrics['f+'] = mc.fecundity(g, v)
		g.nodes[v].metrics['f-'] = mc.inverse_fecundity(g, v)
		g.nodes[v].metrics['ft+'] = mc.fertility(g, v)
		g.nodes[v].metrics['ft-'] = mc.inverse_fertility(g, v)
		g.nodes[v].metrics['c+'] = mc.cousins(g, v)
		g.nodes[v].metrics['c-'] = mc.inverse_cousins(g, v)
		g.nodes[v].metrics['ge+'] = mc.generations(g, v)
		g.nodes[v].metrics['ge-'] = mc.inverse_generations(g, v)
		g.nodes[v].metrics['r+'] = mc.relationships(g, v)
		g.nodes[v].metrics['r-'] = mc.inverse_relationships(g, v)
		g.nodes[v].metrics['gi'] = mc.genealogical_index(g, v)

subg_nodes = sorted(subg_nodes, key=lambda x:int(x.code))
subg_edges = sorted(subg_edges, key=lambda x:(int(x.source.code), int(x.target.code)))

print('[6] writing subgraph on disk')

metrics_header = ['d+', 'd-', 'f+', 'f-', 'ft+', 'ft-', 'c+', 'c-', 'ge+', 'ge-', 'r+', 'r-', 'gi']
str_metrics_header = ','.join([m + ' INTEGER' for m in ['d+', 'd-', 'f+', 'f-', 'ft+', 'ft-', 'c+', 'c-', 'ge+', 'ge-', 'r+', 'r-', 'gi']])
str_node_header = ','.join(head_nodes) + ',lineage VARCHAR,lineage_distance INTEGER,' + str_metrics_header
file_lineage.write(str_node_header + '\n')
for v in subg_nodes:
	file_lineage.write(v.get_full_str(metrics_header, head_nodes[1:]))
	file_lineage.write('\n')

file_lineage.write(','.join(head_edges))
file_lineage.write('\n')
for e in subg_edges:
	file_lineage.write(e.get_full_str(head_edges[2:]))
	file_lineage.write('\n')

file_lineage.close()

end = time.time()
print('The algorithm was executed in %.3f seconds' %(end - start))
