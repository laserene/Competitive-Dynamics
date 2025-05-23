import json
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


def compute_distance_matrix(network, verbose=True):
    if verbose:
        print('IN PROGRESS: Computing distance matrix...')
    adjacent_matrix = nx.adjacency_matrix(network)
    distance_matrix = adjacent_matrix.copy().todense().astype(np.uint16)
    distance_matrix[(distance_matrix == 0) & (np.eye(distance_matrix.shape[0]) == 0)] = INF

    # Floyd-Warshall algorithm for distance matrix D calculation
    for mid_node in tqdm(network.nodes):
        mid_node_id = network.nodes[mid_node]['id']
        distance_matrix = np.minimum(distance_matrix,
                                     distance_matrix[:, mid_node_id][:, np.newaxis] + distance_matrix[mid_node_id, :])

    return distance_matrix


def load_distance_matrix_from_file(filepath, verbose=True):
    if verbose:
        print("IN PROGRESS: Loading distance matrix...")
    distance_matrix = np.loadtxt(filepath, delimiter=",", dtype=np.uint16)
    return distance_matrix


def load_states_from_file(filepath, verbose=True):
    """
        Load pre-computed states.
    """
    if verbose:
        print("IN PROGRESS: Loading state...")
    with open(filepath, 'r') as f:
        state = json.load(f)
    return state


def compete(alpha, network, node_set, max_deg):
    # Hyperparameters
    epsilon = 2 * 1e-7
    max_iterations = len(node_set) * len(network.edges)
    mul_coeff = 1 / max_deg

    state = retrieve_initial_state(network)
    support = {}

    adjacent_matrix = nx.adjacency_matrix(network)
    # distance_matrix = adjacent_matrix.copy().todense().astype(np.uint16)

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
                    if v != beta:
                        s += adjacent_matrix[network.nodes[u]['id'], network.nodes[v]['id']] * (state[v] - state[u])
                    else:
                        s += state[v] - state[u]

                old_state = state[u]
                state[u] += mul_coeff * s
                converging += np.abs(old_state - state[u])

            t += 1
            if not (converging > epsilon and t < max_iterations):
                break

        support[y] = state[y]
        network.remove_edge(beta, y)
        network.remove_node(beta)
        state = retrieve_initial_state(network)

    support[alpha] = 1

    return support


def outside_competition(network, driver_set, verbose=True):
    if verbose:
        print("IN PROGRESS: Competition in progress...")
    node_set = list(network.nodes)
    max_deg = get_max_deg(network)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        agent_supports = list(tqdm(executor.map(
            partial(compete, network=network, node_set=node_set, max_deg=max_deg),
            driver_set)))

    return agent_supports
