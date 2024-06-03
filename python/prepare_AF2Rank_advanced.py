import os
import json
import glob
import argparse
import subprocess
from Bio import PDB

def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        
# read iptm and ptm
def rerank_by_custom_score_multimer(iptm_file, ptm_file):
    data_iptm = read_json(iptm_file)
    data_ptm = read_json(ptm_file)

    # calculate new custom score and store it
    custom_scores = {
        sample_name: 0.8 * data_iptm['iptm'][sample_name] + 0.2 * data_ptm['ptm'][sample_name]
        for sample_name in set(data_iptm['iptm']).intersection(data_ptm['ptm'])
    }
    
    # sort by score
    sorted_custom_scores = {k: v for k, v in sorted(custom_scores.items(), key=lambda item: item[1], reverse=True)}
    
    result = {"custom_scores": sorted_custom_scores, "order": list(sorted_custom_scores.keys())}
    write_json(result, 'ranking_custom.json')
    
def rerank_by_custom_score_monomer(ptm_file):
    data_ptm = read_json(ptm_file)
    
    # use pTM as score
    custom_scores = data_ptm['ptm']
    
    # sort by score
    sorted_custom_scores = {k: v for k, v in sorted(custom_scores.items(), key=lambda item: item[1], reverse=True)}
    
    result = {"custom_scores": sorted_custom_scores, "order": list(sorted_custom_scores.keys())}
    write_json(result, 'ranking_custom.json')
    
def integrate_and_filter_scores(base_dir, score_cutoff, num_cutoff):
    all_scores = []
    for path, _, files in os.walk(base_dir):
        if 'ranking_custom.json' in files:
            data = read_json(os.path.join(path, 'ranking_custom.json'))
            subdir = os.path.basename(path)
            all_scores.extend((model, score, subdir) for model, score in data['custom_scores'].items())
            
    sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
    print(f'total_len : {len(sorted_scores)}')
    
    highest_score = sorted_scores[0][1] * score_cutoff
    filtered_scores = [(model, score, subdir) for model, score, subdir in sorted_scores if score >= highest_score]
    
    print(f'score_thresh_filtered_len : {len(filtered_scores)}')
    
    N_select = min(int(len(sorted_scores) * num_cutoff), len(filtered_scores))
    filtered_scores = filtered_scores[:N_select]
    
    print(f'num_thresh_filtered_len : {len(filtered_scores)}')
    return filtered_scores

def save_filtered_results(base_dir, filtered_results):
    result_data = {"results": [{"model": model, "score": score, "directory": subdir} for model, score, subdir in filtered_results]}
    output_file = os.path.join(base_dir, 'filtered_ranking_custom.json')
    write_json(result_data, output_file)
    print(f"Filtered results have been saved to {output_file}")
    
def link_files(base_dir, target_dir, filtered_results):
    os.makedirs(target_dir, exist_ok=True)
    
    for model, score, subdir in filtered_results:
        pattern = os.path.join(base_dir, subdir, f"*{model}.pdb")
        matching_files = glob.glob(pattern)
        
        if len(matching_files) == 1:
            source_file = matching_files[0]
            target_file = os.path.join(target_dir, f"{subdir}_{model}.pdb")
            if not os.path.exists(target_file):
                os.symlink(source_file, target_file)
                print(f"Linked {source_file} to {target_file}")
            else:
                print(f"Link already exists: {target_file}")
        elif len(matching_files) > 1:
            raise Exception(f"Error: More than one matching file found for model: {model} in {subdir}. Please check the files.")
        else:
            print(f"No matching files found for model: {model} in {subdir}")
            
def change_chain_ids(directory, chain_list):
    parser = PDB.PDBParser(QUIET=True)
    io = PDB.PDBIO()
    chain_ids = chain_list.split(',')
    
    for filename in os.listdir(directory):
        if filename.endswith(".pdb"):
            filepath = os.path.join(directory, filename)
            structure = parser.get_structure('PDB', filepath)
            
            all_chains = list(structure.get_chains())
            if len(all_chains) == len(chain_ids):
                for i_chain, chain_id in enumerate(chain_ids):
                    all_chains[i_chain].id = chain_id
                    
                io.set_structure(structure)
                io.save(filepath)
                print(f"Updated chain IDs to {chain_list} in {filepath}")
            else:
                print(f"File {filepath} does not have exactly the intended number of chains, no changes made.")
                
def main(args):
    base_dir = os.path.abspath(args.base_dir)
    data_dir = os.path.abspath(args.decoy_data_dir)
    chain_list = args.chain_list
    state = args.state
    score_cutoff = args.score_cutoff
    num_cutoff = args.num_cutoff
    
    for subdir in [os.path.join(data_dir, subdir) for subdir in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, subdir))]:
        if 'ranking_ptm.json' in os.listdir(subdir):
            if state == 'multimer':
                rerank_by_custom_score_multimer(os.path.join(subdir, 'ranking_iptm.json'), os.path.join(subdir, 'ranking_ptm.json'))
            elif state == 'monomer':
                rerank_by_custom_score_monomer(os.path.join(subdir, 'ranking_ptm.json'))
            else:
                raise ValueError("--state option should be one of these: monomer, multimer")
                
    filtered_results = integrate_and_filter_scores(base_dir, score_cutoff, num_cutoff)
    save_filtered_results(data_dir, filtered_results)
    
    af2rank_dir = os.path.join(base_dir, "Massivefold.AF2Rank")
    os.makedirs(af2rank_dir, exist_ok=True)
    filtered_pdb_dir = os.path.join(af2rank_dir, 'inputs/')
    os.makedirs(filtered_pdb_dir, exist_ok=True)
    os.makedirs(os.path.join(af2rank_dir, 'ver.AF/'), exist_ok=True)
    os.makedirs(os.path.join(af2rank_dir, 'ver.MULTIMER/'), exist_ok=True)
    
    link_files(data_dir, filtered_pdb_dir, filtered_results)
    change_chain_ids(filtered_pdb_dir, chain_list)
    
    subprocess.run(['python', '/home/casp16/run/TS.human/T2201/utils/change_PDB_idx_for_TM_revised.py', filtered_pdb_dir, filtered_pdb_dir])
    
    for filename in os.listdir(filtered_pdb_dir):
        if not filename.startswith('CHAIN_REVISED_'):
            os.remove(os.path.join(filtered_pdb_dir, filename))
            
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument("--base_dir", type=str, help="base dir to work (e.g./home/casp16/run/TS.human/T2201)")
    argparser.add_argument("--decoy_data_dir", type=str, help="downloaded directory with subdirs with decoy structures (e.g./home/casp16/run/TS.human/T2201/Massivefold.download/CASP16-CAPRI/T1201)")
    argparser.add_argument("--chain_list", type=str, help="chain list of decoys (e.g. A,B,C,D)")
    argparser.add_argument("--state", type=str, help="monomer or multimer")
    argparser.add_argument("--score_cutoff", type=float, default=0.8, help="A model will be discarded if its score is lower than TOP 1 score * this cutoff")
    argparser.add_argument("--num_cutoff", type=float, default=0.2, help="The ratio of AF2Rank candidates to all models will be less than this cutoff")
    args = argparser.parse_args()
    main(args)
    