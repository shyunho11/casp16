# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are scored by AF2Rank.
* model 1: A model from human group (A2)
* model 2-3: best model among ColabFold with UltimateMSA predictions (A3)
* model 4-5: best model among MiniWorld prediction (A2)
* All models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### STOICHIOMETRY
    A2
### METHOD
    Human A2 prediction by Soohyeon Jo
<br/>
<br/>

## model_2
### STOICHIOMETRY
    A3
### METHOD
    ColabFold with UltimateMSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 40
```
### RANKING
```python
AF2Rank Composite Score Top 1
```
<br/>
<br/>

## model_3
### STOICHIOMETRY
    A3
### METHOD
    ColabFold with UltimateMSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 40
```
### RANKING
```python
AF2Rank Composite Score Top 2
```
<br/>
<br/>

## model_4,5
### METHOD
    MiniWorld by PSK
    Recycle : ?
    template : ?
    Seed num : ?
    First Scoring : ?
    Minimization : ?
    Second Scoring : ?
    MSA : ?
    MSA depth : ?