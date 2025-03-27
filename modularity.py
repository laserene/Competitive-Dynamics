import numpy as np


def get_node_degree(weight_matrix):
    rows_sum = np.sum(weight_matrix, axis=1, keepdims=True)
    cols_sum = np.sum(weight_matrix, axis=0, keepdims=True)
    degree_matrix = rows_sum + cols_sum
    return np.diag(degree_matrix)


def calculate_modularity_matrix(weight_matrix, node_dict, n_edges):
    # Store the degree of each node
    degree_arr = get_node_degree(weight_matrix)

    node_degree = {key: degree_arr[node_dict[key]] for key in node_dict.keys()}

    # Expected edge matrix
    expected_edge_matrix = np.zeros_like(weight_matrix)
    for (i, j), _ in np.ndenumerate(expected_edge_matrix):
        expected_edge_matrix[i, j] = node_degree[i] * node_degree[j] / (2 * n_edges)

    # Modularity matrix
    modularity_matrix = weight_matrix - expected_edge_matrix

    return modularity_matrix

