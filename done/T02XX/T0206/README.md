# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by pLDDT * pTM * ipTM score first.
* Then, top 100 models are ranked by AF2Rank score.
* All models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    colabfold with Virus MSA0 (MSA iterative search by Minkyung Baek Virus Ver.)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
hhfilter -i t000_.1e-10.a3m -o T0206.virus.msa0.a3m -id 95 -cov 50
```
<br/>
<br/>

## model_2
### METHOD
    colabfold with Virus MSA0 (MSA iterative search by Minkyung Baek Virus Ver.)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
hhfilter -i t000_.1e-10.a3m -o T0206.virus.msa0.a3m -id 95 -cov 50
```
<br/>
<br/>

## model_3
### METHOD
    colabfold with Virus MSA0 (MSA iterative search by Minkyung Baek Virus Ver.)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
hhfilter -i t000_.1e-10.a3m -o T0206.virus.msa0.a3m -id 95 -cov 50
```
<br/>
<br/>

## model_4
### METHOD
    MiniWorld (24.05.20) by PSK
### Ranking Method
```python
AF2Rank
```
<br/>
<br/>

## model_5
### METHOD
    MiniWorld (24.05.20) by PSK
### Ranking Method
```python
AF2Rank
```
<br/>
<br/>
    