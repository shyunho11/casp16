# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All final models are ordered by AF2Rank score.
* All final models are submitted after **E minimization**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    colabfold with *unpaired* Ultimate MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --num-recycle 40
```
### RANKING
```python
pLDDT * pTM * ipTM (All) -> AF2Rank Composite Score (Top 50)
```
<br/>
<br/>

## model_2
### METHOD
    colabfold with *paired* Ultimate MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --num-recycle 40
```
### RANKING
```python
pLDDT * pTM * ipTM (All) -> AF2Rank Composite Score (Top 50)
```
<br/>
<br/>

## model_3
### METHOD
    colabfold with *unpaired* Ultimate MSA
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --num-recycle 40
```
### RANKING
```python
pLDDT * pTM * ipTM (All) -> AF2Rank Composite Score (Top 50)
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld (24.05.21) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld (24.05.21) by PSK
### RANKING
```python
AF2Rank
```
<br/>
<br/>
    