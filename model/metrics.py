#!/usr/bin/python3
from model.graph import Edge, Graph, Node


class MetricsCalculator:

    @staticmethod
    def in_degree(g: Graph, node_code):
        return len(g.nodes[node_code].parents)


    @staticmethod
    def out_degree(g: Graph, node_code):
        return len(g.nodes[node_code].children)


    @staticmethod
    def fecundity(g: Graph, node_code, get_set=False):
        if not get_set:
            return len(g.nodes[node_code].children)
        else:
            return g.nodes[node_code].children


    @staticmethod
    def inverse_fecundity(g: Graph, node_code, get_set=False):
        if not get_set:
            return len(g.nodes[node_code].parents)
        else:
            return g.nodes[node_code].parents


    @staticmethod
    def descendants(g: Graph, node_code):
        stack = [c for c in g.nodes[node_code].children]
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


    @staticmethod
    def inverse_descendants(g: Graph, node_code):
        stack = [p for p in g.nodes[node_code].parents]
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


    @staticmethod
    def fertility(g: Graph, node_code):
        fertile_direct_descendants = [c for c in g.nodes[node_code].children if len(c.children) > 0]
        return len(fertile_direct_descendants)


    @staticmethod
    def inverse_fertility(g: Graph, node_code):
        fertile_inverse_descendants = [p for p in g.nodes[node_code].parents if len(p.parents) > 0]
        return len(fertile_inverse_descendants)


    @staticmethod
    def relationships(g: Graph, node_code):
        stack = [g.nodes[node_code]]
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


    @staticmethod
    def inverse_relationships(g: Graph, node_code):
        stack = [g.nodes[node_code]]
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


    @staticmethod
    def grandchildren(g: Graph, node_code):
        children = g.nodes[node_code].children
        grandchildren = []
        for c in children:
            for gc in c.children:
                if gc not in grandchildren:
                    grandchildren.append(gc)
        return grandchildren


    @staticmethod
    def generations(g: Graph, node_code, return_length=True):
        height = 0
        stack = [(g.nodes[node_code], height)]
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


    @staticmethod
    def inverse_generations(g: Graph, node_code, return_length=True):
        height = 0
        stack = [(g.nodes[node_code], height)]
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


    @staticmethod
    def cousins(g: Graph, node_code):
        v_inverse_fecundity = g.nodes[node_code].parents
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
        return len(cousins)


    @staticmethod
    def inverse_cousins(g: Graph, node_code):
        v_fecundity = g.nodes[node_code].children
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


    @staticmethod
    def genealogical_index(g: Graph, node_code):
        max_gi = len(g.nodes[node_code].children)
        same_gi = []
        while max_gi > 0:
            for c in g.nodes[node_code].children:
                if len(c.children) >= max_gi:
                    same_gi.append(c)
            if len(same_gi) >= max_gi:
                return max_gi
            else:
                max_gi -= 1
                same_gi.clear()
        return max_gi
