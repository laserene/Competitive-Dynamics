import json

from network import import_network_from_file
from outside_competition import *


def main():
    # dataset = 'Human PPI network'
    filepath = './data/4-Human PPI network - Input1.txt'
    distance_matrix_path = './distance_matrix/Human PPI network_distance_matrix.csv'
    gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'
    support_path = './support/ppi_total_support.json'

    network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path)
    distance_matrix = load_distance_matrix_from_file(distance_matrix_path)

    states = outside_competition(network, distance_matrix, co_expression)
    with open(support_path, 'w') as f:
        json.dump(states, f)


if __name__ == '__main__':
    main()
