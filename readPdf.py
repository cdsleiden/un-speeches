#import pypdf2
import os
import re
from io import StringIO
import PyPDF2
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)
    full_text = output_string.getvalue().strip()
    full_text = re.sub( r'\s+' , ' ' , full_text )
    return full_text




dir = '1970-1980'
pdf_files = []

for root,dirs,files in os.walk( dir ):
   for file_name in files:
       if re.search( r'pdf$' , file_name , re.IGNORECASE ):
           pdf_files.append( os.path.join(root, file_name) )


for file_name in pdf_files:
    print(file_name)
    subfolder = os.path.split(file_name)[0]
    year = re.findall( r'19\d{2}' , subfolder )[-1]
    print(year)
    out_file = str(year) + '_' + os.path.basename(file_name)
    out_file = re.sub( r'pdf$' , 'txt' , out_file , re.IGNORECASE )
    txt = open( os.path.join( 'TXT' , out_file ) , 'w' , encoding = 'utf-8')
    full_text = convert_pdf_to_string(file_name).strip()
    txt.write( f'{full_text} ')
    txt.close()
