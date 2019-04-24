import tkinter as tk
from tkinter import font as tkfont
from loginFunctions import *
from mongoWrapper import *

db_server= r'DESKTOP-F54A5DR\SQLEXPRESS'
db_database= r"ProjectTEst"

class MenuBar(tk.Menu):
    def __init__(self, parent, controller):
        tk.Menu.__init__(self, controller)
        self.controller = controller

        # --- File Submenu ---
        fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=2, command=self.onexit)

        # --- State Submenu ---
        stateMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="State", underline=0, menu=stateMenu)
        stateMenu.add_command(label="Info", command=lambda: SampleApp().show_frame("PageStateInfo"))

        # --- Representative Submenu ---
        representativeMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Representative", menu=representativeMenu)
        representativeMenu.add_command(label="List Active", command=lambda: SampleApp().show_frame("PageRepListActive"))
        representativeMenu.add_separator()
        representativeMenu.add_command(label="Majority Speaker", command=lambda: SampleApp().show_frame("PageRepMajSpkr"))
        representativeMenu.add_command(label="Minority Speaker", command=lambda: SampleApp().show_frame("PageRepMinSpkr"))
        representativeMenu.add_separator()
        representativeMenu.add_command(label="Bio", command=lambda: SampleApp().show_frame("PageRepBio"))
        representativeMenu.add_command(label="Contact", command=lambda: SampleApp().show_frame("PageRepContact"))

        # --- Sefnator Submenu ---
        senatorMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Senator", menu=senatorMenu)
        senatorMenu.add_command(label="List Active", command=lambda: SampleApp().show_frame("PageSenListActive"))
        senatorMenu.add_separator()
        senatorMenu.add_command(label="Bio", command=lambda: SampleApp().show_frame("PageSenBio"))
        senatorMenu.add_command(label="Contact", command=lambda: SampleApp().show_frame("PageSenContact"))

        # --- Bill Submenu ---
        billMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Bill", menu=billMenu)
        billMenu.add_command(label="Search Bills", command=lambda:SampleApp().show_frame("BillSearch"))

    def onexit(self):
        quit()

