import json

from outside_competition import compute_distance_matrix, load_distance_matrix_from_file
from compute_support import compute_total_support


def pipeline(network):
    dataset = 'Human PPI network'
    distance_matrix_path = './distance_matrix/Human PPI network_distance_matrix.csv'

    try:
        distance_matrix = load_distance_matrix_from_file(distance_matrix_path)
    except FileNotFoundError as e:
        print('Distance matrix file does not exist!')
        distance_matrix = compute_distance_matrix(dataset, network)

    start = 1000
    end = 1300
    # states = outside_competition(network, co_expression, start, end)
    with open('./states/ppi_post_competition_state.json') as f:
        states = json.load(f)

    supports = compute_total_support(network, states, distance_matrix)

    return supports
