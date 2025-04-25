import os

import pandas as pd


def compare():
    files = os.listdir("./supports")
    db = pd.read_csv("./OncoKB_geneList.csv")
    db['Gene Aliases'] = db['Gene Aliases'].apply(
        lambda x: [alias.strip() for alias in x.split(',')] if isinstance(x, str) else []
    )

    n_gene = 100

    # Evaluation
    verified_genes = []
    n_file = 0
    for file in files:
        total_supports = pd.read_csv(f"./supports/{file}")
        max_n_supported_genes = total_supports.sort_values(by=total_supports.columns[2], ascending=False)[
                                :n_gene].iloc[:, 1].values.tolist()

        results = []
        for gene in max_n_supported_genes:
            gene_clean = gene.strip()
            found = (((db['Hugo Symbol'] == gene_clean) | (gene.strip() in db['Gene Aliases'])).any() and (
                        (db['Is Oncogene'] == 'Yes') | (db['Is Tumor Suppressor Gene'] == 'Yes')).any())
            if found:
                results.append(
                    f"\\textbf{{{gene.strip()}}} "
                    f"{total_supports[total_supports.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]} \\\\ \n")
                if len(verified_genes) <= n_file:
                    verified_genes.append(1)
                else:
                    verified_genes[n_file] += 1
            else:
                results.append(
                    f"{gene.strip()} {total_supports[total_supports.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]} \\\\ \n")

        results.append(
            f'{verified_genes[n_file]} genes verified over {n_gene} ({verified_genes[n_file] / n_gene * 100}\\%).')

        # Write to file
        filename = file.split(".")[0].split("_total_supports")[0]
        results.insert(0, f"{filename}\n")
        os.makedirs("results", exist_ok=True)
        with open(f"./results/{filename}_{n_gene}.txt", "w") as f:
            f.writelines("".join(results))

        n_file += 1

    n_tested_genes = n_gene * len(files)
    print(
        f'RESULT: {sum(verified_genes)} over {n_tested_genes} ({round(sum(verified_genes) / n_tested_genes * 100, 2)}%) '
        f'verified by OncoKB.')

    return verified_genes, n_tested_genes
