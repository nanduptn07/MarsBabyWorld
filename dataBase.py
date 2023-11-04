import sqlite3
from tkinter import messagebox

class dataBase:
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.c = self.con.cursor()

        # self.c.execute("""
        #     DROP TABLE invoice 
        # """)
        # self.con.commit()

        # self.c.execute("""
        #     DROP TABLE cust
        # """)
        # self.con.commit()

        # Create Tables if not exists
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS cust(
                cust_mob    INTEGER  NOT NULL,
                cust_name   TEXT     NOT NULL,
                invoice_num INTEGER  NOT NULL,
                subscribe   TEXT     NOT NULL,
                PRIMARY KEY(cust_mob,invoice_num)
            )
        """)
        self.con.commit()


        self.c.execute("""
            CREATE TABLE IF NOT EXISTS product(
                HSN_code         INTERGER NOT NULL,
                product_id       INTEGER  NOT NULL,
                product_group    TEXT     NOT NULL,
                product_type     TEXT     NOT NULL,
                quantity_avail   INTEGER  NOT NULL, 
                discount_price   DECIMAL  NOT NULL,
                landing_price    TEXT     NOT NULL,
                unit_price       DECIMAL  NOT NULL,
                gst              DECIMAL  NOT NULL,
                PRIMARY KEY(HSN_code,product_id)
            )
        """)
        self.con.commit()


        self.c.execute("""
            CREATE TABLE IF NOT EXISTS invoice(
                invoice_num      INTERGER NOT NULL,
                product_type     TEXT     NOT NULL,
                quantity         INTEGER  NOT NULL,
                MRP              TEXT     NOT NULL,
                discount_price   DECIMAL  NOT NULL,        
                total_price      DECIMAL  NOT NULL,
                pay_term         TEXT     NOT NULL, 

                PRIMARY KEY(invoice_num,product_type)
            )
        """)
        self.con.commit()


    # Fetch the data from tables 
    def view_Inventory(self):
        result = self.c.execute("SELECT * FROM product")
        fetchedData = []
        for row in result:
            fetchedData.append(row)
        return fetchedData

    # Inventory Management
    def insert_ProductData(self,hsnCode,product_id,prodGroup,prodType,quantity_avail,discountPrice,landing_price,unitPrice,gst):
        if product_id == "":
            count_query = ("SELECT count(*) FROM product where HSN_code = ? GROUP BY HSN_code;")
            self.c.execute(count_query,(hsnCode,))
            prod_count_list = self.c.fetchone()
            if prod_count_list == None: 
                prod_count = 1
            else :
                prod_count = prod_count_list[0] + 1
                
            sql = """
                    INSERT INTO product VALUES(?,?,?,?,?,?,?,?,?)
                """
            try:
                prod_id = str(hsnCode) + str(prod_count).zfill(5)
                self.c.execute(sql,(hsnCode,prod_id,prodGroup,prodType,quantity_avail,discountPrice,landing_price,unitPrice,gst))
            except  sqlite3.IntegrityError:
                messagebox.showinfo("Message",f"Product/Barcode - {product_id}, already available")
            else:
                if sqlite3.Error.__class__.__name__ != "" :
                    self.con.commit()
                    messagebox.showinfo("Message","Product Added Successfully")
                else :
                    print("Error : ",sqlite3.Error.__class__.__name__)
                    messagebox.showinfo("Message",f"Error : Inset to product {sqlite3.Error.__class__.__name__}")

        else :
            sql = """
                    INSERT INTO product VALUES(?,?,?,?,?,?,?,?,?)
                """
            try:
                prod_id = product_id
                self.c.execute(sql,(hsnCode,product_id,prodGroup,prodType,quantity_avail,discountPrice,landing_price,unitPrice,gst))
            except  sqlite3.IntegrityError:
                messagebox.showinfo("Message",f"Product/Barcode - {product_id}, already available")
            else:
                if sqlite3.Error.__class__.__name__ != "" :
                    self.con.commit()
                    messagebox.showinfo("Message","Product Added Successfully")
                else :
                    print("Error : ",sqlite3.Error.__class__.__name__)
                    messagebox.showinfo("Message",f"Error : Inset to product {sqlite3.Error.__class__.__name__}")
        return prod_id

    def update_ProductData(self,hsnCode,product_id,prodGroup,prodType,quantity_avail,discountPrice,landing_price,unitPrice,gst):
            sql = """
                UPDATE product SET HSN_code=?,product_id=?,product_group=?,product_type=?,quantity_avail=?,discount_price=?,landing_price=?,unit_price=?,gst=? 
                WHERE HSN_code=? and product_id=?
            """
            self.c.execute(sql,(hsnCode,product_id,prodGroup,prodType,quantity_avail,discountPrice,landing_price,unitPrice,gst,hsnCode,product_id))
            self.con.commit()
            messagebox.showinfo("Message","Product Updated Successfully")


    def view_ProductData(self,hsnCode,product_id,prodGroup,prodType,quantity):
        if product_id != "":
            result = self.c.execute("SELECT * FROM product where product_id =?",(product_id,))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData
        elif prodType != "":
            result = self.c.execute("SELECT * FROM product where product_type like ? ",(f'%{prodType}%',))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData
        elif prodGroup != "":
            result = self.c.execute("SELECT * FROM product where product_group like ? ",(f'{prodGroup}%',))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData
        elif hsnCode != "":
            result = self.c.execute("SELECT * FROM product where HSN_code like ? ",(f'{hsnCode}%',))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData
        elif quantity !="":
            result = self.c.execute("SELECT * FROM product where quantity_avail like ? ",(quantity,))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData

        
    def delete_ProductData(self,hsnCode,product_id):
        sql = """
                DELETE from product
                WHERE HSN_code=? and product_id=?
            """
        self.c.execute(sql,(hsnCode,product_id))
        self.con.commit()
        messagebox.showinfo("Message","Product Deleted Successfully")

    def get_ProductData(self,prodType):
        if prodType != "":
            result = self.c.execute("SELECT product_type FROM product where product_type like ? ",(f'%{prodType}%',))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
            return fetchedData
        # *******************************************************************************************
                                        # END OF PRODUCTS DEFINITIONS
        # *******************************************************************************************
    def checkCust(self,mob):
        if mob =="":
            messagebox.showinfo("Message","Please Provide CUSTOMER NUMBER")
            return
        result = self.c.execute("SELECT * FROM cust where cust_mob = ? ",(mob,))
        fetchedData = []
        for row in result:
            fetchedData.append(row)
        return fetchedData

    def updateCust(self,mob,name,invNo,subscribe):
        check = self.checkCust(mob)
        if subscribe == 1:
            sub = "yes"
        else:
            sub = "no"

        if check == []:
            if name == "" :
                messagebox.showinfo("Message","New Customer. Please provide Name & confirm subscribtion to ADD CUSTOMER & Generate Bill")
                return
            else:
                sql = """
                        INSERT INTO cust VALUES(?,?,?,?)
                    """
                self.c.execute(sql,(mob,name,invNo,sub))
                self.con.commit()
        else:
            i = 0
            for inv in check:
                if invNo == inv[2]:
                    i+=1
            if i == 1:
                return
            else:
                
                self.con.commit()
                try:
                    sql = """
                        INSERT INTO cust VALUES(?,?,?,?)
                    """
                    self.c.execute(sql,(mob,name,invNo,sub))
                except  sqlite3.IntegrityError:
                    return
                else:
                    if sqlite3.Error.__class__.__name__ != "" :
                        self.con.commit()
                    else :
                        print("Error : ",sqlite3.Error.__class__.__name__)
                        messagebox.showinfo("Message",f"Error : Insert to invoice - {sqlite3.Error.__class__.__name__}")
                    

        # *******************************************************************************************
                                        # END OF CUSTOMER DEFINITIONS
        # *******************************************************************************************

    def insert_InvoiceData(self,inv_num,buyItems,payterm):
        
        for item in buyItems:
            # get landing & quantity
            individualprod = self.c.execute("Select product_type,quantity_avail from product where product_type = ?",(item[0],))
            newQuantity = 0
            quanUpd = []
            for row in individualprod:
                # update quantity
                newQuantity = int(row[1]) - int(item[2])

                if newQuantity < 0:
                    messagebox.showinfo("Message",f"'{item[0]}'- Only {row[1]} available in INVENTORY but {item[2]} is requested. Please remove/alter it from CART")
                    return 0
                else:
                    quanUpd.append([row[0],newQuantity])  
                for product in quanUpd:
                    sql = """
                        UPDATE product SET quantity_avail=?
                        WHERE product_type = ?
                    """
                    self.c.execute(sql,(product[1],product[0]))
                    self.con.commit()
        try:
            for item in buyItems:
                # Insert Invoices
                sql = """
                    INSERT INTO invoice VALUES(?,?,?,?,?,?,?)
                """
                self.c.execute(sql,(inv_num,item[0],item[2],item[3],item[6],item[7],payterm))
        except  sqlite3.IntegrityError:
            self.con.rollback()
            messagebox.showinfo("Message",f"{inv_num} and {item[0]}, already avaiable")
            return 0
        else:
            if sqlite3.Error.__class__.__name__ != "" :
                self.con.commit()
            else :
                print("Error : ",sqlite3.Error.__class__.__name__)
                messagebox.showinfo("Message",f"Error : Insert to invoice - {sqlite3.Error.__class__.__name__}")
                self.con.rollback()
                return 0
        return 1


    # Fetch the invoice details from tables 
    def view_InvoiceDetails(self,invoiceNum,custMob):
        if invoiceNum != "":
            result = self.c.execute("SELECT i.invoice_num,i.pay_term,i.product_type,i.quantity,i.MRP,p.landing_price,i.discount_price,i.total_price FROM invoice as i ,product as p where p.product_type = i.product_type and i.invoice_num  like ?",(f'{invoiceNum}%',))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
        elif custMob != "":
            result = self.c.execute("Select i.invoice_num,i.pay_term,i.product_type,i.quantity,i.MRP,p.landing_price,i.discount_price,i.total_price FROM invoice as i ,product as p ,cust as c where p.product_type = i.product_type and i.invoice_num = c.invoice_num and c.cust_mob = ?",(custMob,))
            fetchedData = []
            for row in result:
                fetchedData.append(row)
        elif invoiceNum == "" and custMob == "":
            result = self.c.execute("SELECT i.invoice_num,i.pay_term,i.product_type,i.quantity,i.MRP,p.landing_price,i.discount_price,i.total_price FROM invoice as i ,product as p where p.product_type = i.product_type")
            fetchedData = []
            for row in result:
                fetchedData.append(row)
        return fetchedData

    def get_InvoiceNumber(self,inv_num):
        sql = """
                Select max(invoice_num) from invoice where invoice_num like ?
            """
        results = self.c.execute(sql,(f'{inv_num}%',))
        fetchedData = []
        for row in results:
            fetchedData.append(row)
        return fetchedData
