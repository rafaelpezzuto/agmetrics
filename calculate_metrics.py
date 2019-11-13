#!/usr/bin/env python3
import sys
import time

sys.path.append('../aglattes')

from model.graph import Graph
from models.acacia import LattesPesquisadorAcacia, LattesRelacaoAcacia
from scripts.file_utils import FileUtils


if __name__ == '__main__':
	start = time.time()

	file_nodes = sys.argv[1]
	file_edges = sys.argv[2]
	file_metrics = open(sys.argv[3], 'w')

	print('[1] reading nodes')
	nodes = FileUtils.get_data_from_csv(file_nodes, class_name=LattesPesquisadorAcacia)

	print('[2] reading edges')
	edges = FileUtils.get_data_from_csv(file_edges, class_name=LattesRelacaoAcacia)

	print('[3] creating graph')
	g = Graph()
	for v in nodes:
		code = v.id_lattes
		g.add_node(code)
	for e in edges:
		source = e.origem_id_lattes
		target = e.destino_id_lattes
		g.add_edge(source, target)

	print('[4] calculating metrics')
	file_metrics.write('node_id,d+,d-,fc+,fc-,ft+,ft-,c+,c-,ge+,ge-,r+,r-,g\n')
	metrics = []
	for index, i in enumerate(g.nodes):
		print('%s of %s\r' %(index + 1, len(nodes)), end='')
		metrics.append(','.join([str(k) for k in [i, g.descendants(i), g.inverse_descendants(i), g.fecundity(i), g.inverse_fecundity(i), g.fertility(i), g.inverse_fertility(i), g.cousins(i), g.inverse_cousins(i), g.generations(i), g.inverse_generations(i), g.relationships(i), g.inverse_relationships(i), g.genealogical_index(i)]]))

	metrics = sorted(metrics, key=lambda x:int(x.split(',')[0]))

	print('[5] writing metrics on disc')
	for i in metrics:
		file_metrics.write(i)
		file_metrics.write('\n')
	file_metrics.close()

	end = time.time()
	print('The calculation was performed in %.3f seconds' % (end - start))
