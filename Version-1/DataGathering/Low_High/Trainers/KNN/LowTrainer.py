#this file includes info on converting irregular data
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
import pickle

path = '/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Low_High/Trainers/data.csv'
data = pd.read_csv(path,sep=';')
print(data.head())

#best = 4
neighbors = 4
#preprocessing.LabelEncoder() is the object that will automaticall convert string values to numbers
le = preprocessing.LabelEncoder()
print("Finished Preprocessing")
#can also be done with preprocessing.LabelEncoder().fit_transform()
data = data[['Ticker','Strength','Average_Low','Average_Volatility','Trend','Actual_Low']]
strength = data['Strength']
a_l = data['Average_Low']
a_v = data['Average_Volatility']
trend = data['Trend']
print("Converted data")

predict = "Actual_Low"

x = list(zip(strength,a_l,a_v,trend))
y = list(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

model = KNeighborsRegressor(n_neighbors=neighbors)

best = 0
for i in range(10000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.2)
    model = KNeighborsRegressor(n_neighbors=neighbors)
    model.fit(x_train,y_train)
        
    acc = model.score(x_test,y_test)
    print(acc)

    if acc > best:
        best = acc
        with open('pickles/LowData.pickle', 'wb') as f:
            pickle.dump(model,f)

print("---")
print(best)
predicted = model.predict(x_test)
for x in range(len(x_test)):
    print('Predicted: ', predicted[x], "Data: ", x_test[x], "Actual: ", y_test[x])
    
