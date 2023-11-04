import tkinter as tk
from tkinter import ttk
from dataBase import *
import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageTk
from datetime import date
from EditableTreeview import *



def inventory():
    inventoryFrame.grid(row=3,column=0,sticky="ew")
    invoiceFrame.grid_forget()
def invoice():
    inventoryFrame.grid_forget()
    invoiceFrame.grid(row=3,column=0,sticky="ew")
    
def clearTreeView():
    for item in viewTree.get_children():
        viewTree.delete(item)

def addInv():
    clearTreeView()
    if txtHSNcode.get() == "" or txtGST.get() == "" or txtDiscountPrice.get() == "" or txtProductGroup.get() == "" or txtProductType.get() == "" or txtQuantityAvail.get() == "" or txtUnitPrice.get() == "":
        messagebox.showinfo("Message", "Please provide all the fields to add Product \nBarcode is optional")
    else:
        productIdreturn = dbObj.insert_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get(),txtQuantityAvail.get(),txtDiscountPrice.get(),txtUnitPrice.get(),txtGST.get())
        genBarCode(productIdreturn)
        hsnCode = txtHSNcode.get()
        clearData()
        txtHSNcode.insert(0,hsnCode)
        viewInv()
        
def updateInv():
    if txtHSNcode.get() == "" or txtGST.get() == "" or txtDiscountPrice.get() == "" or txtProductGroup.get() == "" or txtProductType.get() == "" or txtQuantityAvail.get() == "" or txtUnitPrice.get() == "":
        messagebox.showinfo("Message", "Please provide all the fields update the product")
    else:
        dbObj.update_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get(),txtQuantityAvail.get(),txtDiscountPrice.get(),txtUnitPrice.get(),txtGST.get())
        hsnCode = txtHSNcode.get()
        clearData()
        txtHSNcode.insert(0,hsnCode)
        viewInv()

def deleteInv():
    viewTree.bind("<<TreeviewSelect>>",displaySelected)
    dbObj.delete_ProductData(txtHSNcode.get(),txtBarCode.get())
    hsnCode = txtHSNcode.get()
    clearData()
    txtHSNcode.insert(0,hsnCode)
    viewInv()

def clearData():
    txtBarCode.delete(0,tk.END)
    txtDiscountPrice.delete(0,tk.END)
    txtGST.delete(0,tk.END)
    txtHSNcode.delete(0,tk.END)
    txtProductGroup.delete(0,tk.END)
    txtProductType.delete(0,tk.END)
    txtQuantityAvail.delete(0,tk.END)
    txtUnitPrice.delete(0,tk.END) 

def viewInv():
    clearTreeView()
    if txtHSNcode.get() == "" and  txtProductGroup.get() == "" and txtProductType.get() == "" and txtBarCode.get() == "":
        messagebox.showinfo("Message", "Please provide atlease any one of HSNcode/Product Group/Product Type/Barcode")
    else:
        viewList = dbObj.view_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get())
        for vList in viewList:
            viewTree.insert("",index="end",values=(vList[0],vList[1],vList[2],vList[3],vList[4],vList[5],vList[6],vList[7]))
def viewAllInv():
    clearTreeView()
    productList = dbObj.view_Inventory()
    for prodList in productList:
        viewTree.insert("",index="end",values=(prodList[0],prodList[1],prodList[2],prodList[3],prodList[4],prodList[5],prodList[6],prodList[7]))

def displaySelected(event):
    selected = viewTree.selection()[0]
    values = viewTree.item(selected,'values')
    clearData()
    txtHSNcode.insert(0,values[0])
    txtProductGroup.insert(0,values[2])
    txtProductType.insert(0,values[3])
    txtQuantityAvail.insert(0,values[4])
    txtDiscountPrice.insert(0,values[5])
    txtUnitPrice.insert(0,values[6])
    txtGST.insert(0,values[7])
    txtBarCode.insert(0,values[1])

    # ----------------------------------------------------
    # Add widgets to the Bar frame
    # ----------------------------------------------------
    
    lblBarCodename = ttk.Label(barCodeframe,text=f"BAR Code :",font=("times",13,"bold"),background="white")
    lblBarCodename.grid(row=1,column=0,sticky="nw")

    filename = f"barcode/barcode_{txtBarCode.get()}.png"
    imagebar = Image.open(filename)
    photo = ImageTk.PhotoImage(imagebar)
    
    lblBarCodeDisplay=ttk.Label(barCodeframe,image=photo, borderwidth=2, relief="groove",width=photo.width)
    lblBarCodeDisplay.grid(row=2,column=0)


