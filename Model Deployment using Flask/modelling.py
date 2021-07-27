# note: labels = {'0':'setosa', '1':'versicolor', '2':'virginica'}
# ----------------------------------------------------------------

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# load data
features = load_iris().data
target = load_iris().target

# split data (training and validation)
X_train, X_val, y_train, y_val = train_test_split(features, target, test_size=0.2)

# training phase
model = SVC().fit(X_train, y_train)

# save model
if not os.path.exists('iris.pkl'):
    pickle.dump(model, open('iris.pkl', 'wb'))
    print('model saved!')


# print(model.predict([[1.2,2.3,3.4,4.5]]))