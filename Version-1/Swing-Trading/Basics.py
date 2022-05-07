import json
import math
from finviz.screener import Screener
from config import api
from stockVal import get_current_price
from stockVal import findStockValuation

directory = __file__[:-9]

print("Initializing...")

patterns = [
  'ta_p_channel'
]

def FindTopStocks(b):
  BLACKLIST = ['UPV','FDM','IBTB','SGOV']+b
  def blackFN (obj):
    for black in BLACKLIST:
      if obj == black:
        return False
    return True

  print("Searching Stocks...")
  stocks = []
  for pattern in patterns:
    stocks_ = Screener(signal = pattern)
    for stock in stocks_:  
        stocks.append(stock['Ticker'])
  stocks = list(filter(blackFN,stocks))
  return stocks

def SortSystem(elem):
  return abs(elem[1])

def stockAnal(tickers):
  Stocks = []
  for stock in tickers:
    valuation = findStockValuation(stock[0])
    if valuation != None:
      stock.extend(valuation)
      Stocks.append(stock)
  return Stocks
      
def stockCalc(top_stocks,buying_power,date):
  print("Analyzing Stocks...")
  print("---")
  Stocks = stockAnal(top_stocks)
  print("---")
  print("Filtering Stocks...")
  Stocks = [stock for stock in Stocks if (api.get_asset(stock[0]).tradable)]
  Stocks.sort(key = lambda stock: abs(stock[1]), reverse = True)
  tradable_stocks = []
  for stock in Stocks:
    if stock[1] < 0  and not api.get_asset(stock[0]).shortable:
      print("Cannot short {}. Removing from list".format(stock[0]))
    else:
      tradable_stocks.append(stock)
  tradable_stocks = tradable_stocks[:5]
  TotalRating = 0
  stockp = 0

  def FindStockShares(stock):
    total = math.floor(float(stock[1]/TotalRating)*buying_power)
    totalspending = math.floor(total/stock[-1])
    stock.append(totalspending)
    stock.append(total) 

  for stock in tradable_stocks:
    stock.append(get_current_price(stock[0]))
    TotalRating += abs(stock[1])
  print(TotalRating)
  for stock in tradable_stocks:
    FindStockShares(stock)
  UpdateJson(Stocks,"passed")
  ChangeKey("Date","Var",date)
  return tradable_stocks

#converts stock list to dictionary
def UpdateJson(lst, file):
  stocks = []
  for item in lst:
    stock = {
      "Ticker" : item[0],
      "Rating" : float(item[1]),
      "Resistance" : item[2],
      "Support" : item[3],
      "Average Daily Volatility" : item[4],
      "Trend" : item[5],
      "Potential Profit" : item[6],
      "Average Low to Day Open" : item[7],
      "Average High to Day Open" : item[8],
      "Open Close Average" : item[9],
      "Price" : float(item[-3]),
      "Shares" : item[-2],
      "Total Spent" : item[-1]
      }
    stocks.append(stock)
  with open(directory + "json/{}.json".format(file), 'w') as file:
    json.dump(stocks, file)

#file is string of file path
#changes specific key in JSON file
def ChangeKey (key,file,mod):
  file = directory + "/json/{}.json".format(file)
  fileContent = json.loads(open(file).read())
  fileContent[key] = mod
  with open(file, "w") as f:
    json.dump(fileContent, f)

#file is string of file path
#converts json to python str
def ConvertJson(file):
  return json.loads(open(file).read())

def DebugLog(text):
  with open(directory + '/json/debug.txt','w') as file:
    file.writelines(text)



  
  
