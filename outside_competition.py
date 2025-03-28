import os

import numpy as np

INF = 10000


def compute_adj_matrix(network):
    pass


def compute_distance_matrix(dataset, weight_matrix, node_dict):
    d = weight_matrix.copy()
    d[(d == 0) & (~np.eye(d.shape[0], dtype=bool))] = INF

    # Floyd-Warshall algorithm for distance matrix D calculation
    for k in node_dict.keys():
        for u in node_dict.keys():
            for v in node_dict.keys():
                from_node = node_dict[u]
                to_node = node_dict[v]
                mid_node = node_dict[k]

                candidate = d[from_node][mid_node] + d[mid_node][to_node]
                if d[from_node][to_node] > candidate:
                    d[from_node][to_node] = candidate

    os.makedirs("distance_matrix", exist_ok=True)
    np.savetxt(f"distance_matrix/{dataset}_distance_matrix.csv", d, delimiter=",", fmt='%d')

    return d


def compete(alpha, weight_matrix, node_dict, neighbors, n_edges):
    n = len(node_dict)
    beta_id = n  # Since node_id starts from 0
    alpha_id = node_dict[alpha]

    epsilon = 2 * (10 ** -7)
    max_iterations = n * n_edges

    # Get the agent with max out-degree
    out_deg = np.count_nonzero(weight_matrix, axis=1)
    current_max_deg = max(out_deg)
    max_deg_indices = np.where(out_deg == current_max_deg)[0]

    x = np.zeros(n + 1)
    x[beta_id] = -1
    x[alpha_id] = 1

    # Store the state of each agent after finishing the connection with beta
    state = np.zeros(n + 1)
    state[beta_id] = -1
    state[alpha_id] = 1

    # Initiate the beta connection. Save agent state after completing connection
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
                        s += 1 * (x[neighbor_id] - x[u_id])
                    else:
                        s += weight_matrix[neighbor_id][u_id] * (x[neighbor_id] - x[u_id])

                old_u_state = x[u_id]
                x[u_id] += e * s
                convergence += abs(x[u_id] - old_u_state)

            t += 1
            if convergence <= epsilon or t >= max_iterations:
                break

        state[agent_id] = x[agent_id]
        neighbors[agent_id].remove((beta_id, 1))

    return alpha_id, state


def compute_influence_matrix(states, distance_matrix, node_dict):
    n_nodes = len(node_dict)
    influence_matrix = np.zeros((n_nodes, n_nodes))

    for u in node_dict.keys():
        for v in node_dict.keys():
            u_id = node_dict[u]
            v_id = node_dict[v]
            if distance_matrix[u_id][v_id] != 0:
                influence_matrix[u_id][v_id] = states[v_id] / (distance_matrix[u_id][v_id] ** 2)

    return influence_matrix


def compute_total_support(alpha_id, influence_matrix, node_dict, state):
    def sign(value):
        if value > 0:
            return 1
        elif value == 0:
            return 0
        else:
            return -1

    support = 0
    for node in node_dict.keys():
        node_id = node_dict[node]
        if node_id == alpha_id:
            continue

        support += sign(influence_matrix[alpha_id][node_id] - state[node_id])

    return support
