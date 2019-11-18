import os


GDF_VERTEX_HEADER = ','.join(['nodedef> name', 'cidade_nascimento VARCHAR', 'data_ultima_atualizacao_curriculo VARCHAR', 'nacionalidade VARCHAR', 'nome VARCHAR', 'Label VARCHAR', 'pais_de_nacionalidade VARCHAR', 'pais_de_nascimento VARCHAR', 'primeira_area VARCHAR', 'primeira_especialidade VARCHAR', 'primeira_grande_area VARCHAR', 'primeira_sub_area VARCHAR', 'profi_bairro VARCHAR', 'profi_cep VARCHAR', 'profi_cidade VARCHAR', 'profi_instituicao VARCHAR', 'profi_logradouro VARCHAR', 'profi_orgao VARCHAR', 'profi_pais VARCHAR', 'profi_uf VARCHAR', 'sigla_pais_nacionalidade VARCHAR', 'uf_nascimento VARCHAR', 'is_seed BOOLEAN', 'is_ancestor BOOLEAN', 'is_descendant BOOLEAN', 'bANAIS INTEGER', 'bCATALOGO INTEGER', 'bCOLETANEA INTEGER', 'bENCICLOPEDIA INTEGER', 'bLIVRO INTEGER', 'bNAO_INFORMADO INTEGER', 'bOUTRA INTEGER', 'bPERIODICO INTEGER', 'bTEXTO_INTEGRAL INTEGER', 'bVERBETE INTEGER', 'cCAPITULO INTEGER', 'e INTEGER', 'eCOMPLETO INTEGER', 'eNAO_INFORMADO INTEGER', 'eRESUMO INTEGER', 'eRESUMO_EXPANDIDO INTEGER', 'j INTEGER', 'jCOMPLETO INTEGER', 'jNAO_INFORMADO INTEGER', 'jRESUMO INTEGER', 'bTOTAL INTEGER', 'cTOTAL INTEGER', 'eTOTAL INTEGER', 'jTOTAL INTEGER', 'TOTAL INTEGER', 'bMIN_YEAR INTEGER', 'cMIN_YEAR INTEGER', 'eMIN_YEAR INTEGER', 'jMIN_YEAR INTEGER', 'MIN_YEAR INTEGER', 'd+ INTEGER', 'd- INTEGER', 'fc+ INTEGER', 'fc- INTEGER', 'ft+ INTEGER', 'ft- INTEGER', 'c+ INTEGER', 'c- INTEGER', 'ge+ INTEGER', 'ge- INTEGER', 'r+ INTEGER', 'r- INTEGER', 'g INTEGER', 'dp INTEGER', 'dm INTEGER', 'fcp INTEGER', 'fcm INTEGER', 'ftp INTEGER', 'ftm INTEGER', 'cp INTEGER', 'cm INTEGER', 'gp INTEGER', 'gm INTEGER', 'rp INTEGER', 'rm INTEGER', 'gi INTEGER'])
GDF_EDGE_HEADER = ','.join(['edgedef> source, target, ano_conclusao VARCHAR', 'ano_inicio VARCHAR', 'area VARCHAR', 'codigo_nivel VARCHAR', 'curso VARCHAR', 'destino_nome VARCHAR', 'destino_nome_preprocessado VARCHAR', 'especialidade VARCHAR', 'extra VARCHAR', 'grande_area VARCHAR', 'instituicao VARCHAR', 'origem_nome VARCHAR', 'origem_nome_preprocessado VARCHAR', 'sub_area VARCHAR', 'tese VARCHAR', 'tipo_orientacao VARCHAR', 'Label VARCHAR', 'directed BOOLEAN'])
SUBGRAPHS_DIR = '/home/rafael/Temp/thesis/subgraphs/primeira_grande_area/'
subgraphs = [a.split('/')[-1].split('-')[0] for a in os.listdir(SUBGRAPHS_DIR) if a.endswith('-full_vertices.csv')]

for a in subgraphs:
    print('subgraph %s' % a)
    print('reading full vertices')
    vertices = [v.strip().split(',') for v in open(SUBGRAPHS_DIR + a + '-full_vertices.csv')]
    id2vertex = {}
    for v in vertices[1:]:
        id2vertex[v[2]] = [v[2]] + v[:2] + v[3:]

    print('reading edges')
    edges = [e.strip().split(',') for e in open(SUBGRAPHS_DIR + a + '-edges.csv')]
    ids2edges = {}
    for e in edges[1:]:
        target = e[5]
        source = e[12]
        ids2edges[','.join([source, target])] = [source, target] + e[:5] + e[6:12] + e[13:]

    print('writing gdf')
    file_gdf = open(SUBGRAPHS_DIR + a + '.gdf', 'w')

    file_gdf.write(GDF_VERTEX_HEADER + '\n')
    for v in sorted(id2vertex):
        file_gdf.write(','.join(id2vertex[v]) + '\n')

    file_gdf.write(GDF_EDGE_HEADER + '\n')
    for e in sorted(ids2edges):
        file_gdf.write(','.join(ids2edges[e] + ['true']) + '\n')

    file_gdf.close()
