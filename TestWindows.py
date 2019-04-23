import tkinter as tk
from tkinter import font as tkfont


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

        # --- Senator Submenu ---
        senatorMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Senator", menu=senatorMenu)
        senatorMenu.add_command(label="List Active", command=lambda: SampleApp().show_frame("PageSenListActive"))
        senatorMenu.add_separator()
        senatorMenu.add_command(label="Bio", command=lambda: SampleApp().show_frame("PageSenBio"))
        senatorMenu.add_command(label="Contact", command=lambda: SampleApp().show_frame("PageSenContact"))

        # --- Bill Submenu ---
        billMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Bill", menu=billMenu)
        billMenu.add_command(label="Description", command=doNothing)
        billMenu.add_command(label="Text", command=doNothing)
        billMenu.add_command(label="Status", command=doNothing)

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
                  PageSenListActive, PageSenBio, PageSenContact):
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
        entry_2 = tk.Entry(self)

        label_1.pack()
        entry_1.pack()
        label_2.pack()
        entry_2.pack()

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


if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x500+200+100")
    app.mainloop()