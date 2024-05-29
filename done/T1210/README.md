# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are scored by AF2Rank.
* model 1: best model among All experimental predictions
* model 2-3: best model among ColabFold with UltimateMSA predictions
* model 4-5: best model among MiniWorld prediction
* All models are submitted after **E minimization**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    colabfold with UltimateMSA (Colabfold DB + UniRef30 + BFD + BLAST tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 50
```
### HHFILTER SETTING
```python
hhfilter -i ultimate.a3m -o ultimate9050.a3m -id 90 -cov 50
```
<br/>
<br/>

## model_2
### METHOD
    colabfold with UltimateMSA (Colabfold DB + UniRef30 + BFD + BLAST tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 50
```
<br/>
<br/>

## model_3
### METHOD
    colabfold with UltimateMSA (Colabfold DB + UniRef30 + BFD + BLAST tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 50
```
### HHFILTER SETTING
```python
hhfilter -i ultimate.a3m -o ultimate9575.a3m -id 95 -cov 75
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