#this file includes info on converting irregular data
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
import pickle

path = '/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Open_Close/Trainers/data.csv'
data = pd.read_csv(path,sep=';')
print(data.head())

#best = 2
neighbors = 2
#preprocessing.LabelEncoder() is the object that will automaticall convert string values to numbers
le = preprocessing.LabelEncoder()
print("Finished Preprocessing")
#can also be done with preprocessing.LabelEncoder().fit_transform()
data = data[['Ticker','Strength','Trend','OC_Average','Actual_Increase']]
strength = data['Strength']
trend = data['Trend']
oc = data['OC_Average']
print("Converted data")

predict = "Actual_Increase"

x = list(zip(strength,trend,oc))
y = list(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

model = KNeighborsRegressor(n_neighbors=neighbors)

best = 0
for i in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.2)
    model = KNeighborsRegressor(n_neighbors=neighbors)
    model.fit(x_train,y_train)
        
    acc = model.score(x_test,y_test)
    print(acc)

    if acc > best:
        best = acc
        with open('data.pickle', 'wb') as f:
            pickle.dump(model,f)

print("---")
print(best)
predicted = model.predict(x_test)
for x in range(len(x_test)):
    print('Predicted: ', predicted[x], "Data: ", x_test[x], "Actual: ", y_test[x])
    
