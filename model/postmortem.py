

def failed_partial_success(df):
    result_df = df.copy()
    result_df['PRIMARY'] = result_df['PAIR'].apply(lambda x: x[min(x.keys())])
    result_df['DIAG_LIST'] = result_df['PAIR'].apply(lambda x: list(x.values()))
    result_df['PRIMARY_MATCH'] = result_df['PREDICTION']==result_df['PRIMARY']
    result_df['ONE_IN_LIST_MATCH'] = result_df.apply(lambda x: x['PREDICTION'] in x['DIAG_LIST'],axis=1)
    result_df['STATUS'] = result_df['PRIMARY_MATCH']
    result_df.loc[result_df['ONE_IN_LIST_MATCH'] & (~result_df['PRIMARY_MATCH']),'STATUS'] = 'PARTIAL'
    return result_df