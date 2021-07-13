import argparse
import csv
import graph


METRICS = [
	('descendants', 'd+'),
	('inverse_descendants', 'd-'),
	('fecundity', 'fc+'),
	('inverse_fecundity', 'fc-'),
	('fertility', 'ft+'),
	('inverse_fertility', 'ft-'),
	('cousins', 'c+'),
	('inverse_cousins', 'c-'),
	('generations', 'g+'),
	('inverse_generations', 'g-'),
	('relationships', 'r+'),
	('inverse_relationships', 'r-'),
	('genealogical_index', 'gi')
]


def read_params():
	parser = argparse.ArgumentParser()
	parser.add_argument('-e',
						'--edges',
						dest='path_edges',
						type=str,
						required=True,
						help='Edges file')
	return parser.parse_args()


def create_graph_from_edges(path_edges, delimiter=','):
	g = graph.Graph()

	with open(path_edges) as pe:
		csv_reader = csv.DictReader(pe, delimiter=delimiter)
		for row in csv_reader:
			s = row.get('source')
			t = row.get('target')

			g.add_node(s)
			g.add_node(t)
			g.add_edge(s, t)

	return g


def get_metrics(g):
	results = {}
	for node_code in g.nodes:
		results[node_code] = {}
		for m in METRICS:
			m_name, m_acronym = m
			m_value = getattr(graph.Graph, m_name)(g, node_code)
			results[node_code].update({m_acronym: m_value})
	return results


def tabfy_metrics(ms):
	print(','.join(['node'] + [
		hi[1] for hi in sorted(METRICS)
	]))
	for node_code in sorted(ms, key=lambda x:int(x)):
		node_metrics = ms[node_code]

		line = ','.join([node_code] + [
			str(node_metrics[v[1]]) for v in sorted(METRICS)
		])

		print(line)


def main():
	args = read_params()

	try:
		g1 = create_graph_from_edges(args.path_edges)
		g1_metrics = get_metrics(g1)
		tabfy_metrics(g1_metrics)
	except FileNotFoundError:
		exit(1)


if __name__ == '__main__':
	main()
