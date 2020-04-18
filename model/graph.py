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

	def __hash__(self):
		return hash(self.code)


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

	def ego(self, node_code, max_h=1, return_length=True):
		ego = set()
		parents = self.nodes[node_code].parents
		children = self.nodes[node_code].children
		ego = ego.union(set([p.code for p in parents])).union(set(c.code for c in children))

		counter = 1
		ego_c = {counter: ego}

		up = set()
		down = set()
		while counter < max_h:
			tmp_parents = set()
			tmp_children = set()

			for p in parents:
				for pp in p.parents:
					if pp.code != node_code:
						up.add(pp.code)
						tmp_parents.add(self.nodes[pp.code])
				for pc in p.children:
					if pc.code != node_code:
						up.add(pc.code)
						tmp_parents.add(self.nodes[pc.code])

			for c in children:
				for cc in c.children:
					if cc.code != node_code:
						down.add(cc.code)
						tmp_children.add(self.nodes[cc.code])
				for cp in c.parents:
					if cp.code != node_code:
						down.add(cp.code)
						tmp_children.add(self.nodes[cp.code])

			counter += 1

			parents = tmp_parents
			children = tmp_children

			ego_c[counter] = ego_c[counter-1].union(ego.union(up).union(down))

		# ego = ego.union(up).union(down)

		if return_length:
			return [len(ego_c[i]) for i in range(1, counter + 1)]
		else:
			return [ego_c[i] for i in range(1, counter + 1)]