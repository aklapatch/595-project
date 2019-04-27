import tkinter as tk
from tkinter import font as tkfont

def genErrorWindow(tk_root,err_message,Button_text):
  errWin = tk.Toplevel(tk_root)
  errWin.wm_title("Error!")
  label = tk.Label(errWin,text=err_message)
  label.pack(side='top',fill='both',expand=True)
  exit_button = tk.Button(errWin,text=Button_text,command=lambda:errWin.destroy())
  exit_button.pack()