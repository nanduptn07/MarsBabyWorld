import tkinter as tk
from tkinter import ttk
from dataBase import *
from datetime import date,datetime
from EditableTreeview import *
import os
import shutil
import jinja2
import pdfkit
import subprocess
import os
# import wkhtmltopdf 

class main():
    def landingPrice(lprice):
        code = "SFLAMINGOE"
        word = ""
        lp = str(lprice)
        for i in range(0,len(lp)):
            word =  word + code[int(lp[i])] 
        return word
    
    def invoice_open():
        pdf_file_path = f"invoices\{txtInvNo}.pdf"

        if os.path.exists(pdf_file_path):
            if os.name=="nt":
                subprocess.run(['start','',pdf_file_path],shell=True)
            else:
                messagebox.showinfo("Message","Please manually open the file to print")
        else:
            messagebox.showinfo("Message","file not found")

    def inventory():
        invoiceFrame.grid_forget()
        invoiceDetailsFrame.grid_forget()
        dayClosingFrame.grid_forget()
        inventoryFrame.grid(row=3,column=0,sticky="ew")


    def invoice():
        inventoryFrame.grid_forget()
        invoiceDetailsFrame.grid_forget()
        dayClosingFrame.grid_forget()
        invoiceFrame.grid(row=3,column=0,sticky="ew")

    def invoiceDetails():
        inventoryFrame.grid_forget()
        invoiceFrame.grid_forget()
        dayClosingFrame.grid_forget()
        invoiceDetailsFrame.grid(row=3,column=0,sticky="ew")
    
    def dayClosing():
        inventoryFrame.grid_forget()
        invoiceFrame.grid_forget()
        invoiceDetailsFrame.grid_forget()
        dayClosingFrame.grid(row=3,column=0,sticky="ew")

    def loginEnter(event):
        main.login()
        
    def login():
        global loginFlag
        inventoryFrame.grid_forget()
        invoiceFrame.grid_forget()
        invoiceDetailsFrame.grid_forget()
        dayClosingFrame.grid_forget()
        if txtUserID.get() == "abdul" and txtPassword.get() == "Marsadmin":
            loginFlag = 1
            messagebox.showinfo("Message","WELCOME, ABDUL!")
            loginFrame.grid_forget()
            menuframe.grid(row=2,column=0,pady=0,sticky="ew")
            btnInventory.grid(row=1,column=0,padx=10)
            btnInvoice.grid(row=1,column=1,padx=10)
            btnInvoiceDetails.grid(row=1,column=2,padx=10)
            btnDayClosing.grid(row=1,column=3,padx=10)
            btnLogOut.grid(row=1,column=10,padx=10)
            inventoryFrame.grid(row=3,column=0,sticky="ew")
        elif txtUserID.get() == "mars" and txtPassword.get() == "Mars1234":
            loginFlag = 0
            loginFrame.grid_forget()
            menuframe.grid(row=2,column=0,pady=0,sticky="ew")
            btnInvoice.grid(row=1,column=1,padx=10)
            btnInvoiceDetails.grid(row=1,column=2,padx=10)
            btnLogOut.grid(row=1,column=10,padx=10)
            btnInventory.grid_forget()
            btnDayClosing.grid_forget()
            invoiceFrame.grid(row=3,column=0,sticky="ew")
            messagebox.showinfo("Message","WELCOME, Mars Baby world!")
        else:
            messagebox.showinfo("Message","Sorry, Incorrect Credentials!")
            txtUserID.delete(0,tk.END)
            txtPassword.delete(0,tk.END)

            
    def logOut():
        inventoryFrame.grid_forget()
        invoiceFrame.grid_forget()
        invoiceDetailsFrame.grid_forget()
        dayClosingFrame.grid_forget()
        menuframe.grid_forget()
        if loginFlag >1:
            messagebox.showinfo("Message","Please Sign In")
        else:
            messagebox.showinfo("Message","Signed Out -Successfully!")
        loginFrame.grid(row=3,column=0,sticky="ew")
        txtUserID.delete(0,tk.END)
        txtPassword.delete(0,tk.END)

    
    def clearTreeView():
        for item in viewTree.get_children():
            viewTree.delete(item)
            

    def addInv():
        main.clearTreeView()
        if txtHSNcode.get() == "" or txtGST.get() == "" or txtDiscountPrice.get() == "" or txtProductGroup.get() == "" or txtProductType.get() == "" or txtQuantityAvail.get() == "" or txtUnitPrice.get() == "" or txtLanding.get() =="":
            messagebox.showinfo("Message", "Please provide all the fields to add Product \nBarcode is optional")
        else:
            productIdreturn = dbObj.insert_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get(),txtQuantityAvail.get(),txtDiscountPrice.get(),txtLanding.get(),txtUnitPrice.get(),txtGST.get())
            main.genBarCode(productIdreturn)
            hsnCode = txtHSNcode.get()
            main.clearData()
            txtHSNcode.insert(0,hsnCode)
            main.viewInv()
            
    def updateInv():
        if txtHSNcode.get() == "" or txtGST.get() == "" or txtDiscountPrice.get() == "" or txtProductGroup.get() == "" or txtProductType.get() == "" or txtQuantityAvail.get() == "" or txtUnitPrice.get() == "" or txtLanding.get() =="":
            messagebox.showinfo("Message", "Please provide all the fields to update the product")
        else:
            dbObj.update_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get(),txtQuantityAvail.get(),txtDiscountPrice.get(),txtLanding.get(),txtUnitPrice.get(),txtGST.get())
            hsnCode = txtHSNcode.get()
            main.clearData()
            txtHSNcode.insert(0,hsnCode)
            main.viewInv()

    def deleteInv():
        viewTree.bind("<<TreeviewSelect>>",main.displaySelected)
        dbObj.delete_ProductData(txtHSNcode.get(),txtBarCode.get())
        hsnCode = txtHSNcode.get()
        main.clearData()
        txtHSNcode.insert(0,hsnCode)
        main.viewInv()

    def clearData():
        txtBarCode.delete(0,tk.END)
        txtDiscountPrice.delete(0,tk.END)
        txtGST.delete(0,tk.END)
        txtHSNcode.delete(0,tk.END)
        txtProductGroup.delete(0,tk.END)
        txtProductType.delete(0,tk.END)
        txtQuantityAvail.delete(0,tk.END)
        txtUnitPrice.delete(0,tk.END) 
        txtLanding.delete(0,tk.END)

    def viewInv():
        main.clearTreeView()
        if txtHSNcode.get() == "" and  txtProductGroup.get() == "" and txtProductType.get() == "" and txtBarCode.get() == "" and txtQuantityAvail == "":
            messagebox.showinfo("Message", "Please provide atlease any one of HSNcode/Product Group/Product Type/Barcode")
        else:
            viewList = dbObj.view_ProductData(txtHSNcode.get(),txtBarCode.get(),txtProductGroup.get(),txtProductType.get(),txtQuantityAvail.get())
            for vList in viewList:
                viewTree.insert("",index="end",values=(vList[0],vList[1],vList[2],vList[3],vList[4],vList[5],vList[6],vList[7],vList[8]))
    def viewAllInv():
        main.clearTreeView()
        productLists = dbObj.view_Inventory()
        for prodList in productLists:
            viewTree.insert("",index="end",values=(prodList[0],prodList[1],prodList[2],prodList[3],prodList[4],prodList[5],prodList[6],prodList[7],prodList[8]))

    def displaySelected(event):
        selected = viewTree.selection()[0]
        values = viewTree.item(selected,'values')
        main.clearData()
        txtHSNcode.insert(0,values[0])
        txtProductGroup.insert(0,values[2])
        txtProductType.insert(0,values[3])
        txtQuantityAvail.insert(0,values[4])
        txtDiscountPrice.insert(0,values[5])
        txtLanding.insert(0,values[6])
        txtUnitPrice.insert(0,values[7])
        txtGST.insert(0,values[8])
        txtBarCode.insert(0,values[1])
    

    def on_subscribe():
        return

    def clearProducts():
        for item in productListAdd.get_children():
            productListAdd.delete(item)

    def viewBarProduct(event):
        main.clearProducts()
        if clickedProd.get() == 'Bar Code':
            prodList = dbObj.view_ProductData("",txtGetProd.get(),"","","")
            if prodList == []:
                messagebox.showinfo("Message","Please provide a Valid Barcode or Add the Bar code in INVENTORY")
            else:
             #   values = []
             #   for rowid in productList.get_children():
             #       values.append(productList.item(rowid)['values'])
             #   foundflag = 'n'
             #   for product in values:
             #       if prodList[0][3]==product[1]:
             #           foundflag = 'y'
             #   if foundflag = 'n':
                    productList.insert("",index="end",values=(prodList[0][3],prodList[0][0],"1",prodList[0][7],prodList[0][6],prodList[0][8],prodList[0][5],"0"))



        if clickedProd.get() == 'Product':  
                viewGetList = dbObj.get_ProductData(txtGetProd.get())
                if viewGetList == []:
                    messagebox.showinfo("Message", "Please provide Valid Product Name or Add the new product to INVENTORY")
                for vList in viewGetList:
                    productListAdd.insert("",index="end",values=(vList))

    def viewProducts():
        main.clearProducts()
        if clickedProd.get() != 'Product':
            messagebox.showinfo("Message", "Please choose Product for searching Products")
        if txtGetProd.get() == "":
            messagebox.showinfo("Message", "Please provide Product Name")
        else :
            if clickedProd.get() == 'Product':  
                viewGetList = dbObj.get_ProductData(txtGetProd.get())
                if viewGetList == []:
                    messagebox.showinfo("Message", "Please provide Valid Product Name or Add the new product to INVENTORY")
                for vList in viewGetList:
                    productListAdd.insert("",index="end",values=(vList))

    def addToCart(event):
        # selectedProd = productListAdd.selection()[0]
        # listprod = viewTree.item(selectedProd,'values') 
        selectedProd = productListAdd.focus()
        values = productListAdd.item(selectedProd,'values')
        if clickedProd.get() == 'Product':
            prodList = dbObj.view_ProductData("","","",values[0],"")
        else:
            prodList = dbObj.view_ProductData("",txtGetProd.get(),"","","")
        productList.insert("",index="end",values=(prodList[0][3],prodList[0][0],"0",prodList[0][7],main.landingPrice(prodList[0][6]),prodList[0][8],prodList[0][5],"0"))
    def addToCart2():
        # selectedProd = productListAdd.selection()[0]
        # listprod = viewTree.item(selectedProd,'values') 
        selectedProd = productListAdd.focus()
        values = productListAdd.item(selectedProd,'values')
        if clickedProd.get() == 'Product':
            prodList = dbObj.view_ProductData("","","",values[0],"")
        else:
            prodList = dbObj.view_ProductData("",txtGetProd.get(),"","","")
        productList.insert("",index="end",values=(prodList[0][3],prodList[0][0],"0",prodList[0][7],main.landingPrice(prodList[0][6]),prodList[0][8],prodList[0][5],"0"))

    def removeFromCart():
        selected = productList.selection()[0]
        productList.delete(selected)
        main.updateTotal()

    def updateTotals(event):
        values = []
        for rowid in productList.get_children():
            values.append(productList.item(rowid)['values'])
        FinalPrice = 0.00
        TotalDiscount = 0.0
        StateGST = 0.0
        CentralGST = 0.0
        ActualPrice = 0.0
        totalGST = 0.0
        for product in values:
            ActualPrice = round(ActualPrice + (product[2]*product[3]),2)
            gst = product[7]* (product[5]/100)
            totalGST = round(gst + totalGST,2)
            FinalPrice = FinalPrice + product[7]
        TotalDiscount = ActualPrice - FinalPrice
        StateGST = round(totalGST / 2,2)
        CentralGST = round(totalGST / 2,2)
        txtFinalPrice.config(text=f"{FinalPrice}")
        txtTotalDiscount.config(text=f"{TotalDiscount}")
        txtStateGST.config(text=f"{StateGST}")
        txtCentralGST.config(text=f"{CentralGST}")
        txtActualPrice.config(text=f"{ActualPrice}")

    def updateTotal():
            values = []
            for rowid in productList.get_children():
                values.append(productList.item(rowid)['values'])
            FinalPrice = 0.00
            TotalDiscount = 0.0
            StateGST = 0.0
            CentralGST = 0.0
            ActualPrice = 0.0
            totalGST = 0.0
            for product in values:
                ActualPrice = round(ActualPrice + (product[2]*product[3]),2)
                gst = product[7]* (product[5]/100)
                totalGST = round(gst + totalGST,2)
                FinalPrice = FinalPrice + product[7]
            TotalDiscount = ActualPrice - FinalPrice
            StateGST = round(totalGST / 2,2)
            CentralGST = round(totalGST / 2,2)
            txtFinalPrice.config(text=f"{FinalPrice}")
            txtTotalDiscount.config(text=f"{TotalDiscount}")
            txtStateGST.config(text=f"{StateGST}")
            txtCentralGST.config(text=f"{CentralGST}")
            txtActualPrice.config(text=f"{ActualPrice}")

    def generateInv():
        invoiceMax = dbObj.get_InvoiceNumber(date.today().strftime("%y%m%d"))
        if invoiceMax[0][0] == None:
            invNumber= txtDate.strftime("%y%m%d")+'0001'
        else:
            invNumber = invoiceMax[0][0] + 1
        return invNumber
    
    def viewInvDetails():
        main.clearInvDetails()
        invoiceDet = dbObj.view_InvoiceDetails(txtInvNum.get(),txtCusMobile.get())
        prevInvNumber = 0
        prevtotal = 0
        totalval = []
        for prodList in invoiceDet:
            if prodList[0] != prevInvNumber and prevInvNumber != 0:
                totalval.append((prevInvNumber,prevtotal))
                prevtotal = 0            
            prevInvNumber = prodList[0]
            prevtotal = prevtotal + prodList[7]
            totalval.append((prevInvNumber,prevtotal))

        prevInvNumber = 0
        for prodList in invoiceDet:

            if prodList[0] != prevInvNumber:
                for value in totalval:
                    if prodList[0] == value[0]:
                        total = value[1]
                invoiceList.insert("","end",iid=prodList[0],values=(prodList[0],prodList[1],"","","","","",total),tags="parent")
            
            invoiceList.insert(prodList[0],index="end",values=("","",prodList[2],prodList[3],prodList[4],prodList[5],prodList[6],prodList[7]))
            prevInvNumber = prodList[0]

    def clearInvDetails():
        for item in invoiceList.get_children():
            invoiceList.delete(item)

    def clearClosingDetails():
        for item in closingList.get_children():
            closingList.delete(item)

    def refreshprice():
        main.updateTotal()
    
    def resetscreen():
        main.clearScreen()

    def checkCustDetails(self):
        custDetail = dbObj.checkCust(txtCustMob.get())
        if custDetail == []:
                messagebox.showinfo("Message","Its New Customer. Please provide Name & confirm subscribtion to ADD CUSTOMER")
                txtCustName.delete(0,tk.END)
                checkBox_var.set(0)
        else:
            txtCustName.delete(0,tk.END)
            txtCustName.insert(0,custDetail[0][1])
            if custDetail[0][3] == "yes":
                checkBox_var.set(1)
            
    def clearScreen():
        global txtInvNo
        txtFinalPrice.config(text="0.0")
        txtTotalDiscount.config(text="0.0")
        txtStateGST.config(text="0.0")
        txtCentralGST.config(text="0.0")
        txtActualPrice.config(text="0.0")
        txtGetProd.delete(0,tk.END)
        txtCustMob.delete(0,tk.END)
        txtCustName.delete(0,tk.END)
        for item in productList.get_children():
            productList.delete(item)
        for item in productListAdd.get_children():
            productListAdd.delete(item)
        txtInvNo = main.generateInv()
        lblInvoiceNo.config(text=f"Invoice Number : {txtInvNo}")
        lblDateToday.config(text=f"Date : {date.today()}")
        clickedProd.set("Bar Code")
        clicked.set("CASH")
        checkBox_var.set(0)
        
        
    def genBill():
        buyItems = []
        for item in productList.get_children():
            buyItems.append(productList.item(item)['values'])
        dbObj.updateCust(txtCustMob.get(),txtCustName.get(),txtInvNo,clicked.get())
        qun = dbObj.insert_InvoiceData(txtInvNo,buyItems,clicked.get())
        if qun == 0:
            return
        else:
            main.genPDF(buyItems)
            messagebox.showinfo("Message","Invoice Generated. Opening the INVOICE...")
            main.invoice_open()
            main.clearScreen()
            
            

    def genPDF(items):
        sno = 0
        addrow = ""
        for product in items:
            sno+=1
            prdX = f"<tr><td style='text-align: center;'>{sno}</td><td>{product[0]}</td><td style='text-align: center;'>{product[1]}</td><td style='text-align: center;'>{product[2]}</td><td style='text-align: center;'>{product[3]}</td><td style='text-align: center;'>{product[6]}</td><td style='text-align: center;'>{product[7]}</td></tr>"
            addrow = addrow + prdX
        context= {'cust_name':txtCustName.get(),
                  "cust_mobile":txtCustMob.get(),
                  "invNum":txtInvNo,
                  "date":date.today(),
                  "pay":clicked.get(),
                  "addrow":addrow,
                  "Final": txtFinalPrice.cget("text"),
                  "Actual":txtActualPrice.cget("text"),
                  "Disc":txtTotalDiscount.cget("text"),
                  "CGST":txtCentralGST.cget("text"),
                  "SGST":txtStateGST.cget("text")}
                  

        template_loader = jinja2.FileSystemLoader('./')
        tem_env = jinja2.Environment(loader=template_loader)

        template = tem_env.get_template("bill.html")
        output_text = template.render(context)
        options={'page-size':'A5',"enable-local-file-access": ""}
         
        config = pdfkit.configuration(wkhtmltopdf="./wkhtmltopdf.exe")
        # wkhtmltopdf.WKhtmlToPdf(header)s
        pdfkit.from_string(output_text,f'invoices/{txtInvNo}.pdf',configuration=config,options=options)

        return


    def getClosing(*args):
        main.clearClosingDetails()
        if clickedDay.get() == "Today":
            div = 1
            todayclosing = dbObj.view_InvoiceDetails(date.today().strftime("%y%m%d"),"")
        elif clickedDay.get() == "Month":
            div = 10000
            todayclosing = dbObj.view_InvoiceDetails(date.today().strftime("%y%m"),"")
        elif clickedDay.get() == "Year":
            div = 1000000
            todayclosing = dbObj.view_InvoiceDetails(date.today().strftime("%y"),"")
        elif clickedDay.get() == "Annual":
            div = 100000000
            todayclosing = dbObj.view_InvoiceDetails("","")
        main.getTodayClosing(todayclosing,div)

    def getTodayClosing(closing,d):
        prevInvNumber = 0
        prevtotal = 0
        preLanding = 0
        totalval = []
        for prodList in closing:
            compare = round(prodList[0]/d)
            if compare != prevInvNumber and prevInvNumber != 0:
                totalval.append((prevInvNumber,prevtotal,preLanding))
                prevtotal = 0      
                preLanding = 0      
            prevInvNumber = compare
            preLanding = preLanding + (prodList[3]*int(prodList[5]))
            prevtotal = prevtotal + prodList[7]
        totalval.append((prevInvNumber,prevtotal,preLanding))

        totalFinal = 0
        totalLanding = 0
        totalProfit = 0
        prevInvNumber = 0
        for prodList in closing:
            compare = round(prodList[0]/d)
            if compare != prevInvNumber:
                for value in totalval:
                    if compare == value[0]:
                        total = value[1]
                        landing = value[2]
                        profit = total - landing
                        totalFinal = value[1] + totalFinal
                        totalLanding = value[2] + totalLanding
                        totalProfit = profit + totalProfit
                closingList.insert("","end",iid=compare,values=(compare,"","","","",landing,"","",total,profit),tags="parent")
            if d == 1:
                closingList.insert(compare,index="end",values=("",prodList[1],prodList[2],prodList[3],prodList[4],prodList[5],prodList[6],prodList[7],""),)
            else:
                closingList.insert(compare,index="end",values=(prodList[0],prodList[1],prodList[2],prodList[3],prodList[4],prodList[5],prodList[6],prodList[7],""),)
            
            prevInvNumber = compare
        
        lblFinalCloPrice.config(text=f"{totalFinal}")
        lblFinalLanPrice.config(text=f"{totalLanding}")
        lblFinalProfitPrice.config(text=f"{totalProfit}")

    def closeTheDay():
        source_file = 'marsDb.db'
        destination_dir = 'C:/MARS App/BackupdB'
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        filename = os.path.basename(source_file)
        destination_path = os.path.join(destination_dir, f'{date.today()}_'+filename)
        shutil.copy(source_file, destination_path)



