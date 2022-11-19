# for numerical computing
import numpy as np

# for dataframes
import pandas as pd


# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# to split train and test set
from sklearn.model_selection import train_test_split

# machine learning models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score

df=pd.read_csv('age1.csv')
print(df.shape)
print(df.columns)
print(df.head())
print(df.describe())
print(df.corr())
df = df.drop_duplicates()
print( df.shape )
print(df.isnull().sum())
df=df.dropna()
print(df.isnull().sum())

Gender = {'Male': 1,'Female': 2} 

df.Gender = [Gender[item] for item in df.Gender]

print(df.head())

y = df.Dataset

# create separate object for input features
X = df.drop('Dataset', axis=1)

# split X and y into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# print number of observation in X_train, X_test, y_train, and y_test
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

model1 = LogisticRegression()
model2 = RandomForestClassifier(n_estimators=500)

model4 = KNeighborsClassifier(n_neighbors=5)
model5 = DecisionTreeClassifier()
model6 = GaussianNB()


model1.fit(X_train, y_train)
model2.fit(X_train, y_train)

model4.fit(X_train, y_train)
model5.fit(X_train, y_train)
model6.fit(X_train, y_train)


# predict test set results
y_pred1 = model1.predict(X_test)
y_pred2 = model2.predict(X_test)

y_pred4 = model4.predict(X_test)
y_pred5 = model5.predict(X_test)
y_pred6 = model6.predict(X_test)



acc = accuracy_score(y_test, y_pred1, normalize=True) * float(100)  ## get the accuracy on testing data
print("Accuracy of Logistic Regression is {:.2f}%".format(acc))


acc = accuracy_score(y_test, y_pred2, normalize=True) * float(100)  ## get the accuracy on testing data
print("Accuracy of RandomForestClassifier is {:.2f}%".format(acc))


acc = accuracy_score(y_test, y_pred4, normalize=True) * float(100)  ## get the accuracy on testing data
print("Accuracy of KNeighborsClassifier is {:.2f}%".format(acc))


acc = accuracy_score(y_test, y_pred5, normalize=True) * float(100)  ## get the accuracy on testing data
print("Accuracy of Decision Tree is {:.2f}%".format(acc))


acc = accuracy_score(y_test, y_pred6, normalize=True) * float(100)  ## get the accuracy on testing data
print("Accuracy of GaussianNB is {:.2f}%".format(acc))



import joblib


# save the model as a pickle in a file
joblib.dump(model2, 'final_pickle_model.pkl')

# load the model from the file
final_model = joblib.load('final_pickle_model.pkl')

pred=final_model.predict(X_test)


acc = accuracy_score(y_test, pred, normalize=True) * float(100)  ## get the accuracy on testing data
print("Final Model Accuracy is {:.2f}%".format(acc))


















