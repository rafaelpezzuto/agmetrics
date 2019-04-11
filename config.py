LINEAGE = {
    'LINEAGE_NODE_ID': '1',
    'ONLY_DESCENDANTS': True
}

PATHS = {
    'FILE_IN_NODES': 'example/nodes.gdf',
    'FILE_IN_EDGES': 'example/edges.gdf',
    'FILE_OUT_PATTERNS': 'example/patterns.csv',
    'FILE_OUT_METRICS': 'example/metrics.csv',
    'FILE_OUT_GRANDFATHER_VS_GRANDCHILDREN_METRICS': 'example/gfgc_metrics.csv',
    'FILE_OUT_LINEAGE': 'example/lineage_' + LINEAGE.get('LINEAGE_NODE_ID', '0') + '.gdf'
}

