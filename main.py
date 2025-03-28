import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigs

from network import import_network_from_file, is_undirected_graph
from modularity import *
from helper import visualize


# Example: Zachary’s Karate Club graph
G = import_network_from_file("./data/4-Human PPI network - Input.txt")
comm1, comm2 = spectral_partitioning(G)

# Visualize
# visualize_communities(G, comm1, comm2)
visualize(G)
