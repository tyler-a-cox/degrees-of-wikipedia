import pickle


def save_graph(dictionary, name="graph.pkl"):
    """
    """
    with open(name, "wb") as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)


def load_graph(name="graph.pkl"):
    """
    """
    with open(name, "rb") as f:
        return pickle.load(f)
