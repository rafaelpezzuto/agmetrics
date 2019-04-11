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
		self.id = source_node.code + '->' + target_node.code
		self.source = source_node
		self.target = target_node
		self.other_attributes = other_attributes


	def __str__(self):
		return self.id


	def __repr__(self):
		return self.id


	def __eq__(self, other):
		if self.id == other.id:
			return True
		return False


	def __gt__(self, other):
		self_els = [int(s) for s in self.id.split('->')]
		other_els = [int(o) for o in other.id.split('->')]
		if self_els[0] > other_els[0]:
			return True
		if self_els[0] == other_els[0]:
			if self_els[1] > other_els[1]:
				return True		
		return False


	def __lt__(self, other):
		self_els = [int(s) for s in self.id.split('->')]
		other_els = [int(o) for o in other.id.split('->')]
		if self_els[0] < other_els[0]:
			return True
		if self_els[0] == other_els[0]:
			if self_els[1] < other_els[1]:
				return True		
		return False


	def __ge__(self, other):
		self_els = [int(s) for s in self.id.split('->')]
		other_els = [int(o) for o in other.id.split('->')]
		if self_els[0] >= other_els[0]:
			if self_els[1] >= other_els[1]:
				return True		
		return False


	def __le__(self, other):
		self_els = [int(s) for s in self.id.split('->')]
		other_els = [int(o) for o in other.id.split('->')]
		if self_els[0] <= other_els[0]:
			if self_els[1] <= other_els[1]:
				return True		
		return False


	def get_full_str(self, other_attributes_header):
		str_other_attributes = ','.join([self.other_attributes[k] for k in other_attributes_header])
		if len(other_attributes_header) > 0:
			return ','.join([self.source.code, self.target.code, str_other_attributes])
		else:
			return ','.join([self.source.code, self.target.code])


class Graph:

	def __init__(self):
		self.nodes = {}
		self.edges = []


	def add_node(self, code):
		self.nodes[code] = Node(code)


	def add_edge(self, source_code, target_code, other_attributes={}):
		source_node = self.nodes.get(source_code)
		target_node = self.nodes.get(target_code)

		if target_node not in source_node.children:
			source_node.children.append(target_node)

		if source_node not in target_node.parents:
			target_node.parents.append(source_node)

		new_edge = Edge(source_node, target_node, other_attributes)
		if new_edge not in self.edges:
			self.edges.append(new_edge)
			source_node.down_adjacent_list.append(new_edge)
			target_node.up_adjacent_list.append(new_edge)


	def remove_edge(self, edge):
		source_node = self.nodes.get(edge.source.code)
		target_node = self.nodes.get(edge.target.code)
		source_node.children.remove(target_node)
		target_node.parents.remove(source_node)

		self.edges.remove(edge)
