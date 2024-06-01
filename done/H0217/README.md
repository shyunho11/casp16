# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are scored by AF2Rank.
* model 1: best model among All experimental predictions
* model 2-3: best model among ColabFold with UltimateMSA predictions
* model 4-5: best model among MiniWorld prediction
* All models are submitted after **relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1,4,5
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
<br/>
<br/>

## model_2
### STOICHIOMETRY
    A2B2C2D2E2F2
### METHOD
    First, select AF3 best prediction with highest pTM*ipTM among 100 AF3 models
    Second, predict chain F using ColabFold with UltimateMSA (Colabfold DB + UniRef30 + BFD + BLAST env/tsa_nr + NCBI virus)
    Third, replace AF3 chain F with ColabFold chain F using TMalign
    Fourth, duplicate and align chain A,B,C,D,E,F using TMalign and PDB template 6ezo
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 40
```
### RANKING FOR CHAIN F
```python
AF2Rank Composite Score Top 1
```
<br/>
<br/>

## model_3
### STOICHIOMETRY
    A1B1C1D1E1F1
### METHOD
    Same with model_2 but skipped fourth step (different stoichiometry)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 40
```
### RANKING FOR CHAIN F
```python
AF2Rank Composite Score Top 1
```