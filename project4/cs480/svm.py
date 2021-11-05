import numpy as np
import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
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
  
  # print(train_data)
  # print(train_data.shape)
  # print("")
  # print(class_train_data)
  # print(class_train_data.shape)
  # print(validation_data.shape)
  # print(class_validation_data.shape)

  # split data for cross validation
  X_crosstrain, X_crosstest, y_crosstrain, y_crosstest = train_test_split(
      train_data, class_train_data, test_size=.33, random_state=42)



  # print('SVM modeling build starting...')
  # print('nonlinear c=3 gamma = .05 ')

  #validation
  # #model

  model = SVC(C=200, gamma=.1, kernel='rbf', verbose=2)
  model.fit(train_data, class_train_data)

  # #predict
  # y_pred = model.predict(validation_data)

  # #confusion matrix and accuracy

  # #accuracy
  # print("accuracy:", metrics.accuracy_score(
  #     y_true=class_validation_data, y_pred=y_pred), "\n")


  # testing
  y_pred = model.predict(test_data)

  # #accuracy
  print("accuracy:", metrics.accuracy_score(
      y_true=class_test_data, y_pred=y_pred), "\n")


if __name__ == '__main__':
    main()