if  __name__== "__main__":
    root = tk.Tk()
    root.title("MARS Baby World")
    root.geometry('1920x1080')
    root.configure(bg="white")
    # root.iconbitmap("images\logo.jpg")
    # window.attributes('-fullscreen', True)


    destination_dir = 'C:/MARS App/logo'
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        source_file = 'images\marslogo.JPG'
        filename = os.path.basename(source_file)
        destination_path = os.path.join(destination_dir,filename)
        shutil.copy(source_file, destination_path)

    # Create database
    dbObj = dataBase('marsDb.db')

    # global variable
    hsnCode = int()
    loginFlag = 2
    # Create Frames
    titleFrame=tk.Frame(root, bg='white')
    subTitleFrame=tk.Frame(root, bg='white')
    menuframe = tk.Frame(root, bg='white')

    loginFrame = tk.Frame(root, bg='white')
    loginFrame.grid(row=3,column=0,sticky="ew")

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
    productListFrame = tk.Frame(invoiceFrame, bg='white',bd=1)
    productListFrame.grid(row=3,column=0,columnspan=2)
    detailsFrame = tk.Frame(invoiceFrame, bg='white',bd=1)
    detailsFrame.grid(row=2,column=0,sticky="ew")

    productListFrame1 = tk.Frame(productListFrame, bg='white',bd=1)
    productListFrame1.grid(row=0,column=0,columnspan=2)
    productListFrame2 = tk.Frame(productListFrame, bg='blue',bd=1)
    productListFrame2.grid(row=1,column=0,columnspan=2)

    invoiceDetailsFrame=tk.Frame(root, bg='white')
    invoiceDetailsFrame.grid(row=3,column=0,sticky="ew")

    dayClosingFrame=tk.Frame(root, bg='white')
    dayClosingFrame.grid(row=3,column=0,sticky="ew")


    lblTitle=ttk.Label(titleFrame,text="MARS BABY WORLD",font=("times",25,"bold"),background="white",foreground="#9b1c31")
    lblTitle.grid(row=0,column=0,pady=5)

    lblTitle=ttk.Label(subTitleFrame,text="THE BIG STORE FOR YOUR LITTLE ONES",font=("times",10,"italic","bold"),background="white",foreground="#4169e1")
    lblTitle.grid(row=1,column=0)

    btnInventory = tk.Button(menuframe,borderwidth=10,activebackground="#DEFFE9",text="INVENTORY",command=main.inventory,bg='white',fg="#3e5810",font=("times",14,"bold"),border=0,relief='groove')
    btnInvoice = tk.Button(menuframe,activebackground='#fcd4aa',text="INVOICE",command=main.invoice,bg='white',fg="#e84f04",font=("times",14,"bold"),border=0,relief="ridge")
    btnInvoiceDetails = tk.Button(menuframe,activebackground='#acc3e6',text="INV DETAILS",command=main.invoiceDetails,bg='white',fg="#05164b",font=("times",14,"bold"),border=0,relief="ridge")
    btnDayClosing = tk.Button(menuframe,activebackground='#FFEEDF',text="DAY CLOSING",command=main.dayClosing,bg='white',fg="#fc1208",font=("times",14,"bold"),border=0,relief="ridge")
    btnLogOut = tk.Button(menuframe,activebackground='#FFEEDF',text="Sign Out",command=main.logOut,bg='white',fg="#c49307",font=("times",11,"bold"),border=0,relief="ridge")

    llblUserID = ttk.Label(loginFrame,font=("times",20,"bold"),text="Credentials Please !",background="white",foreground="#002263")
    llblUserID.grid(row=1,column=0,pady=10,padx=10,columnspan=4)

    lblUserID = ttk.Label(loginFrame,font=("times",12,"bold"),text="User ID",background="white",foreground="#cd2d3f")
    lblUserID.grid(row=2,column=0,pady=10,padx=10)
    txtUserID = ttk.Entry(loginFrame,font=("times",12))
    txtUserID.grid(row=2,column=2,pady=10,padx=10)
    lblPassword = ttk.Label(loginFrame,font=("times",12,"bold"),text="Password",background="white",foreground="#cd2d3f")
    lblPassword.grid(row=3,column=0,pady=10,padx=10)
    txtPassword = ttk.Entry(loginFrame,font=("times",12),show="*")
    txtPassword.grid(row=3,column=2,pady=10,padx=10)
    txtPassword.bind("<Return>",main.loginEnter)
    btnLogin = tk.Button(loginFrame,text="Login",command=main.login,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='#ffdb99',fg="#e59400",font=("times",14,"bold"),border=0,relief='groove')
    btnLogin.grid(row=4,column=0,sticky="ewns",columnspan=4,pady=10,padx=10)
    
    inventoryFrame.grid_forget()
    invoiceFrame.grid_forget()
    invoiceDetailsFrame.grid_forget()
    dayClosingFrame.grid_forget()
    menuframe.grid_forget()
    loginFrame.grid(row=3,column=0,sticky="ew")
    
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

    lblLanding = ttk.Label(frame,text="Landing",font=("times",13,"bold"),background="white")
    lblLanding.grid(row=6,column=0,padx=5,pady=5)

    txtLanding  = ttk.Entry(frame,width=40,font=("times",12))
    txtLanding.grid(row=6,column=1,padx=5,pady=5)

    lblUnitPrice = ttk.Label(frame,text="Unit Price",font=("times",13,"bold"),background="white")
    lblUnitPrice.grid(row=7,column=0,padx=5,pady=5)

    txtUnitPrice = ttk.Entry(frame,width=40,font=("times",12))
    txtUnitPrice.grid(row=7,column=1,padx=5,pady=5)

    lblGST = ttk.Label(frame,text="GST",font=("times",13,"bold"),background="white")
    lblGST.grid(row=8,column=0,padx=5,pady=5)

    txtGST  = ttk.Entry(frame,width=40,font=("times",12))
    txtGST.grid(row=8,column=1,padx=5,pady=5)

    lblBarCode = ttk.Label(frame,text="Bar Code - optional",font=("times",13),background="white")
    lblBarCode.grid(row=9,column=0,padx=5,pady=5)

    txtBarCode  = ttk.Entry(frame,width=40,font=("times",12))
    txtBarCode.grid(row=9,column=1,padx=5,pady=5)

    btnFrame = tk.Frame(frame,bg="white")
    btnFrame.grid(columnspan=10)

    viewAllButton = tk.Button(btnFrame,text="Inventory",width=10,command=main.viewAllInv,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#3e5810",font=("times",14,"bold"),border=0,relief='groove')
    viewAllButton.grid(row=0,column=1,padx=5,pady=5)

    viewButton = tk.Button(btnFrame,text="View",width=10,command=main.viewInv,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#6d362b",font=("times",14,"bold"),border=0,relief='groove')
    viewButton.grid(row=0,column=2,padx=5,pady=5)

    clearButton = tk.Button(btnFrame,text="Clear",width=10,command=main.clearData,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#ffab00",font=("times",14,"bold"),border=0,relief='groove')
    clearButton.grid(row=0,column=3,padx=5,pady=5)

    addButton = tk.Button(btnFrame,text="Add",width=10,command=main.addInv,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#3e5810",font=("times",14,"bold"),border=0,relief='groove')
    addButton.grid(row=0,column=4,padx=5,pady=5)

    updateButton = tk.Button(btnFrame,text="Update",width=10,command=main.updateInv,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#e84f04",font=("times",14,"bold"),border=0,relief='groove')
    updateButton.grid(row=0,column=5,padx=5,pady=5)

    deleteButton = tk.Button(btnFrame,text="Delete",width=10,command=main.deleteInv,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='white',fg="#ba1200",font=("times",14,"bold"),border=0,relief='groove')
    deleteButton.grid(row=0,column=6,padx=5,pady=5)

    # ----------------------------------------------------
    # Add widgets to the Treeframe
    # ----------------------------------------------------


    style = ttk.Style()
    # style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 12,'bold')) # Modify the font of the headings

    viewTree = ttk.Treeview(viewTreeFrame,style="mystyle.Treeview")
    viewTree.pack(side="left",fill="x")
    viewTree["columns"] = ("HSN Code","Product ID","Product Group","Product Type","Quantity","Discount Price","Landing","Unit Price","GST")

    vScrolBar = ttk.Scrollbar(viewTreeFrame,orient="vertical",command=viewTree.yview)
    viewTree.configure(xscrollcommand = vScrolBar.set)


    viewTree.column("#0",width=0,stretch=False)
    viewTree.column("#1",width=100,anchor="center")
    viewTree.column("#2",width=150,anchor="center")
    viewTree.column("#3",width=200)
    viewTree.column("#4",width=300)
    viewTree.column("#5",width=100,anchor="center")
    viewTree.column("#6",width=150,anchor="center")
    viewTree.column("#7",width=100,anchor="center")
    viewTree.column("#8",width=150,anchor="center")
    viewTree.column("#9",width=100,anchor="center")
    
    viewTree.heading("#0",text="")
    viewTree.heading("#1",text="HSN Code")
    viewTree.heading("#2",text="Product ID")
    viewTree.heading("#3",text="Product Group")
    viewTree.heading("#4",text="Product Type")
    viewTree.heading("#5",text="Quantity")
    viewTree.heading("#6",text="Max Discount Price")
    viewTree.heading("#7",text="Landing")
    viewTree.heading("#8",text="Unit Price")
    viewTree.heading("#9",text="GST")

    viewTree.bind("<<TreeviewSelect>>",main.displaySelected)


    #############################################
    # INVOICE FRAME
    #############################################


    # productList = ttk.Treeview(productListFrame)
    # productList.pack(side="left",fill="x")




    column_names=("Product","HSN","Quantity","Unit Price","Landing","GST","Discounted Price","Total")
    productList = EditableTreeview(productListFrame2,columns=column_names,style="mystyle.Treeview")
    productList.pack(fill=tk.BOTH,expand=True)

    productList.heading("#0",text="")
    productList.heading("Product",text="Product")
    productList.heading("HSN",text="HSN")
    productList.heading("Quantity",text="Quantity")
    productList.heading("Unit Price",text="MRP")
    productList.heading("Landing",text="Landing")
    productList.heading("GST",text="GST(%)")
    productList.heading("Discounted Price",text="Discounted Price")
    productList.heading("Total",text="Total")

    productList.column("#0",width=0,stretch=False)
    productList.column("#1",width=300)
    productList.column("#2",width=100,anchor="center")
    productList.column("#3",width=150,anchor="center")
    productList.column("#4",width=150,anchor="center")
    productList.column("#5",width=150,anchor="center")
    productList.column("#6",width=150,anchor="center")
    productList.column("#7",width=200,anchor="center")
    productList.column("#8",width=200,anchor="center")

    # productList.insert("",index=tk.END,values=("1","<product>","","","","","",""))
    productList.bind("<Return>",main.updateTotals)
    txtDate=date.today()
    txtInvNo = main.generateInv()
    lblInvoiceNo = ttk.Label(headerFrame,text=f"Invoice Number : {txtInvNo}",font=("times",13,"bold"),background="white")
    lblInvoiceNo.pack(side='left',pady=5)
    lblDateToday = ttk.Label(headerFrame,text=f"Date : {txtDate}",font=("times",13,"bold"),background="white")
    lblDateToday.pack(side='left',pady=5,padx=30)
    


    lblCustName =ttk.Label(detailsFrame,text="Customer Name",font=("times",13,"bold"),background="white")
    lblCustName.grid(row=1,column=0,padx=5,pady=5)
    txtCustName  = ttk.Entry(detailsFrame,width=20,font=("times",12))
    txtCustName.grid(row=1,column=1,padx=5,pady=5)
    
    lblCustMob =ttk.Label(detailsFrame,text="Customer Mobile",font=("times",13,"bold"),background="white")
    lblCustMob.grid(row=2,column=0,padx=5,pady=5)
    txtCustMob  = ttk.Entry(detailsFrame,width=20,font=("times",12))
    txtCustMob.grid(row=2,column=1,padx=5,pady=5)
    txtCustMob.bind("<Return>",main.checkCustDetails) 

    checkBox_var = tk.IntVar()
    lblSubscibe = tk.Checkbutton(detailsFrame,text="Subscribe",variable=checkBox_var,font=("times",13,"bold"),background="white",command=main.on_subscribe)
    lblSubscibe.grid(row=1,column=2,padx=5,pady=5)
    
    clickedProd = tk.StringVar()
    clickedProd.set("Bar Code")
    lblGetProd =tk.OptionMenu(detailsFrame,clickedProd,"Bar Code","Product")
    lblGetProd.grid(row=1,column=4,padx=10)
    lblGetProd.configure(background="white",font=("times",10,"bold"),activebackground="white",foreground="#0B7C95")
    # lblGetProd.configure()  (font=("times",13,"bold"),background="white")
    txtGetProd = ttk.Entry(detailsFrame,font=("times",12),width=60)
    txtGetProd.grid(row=1,column=5,columnspan=3,sticky="ew")
    txtGetProd.bind("<Return>",main.viewBarProduct)
    btnGetProd = tk.Button(detailsFrame,text="Get Product",command=main.viewProducts,
                             activebackground="#FDDE96",activeforeground="#FF8300",
                             bg='white',fg="#FF8300",font=("times",11,"bold"),border=0,relief='groove')
    btnGetProd.grid(row=1,column=8)

    txtCustRating = ttk.Label(detailsFrame,width=20,font=("times",12),background="white")
    txtCustRating.grid(row=1,column=3,padx=5,pady=5)

    lblPayTerm =ttk.Label(detailsFrame,text="Pay Term",font=("times",13,"bold"),background="white")
    lblPayTerm.grid(row=2,column=4)

    clicked = tk.StringVar()
    clicked.set("CASH")
    drop=tk.OptionMenu(detailsFrame,clicked,"CASH","GPAY","PAYTM","CREDIT")
    drop.grid(row=2,column=5)
    # drop.config(background="white")
    drop.configure(background="white",font=("times",10,'bold'),activebackground="white",foreground="#0B7C95")

    columnList=("Product")
    productListAdd = ttk.Treeview(detailsFrame,columns=columnList,style="mystyle.Treeview")
    productListAdd.grid(row=2,column=6,rowspan=3,columnspan=4)
    productListAdd.heading("#0",text="")
    productListAdd.column("#0",width=0,stretch=False)
    productListAdd.heading("Product",text="Products")
    productListAdd.column("Product",width=400)
    productListAdd.bind("<Return>",main.addToCart)
    productListAdd.bind("<Double-1>",main.addToCart)

      
      
    resetButton = tk.Button(detailsFrame,text="Reset",width=10,command=main.resetscreen,
                             borderwidth=10,activebackground="#a6ffa4",activeforeground="green",
                             bg='#DEFFE1',fg="yellow",font=("times",14,"bold"),border=0,relief='groove')
    resetButton.grid(row=2,column=2,padx=5,pady=5)
    
    refreshButton = tk.Button(detailsFrame,text="Refresh",width=10,command=main.refreshprice,
                             borderwidth=10,activebackground="#a6ffa4",activeforeground="green",
                             bg='#DEFFE1',fg="green",font=("times",14,"bold"),border=0,relief='groove')
    refreshButton.grid(row=2,column=3)
    
    lblActualPrice =ttk.Label(detailsFrame,text="Actual Price",font=("times",13,"bold"),background="white")
    lblActualPrice.grid(row=3,column=0,padx=5,pady=5)
    txtActualPrice  = ttk.Label(detailsFrame,text="0.0",font=("times",12),background="white")
    txtActualPrice.grid(row=3,column=1,padx=5,pady=5)

    lblFinalPrice =ttk.Label(detailsFrame,text="Final Price",font=("times",20,"bold"),background="white",anchor="center")
    lblFinalPrice.grid(row=3,column=2,sticky="ewns",columnspan=2,rowspan=2)
    txtFinalPrice  = ttk.Label(detailsFrame,text="0.0",font=("times",50),background="white",anchor="center")
    txtFinalPrice.grid(row=3,column=4,sticky="ewns",columnspan=2,rowspan=2)

    lblTotalDiscount =ttk.Label(detailsFrame,text="Total Discount",font=("times",13,"bold"),background="white")
    lblTotalDiscount.grid(row=4,column=0,padx=5,pady=5)
    txtTotalDiscount = ttk.Label(detailsFrame,text="0.0",font=("times",12),background="white")
    txtTotalDiscount.grid(row=4,column=1,padx=5,pady=5)

    lblStateGST =ttk.Label(detailsFrame,text="S.GST",font=("times",13,"bold"),background="white")
    lblStateGST.grid(row=5,column=0,padx=5,pady=5)
    txtStateGST = ttk.Label(detailsFrame,text="0.0",font=("times",12),background="white")
    txtStateGST.grid(row=5,column=1,padx=5,pady=5)

    lblCentralGST =ttk.Label(detailsFrame,text="C.GST",font=("times",13,"bold"),background="white")
    lblCentralGST.grid(row=6,column=0,padx=5,pady=5)
    txtCentralGST = ttk.Label(detailsFrame,text="0.0",font=("times",12),background="white")
    txtCentralGST.grid(row=6,column=1,padx=5,pady=5)

    btnAddProd = tk.Button(detailsFrame,text="Add To Cart",command=main.addToCart2,
                             borderwidth=10,activebackground="#bae556",activeforeground="green",
                             bg="#DEFFE1",fg="green",font=("times",14,"bold"),border=0
                             ,relief='groove')
    btnAddProd.grid(row=5,column=6,sticky="ewns",columnspan=4)

    btnDelProd = tk.Button(detailsFrame,text="Remove From Cart",command=main.removeFromCart,
                             borderwidth=10,activebackground="#ff7f7f",activeforeground="red",
                             bg='#FFEED0',fg="red",font=("times",14,"bold"),border=0,relief='groove')
    btnDelProd.grid(row=6,column=6,sticky="ewns",columnspan=4)

    genBilButton = tk.Button(detailsFrame,text="Generate Bill",width=10,command=main.genBill,
                             borderwidth=10,activebackground="#ffb732",activeforeground="#FF8300",
                             bg='#ffdb99',fg="#e59400",font=("times",14,"bold"),border=0,relief='groove')
    genBilButton.grid(row=5,column=2,sticky="ewns",columnspan=4,rowspan=2)

    # printBillButton = ttk.Button(detailsFrame,text="Print Bill",width=10,command=main.invoice_open)
    # printBillButton.grid(row=5,column=4,sticky="ewns",columnspan=2,rowspan=2)

    # WhatsappBillButton = ttk.Button(detailsFrame,text="Whatsapp Bill",width=10,command=main.clearData)
    # WhatsappBillButton.grid(row=5,column=6,sticky="ewns",columnspan=2,rowspan=2)

    # dbObj.insert_InvoiceData()

    #############################################
    # INVOICE DETALS FRAME
    #############################################
    lblInvNum = ttk.Label(invoiceDetailsFrame,text="Invoice Number(YYMMDD*)",font=("times",13,"bold"),background="white")
    lblInvNum.grid(row=0,column=0,padx=5,pady=5)
    txtInvNum = ttk.Entry(invoiceDetailsFrame,width=40,font=("times",12))
    txtInvNum.grid(row=0,column=1,padx=5,pady=5)

    lblCusMobile = ttk.Label(invoiceDetailsFrame,text="Customer Number",font=("times",13,"bold"),background="white")
    lblCusMobile.grid(row=1,column=0,padx=5,pady=5)
    txtCusMobile = ttk.Entry(invoiceDetailsFrame,width=40,font=("times",12))
    txtCusMobile.grid(row=1,column=1,padx=5,pady=5)

    lblOr = ttk.Label(invoiceDetailsFrame,text="or",font=("times",13,"bold"),background="white")
    lblOr.grid(row=0,column=2,padx=5,pady=5,sticky="w")

    getInvDButton = tk.Button(invoiceDetailsFrame,text="Invoice Details",width=10,command=main.viewInvDetails,
                             borderwidth=10,activebackground="#9fc5e8",activeforeground="#3d85c6",
                             bg='#cfe2f3',fg="#16537e",font=("times",14,"bold"),border=0,relief='groove')
    getInvDButton.grid(row=2,column=0,sticky="ewns",columnspan=2)

    column_invoice=("Invoice Num","Pay Term","Product","Quantity","Unit Price","Landing","Discount Price","Total")
    invoiceList = ttk.Treeview(invoiceDetailsFrame,columns=column_invoice,style="mystyle.Treeview")
    invoiceList.grid(row=3,column=0,columnspan=10)

    invoiceList.heading("#0",text="")
    invoiceList.heading("Invoice Num",text="Invoice No.")
    invoiceList.heading("Pay Term",text="Pay Term")
    invoiceList.heading("Product",text="Product")
    invoiceList.heading("Quantity",text="Quantity")
    invoiceList.heading("Unit Price",text="MRP")
    invoiceList.heading("Landing",text="Landing")
    invoiceList.heading("Discount Price",text="Discount Price")
    invoiceList.heading("Total",text="Total")

    invoiceList.column("#0",width=0,stretch=False)
    invoiceList.column("#1",width=100,anchor="center")
    invoiceList.column("#2",width=100,anchor="center")
    invoiceList.column("#3",width=300)
    invoiceList.column("#4",width=150,anchor="center")
    invoiceList.column("#5",width=150,anchor="center")
    invoiceList.column("#6",width=150,anchor="center")
    invoiceList.column("#7",width=200,anchor="center")
    invoiceList.column("#8",width=200,anchor="center")


    invoiceList.tag_configure("parent",font=("times",11,"bold"),foreground="red")



    #############################################
    # INVOICE DETALS FRAME
    #############################################



    closingDetails = tk.Frame(dayClosingFrame, bg='white')
    closingDetails.grid(row=0,column=0,sticky="ew")

    clickedDay = tk.StringVar()
    clickedDay.set("<select>")
    lblclosing = ttk.Label(closingDetails,text="Choose Report Type",font=("times",13,"bold"),background="white",)
    lblclosing.grid(row=0,column=0,padx=10,pady=20)
    lblGetProd =tk.OptionMenu(closingDetails,clickedDay,"<select>","Today","Month","Year","Annual")
    lblGetProd.grid(row=0,column=1,padx=10,pady=20)
    lblGetProd.configure(background="white",font=("times",10,'bold'),activebackground="white",foreground="#0B7C95")
    clickedDay.trace("w",main.getClosing)

    
    column_closing=("Invoice Num","Pay Term","Product","Quantity","MRP","Landing","Selling Price","Product Price","Invoice Total","Profit")
    closingList= ttk.Treeview(closingDetails,columns=column_closing,style="mystyle.Treeview")
    closingList.grid(row=1,column=0,columnspan=10)

    closingList.heading("#0",text="")
    closingList.heading("Invoice Num",text="Invoice No.")
    closingList.heading("Pay Term",text="Pay Term")
    closingList.heading("Product",text="Product")
    closingList.heading("Quantity",text="Quantity")
    closingList.heading("MRP",text="MRP")
    closingList.heading("Landing",text="Landing")
    closingList.heading("Selling Price",text="Discount Price")
    closingList.heading("Product Price",text="Product Price")
    closingList.heading("Invoice Total",text="Invoice Total")
    closingList.heading("Profit",text="Profit")

    closingList.column("#0",width=0,stretch=False)
    closingList.column("#1",width=100,anchor="center")
    closingList.column("#2",width=100,anchor="center")
    closingList.column("#3",width=200)
    closingList.column("#4",width=100,anchor="center")
    closingList.column("#5",width=100,anchor="center")
    closingList.column("#6",width=100,anchor="center")
    closingList.column("#7",width=150,anchor="center")
    closingList.column("#8",width=200,anchor="center")
    closingList.column("#9",width=200,anchor="center")
    closingList.column("#10",width=100,anchor="center")


    lblFinalClosing = ttk.Label(closingDetails,text="Final Closing Price",font=("times",13,"bold"),background="white",)
    lblFinalClosing.grid(row=2,column=0,padx=10,pady=20)
    lblFinalCloPrice = ttk.Label(closingDetails,text="",font=("times",13,"bold"),background="white",)
    lblFinalCloPrice.grid(row=2,column=1,padx=10,pady=20)
    lblFinalLanding = ttk.Label(closingDetails,text="Total Landing Price",font=("times",13,"bold"),background="white",)
    lblFinalLanding.grid(row=3,column=0,padx=10,pady=20)
    lblFinalLanPrice = ttk.Label(closingDetails,text="",font=("times",13,"bold"),background="white",)
    lblFinalLanPrice.grid(row=3,column=1,padx=10,pady=20)
    lblFinalProfit = ttk.Label(closingDetails,text="Total Profit",font=("times",13,"bold"),background="white",)
    lblFinalProfit.grid(row=4,column=0,padx=10,pady=20)
    lblFinalProfitPrice = ttk.Label(closingDetails,text="",font=("times",13,"bold"),background="white",)
    lblFinalProfitPrice.grid(row=4,column=1,padx=10,pady=20)
    btnClose = tk.Button(closingDetails,text="Done For The Day",command=main.closeTheDay,
                             borderwidth=10,activebackground="#bae556",activeforeground="green",
                             bg="#DEFFE1",fg="green",font=("times",14,"bold"),border=0
                             ,relief='groove')
    btnClose.grid(row=3,column=4,sticky="ewns",columnspan=2,pady=10,padx=10,rowspan=2)
    








root.mainloop()
