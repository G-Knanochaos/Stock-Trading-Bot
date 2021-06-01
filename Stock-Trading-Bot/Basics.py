import time
import json
import math
import yfinance
from finviz.screener import Screener
from stockVal import get_current_price
from stockVal import findStockValuation

print ("Initializing...")

patterns = [
  'ta_p_channel'
]

def FindTopStocks():
  print("Searching Stocks...")
  stocks = []
  for pattern in patterns:
    stocks_ = Screener(signal = pattern)
    for stock in stocks_:  
        stocks.append(stock['Ticker'])
  return stocks

def SortSystem(elem):
  return abs(elem[1])

def StockCleaning(portfolio):
  stocks = []
  clean = []
  for position in portfolio:
    stocks.append((position.symbol,int(position.qty),position.side))
  for stock in stocks:
    if findStockValuation(stock[0]) == (0,0,0):
      clean.append(stock)
  return clean

def findStockList():
  Stocks = []
  Stocks = [[x] for x in FindTopStocks()]

  print("Analyzing Stocks...")
  print("---")
  print(Stocks)
  for stock in Stocks:
    for thing in findStockValuation(stock[0]):
      stock.append(thing)

  print("---")
  print("Filtering Stocks...")
  Stocks = list(filter(lambda x: x[1] != 0, Stocks))
  Stocks.sort(key = SortSystem, reverse = True)
  return Stocks

def stockCalc(buying_power,date):
  FullStocks = findStockList()
  Stocks = FullStocks[:10]
  TotalRating = 0
  stockp = 0
  for stock in Stocks:
    stock.append(get_current_price(yfinance.Ticker(stock[0])))
    TotalRating += abs(stock[1])
  for stock in Stocks:
      FindStockShares(stock, TotalRating, buying_power)
  UpdateJson(ConvertStockList(Stocks))
  ChangeKey("Date","/Users/oceanhawk/Documents/Python/Stock-Trading-Bot/json/Var.json",date)
  return Stocks

def FindStockShares(stock, TotalRating, buying_power):
  stockp = float(stock[1]*(100/TotalRating)/100)
  print(stockp)
  total = stockp*buying_power
  totalspending = total/stock[4]
  stock.append(math.floor(totalspending))
  stock.append(round(total,2)) 

#converts stock list to dictionary
def ConvertStockList(lst):
  stocks = []
  for item in lst:
    stock = {
      "Ticker" : item[0],
      "Rating" : float(item[1]),
      "Resistance" : (item[2]),
      "Support" : item[3],
      "Price" : float(item[4]),
      "Shares" : item[5],
      "Total Spent" : item[6]
      }
    stocks.append(stock)
  return stocks

def UpdateJson(obj):
  with open("/Users/oceanhawk/Documents/Python/Stock-Trading-Bot/json/StockStorage.json", 'w') as file:
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
  
