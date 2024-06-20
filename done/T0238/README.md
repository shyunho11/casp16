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
### STOICHIOMETRY
    A2
### COLABFOLD SETTING
```python
--num-seeds 20 --model-type alphafold2_multimer_v3
```
### RANKING
```python
AF2Rank considering symmetry (This model ranked 3rd in the AF2Rank results)
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with Ultimate MSA
### STOICHIOMETRY
    A2
### COLABFOLD SETTING
```python
--num-seeds 20 --model-type alphafold2_multimer_v3
```
### RANKING
```python
AF2Rank without considering symmetry (This model ranked 1st in the AF2Rank results)
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with Ultimate MSA
### STOICHIOMETRY
    A2
### RANKING
```python
AF2Rank without considering symmetry (This model ranked 2nd in the AF2Rank results)
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
    