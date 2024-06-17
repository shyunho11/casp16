import os
import re
import sys

def convert_blast_files(blast_out_dir, fasta_dir):
    os.makedirs(fasta_dir, exist_ok=True)
    
    for file in os.listdir(blast_out_dir):
        if file.endswith('.out'):
            blast_file_path = os.path.join(blast_out_dir, file)
            fasta_file_path = os.path.join(fasta_dir, file.replace('.out', '.fasta'))
            
            with open(blast_file_path, 'r') as blast_file, open(fasta_file_path, 'w') as fasta_file:
                for line in blast_file:
                    if line.startswith('#'):
                        continue  # Skip comment lines
                    columns = line.strip().split('\t')
                    if len(columns) >= 13:  # Ensure there are enough columns
                        seq_id = columns[1]  # ID
                        sequence = columns[12]  # sequence
                        # Clean the sequence ID
                        seq_id_clean = re.sub(r'\W+', '_', seq_id)
                        fasta_file.write(f'>{seq_id_clean}\n')
                        fasta_file.write(f'{sequence}\n')
            print(f'Converted {file} into {fasta_file_path}')
            
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python af3_to_pdb.py <BLAST .out directory> <output FASTA directory")
    else:
        convert_blast_files(sys.argv[1], sys.argv[2])