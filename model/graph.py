class Node:
	def __init__(self, code, label=''):
		self.code = code
		self.label = label
		self.parents = []
		self.children = []
		self.down_adjacent_list = []
		self.up_adjacent_list = []
		self.metrics = {}
		self.lineage = ''
		self.lineage_distance = None
		self.other_attributes = {}

	def __hash__(self):
		return hash(self.code)

	def __eq__(self, other):
		if self.__hash__() == other.__hash__():
			return True
		return False


class Edge:
	def __init__(self, source_node, target_node, year):
		self.source = source_node
		self.target = target_node
		self.year = year

	def __hash__(self):
		return hash('->'.join([self.source.code, self.target.code, self.year]))

	def __eq__(self, other):
		if self.__hash__() == other.__hash__():
			return True
		return False


class Graph:

	def __init__(self):
		self.nodes = {}
		self.edges = set()

	def add_node(self, code, label=''):
		self.nodes[code] = Node(code, label)

	def add_edge(self, source_code, target_code, year):
		source_node = self.nodes.get(source_code)
		target_node = self.nodes.get(target_code)

		new_edge = Edge(source_node, target_node, year)
		if new_edge not in self.edges:
			self.edges.add(new_edge)

			self.nodes[source_code].children.append(self.nodes[target_code])
			self.nodes[target_code].parents.append(self.nodes[source_code])

			source_node.down_adjacent_list.append(Edge(source_node, target_node, year))
			target_node.up_adjacent_list.append(Edge(source_node, target_node, year))

	def in_degree(self, node_code):
		return len(self.nodes[node_code].parents)

	def out_degree(self, node_code):
		return len(self.nodes[node_code].children)

	def fecundity(self, node_code, get_set=False):
		if not get_set:
			return self.out_degree(node_code)
		else:
			return self.nodes[node_code].children

	def inverse_fecundity(self, node_code, get_set=False):
		if not get_set:
			return self.in_degree(node_code)
		else:
			return self.nodes[node_code].parents

	def descendants(self, node_code):
		stack = [c for c in self.nodes[node_code].children]
		descendants = set()
		visited = []
		while len(stack) > 0:
			node = stack.pop()
			descendants.add(node)
			visited.append(node)
			for c in node.children:
				if c not in visited:
					stack.append(c)
		return len(descendants)

	def inverse_descendants(self, node_code):
		stack = [p for p in self.nodes[node_code].parents]
		inverse_descendants = set()
		visited = []
		while len(stack) > 0:
			node = stack.pop()
			inverse_descendants.add(node)
			visited.append(node)
			for p in node.parents:
				if p not in visited:
					stack.append(p)
		return len(inverse_descendants)

	def fertility(self, node_code):
		fertile_direct_descendants = [c for c in self.nodes[node_code].children if len(c.children) > 0]
		return len(fertile_direct_descendants)

	def inverse_fertility(self, node_code):
		fertile_inverse_descendants = [p for p in self.nodes[node_code].parents if len(p.parents) > 0]
		return len(fertile_inverse_descendants)

	def relationships(self, node_code):
		stack = [self.nodes[node_code]]
		visited = []
		relationships = []
		while len(stack) > 0:
			node = stack.pop()
			visited.append(node)
			for r in node.down_adjacent_list:
				if r not in relationships:
					relationships.append(r)
			for c in node.children:
				if c not in stack and c not in visited:
					stack.append(c)
		return len(relationships)

	def inverse_relationships(self, node_code):
		stack = [self.nodes[node_code]]
		visited = []
		relationships = []
		while len(stack) > 0:
			node = stack.pop()
			visited.append(node)
			for r in node.up_adjacent_list:
				if r not in relationships:
					relationships.append(r)
			for c in node.parents:
				if c not in stack and c not in visited:
					stack.append(c)
		return len(relationships)

	def grandchildren(self, node_code):
		children = self.nodes[node_code].children
		grandchildren = []
		for c in children:
			for gc in c.children:
				if gc not in grandchildren:
					grandchildren.append(gc)
		return grandchildren

	def generations(self, node_code, return_length=True):
		height = 0
		stack = [(self.nodes[node_code], height)]
		visited = []
		generations = {}
		while len(stack) > 0:
			node, height = stack.pop()
			visited.append(node)
			for c in node.children:
				if c not in visited:
					stack.append((c, height + 1))
					if height not in generations:
						generations[height] = [c]
					else:
						generations[height].append(c)
		if return_length:
			return len(generations)
		else:
			return generations

	def inverse_generations(self, node_code, return_length=True):
		height = 0
		stack = [(self.nodes[node_code], height)]
		visited = []
		generations = {}
		while len(stack) > 0:
			node, height = stack.pop()
			visited.append(node)
			for c in node.parents:
				if c not in visited:
					stack.append((c, height + 1))
					if height not in generations:
						generations[height] = [c]
					else:
						generations[height].append(c)
		if return_length:
			return len(generations)
		else:
			return generations

	def cousins(self, node_code, return_length=True):
		v_inverse_fecundity = self.nodes[node_code].parents
		z_inverse_fecundity = []
		for i in v_inverse_fecundity:
			z_inverse_fecundity.extend(i.parents)
		x_fecundity = []
		for j in z_inverse_fecundity:
			x_fecundity.extend(j.children)
		cousins = set()
		for w in x_fecundity:
			for u in w.children:
				if u.code is not node_code:
					cousins.add(u)
		if return_length:
			return len(cousins)
		else:
			return cousins

	def inverse_cousins(self, node_code):
		v_fecundity = self.nodes[node_code].children
		z_fecundity = []
		for i in v_fecundity:
			z_fecundity.extend(i.children)
		x_inverse_fecundity = []
		for j in z_fecundity:
			x_inverse_fecundity.extend(j.parents)
		cousins = set()
		for w in x_inverse_fecundity:
			for u in w.parents:
				if u.code is not node_code:
					cousins.add(u)
		return len(cousins)

	def genealogical_index(self, node_code):
		max_gi = len(self.nodes[node_code].children)
		same_gi = []
		while max_gi > 0:
			for c in self.nodes[node_code].children:
				if len(c.children) >= max_gi:
					same_gi.append(c)
			if len(same_gi) >= max_gi:
				return max_gi
			else:
				max_gi -= 1
				same_gi.clear()
		return max_gi

	def siblings(self, node_code, return_length=True):
		v_inverse_fecundity = self.nodes[node_code].parents
		siblings = set()
		for j in v_inverse_fecundity:
			for u in j.children:
				if u.code is not node_code:
					siblings.add(u)
		if return_length:
			return len(siblings)
		else:
			return siblings
