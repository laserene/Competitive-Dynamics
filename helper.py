import random

import matplotlib.pyplot as plt
import networkx as nx


def get_random_competitor(n_nodes):
    return random.randint(0, n_nodes - 1)


def visualize(net):
    plt.figure(figsize=(50, 50))
    nx.draw(net, with_labels=True, node_color='lightblue', node_size=800, font_size=10, font_weight='bold',
            arrows=True)
    plt.show()
