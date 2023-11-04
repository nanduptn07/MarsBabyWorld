import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageTk
from tkinter import ttk
import tkinter as tk

class barCodeMaking:
    def genBarCode(productid):
        code = barcode.get('code128',productid,writer=ImageWriter())
        code.save(f'barcode/barcode_{productid}')

    # def displayBarCode(productid,root):
    #     # filename = f"barcode/barcode_{productid}.png"
    #     # print(filename)
    #     # imagebar = Image.open(filename)
    #     # print(imagebar)
    #     # photo = ImageTk.PhotoImage(imagebar)
    #     # print(photo)
    #     # return photo
    #     # productid=700100013
    #     filename = f"barcode/barcode_{productid}.png"
    #     print(filename)
    #     imagebar = Image.open(filename)
    #     print(imagebar)
    #     photo = ImageTk.PhotoImage(imagebar)
    #     print(photo)
    #     barcode1=ttk.Label(root,image=photo)
    #     barcode1.pack()
        
    window = tk.Tk()
    productid=700100013
    barCodeframe=ttk.Frame(window)
    barCodeframe.pack()
    filename = f"barcode/barcode_{productid}.png"
    print(filename)
    imagebar = Image.open(filename)
    print(imagebar)
    photo = ImageTk.PhotoImage(imagebar)
    print(photo)
    ttk.Label(barCodeframe,text="BarCode",font=('times',16,"bold")).pack()
    barcode1=ttk.Label(barCodeframe,image=photo)
    barcode1.pack()
    window.mainloop()