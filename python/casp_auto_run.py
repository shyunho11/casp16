import os
from datetime import date, timedelta
from casp.web import get_target_by_date, get_target_by_id, save_target_files

today = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
new_targets = get_target_by_date(today)

for index, row in new_targets.iterrows():
    target_id = row['Tar-id']
    stoichiom = row['Stoichiom.']
    
    if target_id[1] == '2':
        print(f'Running Phase 2 for {target_id}')
        os.system(f'sbatch /home/iu/casp16/scripts/phase2_auto_run.sh {target_id}')
    
    elif target_id[1] == '1':
        phase0_target_id = target_id[0] + '0' + target_id[2:]
        
        if get_target_by_id(phase0_target_id) is None:
            print(f'Running Phase 1 for {target_id}')
            save_target_files(target_id, stoichiom)
            os.chmod(f'/home/casp16/run/TS.human/{target_id}', 0o775)
            
        else:
            print(f'Skipping {target_id} since Phase 0 target {phase0_target_id} already exists.')
    
    else:
        print(f'Running Phase 0 for {target_id}')
        save_target_files(target_id, stoichiom)
        os.chmod(f'/home/casp16/run/TS.human/{target_id}', 0o775)
        