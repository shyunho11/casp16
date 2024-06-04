******************** Preparing AF2Rank ********************
T2210 is a monomer
Using pTM as the custom score for T2210
----------------------------------------
Detected 8040 MassiveFold models
Excluded    0 models (w/ score cutoff 0.8)
Excluded 7638 models (w/ ratio cutoff 0.05)
Retained  402 models out of 8040 MassiveFold models
******************** Preparing ColabFold ********************
Using AF2Rank Composite score to select templates

■ RANK_BY_COMPOSITE.txt [ver.AF] (Threshold = 0.9)
○ Top 1 model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_99.pdb
Warning: Failed to find a unique model.

■ RANK_BY_COMPOSITE.txt [ver.MULTIMER] (Threshold = 0.9)
○ Top 1 model: CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_55.pdb
Warning: Failed to find a unique model.


Since we have only 2 unique models, adding 10 models based on AF2Rank score

■ RANK_BY_COMPOSITE.txt [ver.AF] (Threshold = None)
○ Top 1 model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_99.pdb
[91m○ Found next model: CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_82.pdb[0m
[91m○ Found next model: CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_24.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_75.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_104.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_176.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_40.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_49.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_178.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_dropout_noSM_woTemplates_model_5_ptm_pred_136.pdb[0m
[91m○ Found next model: CHAIN_REVISED_afm_basic_model_5_ptm_pred_74.pdb[0m

#############################################################
#                    FINAL MODEL SUMMARY                    #
#############################################################

[ColabFold templates]
● tmp1.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_55.pdb
● tmp2.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_99.pdb
----------------------------------------
[FAKER final models]
● FAKER_model_1.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_55.pdb
● FAKER_model_2.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_99.pdb
[91m● FAKER_model_3.pdb = CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_82.pdb (Not unique)[0m
[91m● FAKER_model_4.pdb = CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_24.pdb (Not unique)[0m
[91m● FAKER_model_5.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_75.pdb (Not unique)[0m
----------------------------------------
[For MiniWorld]
● forMiniWorld_model_1.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_55.pdb
● forMiniWorld_model_2.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_99.pdb
[91m● forMiniWorld_model_3.pdb = CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_82.pdb (Not unique)[0m
[91m● forMiniWorld_model_4.pdb = CHAIN_REVISED_cf_dropout_full_woTemplates_model_5_ptm_pred_24.pdb (Not unique)[0m
[91m● forMiniWorld_model_5.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_75.pdb (Not unique)[0m
[91m● forMiniWorld_model_6.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_104.pdb (Not unique)[0m
[91m● forMiniWorld_model_7.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_176.pdb (Not unique)[0m
[91m● forMiniWorld_model_8.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_40.pdb (Not unique)[0m
[91m● forMiniWorld_model_9.pdb = CHAIN_REVISED_afm_basic_model_5_ptm_pred_49.pdb (Not unique)[0m
[91m● forMiniWorld_model_10.pdb = CHAIN_REVISED_afm_woTemplates_model_5_ptm_pred_178.pdb (Not unique)[0m
