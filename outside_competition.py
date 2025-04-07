import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import networkx as nx
import numpy as np
from tqdm import tqdm

INF = 10000


def retrieve_initial_state(network):
    state = {}
    for node in network.nodes:
        state[node] = network.nodes[node]['score']

    return state


def get_max_deg(network):
    max_deg = 0
    for _, degree in network.degree:
        max_deg = max(max_deg, degree)
    return max_deg


def compute_distance_matrix(dataset, network):
    print('Computing distance matrix...')
    adjacent_matrix = nx.adjacency_matrix(network)
    distance_matrix = adjacent_matrix.copy().todense().astype(np.uint16)
    distance_matrix[(distance_matrix == 0) & (np.eye(distance_matrix.shape[0]) == 0)] = INF

    # Floyd-Warshall algorithm for distance matrix D calculation
    for mid_node in tqdm(network.nodes):
        mid_node_id = network.nodes[mid_node]['id']
        distance_matrix = np.minimum(distance_matrix,
                                     distance_matrix[:, mid_node_id][:, np.newaxis] + distance_matrix[mid_node_id, :])

    os.makedirs("distance_matrix", exist_ok=True)
    np.savetxt(f"distance_matrix/{dataset}_distance_matrix.csv", distance_matrix, delimiter=",", fmt='%d')

    return distance_matrix


def load_distance_matrix_from_file(filepath):
    print("Loading distance matrix...")
    distance_matrix = np.loadtxt(filepath, delimiter=",", dtype=np.uint16)
    return distance_matrix


def compete(alpha, network, co_expression, node_set, max_deg):
    # Hyperparameters
    epsilon = 2 * 1e-7
    max_iterations = len(node_set) * len(network.edges)
    mul_coeff = 1 / max_deg

    state = retrieve_initial_state(network)

    for y in node_set:
        # Initially, set of nodes doesn't contain beta
        if y == alpha:
            continue

        # Outside competitors initialization
        beta = 'BETA'

        state[alpha] = 1
        state[beta] = -1

        # Append (Beta, node) edge. Edge can only be appended once node score are retrieved
        network.add_edge(beta, y)

        t = 0
        while True:
            converging = 0
            for u in node_set:
                # Initially, set of nodes doesn't contain beta
                if u == alpha:
                    continue

                s = 0
                for v in network.neighbors(u):
                    co_expression_score = min(co_expression.get(f'{u}, {v}', 1), co_expression.get(f'{v}, {u}', 1))

                    if v != beta:
                        s += (1 + co_expression_score) * (state[v] - state[u])
                    else:
                        s += state[v] - state[u]

                old_state = state[u]
                state[u] += mul_coeff * s
                converging += np.abs(old_state - state[u])

            t += 1
            if converging > epsilon and t < max_iterations:
                break

        network.remove_edge(beta, y)
        network.remove_node(beta)

    return state


def outside_competition(network, co_expression, start, end):
    print("Competition in progress...")
    node_set = list(network.nodes)
    max_deg = get_max_deg(network)
    candidates = node_set[start:end]

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        states = list(tqdm(executor.map(
            partial(compete, network=network, co_expression=co_expression,
                    node_set=node_set, max_deg=max_deg),
            candidates)))

    return states
