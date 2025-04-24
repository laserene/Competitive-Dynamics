import json
import os

import numpy as np

from compute_support import compute_total_support
from helpers import save_dict_as_csv
from outside_competition import outside_competition, compute_distance_matrix, load_distance_matrix_from_file, \
    load_states_from_file


def pipeline(dataset, network, co_expression, verbose=True):
    # Distance matrix
    distance_matrix_path = f'./distance_matrix/{dataset}_distance_matrix.csv'
    try:
        distance_matrix = load_distance_matrix_from_file(distance_matrix_path, verbose=verbose)
    except FileNotFoundError as e:
        if verbose:
            print('INFO: Distance matrix file does not exist!')
        distance_matrix = compute_distance_matrix(network, verbose=verbose)
        os.makedirs("distance_matrix", exist_ok=True)
        np.savetxt(distance_matrix_path, distance_matrix, delimiter=",", fmt='%d')

    # States
    os.makedirs("agent_supports", exist_ok=True)
    agent_supports_path = f'./agent_supports/{dataset}_state.json'
    try:
        agent_supports = load_states_from_file(filepath=agent_supports_path, verbose=verbose)
    except FileNotFoundError as e:
        if verbose:
            print('INFO: States file does not exist!')
        agent_supports = outside_competition(network, co_expression, run_full=True, verbose=verbose)
        with open(agent_supports_path, 'w') as f:
            json.dump(agent_supports, f)

    # Supports for all competitors alpha
    os.makedirs("supports", exist_ok=True)
    supports_path = f'./supports/{dataset}_supports.csv'
    supports = compute_total_support(network, agent_supports, distance_matrix, verbose=verbose)
    save_dict_as_csv(supports_path, supports)

    return supports
