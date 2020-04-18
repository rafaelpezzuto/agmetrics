from model.graph import Edge, Graph, Node
from scripts.file_utils import FileUtils
from models.acacia import LattesPesquisadorAcacia, LattesRelacaoAcacia

import sys
import time


NODE_ATTRS = ['nome', 'primeira_grande_area', 'primeira_area', 'profi_instituicao', 'profi_orgao', 'profi_pais', 'profi_uf', 'profi_cidade', 'profi_bairro', 'profi_logradouro', 'profi_cep', 'pais_de_nascimento', 'uf_nascimento', 'cidade_nascimento', 'nacionalidade', 'pais_de_nacionalidade', 'sigla_pais_nacionalidade', 'data_ultima_atualizacao_curriculo', 'dp', 'dm', 'fcp', 'fcm', 'ftp', 'ftm', 'cp', 'cm', 'gp', 'gm', 'rp', 'rm', 'gi', 'nome_preprocessado']
EDGE_ATTRS = ['origem_nome', 'destino_nome', 'titulacao', 'sensu', 'tipo_orientacao', 'ano_inicio', 'ano_conclusao', 'curso', 'instituicao', 'tese', 'grande_area', 'area', 'titulacoes', 'directed']

start = time.time()

lineage_node_id = sys.argv[1]
file_nodes = sys.argv[2]
file_edges = sys.argv[3]

print('[1] reading nodes and edges')
nodes = FileUtils.get_data_from_csv('/home/rafael/Temp/acacia-v2-2019-10-05/tmp/vertices_final.csv', class_name=LattesPesquisadorAcacia)
edges = FileUtils.get_data_from_csv('/home/rafael/Temp/acacia-v2-2019-10-05/tmp/arestas_final.csv', class_name=LattesRelacaoAcacia)

print('[3] creating graph')
g = Graph()
for v in nodes:
	code = v.id_lattes
	g.add_node(code)
	for k in NODE_ATTRS:
		g.nodes[code].other_attributes[k] = v[k]

for e in edges:
	source = e.origem_id_lattes
	target = e.destino_id_lattes
	other_attributes = {}
	for k in EDGE_ATTRS:
		other_attributes[k] = e[k]
	g.add_edge(source, target, other_attributes)

print('[4] calculating lineage of node %s' % lineage_node_id)
subg_nodes = []
subg_edges = []

node = g.nodes[lineage_node_id]
node.lineage = 'Origin'
node.lineage_distance = 0
subg_nodes.append(node)

node_descendants = g.generations(lineage_node_id, return_length=False)
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
		g.nodes[v].metrics['d+'] = g.descendants(v)
		g.nodes[v].metrics['d-'] = g.inverse_descendants(v)
		g.nodes[v].metrics['f+'] = g.fecundity(v)
		g.nodes[v].metrics['f-'] = g.inverse_fecundity(v)
		g.nodes[v].metrics['ft+'] = g.fertility(v)
		g.nodes[v].metrics['ft-'] = g.inverse_fertility(v)
		g.nodes[v].metrics['c+'] = g.cousins(v)
		g.nodes[v].metrics['c-'] = g.inverse_cousins(v)
		g.nodes[v].metrics['ge+'] = g.generations(v)
		g.nodes[v].metrics['ge-'] = g.inverse_generations(v)
		g.nodes[v].metrics['r+'] = g.relationships(v)
		g.nodes[v].metrics['r-'] = g.inverse_relationships(v)
		g.nodes[v].metrics['gi'] = g.genealogical_index(v)

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
