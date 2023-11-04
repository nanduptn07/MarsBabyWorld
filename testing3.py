import win32print
import win32con

# Get the default printer name
# printer_name = win32print.GetDefaultPrinter()
# Print the image to the printer
# win32print.SetDefaultPrinter(printer_name)
# printer_name ="EPSON M1100 Series"
printer_name ="SNBC TVSE LP 46 NEO BPLE"
details = "Hello Mars baby world"
printer_handle = win32print.OpenPrinter(printer_name)
print(printer_handle)
attributes = win32print.GetPrinter(printer_handle,2)
# attributes['pDevMode'].PaperSize = win32con.DMPAPER_A5
# print(attributes)
# defaults={"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
# win32print.SetPrinter(printer_handle,2,attributes,0)

# properties = win32print.GetPrinter(printer_handle,2)
# properties['pDevMode'].PaperSize = win32con.DMPAPER_A5

win32print.StartDocPrinter(printer_handle,1,("details",None,"RAW"))
win32print.WritePrinter(printer_handle,details.encode('utf-8'))
win32print.EndPagePrinter(printer_handle)
win32print.EndDocPrinter(printer_handle)
win32print.ClosePrinter(printer_handle)