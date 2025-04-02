import json

from networkx import Graph


def load_gene_weight_from_file(network, filepath):
    with open(filepath, 'r') as f:
        d = json.load(f)

    for gene, weight in d.items():
        if gene in network.nodes:
            network.nodes[gene]['score'] = float(weight)

    return network


def load_co_expression(filepath):
    with open(filepath, 'r') as f:
        co_expression = json.load(f)

    return co_expression


def import_network_from_file(filepath, gene_score_path, co_expression_path):
    print("Loading network...")
    with open(filepath, "r") as f:
        data = f.readlines()

    network = Graph()
    for line in data[1:]:
        from_node, to_node, _, _ = line.strip().split("\t")

        # Filter non-existing gene
        if from_node == '(null)' or to_node == '(null)':
            continue

        network.add_edge(from_node, to_node)

    # Assign unique IDs (e.g., integer IDs)
    for i, node in enumerate(network.nodes()):
        network.nodes[node]["id"] = i  # Assign an integer ID
        network.nodes[node]["score"] = 0.0

    # Load gene weight
    network = load_gene_weight_from_file(network, gene_score_path)
    co_expression = load_co_expression(co_expression_path)

    return network, co_expression


def is_undirected_graph(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        _, _, direction, _ = line.strip().split("\t")
        if direction == '1':
            return False
    return True
