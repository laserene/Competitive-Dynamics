# Undirected connection will be converted to 2 directed connections
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import numpy as np
from tqdm import tqdm

INF = 10000


def import_network(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    node_dict = {}
    neighbors = {}
    edges = []

    node_id = 0
    for line in data[1:]:
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction = int(direction)
        weight = int(weight)

        if node_dict.get(from_node) is None:
            node_dict[from_node] = node_id
            node_id += 1

        if node_dict.get(to_node) is None:
            node_dict[to_node] = node_id
            node_id += 1

        from_id = node_dict[from_node]
        to_id = node_dict[to_node]

        if neighbors.get(from_id) is None:
            neighbors[from_id] = []

        if neighbors.get(to_id) is None:
            neighbors[to_id] = []

        neighbors[to_id].append((from_id, weight))
        if direction == 0:
            neighbors[from_id].append((to_id, weight))

        edges.append((from_id, to_id, direction, weight))

    return node_dict, neighbors, edges


def convert_id_to_genename(node_dict):
    gene_dict = {}
    for gene in node_dict:
        gene_dict[node_dict[gene]] = gene

    return gene_dict


def extract_weight_matrix(node_dict, edges):
    n = len(node_dict)
    weight_matrix = np.zeros((n, n))

    for from_id, to_id, direction, weight in edges:
        if weight_matrix[from_id][to_id] == 0:
            weight_matrix[from_id][to_id] = weight
        else:
            weight_matrix[from_id][to_id] = min(weight_matrix[from_id][to_id], weight)

        if direction == 0:
            if weight_matrix[to_id][from_id] == 0:
                weight_matrix[to_id][from_id] = weight
            else:
                weight_matrix[to_id][from_id] = min(weight_matrix[to_id][from_id], weight)

    return weight_matrix


def compete(weight_matrix, node_dict, neighbors, n_edges):
    states = {}

    n = len(node_dict)
    beta_id = n  # Since node_id starts from 0
    epsilon = 2 * (10 ** -7)
    max_iterations = n * n_edges

    # Get the agent with max out-degree
    out_deg = np.count_nonzero(weight_matrix, axis=1)
    current_max_deg = max(out_deg)
    max_deg_indices = np.where(out_deg == current_max_deg)[0]
    for alpha in tqdm(node_dict):
        state = np.zeros(n + 1)
        state[beta_id] = -1

        alpha_id = node_dict[alpha]
        if alpha_id == beta_id:
            continue

        state[alpha_id] = 1
        for agent in node_dict:
            agent_id = node_dict[agent]
            if agent_id == alpha_id or agent_id == beta_id:
                continue

            # Beta connects to agent
            neighbors[agent_id].append((beta_id, 1))
            if agent_id in max_deg_indices:
                current_max_deg = max(out_deg) + 1
            else:
                current_max_deg = max(out_deg)
            e = 1 / current_max_deg
            t = 0
            while True:
                convergence = 0
                for u in node_dict:
                    u_id = node_dict[u]
                    if u_id == alpha_id or u_id == beta_id:
                        continue

                    s = 0
                    for neighbor_id, weight in neighbors[u_id]:
                        if neighbor_id == beta_id:
                            s += 1 * (state[neighbor_id] - state[u_id])
                        else:
                            s += weight_matrix[neighbor_id][u_id] * (state[neighbor_id] - state[u_id])

                    old_u_state = state[u_id]
                    state[u_id] += e * s
                    convergence += abs(state[u_id] - old_u_state)

                t += 1
                if convergence <= epsilon or t >= max_iterations:
                    break

            neighbors[agent_id].remove((beta_id, 1))

        states[alpha_id] = state

    return states


def main():
    # node_dict, neighbors, edges = import_network("./data/test.txt")
    node_dict, neighbors, edges = import_network("./data/Acute myeloid leukemia.txt")
    weight_matrix = extract_weight_matrix(node_dict, edges)
    n_edges = len(edges)
    states = compete(weight_matrix, node_dict, neighbors, n_edges)
    pass

    # datasets = os.listdir("./data")
    # for dataset in tqdm(datasets):
    #     node_dict, neighbors = import_network("./data/" + dataset)
    #     extract_weight_matrix(node_dict, neighbors)

    # print(node_dict)


if __name__ == "__main__":
    main()
