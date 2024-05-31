import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

casp_round = 16
casp_path = "/home/casp16/run/TS.human"

def parse_stoichiometry(stoichiometry):
    matches = re.findall(r'([A-Z])(\d+)', stoichiometry)
    return [(ord(letter)-65, int(count)) for letter, count in matches]

def get_target_sequence(target_id):
    target_url = f'https://predictioncenter.org/casp{casp_round}/target.cgi?target={target_id}&view=sequence'
    response = requests.get(target_url)
    response.raise_for_status()
    
    # filter out all headers and blank strings
    sequences = [seq for seq in response.text.split('\n') if not seq.startswith('>') and seq]
    return sequences
        
# This function requires 'pip install lxml'
def get_target_table():
    target_list_url = f'https://predictioncenter.org/casp{casp_round}/targetlist.cgi'
    response = requests.get(target_list_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    table_df = pd.read_html(str(table), match='Tar-id', header=0)[4] # data is stored in 5-level nested table
    
    return table_df
    
def get_target_by_date(entry_date, ignore_list=['nuca', 'server', 'ligand']):
    table_df = get_target_table()
    targets = table_df[table_df['Entry Date'] == entry_date]
    
    # ignore all targets belong to categories in skip list.
    if ignore_list:
        for keyword in ignore_list:
            targets = targets[~targets['Type'].str.contains(keyword, case=False)] # case insensitive
    
    # drop all subunits
    targets = targets[~targets['Tar-id'].str.contains('s', case=True)] # case sensitive
    
    # remove CAPRI target annotations
    targets['Tar-id'] = targets['Tar-id'].str.replace('[^a-zA-Z0-9]', '', regex=True)
    
    # In case stoichiometry is too long
    targets['Stoichiom.'] = targets['Stoichiom.'].str.strip().replace(' ', '')
    
    return targets

def get_target_by_id(target_id):
    table_df = get_target_table()
    
    # remove CAPRI target annotations
    table_df['Tar-id'] = table_df['Tar-id'].str.replace('[^a-zA-Z0-9]', '', regex=True)
    
    # In case stoichiometry is too long
    table_df['Stoichiom.'] = table_df['Stoichiom.'].str.strip().replace(' ', '')
    
    targets = table_df[table_df['Tar-id'] == target_id]
    
    if len(targets) != 1:
        print(f'{len(targets)} entry(ies) found. Check if your target ID [{target_id}] is correct.')
    else:
        target = targets.iloc[0].squeeze() # convert to Series
        return target

def save_subunits(target_id, sequences, save_fn='subunits.fasta'):
    save_path = os.path.join(casp_path, target_id, save_fn)
    
    with open(save_path, 'w') as f:
        for i, sequence in enumerate(sequences):
            f.write(f'>subunit{i+1}\n')
            f.write(sequence)
            f.write('\n')
    
    print(f'Saved subunit sequences to\t{save_path}')
            
def save_target(target_id, sequences, stoichiometry, save_fn='target.fasta'):
    save_path = os.path.join(casp_path, target_id, save_fn)
    
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

def save_target_template(target_id, save_fn='submit_template.txt'):
    target_url = f'https://predictioncenter.org/casp{casp_round}/target.cgi?target={target_id}&view=template'
    response = requests.get(target_url)
    response.raise_for_status()
    
    save_path = os.path.join(casp_path, target_id, save_fn)
    with open(save_path, 'w') as f:
        f.write(response.text)
        
    print(f'Saved submission template to\t{save_path}')
    
def save_target_files(target_id, stoichiometry='A1'):
    print('-'*50)
    print(f'TARGET\t\t{target_id}')
    print(f'STOICHIOMETRY\t{stoichiometry}')
    os.makedirs(os.path.join(casp_path, target_id), exist_ok=True)
    
    sequences = get_target_sequence(target_id)
    
    if stoichiometry == 'A1':
        save_target(target_id, sequences, stoichiometry)
    elif stoichiometry == 'UNK':
        save_subunits(target_id, sequences)
    else:
        save_subunits(target_id, sequences)
        save_target(target_id, sequences, stoichiometry)
        
        
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        try:
            save_target_files(sys.argv[1], sys.argv[2])
        except:
            print('Usage: python web.py <TARGET ID> <STOICHIOMETRY>')
            sys.exit(1)
    else:
        from datetime import date, timedelta
        
        today = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        new_targets = get_target_by_date(today)
        for _, row in new_targets.iterrows():
            save_target_files(row['Tar-id'], row['Stoichiom.'])