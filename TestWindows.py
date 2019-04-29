import tkinter as tk
from tkinter import font as tkfont
from loginFunctions import *
from mongoWrapper import *
from uifunctions import *

# the server name and database that the program connects to.
serverName= r'DESKTOP-F54A5DR\SQLEXPRESS'
dbName= r"ProjectTEst"

# initalize the connection and the cursor
msSQLConnection=get_database_connection(serverName, dbName)
cursor = msSQLConnection.cursor()

# the menubar for the program
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
        representativeMenu.add_command(label='Search Active',command=lambda:SampleApp().show_frame("PageRepSearchActive") )
        representativeMenu.add_separator()
        representativeMenu.add_command(label="Majority Speaker", command=lambda: SampleApp().show_frame("PageRepMajSpkr"))
        representativeMenu.add_command(label="Minority Speaker", command=lambda: SampleApp().show_frame("PageRepMinSpkr"))
        representativeMenu.add_separator()
        representativeMenu.add_command(label="Vote", command=lambda: SampleApp().show_frame("PageRepVoteBill"))
        representativeMenu.add_command(label="Bio", command=lambda: SampleApp().show_frame("PageRepBio"))
        representativeMenu.add_command(label="Composition",command = lambda: SampleApp().show_frame("PageListComposition") )

        # --- Bill Submenu ---
        billMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Bill", menu=billMenu)
        billMenu.add_command(label="Search Bills", command=lambda:SampleApp().show_frame("BillSearch"))

    def onexit(self):
        quit()

def doNothing():
    print("ok ok I won't...")

# the apps main event loop
class SampleApp(tk.Tk):

    frames = {}
    current_frame = 0

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set the main window settings
        self.title("Ez_Gov")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("500x500+200+100")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # arrange and store all frames in the main window
        for F in (MainWindow, PageStateInfo, PageRepSearchActive,PageRepListActive,
                  PageRepMajSpkr, PageRepMinSpkr, PageRepBio,PageRepVoteBill,
                PageListComposition, BillSearch):
            page_name = F.__name__
            self.current_frame = F(parent=container, controller=self)
            self.frames[page_name] = self.current_frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")

        # show the login window
        self.show_frame("MainWindow")

    # function that brings up new frames with different functionality
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.current_frame = self.frames[page_name]
        self.current_frame.tkraise()

# the login frame
class MainWindow(tk.Frame):
    # tries to add a user, and brings up a error window if it fails
    def submit_user(self,win,user_name,password):
        connection = get_database_connection(serverName,dbName)
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

    # brings up the add user window
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

    # tries to login with the username and password specified by checking the
    #  database for the hash and username
    def login(self,parent, username,password):
        connection = get_database_connection(serverName,dbName)

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
        else:
            self.menubar = MenuBar(self, parent)
            self.controller.config(menu=self.menubar)
            self.destroy()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Federal Database", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Log Into Your Account")
        label.pack(pady=10, padx=10)

        label_1 = tk.Label(self, text="Username: ")
        label_2 = tk.Label(self, text="Password: ")
        entry_1 = tk.Entry(self)
        entry_2 = tk.Entry(self,show="*")
        login_button = tk.Button(self,text="Login",command=lambda: self.login(parent,entry_1.get(),entry_2.get()))
        add_user_button = tk.Button(self,text="Add user",command=self.add_user_win)

        label_1.pack()
        entry_1.pack()
        label_2.pack()
        entry_2.pack()
        login_button.pack()
        add_user_button.pack()

# the page that has our state info
class PageStateInfo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="State Info", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label_1 = tk.Label(self, text="State Name: ", pady=10)
        entry_1 = tk.Entry(self)

        button1 = tk.Button(self, text="Search",
                            command=lambda: self.StateQuery(entry_1.get()))
        label_1.pack()
        entry_1.pack()
        button1.pack()

    # query state info
    def StateQuery(self, txt):
        sqlString = 'SELECT count(State.SName) FROM STATE WHERE State.SName like \'' + txt + '%\''
        
        cursor.execute(sqlString)

        rows = cursor.fetchall()
        
        if rows[0][0] == 0 or rows[0][0] > 1:
            err_label = ""
            if rows[0][0] == 0:
                err_label = "No matching state found!"
            else:
                err_label = "Found more than one mathing state.\n Please search with more characters to narrow your results!"

            # spawn error Window
            err = tk.Toplevel(self)
            err_label = tk.Label(err,text = err_label)
            err_label.pack()
            close_button = tk.Button(err,text="Close",command=lambda: err.destroy())
            close_button.pack()
            return

        # get all the state info
        sqlString = 'SELECT State.disctrictCount FROM STATE WHERE State.SName like \'' + txt + '%\''
        cursor.execute(sqlString)

        rows = cursor.fetchall()

        sqlString = 'SELECT State.population FROM STATE WHERE State.SName like \'' + txt + '%\''
        cursor.execute(sqlString)

        pop_rows = cursor.fetchall()

        sqlString = sqlString = 'SELECT State.SName FROM STATE WHERE State.SName like \'' + txt + '%\''

        cursor.execute(sqlString)

        state_name = cursor.fetchall()

        # print the info that they got from the database
        list = tk.Listbox(self, height=2, width=40)
        for row in rows:
            pop = "District Count:    "
            popLabel = state_name[0][0] + " " + pop
            row = str(row[0])
            # list.insert(1, popLabel)
            list.insert(tk.END, popLabel + row)

        for row in pop_rows:
            pop = "Population:    "
            popLabel = state_name[0][0] + " " + pop
            result = str(row[0])
            list.insert(tk.END, popLabel + result)
        list.pack()

