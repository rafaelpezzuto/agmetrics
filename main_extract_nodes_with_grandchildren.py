import sys

from graph import *
import time

start = time.time()

file_vertices = open(sys.argv[1])
file_edges = open(sys.argv[2])
file_metrics = open(sys.argv[3], 'w')

print('[1] reading vertices')
head_vertices = file_vertices.readline()
vertices = [v.strip().split(',') for v in file_vertices]

print('[2] reading edges')
head_edges = file_edges.readline()
edges = [e.strip().split(',') for e in file_edges]

print('[3] creating graph')
g = Graph()
for v in vertices:
	code = v[0]
	g.add_node(code)
for e in edges:
	source = e[0]
	target = e[1]
	g.add_edge(source, target)

print('[4] extract nodes with grandchildren')
file_metrics.write('node_code;dd_adv;dd_gc;di_adv;di_gc;fcd_adv;fcd_gc;fci_adv;fci_gc;gi_adv;gi_gc\n')
metrics = []
for index, i in enumerate(g.vertices):
	print('%s of %s\r' %(index + 1, len(vertices)), end='')
	netos = g.grandchildren(i)
	if netos is not None and len(netos) > 0:
		netos_metrics = {'d+':[], 'd-':[], 'fc+':[], 'fc-':[], 'gi':[]}
		for n in netos:
			netos_metrics['d+'].append(g.descendants(n.code))
			netos_metrics['d-'].append(g.inverse_descendants(n.code))
			netos_metrics['fc+'].append(g.fecundity(n.code))
			netos_metrics['fc-'].append(g.inverse_fecundity(n.code))
			netos_metrics['gi'].append(g.genealogical_index(n.code))

		netos_metrics['d+'] = sum(netos_metrics['d+']) / len(netos)
		netos_metrics['d-'] = sum(netos_metrics['d-']) / len(netos)
		netos_metrics['fc+'] = sum(netos_metrics['fc+']) / len(netos)
		netos_metrics['fc-'] = sum(netos_metrics['fc-']) / len(netos)
		netos_metrics['gi'] = sum(netos_metrics['gi']) / len(netos)

		metrics.append(';'.join([str(k) for k in [i, g.descendants(i), netos_metrics['d+'], g.inverse_descendants(i), netos_metrics['d-'], g.fecundity(i), netos_metrics['fc+'], g.inverse_fecundity(i), netos_metrics['fc-'], g.genealogical_index(i), netos_metrics['gi']]]))

metrics = sorted(metrics, key=lambda x:int(x.split(';')[0]))

print('[5] writing metrics on disc')
for i in metrics:
	file_metrics.write(i)
	file_metrics.write('\n')
file_metrics.close()

end = time.time()
print('The calculation was performed in %.3f seconds' %(end - start))
