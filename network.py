import subprocess

from networkx import MultiGraph


def import_network_from_file(filepath):
    with open(filepath, "r") as f:
        data = f.readlines()

    network = MultiGraph()
    for line in data[1:]:
        from_node, to_node, _, _ = line.strip().split("\t")

        # Filter non-existing gene
        if from_node == '(null)' or to_node == '(null)':
            continue

        network.add_edge(from_node, to_node)

    # Assign unique IDs (e.g., integer IDs)
    for i, node in enumerate(network.nodes()):
        network.nodes[node]["id"] = i  # Assign an integer ID
        network.nodes[node]["score"] = 0

    return network


def is_undirected_graph(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        _, _, direction, _ = line.strip().split("\t")
        if direction == '1':
            return False
    return True


def convert_ensembl_gene_id_to_symbol(ensembl_gene_id):
    filepath = 'hsapiens_gene_ensembl__gene__main.txt'
    result = subprocess.run(f"bash -c \"cat {filepath} | cut -f7,8 | grep {ensembl_gene_id}\"", shell=True,
                            capture_output=True, text=True)
    return result.stdout.split('\t')[1].strip()