def genBarCode(productid):
    code = barcode.get('code128',productid,writer=ImageWriter())
    code.save(f'barcode/barcode_{productid}')


root = tk.Tk()
root.title("MARS Baby World")
root.geometry('1920x1080')
root.configure(bg="white")
# window.attributes('-fullscreen', True)

# Create database
dbObj = dataBase('marsDb.db')

# global variable
hsnCode = int()

# Create Frames
titleFrame=tk.Frame(root, bg='white')
subTitleFrame=tk.Frame(root, bg='white')
menuframe = tk.Frame(root, bg='white')

inventoryFrame=tk.Frame(root, bg='white')
frame = tk.Frame(inventoryFrame, bg='white')
barCodeframe = tk.Frame(inventoryFrame, bg='white')
viewTreeFrame = tk.Frame(inventoryFrame, bg='blue',bd=1)

titleFrame.grid(row=0,column=0,padx=540)
subTitleFrame.grid(row=1,column=0,padx=580,sticky="n")
menuframe.grid(row=2,column=0,pady=0,sticky="ew")

inventoryFrame.grid(row=3,column=0,sticky="ew")
frame.grid(row=0,column=0,sticky="w")
barCodeframe.grid(row=0,column=1,sticky="nw")
viewTreeFrame.grid(row=1,column=0,columnspan=2)

invoiceFrame=tk.Frame(root, bg='white')
invoiceFrame.grid(row=3,column=0,sticky="ew")
headerFrame = tk.Frame(invoiceFrame, bg='white',bd=1)
headerFrame.grid(row=1,column=0,sticky="ew")
productListFrame = tk.Frame(invoiceFrame, bg='blue',bd=1)
productListFrame.grid(row=2,column=0,columnspan=2)
detailsFrame = tk.Frame(invoiceFrame, bg='blue',bd=1)
detailsFrame.grid(row=3,column=0,sticky="ew")



lblTitle=ttk.Label(titleFrame,text="MARS BABY WORLD",font=("times",25,"bold"),background="white",foreground="#9b1c31")
lblTitle.grid(row=0,column=0,pady=5)

lblTitle=ttk.Label(subTitleFrame,text="THE BIG STORE FOR YOUR LITTLE ONES",font=("times",10,"italic","bold"),background="white",foreground="#4169e1")
lblTitle.grid(row=1,column=0)


btnInventory = tk.Button(menuframe,borderwidth=10,activebackground="#DEFFE9",text="INVENTORY",command=inventory,bg='white',fg="green",font=("times",14,"bold"),border=0,relief='groove')
btnInventory.grid(row=1,column=0,padx=10)
btnInvoice = tk.Button(menuframe,activebackground='#FFEEDF',text="Invoice",command=invoice,bg='white',fg="#F88C2D",font=("times",14,"bold"),border=0,relief="ridge")
btnInvoice.grid(row=1,column=1,padx=10)

inventoryFrame.grid_forget()
invoiceFrame.grid_forget()

# ----------------------------------------------------
# Add widgets to the frame
# ----------------------------------------------------

lblHSNcode = ttk.Label(frame,text="HSN Code",font=("times",13,"bold"),background="white")
lblHSNcode.grid(row=1,column=0,padx=5,pady=5)

txtHSNcode = ttk.Entry(frame,width=4,font=("times",12),textvariable=hsnCode)
txtHSNcode.grid(row=1,column=1,padx=5,pady=5,sticky="w")

lblProductGroup = ttk.Label(frame,text="Product Group",font=("times",13,"bold"),background="white")
lblProductGroup.grid(row=2,column=0,padx=5,pady=5)

txtProductGroup  = ttk.Entry(frame,width=40,font=("times",12))
txtProductGroup.grid(row=2,column=1,padx=5,pady=5)

lblProductType = ttk.Label(frame,text="Product Type",font=("times",13,"bold"),background="white")
lblProductType.grid(row=3,column=0,padx=5,pady=5)

