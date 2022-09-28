import threading
import time
import yfinance as yf

from db_connector import DB

# This class is for update stock info
# Call by Stock(ticker_symbol), e.g. AAPL = Stock('AAPL')
# *** please call DB.addStockToAccount(userID, ticker_symbol) b4 Stock() ***

# timezone      = AAPL.current_timezone
# latest time   = AAPL.current_time
# current price = AAPL.current_price
# latest day    = AAPL.today_date
# start price   = AAPL.today_open
# MAX price     = AAPL.today_max
# % change      = AAPL.today_change

# update above value by AAPL.full_update()

# Buy stock  : buy(0, 'AAPL', 160, 5), userID 0 buy 5 AAPL at $160
# Sell stock : sell(0, 'AAPL', 170, 8), userID 0 sell 8 AAPL at $170
class Stock:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.full_update()

    def __change(self):
        return (self.current_price-self.today_open)/self.today_open*100

    def price_update(self):
        current = Info.current_info(self.ticker_symbol)
        self.current_price = current['Close'][0]

    def full_update(self):
        current = Info.current_info(self.ticker_symbol)
        time = current.index.timetz[0]

        self.current_timezone = time.tzinfo
        self.current_time = f'{time.hour}:{time.minute}'
        self.current_price = current['Close'][0]

        open = Info.open_info(self.ticker_symbol)
        date = open.index.date[0]

        self.today_date = f'{date.year}-{date.month}-{date.day}'
        self.today_open = open['Open'][0]
        self.today_max = open['High'][0]

        self.today_change = self.__change()

class stock_reader(threading.Thread):
    stockList = []
    reader = {}
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            for stock in self.stockList:
                self.reader[stock].full_update()
            time.sleep(1.5)
    @classmethod        
    def add(cls, id, ticker_symbol):
        cls.stockList.append(ticker_symbol)
        cls.reader[ticker_symbol] = Stock(ticker_symbol)
        DB.addStockToAccount(id, ticker_symbol)
        
class Info():
    yfLock = threading.Lock()
    @classmethod
    def current_info(cls, ticker_symbol):
        cls.yfLock.acquire()
        tmp = yf.download(tickers=ticker_symbol, threads = True, period='1d', interval='1m', actions=False)
        cls.yfLock.release()
        return tmp.iloc[-1:]

    @classmethod
    def open_info(cls, ticker_symbol):
        cls.yfLock.acquire()
        tmp = yf.download(tickers=ticker_symbol, threads = True, period='1d', interval='1d', actions=False)
        cls.yfLock.release()
        return tmp

def buy(id, ticker_symbol, price, quantity):
    amount = price * quantity
    if DB.withdrawal(id, amount, 'USD'):
        if DB.makeOrder(id, ticker_symbol, price, quantity, 'buy'):
            Buying_stock(id, ticker_symbol, price, quantity).start()

def sell(id, ticker_symbol, price, quantity):
    if DB.sellShare(quantity, id, ticker_symbol):
        if DB.makeOrder(id, ticker_symbol, price, quantity, 'sell'):
            Selling_stock(id, ticker_symbol, price, quantity).start()


class Buying_stock(threading.Thread):
    def __init__(self, id, ticker_symbol, price, quantity):
        threading.Thread.__init__(self)
        self.id = id
        self.ticker_symbol = ticker_symbol
        self.price = price
        self.quantity = quantity
    def run(self):
        while DB.ifOrderExistsLocked(self.id, self.ticker_symbol):
            if Info.current_info(self.ticker_symbol)['Close'][0] < self.price:
                print('buy'+self.ticker_symbol)
                DB.buyShare(self.quantity, self.id, self.ticker_symbol)
                DB.cancelOrder(self.id, self.ticker_symbol)
                break
            time.sleep(1)
        else:
            DB.deposit(self.id, self.price * self.quantity, 'USD')

class Selling_stock(threading.Thread):
    def __init__(self, id, ticker_symbol, price, quantity):
        threading.Thread.__init__(self)
        self.id = id
        self.ticker_symbol = ticker_symbol
        self.price = price
        self.quantity = quantity
    def run(self):
        while DB.ifOrderExistsLocked(self.id, self.ticker_symbol):
            if Info.current_info(self.ticker_symbol)['Close'][0] >= self.price:
                print('sell'+self.ticker_symbol)
                DB.deposit(self.id, self.price * self.quantity, 'USD')
                DB.cancelOrder(self.id, self.ticker_symbol)
                break
            time.sleep(1)
        else:
            DB.buyShare(self.quantity, self.id, self.ticker_symbol)
