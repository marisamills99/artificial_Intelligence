# implements ordinal regression with all paramaters and no resampling

#source:
# ordinal regression found at https://pythonhosted.org/mord/
# The Mord website requested that this thesis be cited if the package was used, as such I am citing it here in my code
#   Fabian Pedregosa-Izquierdo. Feature extraction and supervised learning on fMRI: from practice to theory. PhD thesis.
#   https://rikunert.com/ordinal_rating
# https://rikunert.com/ordinal_rating

import numpy as np
import pandas as pd
from mord import LogisticAT
from sklearn.metrics import accuracy_score
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score

# make sure the df to nparray conversion does not change data
np.set_printoptions(suppress = True)


def main():
    #where the processing of data is taken care of.  Models are called via methods
    dataLocation = input("Enter the directory where the data is (including the data name): ")
    df = pd.read_csv(dataLocation)

    # make column to indicate if player was in top 10
    df['In Top 10'] = df['Top 10'].apply(lambda x: 1 if x>0 and x <=10 else 0)

    # clean up values so there are no null spaces
    df['Top 10'].fillna(0, inplace=True)
    df['Top 10'] = df['Top 10'].astype(int)

    df['Rounds'].fillna(0, inplace=True)
    df['Rounds'] = df['Rounds'].astype(int)

    df['Points'].fillna('0', inplace = True)
    df['Points'] = df['Points'].astype(str)

    df['Money'].fillna('$0.00', inplace = True)
    df['Money'] = df['Money'].astype(str)

    df['Wins'].fillna(0, inplace = True)
    df['Wins'] = df['Wins'].astype(int)

    df.fillna(0, inplace = True)


    # remove ',' from points and change their type to int
    df['Points'] = df['Points'].apply(lambda x: x.replace(',',''))
    df['Points'] = df['Points'].astype(int)

    # remove '$' and ',' from money and change type to float
    df['Money'] = df['Money'].apply(lambda x: x.replace('$',''))
    df['Money'] = df['Money'].apply(lambda x: x.replace(',',''))
    df['Money'] = df['Money'].astype(float)

    # create a data set of just the rankings and get rid of any places >10
    df = df[df['Top 10'] <= 10]
    inTop10Df = df[['In Top 10']]

    # drop data points that won't affect predictions.
    df = df.drop(['Player Name', 'Year', 'Top 10', 'In Top 10'], axis=1)

    # make panda's data frame into a numpy array.  Flatten the ranking Data to make the lables easier to read
    golfData = np.array(df)
    inTop10Data = np.array(inTop10Df).flatten()
    # print(golfData)        #used for testing
    # print(inTop10Data)     #used for testing


    # do ordinal regression here
    def acc_fun(target_true, target_fit):
        #helper method used to help calculate the accuracy score
        target_fit = np.round(target_fit)
        target_fit.astype('int')
        return accuracy_score(target_true, target_fit)

    #create model
    MAE = make_scorer(mean_absolute_error)
    model_ordinal = LogisticAT(alpha=0)

    #20 fold cross validation to get mean error
    MAE_ordinal = cross_val_score(model_ordinal, golfData, inTop10Data, cv = 20, scoring=MAE)
    # acc as method to get the accuracy score
    acc = make_scorer(acc_fun)

    print('Ordered Logistic Regression mean error: ', np.mean(MAE_ordinal))

    # 20 fold cross validation to get accuracy
    acc_ordinal = cross_val_score(model_ordinal, golfData, inTop10Data, cv=20, scoring = acc)

    print('Ordered logistic regression accuracy: ', np.mean(acc_ordinal))


if __name__ == '__main__':
    # runs main() function
    main()