txtProductType  = ttk.Entry(frame,width=40,font=("times",12))
txtProductType.grid(row=3,column=1,padx=5,pady=5)

lblQunatityAvail = ttk.Label(frame,text="Quantity Available",font=("times",13,"bold"),background="white")
lblQunatityAvail.grid(row=4,column=0,padx=5,pady=5)

txtQuantityAvail  = ttk.Entry(frame,width=40,font=("times",12))
txtQuantityAvail.grid(row=4,column=1,padx=5,pady=5)

lblDiscountPrice = ttk.Label(frame,text="Discount Price",font=("times",13,"bold"),background="white")
lblDiscountPrice.grid(row=5,column=0,padx=5,pady=5)

txtDiscountPrice  = ttk.Entry(frame,width=40,font=("times",12))
txtDiscountPrice.grid(row=5,column=1,padx=5,pady=5)

lblUnitPrice = ttk.Label(frame,text="Unit Price",font=("times",13,"bold"),background="white")
lblUnitPrice.grid(row=6,column=0,padx=5,pady=5)

txtUnitPrice = ttk.Entry(frame,width=40,font=("times",12))
txtUnitPrice.grid(row=6,column=1,padx=5,pady=5)

lblGST = ttk.Label(frame,text="GST",font=("times",13,"bold"),background="white")
lblGST.grid(row=7,column=0,padx=5,pady=5)

txtGST  = ttk.Entry(frame,width=40,font=("times",12))
txtGST.grid(row=7,column=1,padx=5,pady=5)

lblBarCode = ttk.Label(frame,text="Bar Code - optional",font=("times",13),background="white")
lblBarCode.grid(row=8,column=0,padx=5,pady=5)

txtBarCode  = ttk.Entry(frame,width=40,font=("times",12))
txtBarCode.grid(row=8,column=1,padx=5,pady=5)

btnFrame = tk.Frame(frame,bg="white")
btnFrame.grid(columnspan=10)

viewAllButton = ttk.Button(btnFrame,text="Inventory",width=10,command=viewAllInv)
viewAllButton.grid(row=8,column=1,padx=5,pady=5)

viewButton = ttk.Button(btnFrame,text="View",width=10,command=viewInv)
viewButton.grid(row=8,column=2,padx=5,pady=5)

clearButton = ttk.Button(btnFrame,text="Clear",width=10,command=clearData)
clearButton.grid(row=8,column=3,padx=5,pady=5)

addButton = ttk.Button(btnFrame,text="Add",width=10,command=addInv)
addButton.grid(row=8,column=4,padx=5,pady=5)

updateButton = ttk.Button(btnFrame,text="Update",width=10,command=updateInv)
updateButton.grid(row=8,column=5,padx=5,pady=5)

deleteButton = ttk.Button(btnFrame,text="Delete",width=10,command=deleteInv)
deleteButton.grid(row=8,column=6,padx=5,pady=5)


# ----------------------------------------------------
# Add widgets to the Treeframe
# ----------------------------------------------------

viewTree = ttk.Treeview(viewTreeFrame)
viewTree.pack(side="left",fill="x")
viewTree["columns"] = ("HSN Code","Product ID","Product Group","Product Type","Quantity","Max. Discount Price","Unit Price","GST")

vScrolBar = ttk.Scrollbar(viewTreeFrame,orient="vertical",command=viewTree.yview)
viewTree.configure(xscrollcommand = vScrolBar.set)


viewTree.column("#0",width=0,stretch=False)
viewTree.column("#1",width=100)
viewTree.column("#2",width=150)
viewTree.column("#3",width=200)
viewTree.column("#4",width=400)
viewTree.column("#5",width=100)
viewTree.column("#6",width=150)
viewTree.column("#7",width=150)
viewTree.column("#8",width=100)

viewTree.heading("#0",text="")
viewTree.heading("#1",text="HSN Code")
viewTree.heading("#2",text="Product ID")
viewTree.heading("#3",text="Product Group")
viewTree.heading("#4",text="Product Type")
viewTree.heading("#5",text="Quantity")
viewTree.heading("#6",text="Max Discount Price")
viewTree.heading("#7",text="Unit Price")
viewTree.heading("#8",text="GST")

