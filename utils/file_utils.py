import csv
import os


NODE_CODE_COLUMN_HEADER = os.environ.get('NODE_CODE_COLUMN_HEADER', 'Id')
NODE_LABEL_COLUMN_HEADER = os.environ.get('NODE_CODE_COLUMN_HEADER', 'Label')
SOURCE_CODE_COLUMN_HEADER = os.environ.get('SOURCE_CODE_COLUMN_HEADER', 'Source')
TARGET_CODE_COLUMN_HEADER = os.environ.get('TARGET_CODE_COLUMN_HEADER', 'Target')
YEAR_COLUMN_HEADER = os.environ.get('YEAR_COLUMN_HEADER', 'Year')


def read_nodes(path_file_nodes, delimiter):
    nodes = {}

    with open(path_file_nodes) as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        for i in csv_reader:
            code = i.get(NODE_CODE_COLUMN_HEADER)
            label = i.get(NODE_LABEL_COLUMN_HEADER)

            if code not in nodes:
                nodes[code] = label
            else:
                print('Vértice duplicado %s' % code)

    return nodes


def read_edges(path_file_edges, delimiter):
    edges = []

    with open(path_file_edges) as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        for i in csv_reader:
            source = i.get(SOURCE_CODE_COLUMN_HEADER)
            target = i.get(TARGET_CODE_COLUMN_HEADER)
            year = i.get(YEAR_COLUMN_HEADER)
            edges.append((source, target, year))

    return edges
