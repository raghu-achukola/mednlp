import numpy as np

# The idea is converting a regression output into a single class as if it were one hot encoded
# [0.25,0.65, 0.05, 0.03, 0.02] -> [0,1,0,0,0]
def argmax_to_one(y:np.array):
    y_hat_rf_max = np.zeros(y.shape)
    for i,doc in enumerate(y):
        y_hat_rf_max[i][np.argmax(doc)] = 1
    return y_hat_rf_max




# The idea is we want to be able to get a one-hot-encoded array [0,1,0,0,0]
# And a list of labels [A,B,C,D,E] and convert it into the actual label -> B
# By essentially taking the dot product. 
def text_dot_product(matrix:np.array,col_names:list):
    predictions = []
    for enc in matrix:
        pred = ''
        for doc,val  in zip(col_names, enc):
            pred += doc*int(val)
        predictions.append(pred)
    return predictions