from network import import_network_from_file
from pipeline import pipeline
from modularity import *


def main():
    dataset = 'Acute myeloid leukemia'
    filepath = f'./data/17KEGGSubMAX/{dataset}.txt'
    gene_score_path = './resource/differentially_expressed_genes/TCGA-BRCA_de_genes.json'
    co_expression_path = './resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.json'

    network, co_expression = import_network_from_file(filepath, gene_score_path, co_expression_path)
    supports = pipeline(dataset, network, co_expression)

    # os.makedirs("states", exist_ok=True)
    # state_path = f'states/ppi_post_competition_state_{start}_{end}".json'
    # with open(state_path, 'w') as f:
    #     json.dump(states, f)


if __name__ == '__main__':
    main()
