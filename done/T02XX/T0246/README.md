# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with UltimateMSA (Extended recycles)
### STOICHIOMETRY
    A2
### COLABFOLD SETTING
```python
--num-seeds 10 --model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.1 --num-recycle 40
```
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with UltimateMSA
### STOICHIOMETRY
    A2
### COLABFOLD SETTING
```python
--num-seeds 10 --model-type alphafold2_multimer_v3
```
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with UltimateMSA
### STOICHIOMETRY
    A4
### COLABFOLD SETTING
```python
--num-seeds 10 --model-type alphafold2_multimer_v3
```
### RANKING
```python
pLDDT * pTM * ipTM (This models is rank_001 among ColabFold results. it also has highest ipTM score.)
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld by PSK
### STOICHIOMETRY
    A2
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld by PSK
### STOICHIOMETRY
    A2
### RANKING
```python
AF2Rank
```
<br/>
<br/>
