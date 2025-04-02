import json
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from tqdm import tqdm


def preprocess_co_expression(line, lookup):
    from_ensembl_id, to_ensembl_id, score = line.strip().split("\t")
    pair = {}
    try:
        from_symbol = lookup.get(from_ensembl_id, from_ensembl_id)
        to_symbol = lookup.get(to_ensembl_id, to_ensembl_id)
        pair[f'{from_symbol}, {to_symbol}'] = float(score)
    except Exception as e:
        print(f'Err {e} at {line}')

    return pair


def preprocess_co_expression_wrapper(filepath):
    with open(filepath, 'r') as f:
        data = f.readlines()

    with open('./extracted_ensg_genes.json', 'r') as f:
        lookup = json.load(f)

    with ProcessPoolExecutor() as executor:
        states = list(tqdm(executor.map(
            partial(preprocess_co_expression, lookup=lookup), data[1:])))

    d = {k: v for d in states for k, v in d.items()}
    new_filepath = filepath.replace('.tsv', '.json')
    with open(new_filepath, 'w') as f:
        json.dump(d, f, indent=4)


def main():
    preprocess_co_expression_wrapper('./resource/co_exp_network/TCGA-BRCA__co_expression__t_70_.tsv')


if __name__ == '__main__':
    main()
