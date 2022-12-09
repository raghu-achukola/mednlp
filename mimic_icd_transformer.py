import pandas as pd 
import json

def dic_agg(x):
    return {a:b for a,b in x}

with open('transformed_data/icd9_icd10_crosswalk.json','r') as f: 
    CROSSWALK = json.loads(f.read())

diag = pd.read_csv('DIAGNOSES_ICD.csv.gz')
diag['ICD10'] = diag['ICD9_CODE'].map(CROSSWALK)
mimic_diag = diag.dropna(subset = ['ICD10'])
mimic_diag['PAIR'] = mimic_diag.apply(lambda x: (x['SEQ_NUM'],x['ICD10']),axis=1)
agg_diag = mimic_diag.groupby('HADM_ID')[['HADM_ID','PAIR']].agg(dic_agg)
with open('transformed_data/mimic_aggregated_icd10.json','w') as f: 
    f.write(agg_diag.to_json(indent=2))
