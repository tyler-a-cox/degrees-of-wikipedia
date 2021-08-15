import numpy as np
import pylab as plt
import networkx as nx
from copy import deepcopy


class Visualizer:
    """
    """

    def __init__(self, graph: dict):
        """
        """
        self.edges = self.dict_to_edges(graph)
        self.g = nx.Graph()
        self.g.add_edges_from(edges)

    def prune_graph(self, graph: dict, nodes: list):
        """
        """
        pruned = deepcopy(graph)
        for node in nodes:
            for value in graph[node]:
                if pruned.get(value) is None:
                    pruned[node].remove(value)

        return pruned

    def dict_to_edges(self, graph: dict):
        """
        """
        edges = []
        for key, values in pruned.items():
            edges += [(key, value) for value in values]

        edges = list(set(edges))
        return edges

    def plot_graph(self, with_labels: bool = False):
        """
        """
        nx.draw_networkx(g, with_labels=with_labels)
