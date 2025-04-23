import os

import pandas as pd


def compare():
    files = os.listdir("./supports")
    db = pd.read_csv("./OncoKB_geneList.csv")[["Hugo Symbol", "Entrez Gene ID"]]

    n_gene = 3
    verified_genes = 0
    n_tested_genes = 0
    for file in files:
        n_tested_genes += n_gene
        total_supports = pd.read_csv(f"./supports/{file}")
        max_n_supported_genes = total_supports.sort_values(by=total_supports.columns[1], ascending=False)[
                                :n_gene].iloc[:, 0].values.tolist()

        results = []
        for gene in max_n_supported_genes:
            gene_id = gene.split("hsa:")[1]
            oncokb_gene = db[db["Entrez Gene ID"] == int(gene_id)]
            if oncokb_gene.empty:
                results.append(
                    f"{gene_id} {total_supports[total_supports.iloc[:, 0] == gene].iloc[:, 1].values.tolist()[0]}\n")
            else:
                gene_name = oncokb_gene["Hugo Symbol"].values[0]
                results.append(
                    f"\\textbf{{{gene_name}}} {total_supports[total_supports.iloc[:, 0] == gene].iloc[:, 1].values.tolist()[0]}\n")
                verified_genes += 1

                # Write to file
        filename = file.split(".")[0].split("_total_support")[0]
        results.insert(0, f"{filename}\n")
        os.makedirs("results", exist_ok=True)
        with open(f"./results/{filename}.txt", "w") as f:
            f.writelines("".join(results))

    print(
        f'RESULT: {verified_genes} over {n_tested_genes} ({round(verified_genes / n_tested_genes * 100, 2)}%) verified by OncoKB.')
