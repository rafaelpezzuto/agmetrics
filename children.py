from model.graph import Node, Edge, Graph

import config
import time

start = time.time()

file_nodes = open(config.PATHS.get('FILE_IN_NODES'))
file_edges = open(config.PATHS.get('FILE_IN_EDGES'))
file_ids_nodes = open(config.PATHS.get('FILE_IN_IDS_ISSI2019'))
file_children = open(config.PATHS.get('FILE_OUT_CHILDREN'), 'w')

print('[1] reading nodes')
head_nodes = file_nodes.readline()
ids_issi2019 = set([i.strip() for i in file_ids_nodes])
nodes = [n.strip().split(',') for n in file_nodes]

lattes2node = {}
code2lattes = {}
code2name = {}
for n in nodes:
    lattes2node[n[3]] = n
    code2lattes[n[0]] = n[3]
    code2name[n[0]] = n[1]
print('  .', len(nodes), 'nodes')

print('[2] reading edges')
head_edges = file_edges.readline()
edges = [e.strip().split(',') for e in file_edges]
print('  .', len(edges), 'edges')

print('[3] creating graph')
g = Graph()
for v in nodes:
    code = v[0]
    g.add_node(code)
for e in edges:
    source = e[0]
    target = e[1]
    g.add_edge(source, target)

print('[4] collecting children')
file_children.write('father_id,child_id,child_name\n')
children = []
for index, i in enumerate(g.nodes):
    father = g.nodes.get(i)
    father_id_lattes = code2lattes.get(father.code)
    if father_id_lattes in ids_issi2019:
        for child in father.children:
            child_id_lattes = code2lattes.get(child.code)
            child_name = code2name.get(child.code)
            line = ','.join([father_id_lattes, child_id_lattes, child_name])
            children.append(line)

children = sorted(sorted(children, key=lambda x:int(x.split(',')[1])),key=lambda x:int(x.split(',')[0]))

print('[5] writing children on disc')
for i in children:
    file_children.write(i)
    file_children.write('\n')
file_children.close()

end = time.time()
print('The algorithm was performed in %.3f seconds' %(end - start))
