from copy import deepcopy
from model.graph import Edge, Graph, Node
from model.metrics import MetricsCalculator as mc
from random import randrange


class PatternsCalculator:

    @staticmethod
    def generate_null_model(g: Graph, iterations: int):
        r = deepcopy(g)
        for i in range(iterations):
            pos1 = 0
            pos2 = 0
            while (pos1 == pos2):
                pos1 = randrange(0, len(r.edges))
                pos2 = randrange(0, len(r.edges))
            e1 = r.edges[pos1]
            e2 = r.edges[pos2]

            if e1.source.code != e2.target.code and e2.source.code != e1.target.code:
                new_e1 = Edge(e1.source, e2.target)
                new_e2 = Edge(e2.source, e1.target)
                if new_e1 not in r.edges and new_e2 not in r.edges:
                    r.remove_edge(e1)
                    r.remove_edge(e2)
                    r.add_edge(new_e1.source.code, new_e1.target.code)
                    r.add_edge(new_e2.source.code, new_e2.target.code)
        return r
