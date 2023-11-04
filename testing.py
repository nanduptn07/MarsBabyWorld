import jinja2
import pdfkit

cust_name ="nandha"
cust_mobile ="9944222492"
date ="10/06/2023"
pay ='Cash'

Final ='44'
Actual ='50'
Disc ="6"
Taxable ="2"
CGST ="1"
SGST ="1"

addrow ="<tr><td>1</td><td>Car</td><td>2</td><td>1</td><td>50</td><td>44</td><td>44</td></tr>"

context= {'cust_name':cust_name,"cust_mobile":cust_mobile,"date":date,"pay":pay,
          "Final":Final,"Disc":Disc,"Taxable":Taxable,"CGST":CGST,"SGST":SGST,"addrow":addrow}

template_loader = jinja2.FileSystemLoader('./')
tem_env = jinja2.Environment(loader=template_loader)

template = tem_env.get_template("bill.html")
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf="./wkhtmltopdf.exe")
pdfkit.from_string(output_text,'pdfgen.pdf',configuration=config)