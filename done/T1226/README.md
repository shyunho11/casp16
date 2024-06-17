# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with Ultimate MSA
### COLABFOLD SETTING
```python
--num-seeds 50 --model-type alphafold2_multimer_v3
```
### HHFILTER SETTING
```python
-id 90 -cov 50
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with NCBI Virus custom MSA
### COLABFOLD SETTING
```python
--num-seeds 50 --model-type alphafold2_multimer_v3
```
### HHFILTER SETTING
```python
-id 90 -cov 50
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with UltimateMSA
### COLABFOLD SETTING
```python
--num-seeds 50 --model-type alphafold2_multimer_v3
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld (24.06.05) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld (24.06.05) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>
    