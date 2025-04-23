import os

import pandas as pd


def main():
    n_gene = 3
    files = os.listdir("./supports")
    db = pd.read_csv("./OncoKB_geneList.csv")[["Hugo Symbol", "Entrez Gene ID"]]
    for file in files:
        total_supports = pd.read_csv(f"./supports/{file}")
        max_n_supported_genes = total_supports.sort_values(by=total_supports.columns[2], ascending=False)[
                                :n_gene].iloc[:, 1].values.tolist()

        results = []
        for gene in max_n_supported_genes:
            gene_id = gene.split("hsa:")[1]
            oncokb_gene = db[db["Entrez Gene ID"] == int(gene_id)]
            if oncokb_gene.empty:
                results.append(
                    f"{gene_id} {total_supports[total_supports.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]}\n")
            else:
                gene_name = oncokb_gene["Hugo Symbol"].values[0]
                results.append(
                    f"\\textbf{{{gene_name}}} {total_supports[total_supports.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]}\n")

        # Write to file
        filename = file.split(".")[0].split("_total_support")[0]
        results.insert(0, f"{filename}\n")
        os.makedirs("results", exist_ok=True)
        with open(f"./results/{filename}.txt", "w") as f:
            f.writelines("".join(results))


if __name__ == "__main__":
    main()
