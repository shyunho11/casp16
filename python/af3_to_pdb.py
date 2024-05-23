import sys
import json
import re
from Bio.PDB import MMCIFParser, PDBIO

def mmcif_to_structure(mmcif_file):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('structure', mmcif_file)
    return structure

def add_bfactor_plddt(structure, data_json_file):
    with open(data_json_file, 'r') as file:
        plddt_data = json.load(file)
        
    plddt_scores = plddt_data["atom_plddts"]
    
    score_index = 0
    
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    if score_index < len(plddt_scores):
                        atom.bfactor = plddt_scores[score_index]
                        score_index += 1
                    else:
                        print("Warning: Not enough pLDDT scores to cover all atoms.")
                        return

def extract_iptm_ptm(summary_json_file):
    with open(summary_json_file, 'r') as file:
        data = json.load(file)
        
    iptm = data.get("iptm", None)
    ptm = data.get("ptm", None)
    
    return iptm, ptm

def structure_to_pdb(structure, output_file):
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_file)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python af3_to_pdb.py <input MMCIF file>")
    else:
        mmcif_file = sys.argv[1]
        match = re.match(r'fold_(.+?)_model_(\d+)\.cif', mmcif_file)
        
        if match:
            name = match.group(1)
            rank = match.group(2)
        else:
            raise ValueError("Input filename does not match the expected pattern: fold_{NAME}_model_{N}.cif")
        
        structure = mmcif_to_structure(mmcif_file)
        add_bfactor_plddt(structure, f"fold_{name}_full_data_{rank}.json")
        iptm, ptm = extract_iptm_ptm(f"fold_{name}_summary_confidences_{rank}.json")

        iptm_str = f"_ipTM{iptm:.2f}" if iptm is not None else ""
        ptm_str = f"_pTM{ptm:.2f}" if ptm is not None else ""
        output_file = f"af3_{name}_rank{rank}{iptm_str}{ptm_str}.pdb"
        
        structure_to_pdb(structure, output_file)
        