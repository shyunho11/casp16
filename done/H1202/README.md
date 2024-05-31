# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank score.
* All models are submitted after **relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    colabfold with UltimateMSA(MMseqs2 v14.7e284, HHblits v3.3.0 on UniRef30 + BFD, PSI-BLAST on tsa_nr) id95cov75
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
hhfilter -i input.fasta -o output.fasta -id 95 -cov 75
```
<br/>
<br/>

## model_2
### METHOD
    colabfold with UltimateMSA(MMseqs2 v14.7e284, HHblits v3.3.0 on UniRef30 + BFD, PSI-BLAST on tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
None
```
<br/>
<br/>

## model_3
### METHOD
    colabfold with UltimateMSA(MMseqs2 v14.7e284, HHblits v3.3.0 on UniRef30 + BFD, PSI-BLAST on tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
hhfilter -i input.fasta -o output.fasta -id 95 -cov 75
```
<br/>
<br/>

## model_4
### METHOD
    colabfold with UltimateMSA(MMseqs2 v14.7e284, HHblits v3.3.0 on UniRef30 + BFD, PSI-BLAST on tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
None
```
<br/>
<br/>

## model_5
### METHOD
    colabfold with UltimateMSA(MMseqs2 v14.7e284, HHblits v3.3.0 on UniRef30 + BFD, PSI-BLAST on tsa_nr)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
### HHFILTER SETTING
```python
None
```
<br/>
<br/>
    