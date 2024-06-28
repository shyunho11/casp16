# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All full-size models are ranked by ColabFold multimer score. (AF2Rank OOM Error)
* Predicted resi 1-500 seperately since ColabFold failed to make their structure in full-size modeling.
* Resi 1-500 models are ranked manually. (AF2Rank failed to select better structure)
* All final models are submitted after **Relaxation (further relax=True)**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    [FRONT] ColabFold resi 1-500 best model + [BACK] Human model 1 (=hum1)
### COLABFOLD SETTING: RESI 1-500 / ULIIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 2 --num-recycle 10 --model-type alphafold2_multimer_v3
```
### ALIGNING METHOD: PYMOL
```python
# remove all segment identifier from hum1.pdb first
load ultimate_A3_unrelaxed_alphafold2_multimer_v3_model_2_seed_000.pdb, part
load hum1.pdb, full
alter chain B and part, chain='X'
alter chain C and part, chain='B'
alter chain X and part, chain='C'
select r1, part and chain A and resi 450-500
select r2, full and chain A and resi 450-500
align r1, r2
select front, part and resi 1-469
select back, full and resi 470-1263
create merged, front or back
save merged.pdb, merged
```
<br/>
<br/>

## model_2
### METHOD
    [FRONT] ColabFold resi 1-500 best model + [BACK] ColabFold FULL SIZE best model
### COLABFOLD SETTING: FULL SIZE / ULTIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 1 --model-type alphafold2_multimer_v3
```
### COLABFOLD SETTING: RESI 1-500 / ULIIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 2 --num-recycle 10 --model-type alphafold2_multimer_v3
```
### ALIGNING METHOD: PYMOL
```python
load ultimate_A3_unrelaxed_alphafold2_multimer_v3_model_2_seed_000.pdb, part
load candidate_001_result_ult_human1temp_v3_rank_001_31.76.pdb, full
alter chain B and part, chain='X'
alter chain C and part, chain='B'
alter chain X and part, chain='C'
select r1, part and chain A and resi 450-500
select r2, full and chain A and resi 450-500
align r1, r2
select front, part and resi 1-427
select back, full and resi 428-1300
create merged, front or back
save merged.pdb, merged
```
<br/>
<br/>

## model_3
### METHOD
    [FRONT] ColabFold resi 1-500 best model + [MIDDLE] hum1 + [BACK] ColabFold FULL SIZE best model
### COLABFOLD SETTING: FULL SIZE / ULTIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 1 --model-type alphafold2_multimer_v3
```
### COLABFOLD SETTING: RESI 1-500 / ULIIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 2 --num-recycle 10 --model-type alphafold2_multimer_v3
```
### ALIGNING METHOD
```python
TMalign
```
<br/>
<br/>

## model_4
### METHOD
    [FRONT] ColabFold resi 1-500 best model + [BACK] hum1
### COLABFOLD SETTING: RESI 1-500 / ULIIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 2 --num-recycle 10 --model-type alphafold2_multimer_v3
```
### ALIGNING METHOD
```python
TMalign
```
<br/>
<br/>

## model_5
### METHOD
    ColabFold FULL SIZE best model
### COLABFOLD SETTING: FULL SIZE / ULTIMATE MSA
```python
--templates --custom-template-path hum1 --num-seeds 1 --model-type alphafold2_multimer_v3
```
### RANKING
```python
ColabFold multimer score
```
<br/>
<br/>
