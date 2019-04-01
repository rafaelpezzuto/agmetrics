LINEAGE = {
    'LINEAGE_NODE_ID': '535503',
    'ONLY_DESCENDANTS': True
}

PATHS = {
    # 'FILE_IN_NODES': 'example/nodes.gdf',
    # 'FILE_IN_EDGES': 'example/edges.gdf',
    'FILE_IN_NODES': '/mnt/dados/massive/dataset-pa-04-2018/vertices.csv',
    'FILE_IN_EDGES': '/mnt/dados/massive/dataset-pa-04-2018/arestas.csv',
    'FILE_OUT_METRICS': 'example/metrics_pa.csv',
    'FILE_OUT_GRANDFATHER_VS_GRANDCHILDREN_METRICS': 'example/gfgc_metrics.csv',
    'FILE_OUT_LINEAGE': 'example/lineage_' + LINEAGE.get('LINEAGE_NODE_ID', '0') + '.gdf'
}

