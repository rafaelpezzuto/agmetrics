import os

DIR = '/home/rafael/Temp/primeira_grande_area/'

arq_vertices = sorted([DIR + f for f in os.listdir(DIR) if f.endswith('vertices.csv')])
arq_edges = sorted([DIR + f for f in os.listdir(DIR) if f.endswith('edges.csv')])

f2subgraph = {}
home = '/'.join(arq_vertices[0].split('-')[0].split('/')[:-1]) + '/'
for a in arq_vertices:
    els = a.split('/')
    subgraph_name = els[-1].split('-')[0]
    f2subgraph[subgraph_name] = [a]

for a in arq_edges:
    els = a.split('/')
    subgraph_name = els[-1].split('-')[0]
    f2subgraph[subgraph_name].append(a)

for a in f2subgraph:
    print(a.upper())
    fm = home + a + '-metrics.csv'
    os.system(' '.join(['python3 calculate_metrics.py', '"' + f2subgraph[a][0] + '"', '"' + f2subgraph[a][1] + '"', '"' + fm + '"']))
