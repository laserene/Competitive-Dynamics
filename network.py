from networkx import MultiGraph
from biomart import BiomartServer


def import_network_from_file(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    network = MultiGraph()
    for line in data[1:]:
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction = int(direction)
        weight = int(weight)
        network.add_edge(from_node, to_node)

    # Assign unique IDs (e.g., integer IDs)
    for i, node in enumerate(network.nodes()):
        network.nodes[node]["id"] = i  # Assign an integer ID

    return network


def is_undirected_graph(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        _, _, direction, _ = line.strip().split("\t")
        if direction == '1':
            return False
    return True


def load_network_weight(path):
    pass


def convert_ensembl_gene_id_to_symbol(ensembl_gene_id):
    server = BiomartServer("http://www.ensembl.org/biomart")
    mart = server.datasets["hsapiens_gene_ensembl"]
    result = mart.search({
        'filters': {'ensembl_gene_id': ["ENSG00000169242"]},
        'attributes': ["ensembl_gene_id", "external_gene_name"]
    })
    return result.text
