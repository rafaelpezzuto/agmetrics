import argparse
import os

from model.graph import Graph
from utils.file_utils import read_edges, read_nodes

DELIMITER = os.environ.get('DELIMITER', '\t')


def read_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        dest='file_nodes',
        help='Arquivo em que cada linha deve conter o código do vértice e seu '
             'respectivo nome.'
    )
    parser.add_argument(
        '-e',
        dest='file_edges',
        required=True,
        help='Arquivo em que cada linha deve conter o código do vértice origem e o código '
             'do vértice de destino.'
    )
    parser.add_argument(
        '-i',
        dest='id',
        default=''
    )
    params = parser.parse_args()

    if params.file_nodes:
        nodes = read_nodes(params.file_nodes, delimiter=DELIMITER)
    else:
        nodes = {}

    edges = read_edges(params.file_edges, delimiter=DELIMITER)

    return nodes, edges, params.id


def calculate(nodes, edges, filename):
    g = Graph()
    for s, t, y in edges:
        if s not in g.nodes:
            g.add_node(s, nodes.get(s, ''))

        if t not in g.nodes:
            g.add_node(t, nodes.get(t, ''))

    for s, t, y in edges:
        if y.isdigit():
            g.add_edge(s, t, y)

    with open(filename, 'w') as output:
        metrics_names = ['cousins',
                         'inverse_cousins',
                         'descendants',
                         'inverse_descendants',
                         'fecundity',
                         'inverse_fecundity',
                         'fertility',
                         'inverse_fertility',
                         'genealogical_index',
                         'generations',
                         'inverse_generations',
                         'relationships',
                         'inverse_relationships',
                         'siblings']
        output.write(','.join(['code', 'label'] + metrics_names) + '\n')

        for code in g.nodes:
            n_metrics = []
            for mn in metrics_names:
                n_metrics.append(g.__getattribute__(mn)(code))

            output.write(','.join([code, g.nodes[code].label] + [str(m) for m in n_metrics]) + '\n')


if __name__ == '__main__':
    print('Reading data')
    nodes, edges, id = read_data()

    print('Calculating metrics')
    calculate(nodes, edges, 'metrics_' + id + '.csv')
