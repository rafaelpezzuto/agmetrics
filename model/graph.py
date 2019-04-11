class Node:

	def __init__(self, code):
		self.code = code
		self.parents = []
		self.children = []
		self.down_adjacent_list = []
		self.up_adjacent_list = []
		self.metrics = {}
		self.lineage = ''
		self.lineage_distance = None
		self.other_attributes = {}


	def __str__(self):
		return 'node_' + str(self.code)


	def __repr__(self):
		return 'node_' + str(self.code)
	

	def get_full_str(self, metrics_header, other_attributes_header):
		str_metrics = ','.join([str(self.metrics[k]) for k in metrics_header])
		str_other_attributes = ','.join([self.other_attributes[k] for k in other_attributes_header])
		if len(other_attributes_header) > 0:
			return ','.join([self.code, str_other_attributes, self.lineage, str(self.lineage_distance), str_metrics])
		else:
			return ','.join([self.code, self.lineage, str(self.lineage_distance), str_metrics])


class Edge:
	
	def __init__(self, source_node, target_node, other_attributes={}):
		self.source = source_node
		self.target = target_node
		self.other_attributes = other_attributes


	def __str__(self):
		return '->'.join([self.source.code, self.target.code])


	def __repr__(self):
		return '->'.join([self.source.code, self.target.code])


	def get_full_str(self, other_attributes_header):
		str_other_attributes = ','.join([self.other_attributes[k] for k in other_attributes_header])
		if len(other_attributes_header) > 0:
			return ','.join([self.source.code, self.target.code, str_other_attributes])
		else:
			return ','.join([self.source.code, self.target.code])


class Graph:

	def __init__(self):
		self.nodes = {}
		self.edges = set()


	def add_node(self, code):
		self.nodes[code] = Node(code)


	def add_edge(self, source_code, target_code, other_attributes={}):
		source_node = self.nodes.get(source_code)
		target_node = self.nodes.get(target_code)
		self.nodes[source_code].children.append(self.nodes[target_code])
		self.nodes[target_code].parents.append(self.nodes[source_code])
		self.edges.add(Edge(source_node, target_node, other_attributes))
		source_node.down_adjacent_list.append(Edge(source_node, target_node, other_attributes))
		target_node.up_adjacent_list.append(Edge(source_node, target_node, other_attributes))
