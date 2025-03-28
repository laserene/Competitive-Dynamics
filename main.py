from network import import_network_from_file
from outside_competition import outside_competition


def main():
    # dataset = 'Human PPI network'
    filepath = './data/4-Human PPI network - Input.txt'
    gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.tsv'
    network = import_network_from_file(filepath)
    outside_competition(network, gene_score_path)


if __name__ == '__main__':
    main()
