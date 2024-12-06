# with open("./data/4-Human cancer signaling - Input.txt", "r") as f:
#     data = f.readlines()
#
# count_u = 0
# count = 0
# for line in data:
#     if count == 0:
#         count += 1
#         continue
#     from_node, to_node, direction, weight = line.strip().split("\t")
#     direction = int(direction)
#     weight = int(weight)
#
#     if from_node == "14-3-3" and direction == 1:
#         count_u += 1
#
# print(count_u)

import random

n_nodes = 5

# Generate random numbers multiple times
results = [random.randint(0, n_nodes) for _ in range(10)]

print(results)

