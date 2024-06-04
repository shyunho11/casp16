import os
import sys
import shutil
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

# ANSI color codes
RED = "\033[91m"
RESET = "\033[0m"

class MultiOutput:
    def __init__(self, readme_fn):
        self.terminal = sys.stdout
        self.log = open(readme_fn, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def count_chains(pdb_file):
    chains = set()
    with open(pdb_file, 'r') as file:
        chains.update(line[21] for line in file if line.startswith('ATOM'))
    return len(chains)

def calculate_tm_score(pdb1, pdb2):
    chains1 = count_chains(pdb1)
    chains2 = count_chains(pdb2)
    
    # add -ter 0 -c option to TMscore if monomer
    command = ['TMscore', pdb1, pdb2] if chains1 == 1 and chains2 == 1 else ['TMscore', '-ter 0', '-c', pdb1, pdb2]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # extract TM-score
    for line in result.stdout.split('\n'):
        if "TM-score    =" in line:
            return float(line.strip().split('=')[1].split()[0])
        
    return 0.0

def find_farthest_structure(reference, structures):
    # parallelize TMscore calculation
    with ThreadPoolExecutor() as executor:
        scores = list(executor.map(lambda struct: calculate_tm_score(reference, struct), structures))
    
    min_score = min(scores)
    return structures[scores.index(min_score)]

def find_least_average_distance_structure(selected, remaining_structures):
    def average_tm_score(structure):
        return sum(calculate_tm_score(sel, structure) for sel in selected) / len(selected)
    
    # parallelize TMscore calculation
    with ThreadPoolExecutor() as executor:
        scores = list(executor.map(average_tm_score, remaining_structures))
    
    min_score = min(scores)
    return remaining_structures[scores.index(min_score)]

def reorder_structures(structure_files):
    if len(structure_files) <= 2: # no need to compare
        return structure_files
    
    # In case we have at least three structures
    best_structure = structure_files[0]
    selected = [best_structure]
    remaining_structures = structure_files[1:]
    
    # find 2nd structure
    second_structure = find_farthest_structure(best_structure, remaining_structures)
    selected.append(second_structure)
    remaining_structures.remove(second_structure)
    
    # find 3rd, 4th, 5th structure
    for i in range(3):
        if len(remaining_structures) == 1:
            selected.append(remaining_structures[0])
            break
            
        next_structure = find_least_average_distance_structure(selected, remaining_structures)
        selected.append(next_structure)
        remaining_structures.remove(next_structure)
        
    return selected

def filter_pdb_by_bfactor(pdb_file, output_pdb_file, threshold=70.0):
    with open(pdb_file, 'r') as infile, open(output_pdb_file, 'w') as outfile:
        for line in infile:
            if line.startswith('ATOM'):
                bfactor = float(line[60:66].strip())
                if bfactor >= threshold:
                    outfile.write(line)

def process_score_file(score_file, input_pdb_dir, state, threshold=None):
    print(f'\n■ {os.path.basename(score_file)} [{os.path.basename(os.path.dirname(score_file))}] (Threshold = {threshold})')
    
    sorted_list = []
    unique_dict = {}
    not_unique_dict = {}
    
    with open(score_file, 'r') as f:
        lines = f.readlines()[1:]
        
    # Parsing each line
    for line in lines:
        line = line.strip()
        pdb = os.path.join(input_pdb_dir, line.split()[1])
        composite_score = float(line.split()[3])
        custom_score = float(line.split()[-1])
        score = composite_score if state == 'monomer' else custom_score
        sorted_list.append((pdb, score))
        
    # Select top 1 model
    top100_list = sorted_list[:100]
    top1_pdb, top1_score = top100_list[0]
    unique_dict[top1_pdb] = top1_score
    top1_name = os.path.basename(top1_pdb)
    print(f'○ Top 1 model: {top1_name}')
    
    # Calculate TMscore if threshold is provided
    if not threshold:
        count = 2
        for pdb, score in top100_list[1:11]:
            unique_dict[pdb] = score
            print(f'{RED}○ Found next model: {os.path.basename(pdb)}{RESET}')
            count += 1
    else:
        for pdb, score in top100_list:
            unique_fold = all(calculate_tm_score(pdb, unique_pdb) <= threshold for unique_pdb in unique_dict.keys())
            if unique_fold:
                unique_dict[pdb] = score
                print(f'○ Found unique model: {os.path.basename(pdb)}')
                if len(unique_dict) >= 10:
                    break
                    
    if len(unique_dict) <= 1:
        print(f'Warning: Failed to find a unique model.')
        
    return unique_dict

def get_templates_for_colabfold(score_file_AF, score_file_MULTIMER, output_path, input_pdb_dir, state):
    AF_unique_dict = process_score_file(score_file_AF, input_pdb_dir, state, 0.9)
    MULTI_unique_dict = process_score_file(score_file_MULTIMER, input_pdb_dir, state, 0.9)
    
    merged_dict = {}
    
    for key, value in AF_unique_dict.items():
        merged_dict[key] = value
        
    # Insert items from the multimer result, keeping the highest score in case of duplicate PDBs
    for key, value in MULTI_unique_dict.items():
        if key in merged_dict:
            merged_dict[key] = max(merged_dict[key], value)
        else:
            merged_dict[key] = value
            
    sorted_dict = dict(sorted(merged_dict.items(), key=lambda item: item[1], reverse=True)[:10])
    
    top_unique_list = [pdb_file for pdb_file, _ in sorted_dict.items()]
    selected_struct = reorder_structures(top_unique_list)
    
    return selected_struct


def main(args):
    base_dir = args.base_dir
    state = args.state
    sys.stdout = MultiOutput(os.path.join(base_dir, 'README.txt'))
    
    if state == 'monomer': # if monomer, select models w composite score
        AF_score_file = os.path.join(base_dir, 'Massivefold.AF2Rank/ver.AF/RANK_BY_COMPOSITE.txt')
        MULTI_score_file = os.path.join(base_dir, 'Massivefold.AF2Rank/ver.MULTIMER/RANK_BY_COMPOSITE.txt')
    elif state == 'multimer': # if multimer, select models w custom score (plddt*ptm*iptm)
        AF_score_file = os.path.join(base_dir, 'Massivefold.AF2Rank/ver.AF/RANK_BY_CUSTOM_SCORE.txt')
        MULTI_score_file = os.path.join(base_dir, 'Massivefold.AF2Rank/ver.MULTIMER/RANK_BY_CUSTOM_SCORE.txt')
    else:
        raise ValueError("--state option should be one of these: monomer, multimer")
    
    print('******************** Preparing ColabFold ********************')
    print(f'Using AF2Rank {"Custom" if state == "multimer" else "Composite"} score to select templates')
    
    input_pdb_dir = os.path.join(base_dir, 'Massivefold.AF2Rank/inputs')
    output_path = os.path.join(base_dir, 'Massivefold.AF2Rank/')
    colabfold_templ_dir = os.path.join(base_dir, 'Massivefold.colabfold/templates')
    os.makedirs(colabfold_templ_dir, exist_ok=True)
    models_before_Emin_dir = os.path.join(base_dir, 'models_before_Emin')
    os.makedirs(models_before_Emin_dir, exist_ok=True)
    MiniWorld_dir = os.path.join(base_dir, 'for_MiniWorld')
    os.makedirs(MiniWorld_dir, exist_ok=True)
        
    selected_struct = get_templates_for_colabfold(AF_score_file, MULTI_score_file, output_path, input_pdb_dir, state)
    n_unique = len(selected_struct)
    
    if n_unique < 10: # in case we don't have 10 structures
        print(f'\n\nSince we have only {n_unique} models, adding 10 models based on AF2Rank score')
        
        AF_top10_dict = process_score_file(AF_score_file, input_pdb_dir, state)
        for top10_pdb in AF_top10_dict.keys():
            if not top10_pdb in selected_struct:
                selected_struct.append(top10_pdb)
                
    print('\n'+'#'*61+'\n'+'#'+' '*20+'FINAL MODEL SUMMARY'+' '*20+'#'+'\n'+'#'*61+'\n\n'+'[ColabFold templates]')
    
    # Copy up to 4 structures to colabfold_templ_dir, and write residues with higher plddt than threshold in template dir
    for i_templ, templ in enumerate(selected_struct[:min(n_unique, 4)], start=1):
        output_pdb_file = os.path.join(colabfold_templ_dir, f'tmp{i_templ}.pdb')
        print(f'● tmp{i_templ}.pdb = {os.path.basename(templ)}')
        filter_pdb_by_bfactor(templ, output_pdb_file)
    
    print('----------------------------------------\n[FAKER final models]')
    
    # Copy 5 structure to models_before_Emin_dir (for team FAKER)
    for i_struct, structure_file in enumerate(selected_struct[:5], start=1):
        destination_file = os.path.join(models_before_Emin_dir, f'FAKER_model_{i_struct}.pdb')
        shutil.copy(structure_file, destination_file)
        if i_struct > n_unique:
            print(f'{RED}● FAKER_model_{i_struct}.pdb = {os.path.basename(structure_file)} (Not unique){RESET}')
        else:
            print(f'● FAKER_model_{i_struct}.pdb = {os.path.basename(structure_file)}')
            
    print('----------------------------------------\n[For MiniWorld]')
    
    # Copy 10 structures for MiniWorld input models
    for i_struct, structure_file in enumerate(selected_struct[:10], start=1):
        destination_file = os.path.join(MiniWorld_dir, f'forMiniWorld_model_{i_struct}.pdb')
        shutil.copy(structure_file, destination_file)
        if i_struct > n_unique:
            print(f'{RED}● forMiniWorld_model_{i_struct}.pdb = {os.path.basename(structure_file)} (Not unique){RESET}')
        else:
            print(f'● forMiniWorld_model_{i_struct}.pdb = {os.path.basename(structure_file)}')
            
            
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument("--base_dir", type=str, help="base dir to work (e.g./home/casp16/run/TS.human/T2201)")
    argparser.add_argument("--state", type=str, help="monomer or multimer")
    args = argparser.parse_args()
    main(args)
    