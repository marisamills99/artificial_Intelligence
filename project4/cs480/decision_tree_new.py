import numpy as np
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# from sklearn import metrics
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
import pandas as pd

def main():

  #get the test, train and validation data, sort out into needed dataframes, then convert to np arrays

  test_data = pd.read_csv('leaf/test_data.csv')
  class_test_data = test_data['class']
  test_data = test_data.drop(columns=['class'])
  test_data = test_data.to_numpy()
  class_test_data = class_test_data.to_numpy()

  train_data = pd.read_csv('leaf/train_data.csv')
  class_train_data = train_data['class']
  train_data = train_data.drop(columns=['class'])
  train_data = train_data.to_numpy()
  class_train_data = class_train_data.to_numpy()
  class_train_data.flatten()

  validation_data = pd.read_csv('leaf/validation_data.csv')
  class_validation_data = validation_data['class']
  validation_data = validation_data.drop(columns=['class'])
  validation_data = validation_data.to_numpy()
  class_validation_data = class_validation_data.to_numpy()
  #validation_data.flatten()
  class_validation_data.flatten()

  #--------print statments used for testing
  #print(test_data.shape)
  # print(train_data)
  # print(train_data.shape)
  # print("")
  # print(class_train_data)
  # print(class_train_data.shape)
  # print(validation_data.shape)
  # print(class_validation_data.shape)

  # create different tree models using different hyper paramaters, then take best model and use testing data

  #------------model 1-------------------
  # default paramaters
  clf1 = DecisionTreeClassifier(random_state=0)
  cross_val_score(clf1, train_data, class_train_data, cv=10)
  clf1 = clf1.fit(train_data, class_train_data)
  # print("model 1")
  y_pred = clf1.predict(validation_data)
  # #accuracy
  print("accuracy:", metrics.accuracy_score(
      y_true=class_validation_data, y_pred=y_pred), "\n")
  print("")


  #------------model 2-------------
  # paramaeters changed {set criterion -> entropy, splitter -> random, max_features -> auto}
  clf2 = DecisionTreeClassifier(random_state=0, criterion = "entropy", splitter = "random", max_features = "auto")
  clf2 = clf2.fit(train_data, class_train_data)
  cross_val_score(clf2, train_data, class_train_data, cv=10)
  print("model 2")
  y_pred = clf2.predict(validation_data)
  # #accuracy
  print("accuracy:", metrics.accuracy_score(
      y_true=class_validation_data, y_pred=y_pred), "\n")
  print("")


  #-----------model 3-------------
  # paramaters changed {max_depth -> 14, max_features -> log2, class_weight -> balanced}
  clf3 = DecisionTreeClassifier(random_state=0, max_depth = 14, max_features = "log2", class_weight = "balanced")
  clf3 = clf3.fit(train_data, class_train_data)
  cross_val_score(clf3, train_data, class_train_data, cv=10)
  print("model 3")
  y_pred = clf3.predict(validation_data)
  #accuracy
  print("accuracy:",metrics.accuracy_score(
    y_true = class_validation_data, y_pred=y_pred),"\n")
  print("")
  
  #----------------test------------------
  # using model 3, since there is less overfitting in that model.  replace validation data with test data to run test
  y_pred = clf3.predict(test_data)
  # #accuracy
  print("test using model 3")
  print("accuracy:", metrics.accuracy_score(
      y_true=class_test_data, y_pred=y_pred), "\n")



if __name__ == '__main__':
    main()
