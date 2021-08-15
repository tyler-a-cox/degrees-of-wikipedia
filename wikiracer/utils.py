import pickle
from .query import WIKI_URL


def save_graph(dictionary: dict, name: str = "graph.pkl"):
    """
    """
    with open(name, "wb") as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)


def load_graph(name: str = "graph.pkl"):
    """
    """
    with open(name, "rb") as f:
        return pickle.load(f)


def print_path(path: list):
    """
    """
    for i, node in enumerate(path):
        url = WIKI_URL + node.replace(" ", "_")
        print("{}. {}: {}".format(i + 1, node, url))
