import sys
import os
import pandas as pd

def process_rank_by_composite(directory):
    file_path = os.path.join(directory, 'RANK_BY_COMPOSITE.txt')
    
    # Check if RANK_BY_COMPOSITE.txt exists
    if not os.path.exists(file_path):
        print("Error: RANK_BY_COMPOSITE.txt does not exist in the given directory.")
        return
    
    # Read the content of RANK_BY_COMPOSITE.txt
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Get the basename of the directory
    basename = os.path.basename(os.path.normpath(directory))
    
    # Rename the files
    renamed_files = []
    for original_name in df['ID']:
        rank_number = original_name.split('_')[3]
        new_name = f"{basename}_rank_{rank_number}.pdb"
        renamed_files.append(new_name)
    
    # Add the renamed files to the DataFrame
    df['ID'] = renamed_files
    
    # Save the result to the current directory with the new filename format
    output_file_path = os.path.join(os.getcwd(), f'RANK_{basename}.txt')
    df.to_csv(output_file_path, sep='\t', index=False)
    
    print(f"Renamed file saved to {output_file_path}")

directory = sys.argv[1]
process_rank_by_composite(directory)