viewTree.bind("<<TreeviewSelect>>",displaySelected)


#############################################
# INVOICE FRAME
#############################################


# productList = ttk.Treeview(productListFrame)
# productList.pack(side="left",fill="x")


column_names=("Sno","Product","Quantity","Unit Price","GST","Max. Discount Price","Total")
productList = EditableTreeview(productListFrame,columns=column_names)
productList.pack(fill=tk.BOTH,expand=True)

productList.heading("#0",text="")
productList.column("#0",width=0,stretch=False)
productList.heading("Sno",text="Sno")
productList.heading("Product",text="Product")
productList.heading("Quantity",text="Quantity")
productList.heading("Unit Price",text="Unit Price")
productList.heading("GST",text="GST")
productList.heading("Max. Discount Price",text="Max. Discount Price")
productList.heading("Total",text="Total")

productList.insert("",index=tk.END,values=("1","soap","3","43","5","3","129"))
productList.bind("<Double-1>",productList.onDoubleClick)


txtInvNo="2023/0001"
lblInvoiceNo =ttk.Label(headerFrame,text="Invoice Number",font=("times",13,"bold"),background="white")
lblInvoiceNo.pack(side='left')
# lblInvoiceNo.grid(row=0,column=0,padx=5,pady=5,sticky="w")
txtInvoiceNo = ttk.Label(headerFrame,text=f'{txtInvNo}',width=20,font=("times",12)).pack(side='left')
# txtInvoiceNo.grid(row=0,column=1,padx=5,pady=5,sticky="w")

txtDate=date.today()
lblDateToday =ttk.Label(headerFrame,text="Date",font=("times",13,"bold"),background="white").pack(side='left')
# lblDateToday.grid(row=0,column=4,padx=5,pady=5,sticky="w")
txtDateToday = ttk.Label(headerFrame,text=f'{txtDate}',width=20,font=("times",12)).pack(side='left')
# txtDateToday.grid(row=0,column=5,padx=5,pady=5,sticky="w")


lblCustName =ttk.Label(detailsFrame,text="Customer Name",font=("times",13,"bold"),background="white")
lblCustName.grid(row=1,column=0,padx=5,pady=5)
txtCustName  = ttk.Entry(detailsFrame,width=20,font=("times",12))
txtCustName.grid(row=1,column=1,padx=5,pady=5)

lblCustMob =ttk.Label(detailsFrame,text="Customer Mobile",font=("times",13,"bold"),background="white")
lblCustMob.grid(row=2,column=0,padx=5,pady=5)
txtCustMob  = ttk.Entry(detailsFrame,width=20,font=("times",12))
txtCustMob.grid(row=2,column=1,padx=5,pady=5)

lblActualPrice =ttk.Label(detailsFrame,text="Actual Price",font=("times",13,"bold"),background="white")
lblActualPrice.grid(row=3,column=0,padx=5,pady=5)
txtActualPrice  = ttk.Entry(detailsFrame,width=20,font=("times",12))
txtActualPrice.grid(row=3,column=1,padx=5,pady=5)

lblTotalDiscount =ttk.Label(detailsFrame,text="Total Discount",font=("times",13,"bold"),background="white")
lblTotalDiscount.grid(row=4,column=0,padx=5,pady=5)
txtTotalDiscount  = ttk.Entry(detailsFrame,width=20,font=("times",12))
txtTotalDiscount.grid(row=4,column=1,padx=5,pady=5)

lblFinalPrice =ttk.Label(detailsFrame,text="Final Price",font=("times",13,"bold"),background="white")
lblFinalPrice.grid(row=5,column=0,padx=5,pady=5)
txtFinalPrice  = ttk.Entry(detailsFrame,width=20,font=("times",12))
txtFinalPrice.grid(row=5,column=1,padx=5,pady=5)

lblPayTerm =ttk.Label(detailsFrame,text="Pay Term",font=("times",13,"bold"),background="white")
lblPayTerm.grid(row=6,column=0,padx=5,pady=5)

clicked = tk.StringVar()
clicked.set("Select")
drop=ttk.OptionMenu(detailsFrame,clicked,"Select","CASH","GPAY","PAYTM")
drop.grid(row=6,column=1,padx=5,pady=5)




root.mainloop()