# has the tool to search for which representative is active
class PageRepSearchActive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Representative Info", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
 
        label_1 = tk.Label(self, text="First Name: ", pady=10)
        label_1.pack()

        entry_1 = tk.Entry(self)
        entry_1.pack()

        label_2 = tk.Label(self, text="Last Name: ", pady=10)
        label_2.pack()
        entry_2 = tk.Entry(self)
        entry_2.pack()

        button1 = tk.Button(self, text="Current Status",
                            command=lambda: self.RepQueryActive(entry_1.get(), entry_2.get()))

        button1.pack()

        #sqlString = 'SELECT State.disctrictCount FROM STATE WHERE State.SName=\'' + txt + '\''
        #cursor.execute(sqlString)

    # queries if the representative was active and displays if they are or not.
    def RepQueryActive(self, txt1, txt2):
        sqlString = "SELECT employee.active FROM employee WHERE employee.FName like "+"\'"+ txt1 +"%\'" + " AND employee.LName like " + "\'"+ txt2 + "%\';"   
        result = query_cursor(sqlString,cursor)

        if len(result) == 1:
            sqlString = "SELECT fname,lname FROM employee WHERE employee.FName like "+"\'"+ txt1 +"%\'" + " AND employee.LName like " + "\'"+ txt2 + "%\';"   
            rep_name = query_cursor(sqlString,cursor)
            rep_name = rep_name[0][0] + " " + rep_name[0][1]

            list = tk.Listbox(self, height=1, width=40)
            for row in result:
                if row[0] == True:
                    active_label= rep_name + " is active"
                else:
                    active_label= rep_name+ " is not active"

                list.insert(1, active_label)
            list.pack()

# this page pulls up and lists all active representatives
class PageRepListActive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Active Representatives", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        results = tk.Text(self,font=('Calibri',9))

        text_scroller = tk.Scrollbar(self,command=results.yview)
        text_scroller.pack(side='right',anchor='e',fill='y',expand=1)

        results.pack(expand=1,fill='both')

        results['yscrollcommand'] = text_scroller.set

        results.delete(1.0,tk.END)
        
        # print the names of all the active representatives
        sqlString = "SELECT employee.FNAME,employee.LName FROM employee WHERE employee.active=1"
        cursor.execute(sqlString)
        for row in cursor:
            results.insert(1.0,row[0] + " " + row[1] + "\n")

