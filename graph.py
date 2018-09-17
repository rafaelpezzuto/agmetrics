class Node:
	def __init__(self, code):
		self.code = code
		self.parents = []
		self.children = []
		self.down_adjacent_list = []
		self.up_adjacent_list = []

	def __str__(self):
		return str(self.code)

	def __repr__(self):
		return str(self.code)

class Edge:
	def __init__(self, source_node, target_node):
		self.source = source_node
		self.target = target_node

	def __str__(self):
		return '->'.join([self.source.code, self.target.code])

	def __repr__(self):
		return '->'.join([self.source.code, self.target.code])

class Graph:
	def __init__(self):
		self.vertices = {}
		self.edges = set()

	def add_node(self, code):
		self.vertices[code] = Node(code)

	def add_edge(self, source_code, target_code):
		source_node = self.vertices.get(source_code)
		target_node = self.vertices.get(target_code)
		self.vertices[source_code].children.append(self.vertices[target_code])
		self.vertices[target_code].parents.append(self.vertices[source_code])
		self.edges.add(Edge(source_node, target_node))
		source_node.down_adjacent_list.append(Edge(source_node, target_node))
		target_node.up_adjacent_list.append(Edge(source_node, target_node))

	def in_degree(self, node_code):
		return len(self.vertices[node_code].parents)

	def out_degree(self, node_code):
		return len(self.vertices[node_code].children)

	def fecundity(self, node_code):
		return self.out_degree(node_code)

	def inverse_fecundity(self, node_code):
		return self.in_degree(node_code)

	def descendants(self, node_code):
		stack = [c for c in self.vertices[node_code].children]
		descendants = set()
		visited = []
		while len(stack) > 0:
			vertex = stack.pop()
			descendants.add(vertex)
			visited.append(vertex)
			for c in vertex.children:
				if c not in visited:
					stack.append(c)
		return len(descendants)

	def inverse_descendants(self, node_code):
		stack = [p for p in self.vertices[node_code].parents]
		inverse_descendants = set()
		visited = []
		while len(stack) > 0:
			vertex = stack.pop()
			inverse_descendants.add(vertex)
			visited.append(vertex)
			for p in vertex.parents:
				if p not in visited:
					stack.append(p)
		return len(inverse_descendants)

	def fertility(self, node_code):
		fertile_direct_descendants = [c for c in self.vertices[node_code].children if len(c.children) > 0]
		return len(fertile_direct_descendants)

	def inverse_fertility(self, node_code):
		fertile_inverse_descendants = [p for p in self.vertices[node_code].parents if len(p.parents) > 0]
		return len(fertile_inverse_descendants)

	def relationships(self, node_code):
		stack = [self.vertices[node_code]]
		visited = []
		relationships = []
		while len(stack) > 0:
			vertex = stack.pop()
			visited.append(vertex)
			for r in vertex.down_adjacent_list:
				if r not in relationships:
					relationships.append(r)
			for c in vertex.children:
				if c not in stack and c not in visited:
					stack.append(c)
		return len(relationships)

	def inverse_relationships(self, node_code):
		stack = [self.vertices[node_code]]
		visited = []
		relationships = []
		while len(stack) > 0:
			vertex = stack.pop()
			visited.append(vertex)
			for r in vertex.up_adjacent_list:
				if r not in relationships:
					relationships.append(r)
			for c in vertex.parents:
				if c not in stack and c not in visited:
					stack.append(c)
		return len(relationships)

	def generations(self, node_code):
		height = 0
		stack = [(self.vertices[node_code], height)]
		visited = []
		generations = {}
		while len(stack) > 0:
			vertex, height = stack.pop()
			visited.append(vertex)
			for c in vertex.children:
				if c not in visited:
					stack.append((c, height + 1))
					if height not in generations:
						generations[height] = [c]
					else:
						generations[height].append(c)
		return len(generations)

	def inverse_generations(self, node_code):
		height = 0
		stack = [(self.vertices[node_code], height)]
		visited = []
		generations = {}
		while len(stack) > 0:
			vertex, height = stack.pop()
			visited.append(vertex)
			for c in vertex.parents:
				if c not in visited:
					stack.append((c, height + 1))
					if height not in generations:
						generations[height] = [c]
					else:
						generations[height].append(c)
		return len(generations)

	def cousins(self, node_code):
		return 9

	def inverse_cousins(self, node_code):
		return 9

	def genealogical_index(self, node_code):
		max_gi = len(self.vertices[node_code].children)
		same_gi = []
		while max_gi > 0:
			for c in self.vertices[node_code].children:
				if len(c.children) >= max_gi:
					same_gi.append(c)
			if len(same_gi) >= max_gi:
				return max_gi
			else:
				max_gi -= 1
				same_gi.clear()
		return max_gi
