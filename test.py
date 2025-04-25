import pandas as pd

with open('./results/Human Gene Regulatory Network.txt', 'r') as f:
    content = f.readlines()

df = pd.read_csv("./OncoKB_geneList.csv")
candidate = []
n = 100
for line in content[1:100]:
    value, v = line.strip().split(' ')
    found = ((df['Hugo Symbol'] == value) | (df['Gene Aliases'] == value)).any()
    if found:
        candidate.append(value)

print(candidate)
