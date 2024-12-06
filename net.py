# Undirected connection will be converted to 2 directed connections

import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm

INF = 10000


def get_random_competitor(n_nodes):
    return random.randint(0, n_nodes - 1)


def get_node_edge(net):
    nodes = list(net.nodes())
    edges = list(net.edges())
    return nodes, edges


def import_network(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    count = 0
    net = nx.MultiDiGraph()
    for line in data:
        if count == 0:
            count += 1
            continue
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction = int(direction)
        weight = int(weight)

        net.add_edge(from_node, to_node, weight=weight)

        if direction == 0:
            net.add_edge(to_node, from_node, weight=weight)

    return net


def extract_adj_matrix(nodes, edges):
    n_nodes = len(nodes)
    neighbors = {}

    # Node dictionary
    node_dict = {}
    for i in range(n_nodes):
        node_dict[nodes[i]] = i

    # Adjacent directed matrix
    # Set dim to (n_nodes + 1, n_nodes + 1)
    # to easily handle the outside competitor later
    adj_matrix = np.zeros((n_nodes + 1, n_nodes + 1))

    # Update
    for edge in edges:
        from_node, to_node = edge
        from_node_idx = node_dict[from_node]
        to_node_idx = node_dict[to_node]
        adj_matrix[from_node_idx][to_node_idx] += 1

        if neighbors.get(from_node, 0) == 0:
            neighbors[from_node] = [to_node]
            continue

        if to_node not in neighbors[from_node]:
            neighbors[from_node].append(to_node)

    return adj_matrix, neighbors, node_dict


def compete(adj_matrix, neighbors, node_dict, alpha_id, n_edges):
    # Init outside competitor
    beta_id = len(node_dict)
    n_nodes = len(node_dict) + 1
    node_dict["Beta"] = beta_id
    neighbors[beta_id] = []

    # Init node state
    states = {}
    for i in range(n_nodes):
        states[i] = 0
    states[alpha_id] = 1
    states[beta_id] = -1

    n_steps = n_nodes * n_edges
    # Connect Beta to each normal agent
    for node in tqdm(node_dict.keys()):
        node_id = node_dict[node]
        if node_id == alpha_id or node_id == beta_id:
            continue

        if neighbors.get(node, 0) == 0:
            continue

        # Set of V edges
        neighbors[node].append("Beta")
        adj_matrix[beta_id][node_id] = 1
        deg_max = np.delete(adj_matrix.sum(-1) - adj_matrix[:, alpha_id], alpha_id, axis=0).max()
        epsilon = 1 / deg_max

        while True:
            converging = 0
            t = 0

            for u in node_dict.keys():
                u_id = node_dict[u]
                if u_id == alpha_id or u_id == beta_id:
                    continue

                # Node with no out-edge
                if neighbors.get(u, 0) == 0:
                    continue

                s = 0
                for v in neighbors[u]:
                    v_id = node_dict[v]
                    s = s + adj_matrix[u_id][v_id] * (states[v_id] - states[u_id])

                old_u_state = states[u_id]
                states[u_id] = old_u_state + epsilon * s
                converging = converging + abs(states[u_id] - old_u_state)

            if not (converging > epsilon and t < n_steps):
                break

            t += 1

    return states


def compute_distance_matrix(adj_matrix, node_dict):
    d = adj_matrix.copy()
    d[(d == 0) & (~np.eye(d.shape[0], dtype=bool))] = INF

    # Floyd-Warshall algorithm for distance matrix D calculation
    for k in tqdm(node_dict.keys()):
        for u in node_dict.keys():
            for v in node_dict.keys():
                from_node = node_dict[u]
                to_node = node_dict[v]
                mid_node = node_dict[k]

                if d[from_node][to_node] > d[from_node][mid_node] + d[mid_node][to_node]:
                    d[from_node][to_node] = d[from_node][mid_node] + d[mid_node][to_node]

    return d


def visualize(net1):
    plt.figure(figsize=(50, 50))
    nx.draw(net1, with_labels=True, node_color='lightblue', node_size=800, font_size=10, font_weight='bold',
            arrows=True)
    plt.show()


def main():
    path = "./data/4-Human cancer signaling - Input.txt"
    # path = "./data/test.txt"

    # Network generation
    net = import_network(path)
    nodes, edges = get_node_edge(net)
    adj_matrix, neighbors, node_dict = extract_adj_matrix(nodes, edges)

    # Outside competition
    n_nodes = len(nodes)
    n_edges = len(edges)
    alpha_id = get_random_competitor(n_nodes)
    print("===============COMPETING==============")
    states = compete(adj_matrix, neighbors, node_dict, alpha_id, n_edges)

    # print(states.values())

    for i in states.values():
        if i < 0:
            print("no")

    # distance_matrix = compute_distance_matrix(adj_matrix, node_dict)


if __name__ == "__main__":
    main()
