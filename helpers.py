import csv
import os

import matplotlib.pyplot as plt
import networkx as nx


def save_dict_as_csv(filepath, data, key='Node', value='Supports'):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([key, value])  # Header
        for key, value in data.items():
            writer.writerow([key, value])


def visualize(network):
    plt.figure(figsize=(50, 50))
    pos = nx.spring_layout(network, seed=42)
    # node_colors = ['blue' if community_structure[n] == 1 else 'red' for n in network.nodes]
    nx.draw(network, pos, with_labels=True, node_color='blue', node_size=8000, font_size=10, font_weight='bold',
            arrows=True)
    plt.show()


def convert_id_to_genename(node_dict):
    gene_dict = {}
    for gene in node_dict:
        gene_dict[node_dict[gene]] = gene

    return gene_dict


def transform_results_to_latex_table(result_folder, verified_genes, n_tested_genes):
    files = os.listdir(result_folder)

    table_begin_format = """\\begin{table}[h!]
    \\centering
    \\begin{tabular}{|c|c|c|}
    \\hline
    \\textbf{Cancer} & \\textbf{Gene Name} & \\textbf{Total Support} \\\\ \\hline
    """

    table_end_format = """
    \\end{tabular}
    \\caption{Combined table for multiple diseases and gene information}
    \\label{tab:combined}
\\end{table}
        """

    latex_file = './table.tex'
    with open(latex_file, 'w') as f:
        f.writelines(table_begin_format)

    cancer_first_line_format = "\\multirow{{3}}{{*}}{{{}}} & {} & {} \\\\ \n"

    cancer_other_line_format = """
    \\cline{{2-3}} & {} & {} \\\\
    """

    hline_format = "\\hline"

    for file in files:
        with open(os.path.join(result_folder, file), 'r') as f:
            content = f.readlines()

        dataset = content[0].strip()
        first_gene, support = content[1].strip().split(' ')
        other_genes = content[2:]
        with open(latex_file, 'a') as f:
            f.writelines(cancer_first_line_format.format(dataset, first_gene, support))
            for other_gene in other_genes:
                gene, support = other_gene.strip().split(' ')
                f.writelines(cancer_other_line_format.format(gene, support))
            f.writelines(hline_format)

    with open(latex_file, 'a') as f:
        f.writelines(table_end_format)
        f.writelines(
            f'RESULT: {verified_genes} over {n_tested_genes} ({round(verified_genes / n_tested_genes * 100, 2)}%) verified by OncoKB.')
