import matplotlib.pyplot as plt
import networkx as nx


def visualize(network):
    plt.figure(figsize=(50, 50))
    pos = nx.spring_layout(network, seed=42)
    # node_colors = ['blue' if community_structure[n] == 1 else 'red' for n in network.nodes]
    nx.draw(network, pos, with_labels=True, node_color='blue', node_size=8000, font_size=10, font_weight='bold',
            arrows=True)
    plt.show()


def convert_id_to_genename(node_dict):
    gene_dict = {}
    for gene in node_dict:
        gene_dict[node_dict[gene]] = gene

    return gene_dict
