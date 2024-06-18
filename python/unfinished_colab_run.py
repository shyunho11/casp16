import os
import sys
import pandas as pd
from datetime import datetime

if len(sys.argv) != 2:
    ('Usage: python unfinished_colab_run.py <Unfinished ColabFold run path>')
    sys.exit(1)
    
run_path = sys.argv[1]
log_file = os.path.join(run_path, 'log.txt')

models = []
plddts = []
ptms = []
iptms = []
isMultimer = False

with open(log_file, 'r') as f:
    lines = f.readlines()
    
if 'Done' in lines[-1]:
    raise Exception('This ColabFold run has been finished properly. [No need to process]')
    
query = [line.split()[4] for line in lines if 'Query' in line]
print(f'Found query: {query}')

if len(query) != 1:
    raise Exception(f'This script can handle 1 query only (Found {query_N} queries [Failed to process])')

# Iterate over the lines to find and extract model information
for i in range(len(lines)):
    if "took" in lines[i]:
        model_end = lines[i]
        last_cycle = lines[i-1]

        # Extract model information
        model_info = model_end.split(' ')[2]
        models.append(model_info)

        # Extract final values
        plddt = float(last_cycle.split('pLDDT=')[1].split(' ')[0])
        ptm = float(last_cycle.split('pTM=')[1].split(' ')[0])
        iptm = float(last_cycle.split('ipTM=')[1].split(' ')[0]) if 'ipTM=' in last_cycle else 0

        plddts.append(plddt)
        ptms.append(ptm)
        iptms.append(iptm)

df = pd.DataFrame({
    'model': models,
    'plddt': plddts,
    'ptm': ptms,
    'iptm': iptms
})

# Check if ipTM value exists
if max(iptms) > 0:
    isMultimer = True
    df['multimer'] = 0.8 * df['iptm'] + 0.2 * df['ptm']

# Print data before reranking
print(df)

with open(log_file, 'a') as f:
    ranking_metric = 'multimer' if isMultimer else 'plddt'
    print(f"reranking models by '{ranking_metric}' metric")
    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    f.write(f"{time} reranking models by '{ranking_metric}' metric\n")
    
    df_sorted = df.sort_values(by=ranking_metric, ascending=False).reset_index(drop=True)
    print(df_sorted)
    
    for index, row in df_sorted.iterrows():
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        f.write(f"{time} rank_{index+1:03d}_{row['model']} pLDDT={row['plddt']} pTM={row['ptm']}")
        f.write(f" ipTM={row['iptm']}\n" if isMultimer else "\n")
        
        pdb_file = os.path.join(run_path, f"{query[0]}_unrelaxed_{row['model']}.pdb")
        new_pdb_file = os.path.join(run_path, f"{query[0]}_unrelaxed_rank_{index+1:03d}_{row['model']}.pdb")
        
        if os.path.isfile(pdb_file):
            os.rename(pdb_file, new_pdb_file)
            print(f'File renamed as {new_pdb_file}')
            