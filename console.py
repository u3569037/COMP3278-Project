
from tkinter import *
from tkinter import ttk
import datetime
import time
import os
import tkinter.messagebox
import sqlite3
import threading
import mysql.connector
from pytz import timezone
from PIL import ImageTk, Image
from db_connector import DB
from Stock import *
from Currency import *


class bank_console:
    def __init__(self, root,name,cid):
        self.root = root
        self.root.geometry('700x400')
        self.root.title('DOC Bank')
        self.root.configure(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        
        #customer id and name of current user
        self.customer_id = cid
        self.name = name

        #frame for content
        self.content = Frame(root, width=500, bg='white', height=400)
        self.content.place(x=200,y=0)

        #image
        self.bg = ImageTk.PhotoImage(Image.open('bank_bg.jpg'))
        self.bg2 = Label(self.content,image=self.bg)
        self.bg2.place(x=10,y=10)

        self.label1 = Label(self.content,font=('arial', 12, 'bold'), text='DOC Bank iKYC System',bg = 'white')
        #self.label1.grid(row=0, column=30)
        self.label1.place(x=30,y=200)

        self.label1 = Label(self.content,font=('arial', 10, 'bold'), text='Welcome to DOC Bank ^_^ \n DOC Bank has been the best bank in Hong Kong for 10 years.\n We will strive to provide customers with the best service. \n Hope you have a good E-Bank service experience here.',bg = 'white')
        self.label1.place(rely=0.7,relwidth=1)

        # sidebar
        self.sidebar = Frame(root, width=200, bg='lightgreen', height=400, relief='groove', borderwidth=3)
        self.sidebar.grid(row=0, column=0, columnspan=20)

        self.photo = PhotoImage(file='logo.png')
        self.photo = self.photo.subsample(2)
        self.label = Label(self.sidebar,image=self.photo)
        self.label.place(x=0,y=0,relwidth=1)

        #welcome msg
        welcomemsg = "Hi " + self.name + " !"
        Label(self.sidebar,text=welcomemsg,bg="lightgreen",font=("arial",10,"bold"),relief="ridge").place(rely=0.35,relwidth=1)
        
        #sidebar button
        self.b1 = Button(self.sidebar, text='Account Information', command=self.acc_info, bg="lightgreen",activebackground="white",font=("arial",12,"bold"),relief="flat",borderwidth=0,width=18)
        self.b2 = Button(self.sidebar, text='Create Transaction', command=self.transaction, bg="lightgreen",activebackground="white",font=("arial",12,"bold"),relief="flat",borderwidth=0,width=18)
        self.b3 = Button(self.sidebar, text='Transaction History', command=self.trans_hist,  bg="lightgreen",activebackground="white",font=("arial",12,"bold"),relief="flat",borderwidth=0,width=18)
        self.b4 = Button(self.sidebar, text='Currency', command=self.currency, bg="lightgreen",activebackground="white",font=("arial",12,"bold"),relief="flat",borderwidth=0,width=18)
        self.b5 = Button(self.sidebar, text='Stock', command=self.stock, bg="lightgreen",activebackground="white",font=("arial",12,"bold"),relief="flat",borderwidth=0,width=18)

        self.b1.place(rely=0.45,relwidth=1)
        self.b2.place(rely=0.55,relwidth=1)
        self.b3.place(rely=0.65,relwidth=1)
        self.b4.place(rely=0.75,relwidth=1)
        self.b5.place(rely=0.85,relwidth=1)

        #time info
        def clock():
            t = datetime.datetime.now(timezone('UTC'))
            t2 = t.astimezone(timezone("Asia/Hong_Kong"))
            current_date = '{:%d %B,%Y}'.format(t2)

            current_time = t2.strftime('%H:%M:%S')
            self.lblInfo.config(text=(current_time + '\n' + current_date))
            self.lblInfo.after(200, clock)

        self.lblInfo = Label(self.sidebar,font=('consolas', 14, 'bold'),bg ='lightgreen')
        self.lblInfo.place(x=10,y=80)
        clock()

        #topbar
        topbar = Menu(background='lightblue', foreground='black',font=("arial",7))
        topbar.add_command(label='Customer Service', command=self.cs)
        topbar.add_command(label='Activate FaceID', command=self.activate_faceid)
        topbar.add_command(label='Log out', command=self.exit)

        root.config(menu=topbar)
     

    #Customer Service
    def cs(self):
        tkinter.messagebox.showinfo('DOC Bank Customer Service','You may contact our customer service by calling the hotline or sending Email to us ^_^ \n\n Hotline: 21800000 \n\n Email: cs@docbank.hk')

    #activate faceid
    def activate_faceid(self):
      if not os.path.exists('data/{}'.format(self.name)):
        tkinter.messagebox.showinfo('DOC Bank FaceID','Please look at the camera and wait for 1-2 minutes. ^_^')
        a_file = open("face_capture.py", "r")
        list_of_lines = a_file.readlines()
        codestr = "user_name = \"" + self.name + "\"\n"
        list_of_lines[8] = codestr
        a_file = open("face_capture.py", "w")
        a_file.writelines(list_of_lines)
        a_file.close()
        exec(open('face_capture.py').read())
        exec(open('train.py').read())
        tkinter.messagebox.showinfo('DOC Bank FaceID','You have sucessfully activated the FaceID function.\n You may use FaceID to login next time. ^_^')
      else:
        tkinter.messagebox.showinfo('DOC Bank FaceID','You had already activated the FaceID function before!')

    #exit
    def exit(self):
        exit = tkinter.messagebox.askquestion('Exit DOC Bank system','Are you sure you want to log out from DOC Bank system?')
        if exit == 'yes':
            self.root.destroy()

    #account info
    def acc_info(self):
      #remove all contents in content frame
      for wid in self.content.winfo_children():
        wid.destroy()

      #title
      t1 = DB.getaccinfo(self.customer_id)
      t2 = DB.gethkinfo1(self.customer_id)
      t3 = DB.getusinfo1(self.customer_id)
      t4 = DB.gethkinfo2(self.customer_id)
      t5 = DB.getusinfo2(self.customer_id)
      self.acc_info_label1 = Label(self.content,font=('arial', 12, 'bold'), text='Account Information',bg = 'white')
      self.acc_info_label2 = Label(self.content,font=('arial', 12, 'bold'), text='________________________________________________________',bg = 'white')
      print(t1)
      print(t2)
      print(t3)
      print(t4)
      print(t5)
      
      self.acc_info_label3 = Label(self.content,font=('arial', 12, 'bold'), text=("Name : "+str(t1[0][1])+"\n Customer ID: "+str(t1[0][0])),bg = 'lightgray')
      self.acc_info_label4 = Label(self.content,font=('arial', 12, 'bold'), text=("Current Balance(HKD) : "+str(t2[0][2]) + "\n Account ID: " + str(t2[0][1])),bg = 'lightblue')
      self.acc_info_label5 = Label(self.content,font=('arial', 12, 'bold'), text=("Current Balance(USD) : "+str(t3[0][2]) + "\n Account ID: " + str(t3[0][1])),bg = 'lightblue')
      self.acc_info_label6 = Label(self.content,font=('arial', 12, 'bold'), text=("Saving Balance(HKD) : "+str(t4[0][2]) + "\n Account ID: " + str(t4[0][1])),bg = 'lightblue')
      self.acc_info_label7 = Label(self.content,font=('arial', 12, 'bold'), text=("Saving Balance(USD) : "+str(t5[0][2]) + "\n Account ID: " + str(t5[0][1])),bg = 'lightblue')
      
      self.acc_info_label1.place(relx=0.05,rely=0.02)
      self.acc_info_label2.place(relx=0.05,rely=0.07)
      self.acc_info_label3.place(relx=0.1,rely=0.15,relwidth=0.8)
      self.acc_info_label4.place(relx=0.1,rely=0.35,relwidth=0.8)
      self.acc_info_label5.place(relx=0.1,rely=0.50,relwidth=0.8)
      self.acc_info_label6.place(relx=0.1,rely=0.65,relwidth=0.8)
      self.acc_info_label7.place(relx=0.1,rely=0.80,relwidth=0.8)


    
    #transaction
    def transaction(self):
      #remove all contents in content frame
      for wid in self.content.winfo_children():
        wid.destroy()
   
      def deposit():
        amount = self.tran_amt_entry.get()
        source = self.tran_from_entry.get()              
        target = self.tran_to_entry.get()

        if (amount == "") or (target == "") or (source == ""):
              tkinter.messagebox.showwarning('Warning!', 'Please enter a valid value for all boxes!')
              return
              

        sets = []
        sets.append(source)
        print(source)
        currency = ""
        if source == "hk_saving" or source == "hk_current":
          currency="hkd"
        else: 
          currency="usd"

        if int(int(target)/10000000) == 1:
          if currency=="hkd":
            sets.append("hk_saving")
          else: 
            tkinter.messagebox.showwarning('Warning!', 'The currency used in two accounts need to be the same')
            return
        elif int(int(target)/10000000) == 2:
          if currency=="usd":
            sets.append("us_saving")
          else: 
            tkinter.messagebox.showwarning('Warning!', 'The currency used in two accounts need to be the same')
            return
        elif int(int(target)/10000000) == 3:
          if currency=="hkd":
            sets.append("hk_current")
          else: 
            tkinter.messagebox.showwarning('Warning!', 'The currency used in two accounts need to be the same')
            return
        elif int(int(target)/10000000) == 4:
          if currency=="usd":
            sets.append("us_current")
          else: 
            tkinter.messagebox.showwarning('Warning!', 'The currency used in two accounts need to be the same')
            return
        print(sets)

        if len(sets) != 2:
              tkinter.messagebox.showwarning('Warning!', 'Please enter a valid value for all boxes!')
              return
        
        check = DB.checker(amount,str(self.customer_id),target,sets[0],sets[1])
        if check == False:
          tkinter.messagebox.showwarning('Warning!', 'Please enter a valid value for all boxes!')
          return
        elif check == "Not enough balance":
          tkinter.messagebox.showwarning('Warning!', 'The balance in your account is not enough for the transaction')
          return
        elif check[0] != self.customer_id:
              tkinter.messagebox.showwarning('Warning!', 'Please ensure you are using your own account!')
              return
              
        accid = DB.getAccId(str(self.customer_id),sets[0])
        DB.withdrawal(str(self.customer_id),amount,sets[0])
        DB.deposit(target,amount,sets[1])
        DB.record(check[0],check[1],str(accid[0][0]),target,amount,sets[0],sets[1])
        tkinter.messagebox.showinfo(title="Success", message="Successful transfer!")





        
      #title
      self.trans_label1 = Label(self.content,font=('arial', 12, 'bold'), text='Transaction',bg = 'white')
      self.trans_label2 = Label(self.content,font=('arial', 12, 'bold'), text='________________________________________________________',bg = 'white')
      self.trans_label1.place(relx=0.05,rely=0.02)
      self.trans_label2.place(relx=0.05,rely=0.07)
      
      
      self.tran_label3 = Label(self.content,font=('arial', 12, 'bold'), text='Choose Your account: ', bg = 'white')
      self.tran_label3.place(relx=0.05,rely=0.15)
      self.tran_from_entry = ttk.Combobox(self.content,values=["hk_saving","us_saving","hk_current","us_current"])
      self.tran_from_entry["state"] = "readonly"
      self.tran_from_entry.place(relx=0.45,rely=0.15)

      self.tran_label4 = Label(self.content,font=('arial', 12, 'bold'), text='Enter Target account ID: ', bg = 'white')
      self.tran_label4.place(relx=0.05,rely=0.25)
      self.tran_to_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.tran_to_entry.place(relx=0.45,rely=0.25)
      
      self.tran_label5 = Label(self.content,font=('arial', 12, 'bold'), text='Enter amount of money: ', bg = 'white')
      self.tran_label5.place(relx=0.05,rely=0.35)
      self.tran_amt_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.tran_amt_entry.place(relx=0.45,rely=0.35)
      
      
      self.tran_de = ttk.Button(self.content, text='Transact', command=deposit)
      self.tran_de.place(relx=0.45,rely=0.42)

      #image
      img = ImageTk.PhotoImage(file='transaction_img.png')
      img2 = Label(self.content,image=img,border=0,bg="white")
      img2.image = img
      img2.place(rely=0.49,relwidth=1)
              

    
    #currency
    def currency(self):
      #remove all contents in content frame
      for wid in self.content.winfo_children(): 
        wid.destroy()

      self.curr01 = Label(self.content)
      self.curr02 = Label(self.content)
      def display():
        self.curr01.destroy()
        self.curr02.destroy()
        a = self.curr_from_entry.get()
        b = self.curr_to_entry.get()
        Currency.update()
        self.curr01 = Label(self.content, font=('consolas', 12, 'bold'), text=
          a + ' -> ' + b + ' : ' +
          str(round(Currency.exRate(a, b), 4)))
        self.curr01.place(relx=0.05,rely=0.25)
        self.curr02 = Label(self.content, font=('consolas', 12, 'bold'), text=
          a + ' <- ' + b + ' : ' +
          str(round(Currency.exRate(b, a), 4)))
        self.curr02.place(relx=0.05,rely=0.35)

      def curr_buy():
        currency = self.curr_buy_entry.get()
        amount = float(self.curr_buyamount_entry.get())
        if buy_Exchange(id, currency, amount):
          text = 'Success'
        else:
          text= 'Fail'
        Label(self.content, font=('arial', 12, 'bold'), text=text).place(relx=0.05,rely=0.55)
      
      def curr_sell():
        currency = self.curr_sell_entry.get()
        amount = float(self.curr_sellamount_entry.get())
        if sell_Exchange(id, currency, amount):
          text = 'Success'
        else:
          text= 'Fail'
        Label(self.content, font=('arial', 12, 'bold'), text=text).place(relx=0.05,rely=0.55)


      #title
      self.curr_label1 = Label(self.content,font=('arial', 12, 'bold'), text='Currency',bg = 'white')
      self.curr_label1.place(relx=0.05,rely=0.02)
      self.curr_label2 = Label(self.content,font=('arial', 12, 'bold'), text='________________________________________________________',bg = 'white')
      self.curr_label2.place(relx=0.05,rely=0.07)
      
      # Search bar
      self.curr_from_entry = ttk.Combobox(self.content, width=8, font = "Helvetica 13", values=["HKD","USD","JPY","EUR","GBP"])
      self.curr_from_entry.place(relx=0.05,rely=0.15)
      self.curr_label3 = Label(self.content,font=('arial', 12, 'bold'), text='&', bg = 'white')
      self.curr_label3.place(relx=0.25,rely=0.15)
      self.curr_to_entry = ttk.Combobox(self.content, width=8, font = "Helvetica 13", values=["HKD","USD","JPY","EUR","GBP"])
      self.curr_to_entry.place(relx=0.30,rely=0.15)
      self.curr_search = ttk.Button(self.content, text='go', command=display)
      self.curr_search.place(relx=0.50,rely=0.15)

      #image
      img = ImageTk.PhotoImage(file='currency_img.png')
      img2 = Label(self.content,image=img, border=0, bg="white")
      img2.image = img
      img2.place(rely=0.55,relwidth=1)
              

      """
      self.curr_buy = Label(self.content,font=('arial', 12, 'bold'), text='Buy',bg = 'white')
      self.curr_buy.place(relx=0.05,rely=0.35)
      self.curr_buy_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.curr_buy_entry.place(relx=0.12,rely=0.35)
      self.curr_buyamount = Label(self.content,font=('arial', 12, 'bold'), text='Amount',bg = 'white')
      self.curr_buyamount.place(relx=0.32,rely=0.35)
      self.curr_buyamount_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.curr_buyamount_entry.place(relx=0.45,rely=0.35)
      self.curr_buybt = ttk.Button(self.content, text='go', command=curr_buy)
      self.curr_buybt.place(relx=0.65,rely=0.35)

      self.curr_sell = Label(self.content,font=('arial', 12, 'bold'), text='Sell',bg = 'white')
      self.curr_sell.place(relx=0.05,rely=0.45)
      self.curr_sell_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.curr_sell_entry.place(relx=0.12,rely=0.45)
      self.curr_sellamount = Label(self.content,font=('arial', 12, 'bold'), text='Amount',bg = 'white')
      self.curr_sellamount.place(relx=0.32,rely=0.45)
      self.curr_sellamount_entry = ttk.Entry(self.content, width=10, font = "Helvetica 13")
      self.curr_sellamount_entry.place(relx=0.45,rely=0.45)
      self.curr_sellbt = ttk.Button(self.content, text='go', command=curr_sell)
      self.curr_sellbt.place(relx=0.65,rely=0.45)
      """
    #stock
    def stock(self):
      #remove all contents in content frame
      for wid in self.content.winfo_children():
        wid.destroy()
      
      class Display(threading.Thread):
        stock_box = {}
        DLock = threading.Lock()
        def __init__(self, bank_console):
          threading.Thread.__init__(self)
          self.bank_console = bank_console
        def run(self):
          self.DLock.acquire()
          count = 0
          for stock in stock_reader.stockList:
            self.stock_box[stock] = Label(self.bank_console.content,font=('consolas', 9, 'bold'), text=
              stock + '   ' + ' '*(4-len(stock)) +
              str(stock_reader.reader[stock].current_timezone) + '   ' +
              stock_reader.reader[stock].today_date + '   ' +
              stock_reader.reader[stock].current_time + '   ' +
              str(round(stock_reader.reader[stock].current_price, 4)))
            self.stock_box[stock].place(relx=0.05,rely=0.25+0.07*count)
            count += 1
          self.DLock.release()
          while True:
            self.display()
            time.sleep(1)
        def display(self):
          self.DLock.acquire()
          for stock in stock_reader.stockList:
            self.stock_box[stock].config(text=
              stock + '   ' + ' '*(4-len(stock)) +
              str(stock_reader.reader[stock].current_timezone) + '   ' +
              stock_reader.reader[stock].today_date + '   ' +
              stock_reader.reader[stock].current_time + '   ' +
              str(round(stock_reader.reader[stock].current_price, 4)))
          self.DLock.release()
        @classmethod
        def add_to_list(cls, console):
          cls.DLock.acquire()
          ticker_symbol = console.stock_entry.get()
          count = len(stock_reader.stockList) 
          stock_reader.add(0, ticker_symbol)
          cls.stock_box[ticker_symbol] = Label(console.content,font=('consolas', 9, 'bold'), text=
            ticker_symbol + '   ' + ' '*(4-len(ticker_symbol)) +
            str(stock_reader.reader[ticker_symbol].current_timezone) + '   ' +
            stock_reader.reader[ticker_symbol].today_date + '   ' +
            stock_reader.reader[ticker_symbol].current_time + '   ' +
            str(round(stock_reader.reader[ticker_symbol].current_price, 4)))
          cls.stock_box[ticker_symbol].place(relx=0.05,rely=0.25+0.07*count)
          cls.DLock.release()
      
      Display(self).start()

      #title
      self.stock_label1 = Label(self.content,font=('arial', 12, 'bold'), text='Stock',bg = 'white')
      self.stock_label1.place(relx=0.05,rely=0.02)
      self.stock_label2 = Label(self.content,font=('arial', 12, 'bold'), text='________________________________________________________',bg = 'white')
      self.stock_label2.place(relx=0.05,rely=0.07)

      # Search bar
      self.stock_label3 = Label(self.content,font=('arial', 12, 'bold'), text='Search',bg = 'white')
      self.stock_label3.place(relx=0.05,rely=0.15)
      self.stock_entry = ttk.Entry(self.content, width=20, font = "Helvetica 13")
      self.stock_entry.place(relx=0.20,rely=0.15)
      self.stock_search = ttk.Button(self.content, text='go', command=lambda:Display.add_to_list(self))
      self.stock_search.place(relx=0.60,rely=0.15)

      #image
      img = ImageTk.PhotoImage(Image.open('stock_img.jfif'))
      img2 = Label(self.content,image=img, border=0, bg="white")
      img2.image = img
      img2.place(rely=0.66,relwidth=1)



      
    def trans_hist(self):
        #remove all contents in content frame
        for wid in self.content.winfo_children():
            wid.destroy()

        #title
        self.hist_label1 = Label(self.content,font=('arial', 12, 'bold'), text='Transaction History',bg = 'white')
        self.hist_label1.place(relx=0.05,rely=0.02)
        self.hist_label2 = Label(self.content,font=('arial', 12, 'bold'), text='________________________________________________________',bg = 'white')
        self.hist_label2.place(relx=0.05,rely=0.07)
        self.hist_label3 = Label(self.content,font=('arial', 12), text='id    from_acc         to_acc      amount         date              time ',bg = 'white')
        self.hist_label3.place(relx=0.01,rely=0.35)

        #transaction history      
        self.trans_win = Frame(self.content,height=240,width=500)
        self.trans_win.pack_propagate(0)
        self.trans_win.place(x=0,rely=0.4,relwidth=1)

        self.trans_record = Listbox(self.trans_win, height=100, width=300,bg="white",bd=0,font=("ariel",10))
        self.scroll_bar = Scrollbar(self.trans_win)
        self.scroll_bar.pack(side=RIGHT,fill=Y)
        self.scroll_bar.config(command=self.trans_record.yview)
        self.trans_record.config(yscrollcommand=self.scroll_bar.set, background="white", highlightbackground="lightgrey", bd=0, selectbackground="grey",font=("ariel",14), height=100)
        self.trans_record.pack(side=BOTTOM, fill=Y, padx=0, pady=0)
        
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="123456",
          database="facerecognition"
        )

        def display():
          choice = self.hist_search.get()
          self.trans_record.delete(0,END)
          if choice != "NULL":
            cursor = self.mydb.cursor()
            ac = DB.getAccId(str(self.customer_id), self.hist_acc.get())
            extra = " ORDER BY trans_date DESC, trans_time DESC"
            _from = self.hist_from.get()
            _to = self.hist_to.get()
            search = self.hist_search.get()
            if search == 'Amount':
              extra = f' AND amount >=\'{_from}\' AND amount <=\'{_to}\''+extra
            elif search == 'Time':
              extra = f'AND trans_date >=\'{_from}\' AND trans_date <=\'{_to}\''+extra
            sql = """SELECT target_id, from_account_id, to_account_id, amount, trans_date, trans_time
                    FROM Transaction WHERE customer_id = %s AND (from_account_id = %s OR to_account_id = %s)"""+extra
            val = (self.customer_id,) + ac[0] + ac[0]
            cursor.execute(sql, val)
            results = cursor.fetchall()
            count = 0
            for result in results:
              self.trans_record.insert(END,result)
              count += 1
          else:
            cursor = self.mydb.cursor()
            ac = DB.getAccId(str(self.customer_id), self.hist_acc.get())
            sql = """SELECT target_id, from_account_id, to_account_id, amount, trans_date, trans_time
                    FROM Transaction WHERE customer_id = %s AND (from_account_id = %s OR to_account_id = %s)"""
            val = (self.customer_id,) + ac[0] + ac[0]
            cursor.execute(sql, val)
            results = cursor.fetchall()
            count = 0
            for result in results:
              self.trans_record.insert(END,result)
              count += 1

        self.hist_acc = ttk.Combobox(self.content, width=13, font = "Helvetica 13", values=["HK_Saving", "HK_current", "US_Saving", "US_current"])
        self.hist_acc.place(relx=0.05,rely=0.15)
        Label(self.content,font=('arial', 12, 'bold'), text='Sort by',bg = 'white').place(relx=0.4,rely=0.15)
        self.hist_search = ttk.Combobox(self.content, width=8, font = "Helvetica 13", values=["Amount", "Time","NULL"])
        self.hist_search.place(relx=0.55,rely=0.15)
        self.hist_labelf = Label(self.content,font=('arial', 12, 'bold'), text='From',bg = 'white')
        self.hist_labelf.place(relx=0.05,rely=0.25)
        self.hist_from = ttk.Entry(self.content, width=13, font = "Helvetica 13")
        self.hist_from.place(relx=0.15,rely=0.25)
        self.hist_labelf = Label(self.content,font=('arial', 12, 'bold'), text='To',bg = 'white')
        self.hist_labelf.place(relx=0.42,rely=0.25)
        self.hist_to = ttk.Entry(self.content, width=13, font = "Helvetica 13")
        self.hist_to.place(relx=0.50,rely=0.25)
        self.hist_go = ttk.Button(self.content, text='go', command=display)
        self.hist_go.place(relx=0.78,rely=0.25)


if __name__ == '__main__':
    root = Tk()
    application = bank_console(root,"Admin",-1)
    root.mainloop()
