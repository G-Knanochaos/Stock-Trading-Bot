import pickle
import numpy as np

manualInput = input('Input Manually?') == 'y'
if input('Predict Low or High (l/h)') == 'l':
    pickle_in = open("/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Trainers/Regression/pandas/LowData.pickle", 'rb')
else:
    pickle_in = open("/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Trainers/Regression/pandas/HighData.pickle", 'rb')
linear = pickle.load(pickle_in)

print('---')
average_low = input('average_low?')
average_volatility = input('average_volatility?')
trend = input('trend?')

x_test = np.array([[float(stock_rating), float(average_low), float(average_volatility), float(trend)]])
predictions = linear.predict(x_test)
print (predictions[0])
