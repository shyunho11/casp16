# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All final models are ranked by pLDDT * pTM * ipTM score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with NCBI Virus custom MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --num-recycle 40
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with NCBI Virus custom MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 4
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with NCBI Virus custom MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 4
```
### HHFILTER SETTING
```python
-id 90 -cov 50
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld (24.06.03) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld (24.06.03) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>
    