import sys

sys.path.append('../aglattes/')

from models.acacia import LattesPesquisadorAnalysis, LattesRelacaoAcacia
from models.graph import Graph
from scripts.file_utils import FileUtils


def mount_graph(vertices: list, edges: list):
    g = Graph()
    for v in vertices:
        code = v.id_lattes
        g.add_node(code)

    for e in edges:
        source = e.origem_id_lattes
        target = e.destino_id_lattes
        g.add_edge(source, target)
    return g


def mount_id2vertex(vertices: list):
    id2vertex = {}
    for v in vertices:
        id2vertex[v.id_lattes] = v
    return id2vertex


if __name__ == '__main__':
    FILE_IN_VERTICES = sys.argv[1]
    FILE_IN_EDGES = sys.argv[2]
    DIR = '/'.join(FILE_IN_VERTICES.split('/')[:-1]) + '/'

    print('reading vertices')
    vertices = FileUtils.get_data_from_csv(FILE_IN_VERTICES, class_name=LattesPesquisadorAnalysis)

    print('reading edges')
    edges = FileUtils.get_data_from_csv(FILE_IN_EDGES, class_name=LattesRelacaoAcacia)

    print('mounting id2vertex')
    id2vertex = mount_id2vertex(vertices)

    print('mounting graph')
    g = mount_graph(vertices, edges)

    del vertices
    del edges

    gf2gc = {}
    for v in g.vertices:
        vi = g.vertices[v]
        vi_fcp = g.fecundity(vi.code)
        if vi_fcp > 0:
            for ci in vi.children:
                ci_fcp = g.fecundity(ci.code)
                if ci_fcp > 0:
                    if vi.code not in gf2gc:
                        gf2gc[vi.code] = set()
                    gf2gc[vi.code] = gf2gc[vi.code].union(set([cii.code for cii in ci.children]))

    f2c = {}
    for v in g.vertices:
        vi = g.vertices[v]
        vi_fcp = g.fecundity(vi.code)
        if vi_fcp > 0:
            if vi.code not in f2c:
                f2c[vi.code] = set()
            f2c[vi.code] = f2c[vi.code].union(set([vii.code for vii in vi.children]))

    measures = ['dm', 'dp', 'rm', 'rp', 'cm', 'cp', 'fcm', 'fcp', 'ftm', 'ftp', 'gi', 'gm', 'gp', 'academic_age', 'mentoring_age', 'books', 'chapters',
                'event_papers', 'journal_papers', 'total']

    print('father -> children')
    wf2c = open('f2c-raw.csv', 'w')
    wf2c.write('\t'.join(['father-code'] + ['father-' + m for m in measures] + ['child-code'] + ['child-' + m for m in measures]) + '\n')
    for f in f2c:
        for c in f2c[f]:
            wf2c.write('\t'.join([f] + [str(id2vertex[f].__dict__[m]) for m in measures] + [c] + [str(id2vertex[c].__dict__[m]) for m in measures]) + '\n')
    wf2c.close()

    wf2c = open('f2c-mean.csv', 'w')
    wf2c.write('\t'.join(['father-code'] + ['father-' + m for m in measures] + ['child-mean-' + m for m in measures]) + '\n')
    for f in f2c:
        fm = [str(id2vertex[f].__dict__[m]) for m in measures]
        cm = [[] for x in measures]
        for c in f2c[f]:
            for i, m in enumerate(measures):
                v = id2vertex[c].__dict__[m]
                if isinstance(v, str):
                    if v.isdigit():
                        v = int(v)
                    else:
                        v = -1
                cm[i].append(v)
        cmmean = []
        for cmi in cm:
            nonnull = [x for x in cmi if x >= 0]
            n = len(nonnull)
            if n > 0:
                cmmean.append(float(sum(nonnull)/n))
            else:
                cmmean.append('nan')
        wf2c.write('\t'.join([f] + fm + [str(y) for y in cmmean]) + '\n')

    print('grandfather -> grandchildren')
    wgf2gc = open('gf2gc-raw.csv', 'w')
    wgf2gc.write('\t'.join(['grandfather-code'] + ['grandfather-' + m for m in measures] + ['grandchild-code'] + ['grandchild-' + m for m in measures]) + '\n')
    for gf in gf2gc:
        for gc in gf2gc[gf]:
            wgf2gc.write('\t'.join([gf] + [str(id2vertex[gf].__dict__[m]) for m in measures] + [gc] + [str(id2vertex[gc].__dict__[m]) for m in measures]) + '\n')
    wgf2gc.close()

    wgf2gc = open('gf2gc-mean.csv', 'w')
    wgf2gc.write('\t'.join(['grandfather-code'] + ['grandfather-' + m for m in measures] + ['grandchild-mean-' + m for m in measures]) + '\n')
    for gf in gf2gc:
        gfm = [str(id2vertex[gf].__dict__[m]) for m in measures]
        gcm = [[] for x in measures]
        for gc in gf2gc[gf]:
            for i, m in enumerate(measures):
                v = id2vertex[gc].__dict__[m]
                if isinstance(v, str):
                    if v.isdigit():
                        v = int(v)
                    else:
                        v = -1
                gcm[i].append(v)
        gcmmean = []
        for gcmi in gcm:
            nonnull = [x for x in gcmi if x >= 0]
            n = len(nonnull)
            if n > 0:
                gcmmean.append(float(sum(nonnull)/n))
            else:
                gcmmean.append('nan')
        wgf2gc.write('\t'.join([gf] + gfm + [str(y) for y in gcmmean]) + '\n')
    wgf2gc.close()
