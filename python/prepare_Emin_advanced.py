import os
import glob
import argparse
import subprocess
import shutil
import numpy as np
from prepare_ColabFold_advanced import reorder_structures

def filter_and_write_top_models(colab_out_dir, state):
    pdb_files = glob.glob(os.path.join(colab_out_dir, '*_unrelaxed_rank_*.pdb'))
    log_file = os.path.join(colab_out_dir, 'log.txt')
    custom_scores = []
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if 'reranking' in line:
            lines = lines[i+1:]
            break
            
    for line in lines:
        model_info = line.strip().split()
        model_name = model_info[2]
        
        if state == 'multimer':
            iptm = float(model_info[5].split('=')[1])
            ptm = float(model_info[4].split('=')[1])
            custom_score = 0.8 * iptm + 0.2 * ptm
        elif state == 'monomer':
            plddt = model_info[3].split('=')[1]
            plddt = float(model_info[4].split('=')[1])
            custom_score = 0.01 * np.mean(data['plddt']) * data['ptm']
        else:
            raise ValueError("Invalid state info (should be 'monomer' or 'multimer')")
            
        custom_scores.append((custom_score, model_name))
        
    custom_scores.sort(reverse=True)
    
    score_thresh = custom_scores[0][0] * 0.9
    filtered_info = [(score, model_name) for score, model_name in custom_scores if score >= score_thresh]
    
    new_info_with_pdb = []
    with open(f'{colab_out_dir}/MODEL_RANK_FILTERED.txt', 'w') as rank_file:
        rank_file.write('rank, monomer:(0.01*plddt*ptm)/multimer:(0.8*iptm+0.2*ptm), pdb_path\n')
        for i, (score, model_name) in enumerate(filtered_info):
            for pdb in pdb_files:
                if model_name in os.path.basename(pdb):
                    rank_file.write(f'{i + 1}, {model_name}, {pdb}\n')
                    new_info_with_pdb.append((score, pdb))
                    break
                    
    return new_info_with_pdb

def select_human_models(filtered_info, permuted_out_dir):
    os.makedirs(permuted_out_dir, exist_ok=True)
    
    score_lookup = {info[1]: info[0] for info in filtered_info}
    
    for pdb_path in score_lookup.keys():
        shutil.copy(pdb_path, permuted_out_dir)
        
    subprocess.run(['python', '/home/casp16/run/TS.human/T2201/utils/change_PDB_idx_for_TM_revised.py', permuted_out_dir, permuted_out_dir])
    
    for filename in os.listdir(permuted_out_dir):
        if not filename.startswith('CHAIN_REVISED_'):
            os.remove(os.path.join(permuted_out_dir, filename))
            
    score_lookup_base = {os.path.basename(info[1]): info[0] for info in filtered_info}
    revised_files = {file: score_lookup_base[file.split('CHAIN_REVISED_')[-1]] for file in os.listdir(permuted_out_dir) if file.startswith('CHAIN_REVISED_')}
    top_struct_with_new_chain = [os.path.join(permuted_out_dir, file) for file, _ in sorted(revised_files.items(), key=lambda item: item[1], reverse=True)]
    
    selected_structures = reorder_structures(top_struct_with_new_chain)
    
    return selected_structures

def main(args):
    base_dir = os.path.abspath(args.base_dir)
    state = args.state
    output_path = os.path.join(base_dir, 'Massivefold.colabfold/model')
    
    permuted_pdb_dir = os.path.join(base_dir, 'Massivefold.colabfold/permuted_top_models')
    models_before_Emin_dir = os.path.join(base_dir, 'models_before_Emin')
    os.makedirs(permuted_pdb_dir, exist_ok=True)
    os.makedirs(models_before_Emin_dir, exist_ok=True)
    
    filtered_info = filter_and_write_top_models(output_path, state)
    selected_structures = select_human_models(filtered_info, permuted_pdb_dir)
    
    for i, structure_file in enumerate(selected_structures[:5], start=1):
        destination_file = os.path.join(models_before_Emin_dir, f'human_model_{i}.pdb')
        shutil.copy(structure_file, destination_file)
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument("--base_dir", type=str, required=True, help="Base directory to work (e.g., /home/casp16/run/TS.human/T2201)")
    argparser.add_argument("--state", type=str, choices=['monomer', 'multimer'], required=True, help="Specify 'monomer' or 'multimer'")
    args = argparser.parse_args()
    main(args)
    