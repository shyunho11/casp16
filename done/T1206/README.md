# COMMON INFO
* All processes are *automated* by Bash/Python script.
* All models are ranked by AF2Rank Composite score.
* All models are submitted after **Relaxation**.
<br/>
<br/>

# MODEL INFO
## model_1
### METHOD
    colabfold with Virus MSA0 (MSA iterative search by Minkyung Baek - Virus Ver.)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
<br/>
<br/>

## model_2
### METHOD
    colabfold with UltimateMSA (ColabFold DB + [UniRef30 + BFD + Vir70] + [BLAST + NCBI Virus])
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v2 --num-recycle 40
```
<br/>
<br/>

## model_3
### METHOD
    colabfold with Virus MSA0 (MSA iterative search by Minkyung Baek - Virus Ver.)
### COLABFOLD SETTING
```python
--model-type alphafold2_multimer_v3 --num-recycle 40
```
<br/>
<br/>

## model_4,5
### METHOD
    MiniWorld (24.05.20) by PSK
    Recycle : 40
    template : None
    Seed num : 1000
    First Scoring : by average pae * (1-average plddt) (lower is better) (1000 -> 5)
    Minimization : python "$str_relax_script" -pdb_fn "$pdb_file" -out_prefix "$out_prefix" -w_rst 0.1 -lddt_cut 60.0 -rst_CA_only -disulf_cutoff 1.0 -relax
    Second Scoring : AF2rank ptm version. (5 -> 2)

    MSA : '/home/casp16/run/TS.human/T0206/literature/T0206_dimer/T0206_Porcine_astrovirus_4_capsid_spike__Porcine_astrovirus_4__237_residues_.a3m'
    MSA depth : 1024
