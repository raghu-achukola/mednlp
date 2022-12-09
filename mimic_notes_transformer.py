import pandas as pd
import re

IMPORTANT_NOTES = ['DISCHARGE DIAGNOSIS','HISTORY OF PRESENT ILLNESS','DISCHARGE DIAGNOSIS:\nPRIMARY']
def sanitize_note(x):
    return re.sub(r"\[\*{2}.*\*{2}\]","",x).replace('\n',' ')

def clean_notes_df(df:pd.DataFrame) -> pd.DataFrame:
    note_events = df[['HADM_ID','CATEGORY','TEXT']]
    discharge_notes = note_events[note_events['CATEGORY']=='Discharge summary']
    discharge_counts = discharge_notes.groupby('HADM_ID')['CATEGORY'].count()
    single_discharge = discharge_counts[discharge_counts!=1]
    sdn = discharge_notes[discharge_notes.apply(lambda x: x['HADM_ID'] not in list(single_discharge.index),axis = 1)]

    sdn['TEXT_DICT'] = sdn['TEXT'].apply(lambda x: 
                                {
                                    k.strip('\n').upper():v for k,v in 
                                    [re.search(re.compile("(.*)\:\s*(.*)",re.DOTALL),d).groups(1) for d in x.split('\n\n') if  re.search(r".*\:\s*(.*)",d) ]
                                }       | 
                                                                    {
                                    k.strip('\n').upper():v for k,v in 
                                    [re.search(re.compile("(.*)\:\n(.*)",re.DOTALL),d).groups(1) for d in x.split('\n\n') if  re.search(r".*\:\n(.*)",d) ]
                                }
                                )
    sdn['IMPORTANT_NOTES'] = sdn['TEXT_DICT'].apply(lambda x: {k:sanitize_note(v).strip() for k,v in x.items() if k in IMPORTANT_NOTES})
    sdn['HISTORY'] = sdn['IMPORTANT_NOTES'].apply(lambda x: x.get('HISTORY OF PRESENT ILLNESS',''))
    sdn['DISCHARGE_PRIMARY'] = sdn['IMPORTANT_NOTES'].apply(lambda x: x.get('DISCHARGE DIAGNOSIS:\nPRIMARY',''))

    sdn['DISCHARGE'] = sdn['IMPORTANT_NOTES'].apply(lambda x: x.get('DISCHARGE DIAGNOSIS',''))
    notes_cleaned = sdn[['HADM_ID','HISTORY','DISCHARGE_PRIMARY','DISCHARGE']]
    return notes_cleaned.dropna(how = 'all')

if __name__ == '__main__':
    df = pd.read_csv('NOTEEVENTS.csv.gz')
    notes_cleaned = clean_notes_df(df)
    notes_cleaned.to_csv('transformed_data/notes_cleaned.csv')
