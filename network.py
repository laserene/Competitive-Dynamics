from networkx import MultiGraph


def import_network_from_file(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    network = MultiGraph()
    for line in data[1:]:
        from_node, to_node, _, _ = line.strip().split("\t")
        # direction = int(direction)
        # weight = int(weight)

        network.add_edge(from_node, to_node)

    return network


def is_undirected_graph(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        _, _, direction, _ = line.strip().split("\t")
        if direction == '1':
            return False
    return True
