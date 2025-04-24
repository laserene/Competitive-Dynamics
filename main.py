import os

from compare import compare
from helpers import transform_results_to_latex_table


def main():
    data_folder = './data/17KEGGSubMAX'
    files = os.listdir(data_folder)
    verbose = True

    # Computing
    # for file in files[:2]:
    #     dataset = file.split('.txt')[0]
    #     filepath = os.path.join(data_folder, file)
    #     gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    #     co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'
    #
    #     print(f'INFO: {dataset} dataset')
    #     network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path, verbose=verbose)
    #     pipeline(dataset, network, co_expression, verbose=verbose)
    #     print()

    # Evaluation
    # verified_genes, n_tested_genes = compare()

    # Export result
    verified_genes, n_tested_genes = 40, 80
    transform_results_to_latex_table('./results', verified_genes, n_tested_genes)


if __name__ == '__main__':
    main()
