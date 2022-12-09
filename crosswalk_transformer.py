import pandas as pd 


def unique_icd_agg(codes,str_len):
    return set([x[:min(len(x),str_len)] for x in codes])
def min_exact_diag(x):
    if len(x['ICD10_7']) == 1:
        return list(x['ICD10_7'])[0]
    elif len(x['ICD10_6']) == 1:
        return list(x['ICD10_6'])[0]
    elif len(x['ICD10_5']) == 1:
        return list(x['ICD10_5'])[0]
    elif len(x['ICD10_4']) == 1:
        return list(x['ICD10_4'])[0]
    elif len(x['ICD10_3']) == 1:
        return list(x['ICD10_3'])[0]
    else:
        return None

def transform_crosswalk(input_file_path:str, output_file_path:str): 
    crosswalk = pd.read_csv('Data/icd9_icd10_crosswalk.csv')
    set_7 = crosswalk.groupby('icd9cm')['icd10cm'].agg( lambda x: unique_icd_agg(x,7))
    set_6 = crosswalk.groupby('icd9cm')['icd10cm'].agg( lambda x: unique_icd_agg(x,6))
    set_5 = crosswalk.groupby('icd9cm')['icd10cm'].agg( lambda x: unique_icd_agg(x,5))
    set_4 = crosswalk.groupby('icd9cm')['icd10cm'].agg( lambda x: unique_icd_agg(x,4))
    set_3 = crosswalk.groupby('icd9cm')['icd10cm'].agg( lambda x: unique_icd_agg(x,3))
            
    cwalk_cust = pd.DataFrame({'ICD10_3':set_3,'ICD10_4':set_4,'ICD10_5':set_5,'ICD10_6':set_6,'ICD10_7':set_7})
    cwalk_cust['Exact'] = cwalk_cust.apply(min_exact_diag,axis=1)

    final_cwalk = cwalk_cust['Exact']
    with open('transformed_data/icd9_icd10_crosswalk.json','w') as f:
        f.write(final_cwalk[cwalk_cust.apply(lambda x: x['Exact'] is not None,axis=1)].to_json())

if __name__ == '__main__':
    INPUT = 'Data/icd9_icd10_crosswalk.csv'
    OUTPUT = 'transformed_data/icd9_icd10_crosswalk.json'
    transform_crosswalk(INPUT,OUTPUT)