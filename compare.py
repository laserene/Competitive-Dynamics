import os

import pandas as pd


def main():
    files = os.listdir("./total_support")
    db = pd.read_csv("./OncoKB_geneList.csv")[["Hugo Symbol", "Entrez Gene ID", "Is Tumor Suppressor Gene"]]
    for file in files:
        data = pd.read_csv(f"./total_support/{file}")
        max_support = data.iloc[:, 2].min()
        genes = data[data.iloc[:, 2] == max_support].iloc[:, 1].values.tolist()

        # Get the top 10 genes if there are less than 10 genes with the same states
        if len(genes) < 10:
            genes = data.sort_values(by=data.columns[2], ascending=True).iloc[:10, 1].values.tolist()
        results = []

        for gene in genes:
            gene_id = gene.split("hsa:")[1]
            oncokb_gene = db[db["Entrez Gene ID"] == int(gene_id)]
            if oncokb_gene.empty:
                results.append(f"{gene_id} {data[data.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]}\n")
            else:
                gene_name = oncokb_gene["Hugo Symbol"].values[0]
                results.append(f"\\textbf{{{gene_name}}} {data[data.iloc[:, 1] == gene].iloc[:, 2].values.tolist()[0]}\n")

        # Write to file
        filename = file.split(".")[0].split("_total_support")[0]
        results.insert(0, f"{filename}\n")
        os.makedirs("results", exist_ok=True)
        with open(f"./results/{filename}.txt", "w") as f:
            f.writelines("".join(results))


if __name__ == "__main__":
    main()
