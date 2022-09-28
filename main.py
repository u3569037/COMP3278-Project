from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pickle
from PIL import Image, ImageTk
from db_connector import *
from console import *
import datetime
#import Stock.py
#import faces.py
#import faces_gui.py
#import face_capture.py
#import train.py


class Login_GUI():
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='#f2f2f2')
        self.root.title("DOC Bank")
        self.root.geometry("600x400")
        self.initialView()
        self.root.protocol("WM_DELETE_WINDOW", self.Closing)
        self.root.mainloop()

    def Closing(self):
        if messagebox.askokcancel("Quit", "Quit the DOC Bank system?"):
            self.root.destroy() 
            quit()


    def initialView(self):
        for x in self.root.winfo_children():
            x.destroy()

        #connect to database
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="123456",
          database="facerecognition"
        )

        self.canvas = Canvas(self.root, width=600, height=150, bg='white')
        self.canvas.pack(side='top')
        self.canvas.configure(bg="white")

        #image
        self.login1 = PhotoImage(file = "login1.png")
        self.signup1 = PhotoImage(file = "signup1.png")
        self.faceid1 = PhotoImage(file = "faceid.png")

        #set buttons
        self.btn_login = Button(self.root, image=self.login1,bg="white",command=self.usr_login)
        self.btn_signup = Button(self.root, image=self.signup1,bg="white",command=self.usr_sign_up)
        self.btn_faceid = Button(self.root, image=self.faceid1,bg="#f2f2f2",border=0,command=self.faceid_login)
        self.btn_login.place(relx=0.2, rely=0.85)
        self.btn_signup.place(relx=0.4, rely=0.85)
        self.btn_faceid.place(relx=0.65, rely=0.5)

        #set logo
        self.banklogo = ImageTk.PhotoImage(Image.open("logo.png"))  
        self.logo = self.canvas.create_image(300,10,anchor="n", image=self.banklogo)

        # input information
        self.acc_message = Label(self.root, bg="#f2f2f2", text='Account:', font=('Consolas', 12)).place(relx=0.02, rely=0.45)
        
        self.pw_message = Label(self.root, bg="#f2f2f2", text='Password:', font=('Consolas', 12)).place(relx=0.02, rely=0.65)

        self.usr_name = StringVar()
        self.usr_name.set('')
        self.entry_usr_name = Entry(self.root, textvariable=self.usr_name, font=('Consolas', 14))
        self.entry_usr_name.place(relx=0.18, rely=0.45)

        self.usr_pw = StringVar()
        self.entry_usr_pw = Entry(self.root, textvariable=self.usr_pw, font=('Consolas', 14), show='*')
        self.entry_usr_pw.place(relx=0.18, rely=0.65)        
        
        #faceid login label
        self.faceid_label = Label(self.root, text= "FaceID login ", font= ("consolas",10),bg="#f2f2f2").place(relx=0.7, rely=0.43)
        
        #bottom info
        self.bottom_info= Label(self.root, text= "© DOC Bank iKYC system -- developed by COMP3278 Group 20 (2021 Fall) ", font= ("consolas",7),bg="#f2f2f2").pack(side="bottom")


     # Function for user using face ID login
    def faceid_login(self):
        self.root.destroy()
        exec(open('faces_gui.py').read())

    # Function for user log in
    def usr_login(self):
        #connect to database
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="123456",
          database="facerecognition"
        )
        
        # get the user input for username and password
        usr_name = self.usr_name.get()
        usr_pw = self.usr_pw.get()

        result = DB.login(mydb,usr_name,usr_pw)
        if result == "":
            is_sign_up = messagebox.askyesno('Welcome！ ', 'You have not sign up yet. Sign up now?')
            if is_sign_up:
                self.usr_sign_up()
        elif result == "Warning: pw wrong":
            #incorrect password
            messagebox.showerror(message='Error, your password is wrong, try again.')
        else:
            #successfully login

            #time info
            t = datetime.datetime.now(timezone('UTC'))
            t2 = t.astimezone(timezone("Asia/Hong_Kong"))
            current_date = '{:%d %B,%Y}'.format(t2)
            current_time = t2.strftime('%H:%M:%S')

            if result["login_date"] == None or  result["login_time"] == None:
                last_login_date = 'NULL'
                last_login_time = 'NULL'
            else:
                last_login_date = '{:%d %B,%Y}'.format(result["login_date"])
                last_login_time = str(result["login_time"])
            
            #welcome msg
            messagebox.showinfo(title='DOC Bank',
                                message='Hello ' +
                                result["name"] + 
                                " ^_^\n" +
                                'Welcome to DOC Bank\n\n' +
                                "Last login date: " +
                                last_login_date + "\n" +
                                "Last login time: " + 
                                last_login_time +         
                                "\n\n" +
                                "Current time: " +
                                current_time + "\n" + 
                                "Today's date: " +
                                current_date)

            #Destroy the current window
            self.root.destroy()

            #Open new window
            newroot = Tk()
            application = bank_console(newroot, result["name"], result["cid"])
            application.customer_id = result["cid"]
            application.name = result["name"]
            newroot.mainloop()


    # Function for user sign up
    def usr_sign_up(self):
        def create_account():
            #connect to database
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="123456",
              database="facerecognition"
            )
            
            np = new_pw.get()
            npf = new_pw_confirm.get()
            nan = new_accname.get()
            nn = new_name.get()
     
            # Check the password and confirmed password
            if np != npf:
                messagebox.showerror('Error', 'Password and confirm password must be the same!')
     
            # If the username exists, throw error
            elif not DB.signup(mydb, nn, nan, np):
                messagebox.showerror('Error', 'The user has already signed up!')
     
            # successfully sign up
            else:
                messagebox.showinfo('Welcome', 'You have successfully signed up!')
                # destroy the window
                sign_up_window.destroy()
 
        # sign up window
        sign_up_window = Toplevel(self.root)
        sign_up_window.geometry('400x250')
        sign_up_window.title('DOC Bank E-Account Sign up')

        # Entry for new username
        new_name = StringVar()  
        new_name.set('Chan Tai Man')  
        Label(sign_up_window, text='Name: ',font= ("consolas",12)).place(x=10, y=10)  
        entry_new_name = Entry(sign_up_window, textvariable=new_name) 
        entry_new_name.place(x=180, y=10)  

        # Entry for new accountname
        new_accname = StringVar()  
        new_accname.set('')  
        Label(sign_up_window, text='Account Name: ',font= ("consolas",12)).place(x=10, y=50)  
        entry_new_accname = Entry(sign_up_window, textvariable=new_accname) 
        entry_new_accname.place(x=180, y=50)  
        
        # Entry for new password
        new_pw = StringVar()
        Label(sign_up_window, text='Password: ',font= ("consolas",12)).place(x=10, y=90)
        entry_usr_pw = Entry(sign_up_window, textvariable=new_pw, show='*')
        entry_usr_pw.place(x=180, y=90)
     
        new_pw_confirm = StringVar()
        Label(sign_up_window, text='Confirm password: ',font= ("consolas",12)).place(x=10, y=130)
        entry_usr_pw_confirm = Entry(sign_up_window, textvariable=new_pw_confirm, show='*')
        entry_usr_pw_confirm.place(x=180, y=130)

        #face id reminder
        #Label(sign_up_window, text='After signing up, your face will be recorded for Face ID login',font= ("consolas",7)).place(x=8,y=120)

        #account agreement
        Label(sign_up_window, text='Creating this account, it means you agree to our user agreement.\n The agreement details can be found by this link www.docbank.hk/user_agreement',font= ("consolas",5)).place(relx=0.15,rely=0.9)

        # record the user information in the .pickle file
        btn_comfirm_sign_up = Button(sign_up_window, text='Sign Up', command=create_account)
        btn_comfirm_sign_up.place(relx=0.4, y=180)
    
# Start the GUI
login_gui = Login_GUI()
