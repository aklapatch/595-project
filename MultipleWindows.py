import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import tkinter.messagebox

LARGE_FONT = ("Verdona", 12)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)


        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # An empty dictionary
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]

        # raise frame to the front
        frame.tkraise()

#def qf(param):
#    print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg="Ghost White")


        ''''# *** Toolbar ***

        toolbar = Frame(self, bg="grey")

        insertButt = Button(toolbar, text="Insert Image", command=doNothing())
        insertButt.pack(side=LEFT, padx=2, pady=2)
        printButt = Button(toolbar, text="Print", command=doNothing)
        printButt.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)'''
        # --- End Tool Bar ---

        label = tk.Label(self, text="Log Into Your Account", font=LARGE_FONT, bg="Ghost White")
        label.pack(pady=10, padx=10)
        #label.grid(row=0, column=1, sticky="nw", padx=150, pady=1)

        #button1 = tk.Button(self, text="Visit Page 1",
        #                   command=lambda: qf("See this worked"))
        #button1.grid(row=1, column=1)
        button1 = tk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(PageOne))
        #button1.grid(row=4, column=1)
        button1.pack()

        button2 = tk.Button(self, text="Visit Page Two",
                           command=lambda: controller.show_frame(PageTwo))
        #button2.grid(row=5, column=1)
        button2.pack()

        label_1 = tk.Label(self, text="Username :")
        label_2 = tk.Label(self, text="Password :")
        entry_1 = tk.Entry(self)
        entry_2 = tk.Entry(self)

        #label_1.grid(row=6, column=0, sticky="e")
        #label_2.grid(row=7, column=0, sticky="e")
        label_1.pack()
        entry_1.pack()
        label_2.pack()
        entry_2.pack()

        #entry_1.grid(row=6, column=1)
        #entry_2.grid(row=7, column=1)

        # *** List Box for Scroller ***

        # txt1=scrolledtext.ScrolledText(app,height=20,width=10,yscrollcommand=tk.scroll.set)
        list = Listbox(self, width=30)
        # list.grid(column=0, columnspan=2, row=15, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
        list.pack(padx=10, pady=50)
        list.insert(tkinter.END, "hello")
        list.insert(tkinter.END, "hello1")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                           command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                           command=lambda: controller.show_frame(PageTwo))
        button2.pack()





class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 2", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


def doNothing():
    print("ok ok I won't...")


app = SeaofBTCapp()

app.title("Congressional Database")
app.geometry("500x500+200+100")
#app.config(bg="cadet blue")

# ---

menu = tk.Menu(app)
app.config(menu=menu)
fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Exit", command=app.quit)

stateMenu = tk.Menu(menu)
menu.add_cascade(label="State", menu=stateMenu)
stateMenu.add_command(label="Info", command=doNothing)

representativeMenu = tk.Menu(menu)
menu.add_cascade(label="Representative", menu=representativeMenu)
representativeMenu.add_command(label="List Active", command=doNothing)
representativeMenu.add_separator()
representativeMenu.add_command(label="Majority Speaker", command=doNothing)
representativeMenu.add_command(label="Minority Speaker", command=doNothing)
representativeMenu.add_separator()
representativeMenu.add_command(label="Bio", command=doNothing)
representativeMenu.add_command(label="Contact", command=doNothing)

senatorMenu = tk.Menu(menu)
menu.add_cascade(label="Senator", menu=senatorMenu)
senatorMenu.add_command(label="List Active", command=doNothing)
senatorMenu.add_separator()
senatorMenu.add_command(label="Bio", command=doNothing)
senatorMenu.add_command(label="Contact", command=doNothing)

billMenu = tk.Menu(menu)
menu.add_cascade(label="Senator", menu=billMenu)
billMenu.add_command(label="List Active", command=doNothing)
billMenu.add_command(label="Bio", command=doNothing)
billMenu.add_command(label="Contact", command=doNothing)

'''
# *** List Box for Scroller ***

#txt1=scrolledtext.ScrolledText(app,height=20,width=10,yscrollcommand=tk.scroll.set)
list = Listbox(app, width=30)
#list.grid(column=0, columnspan=2, row=15, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
list.pack(padx=10,pady=50)
list.insert(tkinter.END, "hello")
list.insert(tkinter.END, "hello1")
'''

# *** Status Bar ***

status = Label(app, text="United States of America", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)


app.mainloop()


#root = Tk()

#root.geometry("500x500+200+100")

#root.mainloop()