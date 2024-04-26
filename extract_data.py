# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:16:06 2023

@author: ASUS
"""

import pypdfium2 as pdfium

f = r"C:\Users\ASUS\Desktop\Research\Probability Distribution\CME_DailyBulletin\Section06_Currency_Futures.pdf"

pdf = pdfium.PdfDocument(f)

page = pdf[0]
width, height = page.get_size()

# Load a text page helper
textpage = page.get_textpage()
# Extract text from the whole page
text_all = textpage.get_text_range()

pdf.close()
    
for garbage in (textpage, page, pdf):
    garbage.close()