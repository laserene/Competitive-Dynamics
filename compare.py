import os

import pandas as pd


def main():
    files = os.listdir("./total_support")
    db = pd.read_csv("./cancerGeneList.csv")[["Hugo Symbol", "Entrez Gene ID", "Is Tumor Suppressor Gene"]]
    for file in files:
        data = pd.read_csv(f"./total_support/{file}")
        max_support = data.iloc[:, 2].max()
        genes = data[data.iloc[:, 2] == max_support].iloc[:, 1].values.tolist()
        if len(genes) < 3:
            genes = data.sort_values(by=data.columns[2], ascending=False).iloc[:3, 1].values.tolist()
        results = []
        for gene in genes:
            gene_id = gene.split("hsa:")[1]
            oncokb_gene = db[db["Entrez Gene ID"] == int(gene_id)]
            if oncokb_gene.empty:
                results.append(gene_id)
            else:
                gene_name = oncokb_gene["Hugo Symbol"].values[0]
                if oncokb_gene["Is Tumor Suppressor Gene"].values[0] == "Yes":
                    results.append(f"\\textbf{{{gene_name}}}")
                else:
                    results.append(gene_name)
        filename = file.split(".")[0].split("_total_support")[0]
        results.insert(0, f"{filename}\n")
        with open(f"./results/{filename}.txt", "w") as f:
            f.writelines(", ".join(results))


if __name__ == "__main__":
    main()
