import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta
from utils import parse_stoichiometry

casp_round = 16

def get_target_info(entry_date=None, ignore_list=['rna', 'server']):
    target_list_url = f'https://predictioncenter.org/casp{casp_round}/targetlist.cgi'
    response = requests.get(target_list_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table), match='Tar-id', header=0)[4] # data is stored in 5-level nested table
    
    entry_date = entry_date if entry_date else (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    targets = df[df['Entry Date'] == entry_date]
    
    # ignore all targets belong to categories in skip list.
    if ignore_list:
        for keyword in ignore_list:
            targets = targets[~targets['Type'].str.contains(keyword, case=False)] # case insensitive
    
    # drop all subunits
    targets = targets[~targets['Tar-id'].str.contains('s', case=True)] # case sensitive
    
    # remove CAPRI target annotations
    targets['Tar-id'] = targets['Tar-id'].str.replace('[^a-zA-Z0-9]', '', regex=True)
    
    return targets

def save_subunits(target_id, sequences, save_fn='subunits.fasta'):
    save_path = os.path.join(target_id, save_fn)
    
    with open(save_path, 'w') as f:
        for i, sequence in enumerate(sequences):
            f.write(f'>subunit{i+1}\n')
            f.write(sequence)
            f.write('\n')
    
    print(f'Saved subunit sequences to\t{save_path}')
            
def save_target(target_id, sequences, stoichiometry, save_fn='target.fasta'):
    save_path = os.path.join(target_id, save_fn)
    
    counts = parse_stoichiometry(stoichiometry)
    max_count = max(count for _, count in counts)
    total_count = sum(count for _, count in counts)
    current_count = 0
    
    with open(save_path, 'w') as f:
        f.write(f'>{target_id}\n')
        
        for i in range(max_count):
            for subunit_id, count in counts:
                if i < count:
                    f.write(sequences[subunit_id])
                    current_count += 1
                    if current_count < total_count:
                        f.write(':')
        
    print(f'Saved target sequence to\t{save_path}')

def get_target_sequence(target_id, stoichiometry='A1'):
    print('-'*50)
    print(f'TARGET\t\t{target_id}')
    print(f'STOICHIOMETRY\t{stoichiometry}')
    
    target_url = f'https://predictioncenter.org/casp{casp_round}/target.cgi?target={target_id}&view=sequence'
    response = requests.get(target_url)
    response.raise_for_status()
    
    os.makedirs(target_id, exist_ok=True)
    
    # filter out all headers and blank strings
    sequences = [seq for seq in response.text.split('\n') if not seq.startswith('>') and seq]
    
    if stoichiometry == 'A1':
        save_target(target_id, sequences, stoichiometry)
    elif stoichiometry == 'UNK':
        save_subunits(target_id, sequences)
    else:
        save_subunits(target_id, sequences)
        save_target(target_id, sequences, stoichiometry)
        
        
if __name__ == "__main__":
    new_targets = get_target_info()
    for _, row in new_targets.iterrows():
        get_target_sequence(row['Tar-id'], row['Stoichiom.'].strip().replace(' ', ''))