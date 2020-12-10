# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 21:13:10 2020

@author: abheenav
"""

from PIL import Image
import pytesseract
import sys 
from pdf2image import convert_from_path 
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

path = "D:/udemy/3. ml/assuption of linear regression.png"
name, extension = os.path.splitext(path)

if extension == ".png" or extension ==  ".jpg" or extension == ".jpeg":
    
    image = Image.open(path)
    text = str(((pytesseract.image_to_string(image))))
    file = open("recognized_text_from_image.txt", "w+")
    file.write(text) 
    file.close()
elif extension ==  ".pdf" or extension == ".docx":
    pages = convert_from_path(path, 500)
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    filelimit = image_counter-1
    outfile = "recognized_text_from_document.txt"
    f = open(outfile, "a")
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')
        f.write(text)
    f.close()
else:
    print("file type is not supported to extract the text")
    print("supported file types are .png, .jpg, .jpeg, .docx, .pdf ")
    
