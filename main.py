from network import import_network_from_file
from outside_competition import load_distance_matrix_from_file

def main():
    # dataset = 'Human PPI network'
    filepath = './data/4-Human PPI network - Input.txt'
    distance_matrix_path = './distance_matrix/Human PPI network_distance_matrix.csv'
    gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'

    network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path)
    distance_matrix = load_distance_matrix_from_file(distance_matrix_path)
    pass
    # outside_competition(network, gene_score_path, co_expression_path)


if __name__ == '__main__':
    main()
