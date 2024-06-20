# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with Ultimate MSA (symmetry: Yes)
### STOICHIOMETRY
    A2
### COLABFOLD SETTING
```python
--num-seeds 20 --model-type alphafold2_multimer_v3
```
### RANKING METHOD
```python
AF2Rank considering symmetry (This model was No.3 in AF2Rank result)
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
### RANKING METHOD
```python
AF2Rank without considering symmetry
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with Ultimate MSA
### STOICHIOMETRY
    A2
### RANKING METHOD
```python
AF2Rank without considering symmetry
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>
    