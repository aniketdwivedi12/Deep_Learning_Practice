# Artificial Neural Network

# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:12].values
y = dataset.iloc[:, 13].values

# Encoding Categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1= LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2= LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Import Keras lib and required packages
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
# Initialize Neural Network
classifier = Sequential()

#Adding initial layer and hidden layer with Dropout
classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
classifier.add(Dropout(rate=0.1))
#Adding second hidden layer
classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
classifier.add(Dropout(rate=0.1))
# Adding output layer
classifier.add(Dense(units= 1,kernel_initializer = 'uniform',activation='sigmoid'))

# Compiling the ANN
classifier.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])

# Fitting ANN to training set
classifier.fit(X_train,y_train,batch_size=10,epochs=100)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

#Evaluating the ANN
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score

def build_classifier():
    classifier = Sequential()
    classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
    classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
    classifier.add(Dense(units= 1,kernel_initializer = 'uniform',activation='sigmoid'))
    classifier.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])
    return classifier

classifier = KerasClassifier(build_fn=build_classifier, batch_size=10,epochs=100)
accuracies = cross_val_score(classifier, X= X_train, y=y_train, cv=10, n_jobs=-1)

mean = accuracies.mean()
variance = accuracies.std()

#Tuning the ANN
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

def build_classifier(optimizer):
    classifier = Sequential()
    classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
    classifier.add(Dense(units= 6,kernel_initializer = 'uniform',activation='relu'))
    classifier.add(Dense(units= 1,kernel_initializer = 'uniform',activation='sigmoid'))
    classifier.compile(optimizer=optimizer,loss='binary_crossentropy', metrics=['accuracy'])
    return classifier

classifier = KerasClassifier(build_fn=build_classifier)
parameters = {'batch_size':[25,32] ,
              'epochs':[100,500] ,
              'optimizer':['adam','rmsprop']}

grid_search = GridSearchCV(estimator= classifier,
                           param_grid = parameters,
                           scoring='accuracy',
                           cv = 10)
grid_search = grid_search.fit(X_train,y_train)
best_params = grid_search.best_params_
best_accuracy = grid_search.best_score_







