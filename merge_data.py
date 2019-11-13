import os

GLOBAL_VERTICES = '/home/rafael/Temp/acacia-v2-2019-10-05/oficial_data/data_vertices.csv'
BIBLIOMETRICS = '/home/rafael/Temp/acacia-v2-2019-10-05/oficial_data/data_bibliometrics.csv'
SUBGRAPHS_DIR = '/home/rafael/Temp/primeira_grande_area/'

print('reading global vertices')
global_vertices = [m.strip().split(',') for m in open(GLOBAL_VERTICES)]
id2global_vertex = {}
for i in global_vertices[1:]:
    id2global_vertex[i[0]] = i[-14:-1]

print('reading global bibliometrics')
bibliometrics = [b.strip().split('\t') for b in open(BIBLIOMETRICS)]
id2bibliometrics = {}
for i in bibliometrics:
    id2bibliometrics[i[0]] = i[1:]

subgraphs = [a.split('/')[-1].split('-')[0] for a in os.listdir(SUBGRAPHS_DIR) if a.endswith('-vertices.csv')]
for a in subgraphs:
    print('subgraph %s' % a)
    print('reading local vertices')
    local_vertices = [v.strip().split(',') for v in open(SUBGRAPHS_DIR + a + '-vertices.csv')]
    id2local_vertex = {}
    for i in local_vertices[1:]:
        id2local_vertex[i[2]] = i

    print('reading local metrics')
    local_metrics = [lm.strip().split(',') for lm in open(SUBGRAPHS_DIR + a + '-metrics.csv')]
    id2local_metrics = {}
    for i in local_metrics[1:]:
        id2local_metrics[i[0]] = i[1:]

    header = ','.join(local_vertices[0] + bibliometrics[0][1:] + local_metrics[0][1:] + global_vertices[0][-14:-1])

    num_els_local_metrics = len(local_metrics[0][1:])
    num_els_bibliometrics = len(bibliometrics[0][1:])

    print('writing full vertices')
    full_vertices = open(SUBGRAPHS_DIR + a + '-full_vertices.csv', 'w')
    full_vertices.write(header + '\n')
    for i in sorted(id2local_vertex):
        vstr = id2local_vertex[i]

        if i not in id2bibliometrics:
            vstr.extend(['0' for x in range(num_els_bibliometrics)])
        else:
            vstr.extend(id2bibliometrics[i])

        if i not in id2local_metrics:
            vstr.extend(['0' for x in range(num_els_local_metrics)])
        else:
            vstr.extend(id2local_metrics[i])

        vstr.extend(id2global_vertex[i])

        full_vertices.write(','.join(vstr) + '\n')
    full_vertices.close()
