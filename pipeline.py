import json
import os

import numpy as np

from compute_support import compute_total_support
from helpers import save_dict_as_csv
from outside_competition import outside_competition, compute_distance_matrix, load_distance_matrix_from_file, \
    load_states_from_file


def pipeline(dataset, network, co_expression):
    # Distance matrix
    distance_matrix_path = f'./distance_matrix/{dataset}_distance_matrix.csv'
    try:
        distance_matrix = load_distance_matrix_from_file(distance_matrix_path)
    except FileNotFoundError as e:
        print('INFO: Distance matrix file does not exist!')
        distance_matrix = compute_distance_matrix(dataset, network)
        os.makedirs("distance_matrix", exist_ok=True)
        np.savetxt(distance_matrix_path, distance_matrix, delimiter=",", fmt='%d')

    # States
    states_path = f'./states/{dataset}_state.json'
    try:
        states = load_states_from_file(filepath=states_path)
    except FileNotFoundError as e:
        print('INFO: States file does not exist!')
        states = outside_competition(network, co_expression, run_full=True)
        with open(states_path, 'w') as f:
            json.dump(states, f)

    # Supports
    supports_path = f'./supports/{dataset}_supports.csv'
    supports = compute_total_support(network, states, distance_matrix)
    save_dict_as_csv(supports_path, supports)

    return supports
