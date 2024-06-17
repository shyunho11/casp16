# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with custom template 7NZM
### COLABFOLD SETTING
```python
--templates --custom-template-path 7nzm --num-seeds 10 --model-type alphafold2_multimer_v3
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold without any template
### COLABFOLD SETTING
```python
--num-seeds 10 --model-type alphafold2_multimer_v3
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with custom template 7NZM
### COLABFOLD SETTING
```python
--templates --custom-template-path 7nzm --num-seeds 10 --model-type alphafold2_multimer_v3
```
<br/>
<br/>

## model_4
### METHOD
    ColabFold with automatically searched from PDB
### COLABFOLD SETTING
```python
--templates --model-type alphafold2_multimer_v3
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with custom template 7NZM
### COLABFOLD SETTING
```python
--templates --custom-template-path 7nzm --num-seeds 10 --model-type alphafold2_multimer_v3
```
<br/>
<br/>
