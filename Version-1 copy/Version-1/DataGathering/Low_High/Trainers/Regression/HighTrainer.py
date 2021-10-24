import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style


#Importing Dataset of student's grades
path = '/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Low_High/Trainers/data.csv'
data = pd.read_csv(path,sep=';')
data = data[['Ticker','Strength','Average_High','Average_Volatility','Trend','Actual_High']]
print(data.head())
predict = 'Actual_High'


#Cutting 'Actual Low' (item we want to predict) out of dataset and storing into x (input)
x = np.array(data.drop([predict,'Ticker'], 1))
#Isolating 'Actual Low' (item we want to predict) and storing into y (output)
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.25)

if input('Run Sim?') != 'n':
    best = 0
    for i in range(10000):
        #Splitting x and y axis into the said variables randomly
        #If we used the same values for training and testing, the computer would simply memorize the dataset
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.25)
        linear = linear_model.LinearRegression()
        

        #This calculates the line of best fit using x_train and y_train
        linear.fit(x_train,y_train)

        #Scores the line of best fit calculated in the previous line
        #Scores using the x_test and y_test datasets
        acc = linear.score(x_test, y_test)
        print(acc)
        
        if acc > best:
            best = acc
            with open('pickles/HighData.pickle', "wb") as f:
                pickle.dump(linear,f)
    print("---")
    print(best)
pickle_in = open('pickles/HighData.pickle', "rb")
linear = pickle.load(pickle_in)

print("Co: \n", linear.coef_)
print("Intercept: \n", linear.intercept_)

#This uses the line of best fit to calculate the output of the values in x_test
predictions = linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

p = 'Trend'
style.use("ggplot")
pyplot.scatter(data[p],data['Actual_High'])
pyplot.xlabel(p)
pyplot.ylabel('Actual_High')
pyplot.show()
    


