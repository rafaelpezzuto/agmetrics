import sys

from graph import *
import time

start = time.time()

file_vertices = open(sys.argv[1])
file_edges = open(sys.argv[2])
node_id = sys.argv[3]

print('[1] reading vertices')
head_vertices = file_vertices.readline().strip().split(',')
vertices = []
for line in file_vertices:
	vertex = {}
	elements = line.strip().split(',')
	for i, element in enumerate(elements):
		vertex[head_vertices[i]] = element
	vertices.append(vertex)

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
for v in vertices:
	code = v[head_vertices[0]]
	keys = [i for i in v.keys() if i != head_vertices[0]]
	g.add_node(code)
	for k in keys:
		g.vertices[code].other_attributes[k] = v[k]

for e in edges:
	source = e[head_edges[0]]
	target = e[head_edges[1]]
	keys = [i for i in e.keys() if i != head_edges[0] and i != head_edges[1]]
	other_attributes = {}
	for k in keys:
		other_attributes[k] = e[k]
	g.add_edge(source, target, other_attributes)

print('[4] calculating lineage of vertex %s' %node_id)
subg_vertices = []
subg_edges = []

vertex = g.vertices[node_id]
vertex.lineage = 'Origin'
vertex.lineage_distance = 0
subg_vertices.append(vertex)

vertex_ancestors = g.inverse_generations(node_id, return_length=False)
for k, gen in vertex_ancestors.items():
	for v in gen:
		d = k + 1
		v.lineage = 'Ancestor'
		v.lineage_distance = -d
		subg_vertices.append(v)

vertex_descendants = g.generations(node_id, return_length=False)
for k, gen in vertex_descendants.items():
	for v in gen:
		d = k + 1
		v.lineage = 'Descendant'
		v.lineage_distance = d
		subg_vertices.append(v)

for e in g.edges:
	if e.source in subg_vertices and e.target in subg_vertices:
		subg_edges.append(e)

print('[5] calculating metrics')
subg_codes = [v.code for v in subg_vertices]
for v in g.vertices:
	if v in subg_codes:
		g.vertices[v].metrics['d+'] = g.descendants(v)
		g.vertices[v].metrics['d-'] = g.inverse_descendants(v)
		g.vertices[v].metrics['f+'] = g.fecundity(v)
		g.vertices[v].metrics['f-'] = g.inverse_fecundity(v)
		g.vertices[v].metrics['ft+'] = g.fertility(v)
		g.vertices[v].metrics['ft-'] = g.inverse_fertility(v)
		g.vertices[v].metrics['c+'] = g.cousins(v)
		g.vertices[v].metrics['c-'] = g.inverse_cousins(v)
		g.vertices[v].metrics['ge+'] = g.generations(v)
		g.vertices[v].metrics['ge-'] = g.inverse_generations(v)
		g.vertices[v].metrics['r+'] = g.relationships(v)
		g.vertices[v].metrics['r-'] = g.inverse_relationships(v)
		g.vertices[v].metrics['gi'] = g.genealogical_index(v)

subg_vertices = sorted(subg_vertices, key=lambda x:int(x.code))
subg_edges = sorted(subg_edges, key=lambda x:(int(x.source.code), int(x.target.code)))

print('[6] writing subgraph on disk')
out_file = open('lineage_%s.gdf' % node_id, 'w')

metrics_header = ['d+', 'd-', 'f+', 'f-', 'ft+', 'ft-', 'c+', 'c-', 'ge+', 'ge-', 'r+', 'r-', 'gi']
str_metrics_header = ','.join([m + ' INTEGER' for m in ['d+', 'd-', 'f+', 'f-', 'ft+', 'ft-', 'c+', 'c-', 'ge+', 'ge-', 'r+', 'r-', 'gi']])
str_vertex_header = ','.join(head_vertices) + ',lineage VARCHAR,lineage_distance INTEGER,' + str_metrics_header
out_file.write(str_vertex_header + '\n')
for v in subg_vertices:
	out_file.write(v.get_full_str(metrics_header, head_vertices[1:]))
	out_file.write('\n')

out_file.write(','.join(head_edges))
out_file.write('\n')
for e in subg_edges:
	out_file.write(e.get_full_str(head_edges[2:]))
	out_file.write('\n')

out_file.close()

end = time.time()
print('The algorithm was executed in %.3f seconds' %(end - start))
