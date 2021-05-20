import time
import json
import math
import yfinance
from finviz.screener import Screener

print ("Initializing...")

patterns = [
  'ta_p_channel',
  'ta_p_doubletop',
  'ta_p_multipletop',
  'ta_p_doublebottom',
  'ta_p_multiplebottom',
  'ta_p_wedgeresistance',
  'ta_p_wedgesupport',
]

def FindTopStocks():
  print("Searching Stocks...")
  stocks = []
  for pattern in patterns:
    stocks_ = Screener(signal = pattern)
    for stock in stocks_[:20]:  
        stocks.append(stock['Ticker'])
  return stocks

def SortSystem(elem):
  return abs(elem[1])

#converts stock list to dictionary
def ConvertStockList(lst):
  stocks = []
  for item in lst:
    stock = {
      "Ticker" : item[0],
      "Rating" : float(item[1]),
      "Price" : float(item[2]),
      "Shares" : item[3]
      }
    stocks.append(stock)
  return stocks

def UpdateJson(obj):
  with open("json/StockStorage.json", 'w') as file:
    json.dump(obj, file)

#file is string of file path
#changes specific key in JSON file
def ChangeKey (key,file,mod):
  fileContent = json.loads(open(file).read())
  fileContent[key] = mod
  with open(file, "w") as f:
    json.dump(fileContent, f)

#file is string of file path
#converts json to python str
def ConvertJson(file):
  return json.loads(open(file).read())
  
