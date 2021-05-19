import time
import json
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

