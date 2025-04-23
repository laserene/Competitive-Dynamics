import os

from network import import_network_from_file
from pipeline import pipeline
from compare import compare
from modularity import *


def main():
    data_folder = './data/17KEGGSubMAX'
    files = os.listdir(data_folder)

    for file in files[:2]:
        dataset = file.split('.txt')[0]
        filepath = os.path.join(data_folder, file)
        gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
        co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'

        network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path)
        supports = pipeline(dataset, network, co_expression)

        compare()


if __name__ == '__main__':
    main()
