import random
import json
import time
import argparse
from casp.web import get_target_sequence
from casp.utils import parse_stoichiometry

def make_af3_json(target_id, stoichiometry, seed):
    protein_sequences = get_target_sequence(target_id)
    counts = parse_stoichiometry(stoichiometry)
    
    json_structure = {
        "name": f'{target_id}_{seed}',
        "modelSeeds": [seed],
        "sequences": []
    }
    
    # Add protein sequences with their respective counts
    for seq, count in zip(protein_sequences, counts):
        json_structure["sequences"].append({
            "proteinChain": {
                "sequence": seq,
                "count": count[1]  # count[1] holds the count value
            }
        })
    
    return json_structure

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate JSON for protein sequences.')
    parser.add_argument('target_id', type=str, help='The target ID for the protein sequences.')
    parser.add_argument('stoichiometry', type=str, help='The stoichiometry string.')
    parser.add_argument('-n', '--num_seeds', type=int, default=20, help='The number of seeds to generate.')

    args = parser.parse_args()
    
    all_json_structures = []
    
    current_time_seed = int(time.time())
    random.seed(current_time_seed)
    
    # Generate multiple JSON structures each with a unique seed
    for _ in range(args.num_seeds):
        generated_json = make_af3_json(args.target_id, args.stoichiometry, random.randint(1, 999999999))
        all_json_structures.append(generated_json)
    
    # Wrap all JSON structures into one list and save to file
    json_output = json.dumps(all_json_structures, indent=4)
    
    output_file = f'AF3_{args.target_id}.json'
    with open(output_file, 'w') as f:
        f.write(json_output)
        
    print(f'File saved as {output_file}')
