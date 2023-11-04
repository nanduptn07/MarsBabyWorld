import tkinter as tk
from tkinter import ttk



class EditableTreeview(ttk.Treeview):
    def __init__(self, master,**kw):
        super().__init__(master,**kw)
        self.bind("<Double-1>",self.onDoubleClick)
        self.bind("<Tab>",self.onDoubleClick)

    def onDoubleClick(self,event):
        # identfies the region that was dubleclicked
        regionClicked= self.identify_region(event.x,event.y)

        if regionClicked not in("tree","cell"):
            return
        
        #which item was doubleclicked #0,#1,#2...
        column = self.identify_column(event.x)
        columnIndex =int(column[1:])-1

        #row id I001,I002...
        selectedIId = self.focus()

        #items in clicked row
        selectedValues=self.item(selectedIId)

        if column =="#0":
            selectedText = selectedValues.get("text")
        else:
            selectedText = selectedValues.get("values")[columnIndex]
        
        #coordinaes x,y,w,h
        columnBox = self.bbox(selectedIId,column)
        
        entryEdit = ttk.Entry(self,width=columnBox[2])
        
        # Record the column index and iid
        entryEdit.editing_column_index=columnIndex
        entryEdit.editing_item_iid=selectedIId

        entryEdit.insert(0,selectedText)
        entryEdit.select_range(0,tk.END)
        entryEdit.focus()
        entryEdit.bind("<FocusOut>",self.onFocusOut)
        entryEdit.bind("<Return>",self.onEnter)
        entryEdit.place(x=columnBox[0],y=columnBox[1],width=columnBox[2],height=columnBox[3])
    
    def onFocusOut(self,event):
        event.widget.destroy()

    def onEnter(self,event):
        newText = event.widget.get()

        selectedIID=event.widget.editing_item_iid
        column_index = event.widget.editing_column_index
        
        if column_index == -1:
            self.item(selectedIID,text=newText)
        else:
            currentValues = self.item(selectedIID).get("values")
            currentValues[column_index] = newText
            currentValues[7]= (int(currentValues[2])*int(currentValues[6])) 
            self.item(selectedIID,values=currentValues)
        event.widget.destroy()
        self.focus_set()

if  __name__== "__main__":
    root = tk.Tk()

    column_names=("Sno","Product","HSN","Quantity","Unit Price","GST","Max. Discount Price","Total")
    productList = EditableTreeview(root,columns=column_names)
    productList.pack(fill=tk.BOTH,expand=True)

    productList.heading("#0",text="")
    productList.column("#0",width=0,stretch=False)
    productList.heading("Sno",text="Sno")
    productList.column("Sno",width=20)
    productList.heading("Product",text="Product")
    productList.heading("HSN",text="HSN")
    productList.heading("Quantity",text="Quantity")
    productList.heading("Unit Price",text="Unit Price")
    productList.heading("GST",text="GST")
    productList.heading("Max. Discount Price",text="Max. Discount Price")
    productList.heading("Total",text="Total")

    productList.insert("",index=tk.END,values=("1","soap","3","43","5","3","129"))



    root.mainloop()
