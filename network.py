def import_network(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    node_dict = {}
    neighbors = {}
    edges = []

    node_id = 0
    for line in data[1:]:
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction = int(direction)
        weight = int(weight)

        if node_dict.get(from_node) is None:
            node_dict[from_node] = node_id
            node_id += 1

        if node_dict.get(to_node) is None:
            node_dict[to_node] = node_id
            node_id += 1

        from_id = node_dict[from_node]
        to_id = node_dict[to_node]

        if neighbors.get(from_id) is None:
            neighbors[from_id] = []

        if neighbors.get(to_id) is None:
            neighbors[to_id] = []

        neighbors[to_id].append((from_id, weight))
        if direction == 0:
            neighbors[from_id].append((to_id, weight))

        edges.append((from_id, to_id, direction, weight))

    return node_dict, neighbors, edges