def doNothing():
    print("ok ok I won't...")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("500x500+200+100")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainWindow, PageStateInfo, PageRepListActive,
                  PageRepMajSpkr, PageRepMinSpkr, PageRepBio, PageRepContact,
                  PageSenListActive, PageSenBio, PageSenContact, BillSearch):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainWindow")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MainWindow(tk.Frame):
    
    def submit_user(self,win,user_name,password):
        connection = get_database_connection(db_server,db_database)
        added = add_user(connection.cursor(),user_name,password)
        if added:
            win.destroy()
            added_win = tk.Toplevel(self)
            added_label =tk.Label(added_win,text="User was added successfully")
            added_label.pack()
            close_button = tk.Button(added_win,text="Close",command=lambda: added_win.destroy())
            close_button.pack()
        else:
            err = tk.Toplevel(self)
            err_label = tk.Label(err,text = "That user is already in the database!")
            err_label.pack()
            close_button = tk.Button(err,text="Close",command=lambda: err.destroy())
            close_button.pack()

    def add_user_win(self):
        win = tk.Toplevel(self)
        user_label = tk.Label(win, text="Username: ")
        pass_label = tk.Label(win, text="Password: ")

        user_entry = tk.Entry(win)
        pass_entry = tk.Entry(win,show="*")
        
        user_label.pack()
        user_entry.pack()

        pass_label.pack()
        pass_entry.pack()
        
        submit_button = tk.Button(win,text="Submit",command=lambda: self.submit_user(win, user_entry.get(),pass_entry.get()) )
        submit_button.pack()

    def login(self, username,password):
        connection = get_database_connection(db_server,db_database)

        if not connection:
            return False
        
        cursor = connection.cursor()

        if not user_login(cursor,username,password):
            errWin = tk.Toplevel(self)
            errWin.wm_title("Error!")
            label = tk.Label(errWin,text="Login Failed, Username or Password were incorrect")
            label.pack(side='top',fill='both',expand=True)
            exit_button = tk.Button(errWin,text="Close",command=lambda:errWin.destroy())
            exit_button.pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.menubar = MenuBar(self, parent)
        self.controller.config(menu=self.menubar)



        label = tk.Label(self, text="Federal Database", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Log Into Your Account")
        label.pack(pady=10, padx=10)

        label_1 = tk.Label(self, text="Username: ")
        label_2 = tk.Label(self, text="Password: ")
        entry_1 = tk.Entry(self)
        entry_2 = tk.Entry(self,show="*")
        login_button = tk.Button(self,text="Login",command=lambda: self.login(entry_1.get(),entry_2.get()))
        add_user_button = tk.Button(self,text="Add user",command=self.add_user_win)

        label_1.pack()
        entry_1.pack()
        label_2.pack()
        entry_2.pack()
        login_button.pack()
        add_user_button.pack()

        button1 = tk.Button(self, text="Start new test",
                            command=lambda: controller.show_frame("NewTestWindow"))
        button1.pack()


class PageStateInfo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="State Info", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()

class PageRepListActive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Active Representatives", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageRepMajSpkr(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Majority Speaker", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageRepMinSpkr(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Minority Speaker", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

class PageRepBio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Representative's Bio", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageRepContact(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Representative's Contact Information", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageSenListActive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Active Senators", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageSenBio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Senator's Bio", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class PageSenContact(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Senator's Contact Information", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

class BillSearch(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        #set the grid to expand
        tk.Grid.columnconfigure(self,1,weight=1)
        tk.Grid.rowconfigure(self,5,weight=1)

        title_label = tk.Label(self,text="Bill Title:")
        title_label.grid(row=0,column=0,stick='w')
        title_entry = tk.Entry(self)
        title_entry.grid(row=0,column=1,stick='ew')

        status_label = tk.Label(self,text="Bill Status:")
        status_label.grid(row=1,column=0,sticky='w')
        status_entry = tk.Entry(self)
        status_entry.grid(row=1,column=1,sticky='ew')
        
        sponsor_label = tk.Label(self,text="Bill Sponsor:")
        sponsor_label.grid(row='2',sticky='w')
        sponsor_entry = tk.Entry(self)
        sponsor_entry.grid(row='2',column='1',sticky='ew')

        date_label = tk.Label(self,text="Bill Date:")
        date_label.grid(row='3',sticky='w')
        date_entry = tk.Entry(self)
        date_entry.grid(row='3',column='1',sticky='ew')

        results = tk.Text(self,font=('Calibri',9))

        search_title_button = tk.Button(self,text="Search Bill Titles",command =lambda: getBillTitles(results,title_entry.get(),status_entry.get(),sponsor_entry.get(),date_entry.get()))
        search_title_button.grid(row=4,column=0)

        search_bill_button= tk.Button(self,text="Search Bills",command =lambda: getBillResults(results,title_entry.get(),status_entry.get(),sponsor_entry.get(),date_entry.get()))
        search_bill_button.grid(row=4,column=1,stick=tk.W)

        results.grid(row=5,column=0,columnspan=2,sticky='news')

        text_scroller = tk.Scrollbar(self,command=results.yview)

        text_scroller.grid(row=5,column=2,sticky='ens')
        results['yscrollcommand'] = text_scroller.set

# gets the full text of a bill that matches
def getBillResults(text_box,bill_title,bill_status,bill_sponsor,bill_date):
    # clear text from dest box
    text_box.delete(1.0,tk.END)
    print("not done yet")

    bill_collection = get_bill_collection('localhost',27017)

    matches = get_matching_bills(bill_collection,bill_title,bill_date,bill_status,bill_sponsor,'')
    for bill in matches:

        
        text_box.insert(1.0,bill['text'])
        text_box.insert(1.0,'\n\nBill Text:')

        text_box.insert(1.0,bill['date'])
        text_box.insert(1.0,'\n\nAction Date: ')

        text_box.insert(1.0,bill['status'])
        text_box.insert(1.0,'\n\nStatus: ')

        text_box.insert(1.0,bill['title'])
        text_box.insert(1.0,'Bill Title:\n')

# returns just the bill title of a bill that matches
def getBillTitles(text_box,bill_title,bill_status,bill_sponsor,bill_date):
    bill_collection = get_bill_collection('localhost',27017)
    # clear text from dest box
    text_box.delete(1.0,tk.END)
    matches = get_matching_bills(bill_collection,bill_title,bill_date,bill_status,bill_sponsor,'')
    for bill in matches:
        text_box.insert(1.0,bill['title'])
        text_box.insert(1.0,'\n')


if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x500+200+100")
    app.mainloop()