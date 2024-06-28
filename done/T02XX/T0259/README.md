# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with UltimateMSA (Extended recycle)
### STOICHIOMETRY
    A3
### COLABFOLD SETTING
```python
--templates --num-seeds 10 --model-type alphafold2_multimer_v2 --recycle-early-stop-tolerance 0.1 --num-recycle 40
```
### RANKING
```python
AF2Rank (This model ranked at 1st among all models)
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with UltimateMSA
### STOICHIOMETRY
    A3
### COLABFOLD SETTING
```python
--templates --num-seeds 10 --model-type alphafold2_multimer_v3
```
### RANKING
```python
AF2Rank (This model ranked at 1st among no extended recycler models)
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with UltimateMSA (no template)
### STOICHIOMETRY
    A3
### COLABFOLD SETTING
```python
--num-seeds 10 --model-type alphafold2_multimer_v3
```
### RANKING
```python
AF2Rank (This model ranked at 1st among no template models)
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld by PSK
### STOICHIOMETRY
    A3
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
    A3
### RANKING
```python
AF2Rank
```
<br/>
<br/>
