import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigs


def compute_modularity_matrix(G):
    """Compute the modularity matrix B for an undirected graph G."""
    A = nx.adjacency_matrix(G).todense()
    degrees = np.array([d for _, d in G.degree()])
    m = G.number_of_edges()

    # Compute B = A - (k_i * k_j) / (2m)
    B = A - np.outer(degrees, degrees) / (2 * m)
    return np.array(B)


def spectral_partitioning(G):
    """Use spectral method to split a graph into two communities."""
    B = compute_modularity_matrix(G)

    # Compute the leading eigenvector
    eigenvalues, eigenvectors = eigs(B, k=1, which='LR')  # 'LR' -> largest real part
    leading_eigenvector = np.real(eigenvectors[:, 0])  # Extract real part

    # Split nodes based on sign of eigenvector components
    nodes = list(G.nodes())
    community_1 = [nodes[i] for i in range(len(nodes)) if leading_eigenvector[i] > 0]
    community_2 = [nodes[i] for i in range(len(nodes)) if leading_eigenvector[i] <= 0]

    return community_1, community_2


def visualize_communities(G, comm1, comm2):
    """Visualize the graph with two detected communities."""
    pos = nx.spring_layout(G, seed=42)  # Layout for positioning nodes

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, node_color='gray', edge_color='lightgray', node_size=300, alpha=0.5)

    # Draw communities in different colors
    nx.draw_networkx_nodes(G, pos, nodelist=comm1, node_color='blue', label='Community 1')
    nx.draw_networkx_nodes(G, pos, nodelist=comm2, node_color='red', label='Community 2')

    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    plt.title("Spectral Community Detection (2 Communities)")
    plt.legend()
    plt.show()
