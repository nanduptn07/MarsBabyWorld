import tkinter as tk
from tkinter import ttk
from dataBase import *

# ---------------------------
# Window Design
# ---------------------------
window = tk.Tk()
window.title("MARS Baby World")
window.geometry('1920x1080')
# window.attributes('-fullscreen', True)
ttk.Label(window,text="Mars Baby World",font=("times",25,"bold")).pack()

# Create database
dbObj = dataBase('marsDb.db')

# ----------------------------------------------------
#  Invoice Frame - Start
# ----------------------------------------------------

frameInv = ttk.Frame(window)
frameInv.pack(side="top",fill="x")


lblCustName = ttk.Label(frameInv,text="Customer Name",font=("times",13,"bold"))
lblCustName.grid(row=1,column=0,padx=5,pady=5)

txtCustName = ttk.Entry(frameInv,width=10,font=("times",12))
txtCustName.grid(row=1,column=1,padx=5,pady=5)

lblCustMob = ttk.Label(frameInv,text="Customer Mobile",font=("times",13,"bold"))
lblCustMob.grid(row=2,column=0,padx=5,pady=5)

txtCustMob = ttk.Entry(frameInv,width=10,font=("times",12))
txtCustMob.grid(row=2,column=1,padx=5,pady=5)

# ----------------------------------------------------
#  END of Invoice Frame
# ----------------------------------------------------



window.mainloop()
