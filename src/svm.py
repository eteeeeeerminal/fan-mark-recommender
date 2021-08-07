from sklearn import svm
from sklearn.metrics import accuracy_score

from sklearn_dataload import data_load

X_train, X_test, Y_train, Y_test = data_load()

clf = svm.SVC(gamma="scale")
clf.fit(X_train, Y_train)

Y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=Y_pred)
print(accuracy)