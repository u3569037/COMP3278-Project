import requests as re

from db_connector import DB

# find the rate from 'HKD' to 'USD' :
# rate = Currency.exRate('HKD', 'USD')
class Currency():
    url = 'https://tw.rter.info/capi.php'
    currency = re.get(url).json()

    @classmethod
    def update(cls):
        cls.currency = re.get(cls.url).json()
    
    @classmethod
    def exRate(cls, a, b):
        if a == 'USD':
            return cls.currency[a+b]['Exrate']
        elif b == 'USD':
            return 1 / cls.currency[b+a]['Exrate']
        else:
            return cls.exRate(a, 'USD') * cls.exRate('USD', b)

# buy foreign exChange = HKD$amount
# customer must buy foreign exChange in HKD
# e.g. buy_Exchange(0, 'JPY', 1500)
# use HKD1500 to buy 'JPY'

# *** DB.withdrawal() and DB.deposit() are not yet implemented ***
# *** please write query in db_connector.py ***
def buy_Exchange(id, currency, amount):
    if DB.withdrawal(id, amount, 'HKD'):
        DB.deposit(id, amount * Currency.exRate('HKD', currency), currency)

def sell_Exchange(id, currency, amount):
    if DB.withdrawal(id, amount, currency):
        DB.deposit(id, amount * Currency.exRate(currency, 'HKD'), 'HKD')
