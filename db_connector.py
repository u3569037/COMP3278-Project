import threading
import mysql.connector
from datetime import datetime
from datetime import date

# This class store mysql connector
# classmethod can be called by DB.func(), e.g. DB.withdrawal(0, 1000)

class DB:
    transactionLock = threading.Lock()
    stockOrderLock = threading.Lock()
    stockAccountLock = threading.Lock()
    sqlLock = threading.Lock()
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="123456",
      database="facerecognition"
    )
    cursor = mydb.cursor()

    @classmethod
    def login(self, mydb, account_name, password):
        cursor = mydb.cursor() 
        date = datetime.utcnow()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        sql = "SELECT Password, customer_id, login_date, login_time FROM Customer WHERE account_name = %s"
        val = (account_name,)
        cursor.execute(sql,val)
        result = cursor.fetchall()
        if result == []:
          return "" 
        customerid = result[0][1]
        login_date = result[0][2]
        login_time = result[0][3]
        if result[0][0] == password:
          update =  "UPDATE Customer SET login_date=%s WHERE account_name=%s"
          val2 = (date, account_name)
          cursor.execute(update, val2)
          update = "UPDATE Customer SET login_time=%s WHERE account_name=%s"
          val2 = (current_time, account_name)
          cursor.execute(update, val2)
          update = "INSERT INTO Login VALUES (%s,%s,%s)"
          val2 = (customerid,current_time,date)
          cursor.execute(update, val2)
          mydb.commit()
          
          return {"name": account_name, "cid" : customerid, "login_date" : login_date, "login_time" : login_time}
        else:
           return "Warning: pw wrong"


    @classmethod
    #initialize the accounts of the user
    def init_acc(self, mydb, cid):
        cursor = mydb.cursor()
        #hk saving
        sql = "INSERT INTO HK_Saving_Account VALUES (%s, %s, %s)"
        val = (cid,0,0)
        cursor.execute(sql,val)
        mydb.commit()
        #US saving
        sql = "INSERT INTO US_Saving_Account VALUES (%s, %s, %s)"
        val = (cid,0,0)
        cursor.execute(sql,val)
        mydb.commit()
        #hk current
        sql = "INSERT INTO HK_Current_Account VALUES (%s, %s, %s)"
        val = (cid,0,0)
        cursor.execute(sql,val)
        mydb.commit()
        #US current
        sql = "INSERT INTO US_Current_Account VALUES (%s, %s, %s)"
        val = (cid,0,0)
        cursor.execute(sql,val)
        mydb.commit()
       

        
    @classmethod
    def signup(self, mydb, name, account_name, password):
        cursor = mydb.cursor()
        sql = "INSERT INTO Customer VALUES (NULL, %s, %s, %s, NULL, NULL)"
        val = (name, account_name, password)
        sql2 = "SELECT customer_id FROM Customer WHERE account_name = %s"
        val2 = (account_name,)
        cursor.execute(sql2, val2)
        result = cursor.fetchall()
        if result != []:
            return False
        else:
            cursor.execute(sql, val)
            mydb.commit()
            cursor.execute(sql2, val2)
            result2 = cursor.fetchall()
            DB.init_acc(mydb, result2[0][0])
            return True



    @classmethod    
    def getaccinfo(mydb, cid):
        #cursor = mydb.cursor()
        sql2 = "SELECT * FROM Customer WHERE customer_id = %s"
        val2 = (cid,)
        mydb.cursor.execute(sql2, val2)
        result2 = mydb.cursor.fetchall()
        #mydb.commit()
        if result2 != None:
            return result2
        else:
            return False
    @classmethod    
    def gethkinfo1(self, cid):
        cursor = self.mydb.cursor()
        sql2 = "SELECT * FROM hk_current_account WHERE customer_id = %s"
        val2 = (cid,)
        cursor.execute(sql2, val2)
        result2 = cursor.fetchall()
        #mydb.commit()
        if result2 != None:
            return result2
        else:
            return False
    @classmethod    
    def gethkinfo2(self, cid):
        cursor = self.mydb.cursor()
        sql2 = "SELECT * FROM hk_saving_account WHERE customer_id = %s"
        val2 = (cid,)
        cursor.execute(sql2, val2)
        result2 = cursor.fetchall()
        #mydb.commit()
        if result2 != None:
            return result2
        else:
            return False
    @classmethod    
    def getusinfo1(self, cid):
        cursor = self.mydb.cursor()
        sql2 = "SELECT * FROM us_current_account WHERE customer_id = %s"
        val2 = (cid,)
        cursor.execute(sql2, val2)
        result2 = cursor.fetchall()
        #mydb.commit()
        if result2 != None:
            return result2
        else:
            return False
    @classmethod    
    def getusinfo2(self, cid):
        cursor = self.mydb.cursor()
        sql2 = "SELECT * FROM us_saving_account WHERE customer_id = %s"
        val2 = (cid,)
        cursor.execute(sql2, val2)
        result2 = cursor.fetchall()
        #mydb.commit()
        if result2 != None:
            return result2
        else:
            return False


    @classmethod
    def __isBalanceGreaterThan(cls, id, amount, currency):
        # check enough balance
        return True

    @classmethod    
    def checker(self, amount,cid,tid,opt1,opt2):
        cursor = self.mydb.cursor()
        ans = []
        print(opt1)
        print(opt2)
        sql = "SELECT balance,customer_id FROM "+opt1+"_account WHERE customer_id ="+ cid
        cursor.execute(sql)
        result = cursor.fetchall()
        print("checker")
        print (result)
        print(result[0][1])
        if (result == []):
            return False
        elif (int(result[0][0])- int(amount)) < 0:
            return "Not enough balance"
        else:
            ans.append(result[0][1])
        
        sql2 = "SELECT balance,customer_id FROM "+opt2+"_account WHERE account_id ="+ tid
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        print("checker")
        print (result2)
        if (result2 == []):
            return False
        else:
            ans.append(result2[0][1])
            return ans
        
    
    @classmethod
    def withdrawal(self,cid,amount,option):
        cursor = self.mydb.cursor()
        sql2 = "UPDATE "+option+"_account SET balance = balance-%s WHERE customer_id = %s"
        val2 = (amount,cid)
        cursor.execute(sql2, val2)
        self.mydb.commit()
        print("withdraw",option)
        
    @classmethod
    def deposit(self,aid,amount,option):
        cursor = self.mydb.cursor()
        sql2 = "UPDATE "+option+"_account SET balance = balance+%s WHERE account_id = %s"
        val2 = (amount,aid)
        cursor.execute(sql2, val2)
        self.mydb.commit()

        print('deposit',option)
    @classmethod
    def record(self,src,to,srcid,toid,amount,option1,option2):
        cursor = self.mydb.cursor()
        date = datetime.utcnow()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        sql2 = ("INSERT INTO transaction (customer_id,target_id,from_account_id,to_account_id,amount,trans_time,trans_date) ""VALUES (%s,%s,%s, %s, %s, %s, %s)")
        val2 = (src,to,srcid,toid,amount,current_time,date)
        cursor.execute(sql2, val2)
        self.mydb.commit()

        print('recorded')

    @classmethod
    def getAccId(self, cid,opt):
        cursor = self.mydb.cursor()
        sql = "SELECT account_id FROM "+opt+"_account WHERE customer_id ="+ cid
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result





    @classmethod
    def addStockToAccount(cls, id, ticker_symbol):
        cls.stockAccountLock.acquire()
        sql = "SELECT ticker_symbol FROM Stock_account WHERE customer_id=%s AND ticker_symbol=%s"
        val = (id, ticker_symbol)
        if cls.__exec_fetchone(sql, val) == None:
            sql = "INSERT INTO Stock_account VALUES (%s, %s, %s)"
            val = (id, ticker_symbol, 0)
            cls.__exec_commit(sql, val)
        cls.stockAccountLock.release()

    @classmethod
    def ifOrderExists(cls, id, ticker_symbol):
        sql = "SELECT ticker_symbol FROM Stock_order WHERE customer_id=%s AND ticker_symbol=%s"
        val = (id, ticker_symbol)
        if cls.__exec_fetchone(sql, val) == None:
            return False
        else:
            return True
    
    @classmethod
    def ifOrderExistsLocked(cls, id, ticker_symbol):
        cls.stockOrderLock.acquire()
        sql = "SELECT ticker_symbol FROM Stock_order WHERE customer_id=%s AND ticker_symbol=%s"
        val = (id, ticker_symbol)
        if cls.__exec_fetchone(sql, val) == None:
            cls.stockOrderLock.release()
            return False
        else:
            cls.stockOrderLock.release()
            return True

    @classmethod
    def makeOrder(cls, id, ticker_symbol, price, quantity, side):
        cls.stockOrderLock.acquire()
        flag = cls.ifOrderExists(id, ticker_symbol)
        print('makeOrder')
        if flag:
            if side == 'buy':
                cls.deposit(id, price * quantity, 'USD')
            else:
                cls.buyShare(quantity, id, ticker_symbol)
        else:
            sql = "INSERT INTO `Stock_order` VALUES (%s, %s, %s, %s, %s)"
            val = (id, ticker_symbol, price, quantity, side)
            cls.__exec_commit(sql, val)
        cls.stockOrderLock.release()
        return not flag

    @classmethod
    def cancelOrder(cls, id, ticker_symbol):
        cls.stockOrderLock.acquire()
        sql = "DELETE FROM Stock_order WHERE customer_id=%s AND ticker_symbol=%s"
        val = (id, ticker_symbol)
        cls.__exec_commit(sql, val)
        cls.stockOrderLock.release()
    
    @classmethod
    def cancelAllOrder(cls, id):
        cls.stockOrderLock.acquire()
        sql = "SELECT ticker_symbol FROM Stock_order WHERE customer_id=%s"
        val = (id, )
        cls.sqlLock.acquire()
        cls.cursor.execute(sql, val)
        result = cls.cursor.fetchall()
        cls.sqlLock.release()

        for symbol in result:
            sql = "DELETE FROM Stock_order WHERE customer_id=%s AND ticker_symbol=%s"
            val = (id, symbol[0])
            cls.__exec_commit(sql, val)
        cls.stockOrderLock.release()

    @classmethod
    def buyShare(cls, quantity, id, ticker_symbol):
        cls.stockAccountLock.acquire()
        sql = "UPDATE Stock_account SET quantity = quantity + %s WHERE customer_id=%s AND ticker_symbol=%s"
        val = (quantity, id, ticker_symbol)
        cls.__exec_commit(sql, val)
        cls.stockAccountLock.release()

    @classmethod
    def __isEnoughShare(cls, id, ticker_symbol, quantity):
        sql = "SELECT quantity FROM Stock_account WHERE customer_id=%s AND ticker_symbol=%s"
        val = (id, ticker_symbol)
        if cls.__exec_fetchone(sql, val)[0] >= quantity:
            return True
        else:
            return False

    @classmethod
    def sellShare(cls, quantity, id, ticker_symbol):
        cls.stockAccountLock.acquire()
        flag = cls.__isEnoughShare(id, ticker_symbol, quantity)
        if flag:
            sql = "UPDATE Stock_account SET quantity = quantity - %s WHERE customer_id=%s AND ticker_symbol=%s"
            val = (quantity, id, ticker_symbol)
            cls.__exec_commit(sql, val)
        cls.stockAccountLock.release()
        return flag
    
    @classmethod
    def __exec_commit(cls, sql, val):
        cls.sqlLock.acquire()
        cls.cursor.execute(sql, val)
        cls.mydb.commit()
        cls.sqlLock.release()
    
    @classmethod
    def __exec_fetchone(cls, sql, val):
        cls.sqlLock.acquire()
        cls.cursor.execute(sql, val)
        result = cls.cursor.fetchone()
        cls.sqlLock.release()
        return result
