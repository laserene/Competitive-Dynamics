import os
import json

from network import import_network_from_file
from outside_competition import outside_competition, compute_distance_matrix, load_distance_matrix_from_file


def main():
    dataset = 'Human PPI network'
    filepath = './data/4-Human PPI network - Input.txt'
    distance_matrix_path = './distance_matrix/Human PPI network_distance_matrix.csv'
    gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'

    network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path)
    try:
        distance_matrix = load_distance_matrix_from_file(distance_matrix_path)
    except FileNotFoundError as e:
        print('Distance matrix file does not exist!')
        distance_matrix = compute_distance_matrix(dataset, network)

    start = 1000
    end = 1300
    states = outside_competition(network, co_expression, start, end)

    os.makedirs("support", exist_ok=True)
    state_path = f'./support/ppi_post_competition_state_{start}_{end}".json'
    with open(state_path, 'w') as f:
        json.dump(states, f)


if __name__ == '__main__':
    main()
