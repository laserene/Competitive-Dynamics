# Undirected connection will be converted to 2 directed connections
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from tqdm import tqdm

from network import *
from outside_competition import *


def main():
    datasets = os.listdir("./data")
    data_objects = [(os.path.join("./data", dataset), dataset.split(".txt")[0].strip()) for dataset in datasets]
    for path, dataset in data_objects:
        print(dataset)
        node_dict, neighbors, edges = import_network(path)
        weight_matrix = extract_weight_matrix(node_dict, edges)
        distance_matrix = compute_distance_matrix(dataset, weight_matrix, node_dict)
        n_edges = len(edges)
        with ProcessPoolExecutor() as executor:
            states = list(tqdm(executor.map(
                partial(compete, weight_matrix=weight_matrix,
                        node_dict=node_dict, neighbors=neighbors,
                        n_edges=n_edges),
                node_dict.keys())))

        total_supports = {}
        for alpha_id, state in states:
            influence_matrix = compute_influence_matrix(state, distance_matrix, node_dict)
            support = compute_total_support(alpha_id, influence_matrix, node_dict, state)
            total_supports[alpha_id] = support

        os.makedirs("total_support", exist_ok=True)
        with open(f"total_support/{dataset}_total_supports.csv", "w") as f:
            id_to_node = {v: k for k, v in node_dict.items()}
            f.write("Node_ID, Node, Total Support\n")
            for node, support in total_supports.items():
                f.write(f"{node}, {id_to_node[node]}, {support}\n")


if __name__ == "__main__":
    main()
