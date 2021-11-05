import numpy as np
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn import metrics

# from sklearn import metrics
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
import pandas as pd


def main():

  #get the test, train and validation data, sort out into needed dataframes, then convert to np arrays

  test_data = pd.read_csv('auto_mpg/test_data.csv')
  class_test_data = test_data['mpg']
  test_data = test_data.drop(columns=['mpg'])
  test_data = test_data.to_numpy()
  class_test_data = class_test_data.to_numpy()

  train_data = pd.read_csv('auto_mpg/train_data.csv')
  class_train_data = train_data['mpg']
  train_data = train_data.drop(columns=['mpg'])
  train_data = train_data.to_numpy()
  class_train_data = class_train_data.to_numpy()
  class_train_data.flatten()

  validation_data = pd.read_csv('auto_mpg/validation_data.csv')
  class_validation_data = validation_data['mpg']
  validation_data = validation_data.drop(columns=['mpg'])
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

  #make training tree and validate

  # #model 1
  # clf = DecisionTreeClassifier(random_state=0)
  # cross_val_score(clf, train_data, class_train_data, cv=10)
  # clf = clf.fit(train_data, class_train_data)

  #model 2
  clf = DecisionTreeClassifier(random_state=0)
  clf = clf.fit(train_data, class_train_data)
  cross_val_score(clf, train_data, class_train_data, cv=10)

regression_model = LinearRegression()
regression_model.fit(train_data, class_train_data)
intercept = regression_model.intercept_[0]

print("The intercept for our model is {}".format(intercept))
regression_model.score(test_data, class_test_data)
#test data
#classtestdata
  y_pred = clf.predict(validation_data)
  # #accuracy
  print("accuracy:", metrics.accuracy_score(
      y_true=class_validation_data, y_pred=y_pred), "\n")


if __name__ == '__main__':
    main()
