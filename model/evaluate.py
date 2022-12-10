import pandas as pd

def evaluate_single_prediction_accuracy(labeled_df:pd.DataFrame)-> float:
    labeled_df['DIAG'] = labeled_df['PAIR'].apply(lambda x: x[min(x.keys())])
    return (labeled_df['DIAG'] == labeled_df['PREDICTION']).mean()
def evaluate_in_the_list_accuracy(labeled_df:pd.DataFrame)-> float:
    labeled_df['DIAG'] = labeled_df['PAIR'].apply(lambda x: x.values())
    return (labeled_df.apply(lambda x: x['PREDICTION'] in x['DIAG'],axis=1 )).mean()
def print_accuracy_results(test_df:pd.DataFrame, predictions) -> tuple: 
    X_labeled = test_df.copy()
    X_labeled['PREDICTION'] = predictions
    spa =evaluate_single_prediction_accuracy(X_labeled)
    itla = evaluate_in_the_list_accuracy(X_labeled)
    print('ACCURACY: TOP_DIAGNOSIS:{:.2f}%, IN THE LIST: {:.2f}%'.format(spa*100,itla*100))