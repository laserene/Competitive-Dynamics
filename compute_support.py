import json

import numpy as np
from tqdm import tqdm


def compute_influence_matrix(network, state, distance_matrix):
    n_nodes = len(network.nodes)
    influence_matrix = np.zeros((n_nodes, n_nodes))
    node_set = list(network.nodes)

    print('Computing influence matrix...')
    for u in node_set:
        for v in node_set:
            u_id = network.nodes[u]['id']
            v_id = network.nodes[v]['id']
            if distance_matrix[u_id][v_id] != 0:
                influence_matrix[u_id][v_id] = state[v] / (distance_matrix[u_id][v_id] ** 2)

    return influence_matrix


def compute_total_support(network, states, distance_matrix):
    def sign(value):
        if value > 0:
            return 1
        elif value == 0:
            return 0
        else:
            return -1

    print('Computing support...')

    node_set = list(network.nodes)

    supports = {}
    for i in tqdm(range(len(states))):
        alpha = node_set[i]
        state = states[i]
        influence_matrix = compute_influence_matrix(network, state, distance_matrix)

        alpha_id = network.nodes[alpha]['id']
        support = 0
        for node in node_set:
            if node == alpha:
                continue

            node_id = network.nodes[node]['id']
            support += sign(influence_matrix[alpha_id][node_id] - state[node])

        supports[alpha] = support

    total_support_path = './support/support.json'
    with open(total_support_path, 'w') as f:
        json.dump(supports, f)

    return supports
