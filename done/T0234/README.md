# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All final models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    ColabFold with NCBI-Virus MSA (Extended recycles)
### COLABFOLD SETTING
```python
--num-seeds 2 --recycle-early-stop-tolerance 0.3 --num-recycle 40
```
### RANKING
```python
Human intuition
```
<br/>
<br/>

## model_2
### METHOD
    ColabFold with NCBI-Virus MSA (Extended recycles)
### COLABFOLD SETTING
```python
--num-seeds 2 --recycle-early-stop-tolerance 0.3 --num-recycle 40
```
### RANKING
```python
AF2Rank
```
<br/>
<br/>

## model_3
### METHOD
    ColabFold with NCBI-Virus MSA
### COLABFOLD SETTING
```python
--num-seeds 4 --recycle-early-stop-tolerance 0.3 --num-recycle 10
```
### RANKING
```python
pLDDT * pTM * ipTM
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
    