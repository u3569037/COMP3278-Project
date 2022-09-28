from db_connector import DB
from Stock import Stock
from Stock import buy
from Stock import sell

import time

DB.cancelAllOrder(0)
stockList = ['INTC', 'NVDA', 'AMD', 'MU']
reader = {}
for stock in stockList:
    reader[stock] = Stock(stock)
    DB.addStockToAccount(0, stock)

buy(0, 'INTC', 60, 20)
buy(0, 'NVDA', 300, 20)
buy(0, 'AMD', 60, 20)
buy(0, 'MU', 80, 20)
time.sleep(5)
sell(0, 'INTC', 1, 3)
sell(0, 'MU', 1, 3)
sell(0, 'AMD', 1, 3)

time.sleep(5)
DB.cancelAllOrder(0)