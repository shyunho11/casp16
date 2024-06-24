# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with HHblits-BFD MSA
### STOICHIOMETRY
    A3
### COLABFOLD SETTING
```python
--num-seeds 10 --recycle-early-stop-tolerance 0.3 --num-recycle 10
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
--num-seeds 10 --recycle-early-stop-tolerance 0.3 --num-recycle 10
```
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with HHblits-BFD MSA
### STOICHIOMETRY
    A4
### COLABFOLD SETTING
```python
--num-seeds 10 --recycle-early-stop-tolerance 0.3 --num-recycle 10
```
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld by PSK
### STOICHIOMETRY
    A1
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
    A1
### RANKING
```python
AF2Rank
```
<br/>
<br/>
