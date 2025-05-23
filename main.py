import os

from compare import compare
from helpers import transform_results_to_latex_table
from network import import_network_from_file
from pipeline import pipeline


def main():
    data_folder = './data/4-Human Gene Regulatory Network - Input.txt'
    # files = os.listdir(data_folder)
    verbose = True

    # Computing
    # for file in files:
    #     dataset = file.split('.txt')[0]
    #     filepath = os.path.join(data_folder, file)
    #     # gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    #     # co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'
    #
    #     print(f'INFO: {dataset} dataset')
    #     network, co_expression = import_network_from_file(filepath,
    #                                                       verbose=verbose)
    #     with open('driver.txt', 'r') as file:
    #         content = file.read()
    #
    #     # Split the content by whitespace and convert each item to an integer
    #     numbers = set([int(num) for num in content.split()])
    #
    #     driver_id = []
    #     for node in set(network.nodes):
    #         if node['id'] in numbers:
    #             driver_id.append(node)


        # pipeline(dataset, network, co_expression, verbose=verbose)
        # print()

    dataset = data_folder.split('.txt')[0]
    # gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    # co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'

    print(f'INFO: {dataset} dataset')
    network, co_expression = import_network_from_file(data_folder,
                                                      verbose=verbose)
    with open('driver.txt', 'r') as file:
        content = file.read()

    # Split the content by whitespace and convert each item to an integer
    numbers = set([int(num) for num in content.split()])

    driver_set = []
    for node in network.nodes:
        if network.nodes[node]['id'] in numbers:
            driver_set.append(node)

    pipeline(dataset, network, driver_set, verbose=verbose)

    # Evaluation
    verified_genes, n_tested_genes = compare()

    # Export result
    transform_results_to_latex_table('./results', verified_genes, n_tested_genes)


if __name__ == '__main__':
    main()