# lists the number of members of each political party
class PageListComposition(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="House Composition", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        results = tk.Text(self,font=('Calibri',10))

        text_scroller = tk.Scrollbar(self,command=results.yview)
        text_scroller.pack(side='right',anchor='e',fill='y',expand=1)

        results.pack(expand=1,fill='both')

        results['yscrollcommand'] = text_scroller.set

        results.delete(1.0,tk.END)
        
        # get all the represetnatives by parties
        sqlString = "Select count(employeeID) from employee where active=1"
        cursor.execute(sqlString)
        total_reps = cursor.fetchall()
        sqlString = "Select count(employeeID) from employee where active=1 AND  partyAffiliation = \'R\'"
        cursor.execute(sqlString)
        total_repubs = cursor.fetchall()

        sqlString = "Select count(employeeID) from employee where active = 1 AND   partyAffiliation = \'D\'"
        cursor.execute(sqlString)
        total_dems = cursor.fetchall()

        sqlString = "Select count(employeeID) from employee where active = 1 AND NOT(partyAffiliation = \'D\') and NOT(partyAffiliation = \'R\')"
        cursor.execute(sqlString)
        total_ind = cursor.fetchall()
        

        results.insert(1.0,"Number of Republican Representatives is " + str(total_repubs[0][0]) + " out of "+ str(total_reps[0][0]) + "\n")
        results.insert(1.0,"Number of Democrat Representatives is " + str(total_dems[0][0]) + " out of " + str(total_reps[0][0]) + "\n")
        results.insert(1.0,"Number of Independent Representatives is " + str(total_ind[0][0]) + " out of " + str(total_reps[0][0]) + "\n")

# displays the majority speaker if that is set
class PageRepMajSpkr(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Majority Speaker", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        sqlString = "Select employee.FName,employee.LName from employee,representative where employee.active = 1 and majoritySpeaker=1 and employee.EmployeeID = representative.EmployeeID"
        cursor.execute(sqlString)
        name = cursor.fetchall()

        result_label = tk.Label(self,text=(str(name[0][0]) + " " + str(name[0][1])) )
        result_label.pack()

# displays the minority speaker if that is set
class PageRepMinSpkr(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Minority Speaker", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        sqlString = "Select employee.FName,employee.LName from employee,representative where employee.active = 1 and minoritySpeaker=1 and employee.EmployeeID = representative.EmployeeID"
        cursor.execute(sqlString)
        name = cursor.fetchall()
        result_label = tk.Label(self,text=(str(name[0][0]) + " " + str(name[0][1])))
        result_label.pack()

# page where a user can search for a representatives vote on a bill
class PageRepVoteBill(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Representative Vote Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label_1 = tk.Label(self, text="First Name: ", pady=10)
        label_1.pack()
        entry_1 = tk.Entry(self)
        entry_1.pack()

        label_2 = tk.Label(self, text="Last Name: ", pady=10)
        label_2.pack()
        entry_2 = tk.Entry(self)
        entry_2.pack()

        label_3 = tk.Label(self, text="Bill Title: ", pady=10)
        label_3.pack()
        entry_3 = tk.Entry(self)
        entry_3.pack()

        results = tk.Text(self,font=('Calibri',9))

        button1 = tk.Button(self, text="Vote Status",
                            command=lambda: self.RepQueryVote(results,entry_1.get(), entry_2.get(), entry_3.get()))

        button1.pack()

        text_scroller = tk.Scrollbar(self,command=results.yview)
        text_scroller.pack(side='right',anchor='e',fill='y',expand=1)

        results.pack(expand=1,fill='both')

        results['yscrollcommand'] = text_scroller.set

    # search for a title in mongodb that matches the bill name, then take that id
    # and search for a vote with that.
    def RepQueryVote(self,result_box, first_name, last_name, bill_name):
        result_box.delete(1.0,tk.END)

        sql = "select billid,stat,vote.employeeID,fname,lname,partyaffiliation from vote,employee where billid like \'%" + bill_name + "%\' "
        sql += " and vote.employeeID=employee.employeeid and employee.fname like \'%" + first_name + "%\' and employee.lname like \'%"
        sql += last_name + "%\' order by billid desc"
        
        composition = []
        r_votes = { "yes" : 0, "no" : 0, "present" : 0}
        d_votes = { "yes" : 0, "no" : 0, "present" : 0}
        i_votes = { "yes" : 0, "no" : 0, "present" : 0}

        bills = query_cursor(sql,cursor)

        if len(bills) > 0:

            curr_bill_id = bills[0][0]

            result_box.insert(tk.END,"Bill Title: " + bills[0][0] + "\n")

            for bill in bills:
                
                # what to do if a new bill comes up
                if bill[0] != curr_bill_id:

                    # get results for who voted by party
                    r_votes = { "yes" : 0, "no" : 0, "present" : 0}
                    d_votes = { "yes" : 0, "no" : 0, "present" : 0}
                    i_votes = { "yes" : 0, "no" : 0, "present" : 0}

                    # sort vote by party composition
                    for  vote in composition:
                        if vote[0] == 'R':
                            if vote[1] == 'Y':
                                r_votes['yes'] +=1
                            if vote[1] == 'N':
                                r_votes['no'] +=1
                            if vote[1] == 'P':
                                r_votes['present'] +=1

                        elif vote[0] == 'D':
                            if vote[1] == 'Y':
                                d_votes['yes'] +=1
                            if vote[1] == 'N':
                                d_votes['no'] +=1
                            if vote[1] == 'P':
                                d_votes['present'] +=1

                        else:
                            if vote[1] == 'Y':
                                i_votes['yes'] +=1
                            if vote[1] == 'N':
                                i_votes['no'] +=1
                            if vote[1] == 'P':
                                i_votes['present'] +=1

                    for key in ['yes','no','present']:
                        if r_votes[key] > 0:
                            result_box.insert(tk.END,"\n " + str(r_votes[key]) + " Republicans voted " + key + ". \n")

                        if d_votes[key] > 0:
                            result_box.insert(tk.END,"\n " + str(d_votes[key]) + " Democrats voted " + key + ".")

                        if i_votes[key] > 0:
                            result_box.insert(tk.END,"\n " + str(i_votes[key]) + " Independents voted " + key + ".")

                    result_box.insert(tk.END,"-----------------------------------------------------------------------------------------------\n")
                    result_box.insert(tk.END,"Bill Title: " + bill[0] + "\n")
                    curr_bill_id = bill[0]
                    composition = []

                composition.append( (bill[5],bill[1]))
                result_box.insert(tk.END, bill[3] + " " + bill[4] + " " + " voted " + bill[1] + "\n")
            
            # get results for who voted by party
            r_votes = { "yes" : 0, "no" : 0, "present" : 0}
            d_votes = { "yes" : 0, "no" : 0, "present" : 0}
            i_votes = { "yes" : 0, "no" : 0, "present" : 0}

            # this is for the last vote, the previous loop does not account 
            # for the last loop
            for  vote in composition:
                if vote[0] == 'R':
                    if vote[1] == 'Y':
                        r_votes['yes'] +=1
                    if vote[1] == 'N':
                        r_votes['no'] +=1
                    if vote[1] == 'P':
                        r_votes['present'] +=1

                elif vote[0] == 'D':
                    if vote[1] == 'Y':
                        d_votes['yes'] +=1
                    if vote[1] == 'N':
                        d_votes['no'] +=1
                    if vote[1] == 'P':
                        d_votes['present'] +=1

                else:
                    if vote[1] == 'Y':
                        i_votes['yes'] +=1
                    if vote[1] == 'N':
                        i_votes['no'] +=1
                    if vote[1] == 'P':
                        i_votes['present'] +=1

            for key in ['yes','no','present']:
                if r_votes[key] > 0:
                    result_box.insert(tk.END,"\n " + str(r_votes[key]) + " Republicans voted " + key + ".")

                if d_votes[key] > 0:
                    result_box.insert(tk.END,"\n " + str(d_votes[key]) + " Democrats voted " + key + ".")

                if i_votes[key] > 0:
                    result_box.insert(tk.END,"\n " + str(i_votes[key]) + " Independents voted " + key + ".")
                result_box.insert(tk.END,"\n")

# lists the contact information for a representative
class PageRepBio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Representative Bio", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
 
        label_1 = tk.Label(self, text="First Name: ", pady=10)
        label_1.pack()

        entry_1 = tk.Entry(self)
        entry_1.pack()

        label_2 = tk.Label(self, text="Last Name: ", pady=10)
        label_2.pack()
        entry_2 = tk.Entry(self)
        entry_2.pack()

        text_box = tk.Listbox(self, height=8, width=40)

        button1 = tk.Button(self, text="Current Status",
                            command=lambda: self.RepQueryActive(text_box,entry_1.get(), entry_2.get()))

        button1.pack()

    # Get all the information on a representative and print it in a text box.
    def RepQueryActive(self,text_list, txt1, txt2):
        text_list.delete(0,tk.END)
        sqlString = "SELECT employee.active FROM employee WHERE employee.FName like "+"\'"+ txt1 +"%\'" + " AND employee.LName like " + "\'"+ txt2 + "%\';"   
        result = query_cursor(sqlString,cursor)

        if len(result) == 1:
            sqlString = "SELECT fname,lname,dob,partyAffiliation,phoneNum,email,occupation FROM employee WHERE employee.FName like "+"\'"+ txt1 +"%\'" + " AND employee.LName like " + "\'"+ txt2 + "%\';"   
            rep_info = query_cursor(sqlString,cursor)
            rep_name = rep_info[0][0] + " " + rep_info[0][1]
            rep = rep_info[0]

            text_list = tk.Listbox(self, height=8, width=40)
            
            text_list.insert(tk.END, "Name:              " + rep_name)
            text_list.insert(tk.END,"Date of Birth:        " + str(rep[2]))
            text_list.insert(tk.END,"Party Affiliation:     " + str(rep[3]))
            text_list.insert(tk.END,"Phone Number:     " + str(rep[4]))
            text_list.insert(tk.END,"Email                 " + str(rep[5]))
            text_list.insert(tk.END,"Occupation:       " + str(rep[6]))
            text_list.pack()
        else:
            print("Could not find a representative with that entry combination")

# the page where a user can search for bills
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
        text_box.insert(1.0,'\n---------------------------------------------------------------------------------------------------------------\n')

# returns just the bill title of a bill that matches
def getBillTitles(text_box,bill_title,bill_status,bill_sponsor,bill_date):
    bill_collection = get_bill_collection('localhost',27017)
    # clear text from dest box
    text_box.delete(1.0,tk.END)
    matches = get_matching_bills(bill_collection,bill_title,bill_date,bill_status,bill_sponsor,'')
    for bill in matches:
        text_box.insert(1.0,bill['title'])
        text_box.insert(1.0,'\n')

# starts the main app event loop
if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x500+200+100")
    app.mainloop()