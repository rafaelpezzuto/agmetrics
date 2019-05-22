LINEAGE = {
    'LINEAGE_NODE_ID': '535503',
    'ONLY_DESCENDANTS': True
}

PATHS = {
    'FILE_IN_NODES': '/mnt/dados/Rafael/issi-2019/base/grafo/vertices.gdf',
    'FILE_IN_EDGES': '/mnt/dados/Rafael/issi-2019/base/grafo/arestas.gdf',
    'FILE_IN_IDS_ISSI2019': '/mnt/dados/Rafael/issi-2019/base/grafo/ids-table-2.csv',
    'FILE_OUT_METRICS': '/mnt/dados/Rafael/issi-2019/base/metricas.csv',
    'FILE_OUT_CHILDREN': '/mnt/dados/Rafael/issi-2019/base/filhos.csv',
    'FILE_OUT_GRANDFATHER_VS_GRANDCHILDREN_METRICS': '/mnt/dados/Rafael/issi-2019/base/metricas_gf_vs_gc.csv',
    'FILE_OUT_LINEAGE': '/mnt/dados/Rafael/issi-2019/base/lineage_' + LINEAGE.get('LINEAGE_NODE_ID', '0') + '.gdf'
}

