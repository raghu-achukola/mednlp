from sklearn.feature_extraction.text import TfidfVectorizer

#Start - preprocess_tfidf
def preprocess_tfidf(doc_list, vec_params, keep_sparse =False):
    vec = TfidfVectorizer(**vec_params)
    doc_vec = vec.fit_transform(doc_list.values)
    return vec

# Train-Test -Split 
def train_test_split(df, train_pct, split_random_seed:int):
    df_shuffled = df.sample(len(df),random_state = split_random_seed)
    threshhold = int(len(df_shuffled)*train_pct)
    df_shuffled['Split'] = ''
    df_shuffled.iloc[:threshhold,-1] = 'TRAIN'
    df_shuffled.iloc[threshhold:,-1] = 'TEST'
    return df_shuffled

def preprocess_y(df_orig, diag_list, top_only = True, dummy = True):
    df = df_orig.copy()
    if top_only:
        #Changed after PAIR refactor (see above)
        fn = (lambda x: [x]) if  dummy else (lambda x: x)
        df['DIAGS'] = df['PAIR'].apply(lambda x: fn(x[min(x.keys())]) if x[min(x.keys())] in diag_list else '')
    else:
        df['DIAGS'] = df['PAIR'].apply(lambda x: list( set(x.values()).intersection(set(diag_list))))
    del df['PAIR']
    cols = list(set(df_orig.columns) - set(['PAIR']))
    if dummy:
        output =  df.set_index(cols).DIAGS.str.join('|').str.get_dummies()
        return output.reindex(output.columns.union(diag_list, sort=None), axis=1, fill_value=0)
    else:
        return  df.set_index(cols)

def first_diag(x:dict)-> str:
    return x[min(x.keys())]
