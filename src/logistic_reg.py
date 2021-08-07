import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from sklearn_dataload import data_load

X_train, X_test, Y_train, Y_test = data_load()

lr = LogisticRegression()
lr.fit(X_train, Y_train)

Y_pred = lr.predict(X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=Y_pred)
print(accuracy)