# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:00:38 2020

@author: admin
"""

from PIL import Image
import cv2
import pytesseract
import imutils
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

filename = 'sample1.jpg'
#filename = 'video12.mp4'
cap = cv2.VideoCapture(filename)
name, extension = os.path.splitext(filename)
if extension == ".png" or extension ==  ".jpg" or extension == ".jpeg":
    image=cv2.imread(filename)
elif extension ==  ".mp4":
    cap = cv2.VideoCapture(filename)
    ret, image = cap.read()


image = imutils.resize(image, width=min(500, len(image[0])))
gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray=cv2.bilateralFilter(gray,11,17,17)
edged=cv2.Canny(gray,170,200)
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
img1 = image.copy()
cv2.drawContours(img1, cnts ,-1, (0,255,0), 3)
cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:30]
NumberPlateCnt = None
img2 = image.copy()
cv2.drawContours(img2,cnts,-1, (0,255,0), 3)
count=0
idx=7
for c in cnts:
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)
    if len(approx) == 4:
        NumberPlateCnt = approx
        x,y,w,h = cv2.boundingRect(c)
        new_img = image[y:y+h, x:x+w]
        cv2.imwrite(str(idx) + '.png', new_img)
        idx+=1
        break
cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
Cropped_img_loc = '7.png'
pic=cv2.imread(Cropped_img_loc)
text= pytesseract.image_to_string(Cropped_img_loc, lang='eng')
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
word=LETTERS + DIGITS
tes= list(text.partition('\n')[0])
number =[]
for i in tes:
    if i in word:
        number.append(i)
text_in_number_plate = ''.join([str(elem) for elem in number])
print(text_in_number_plate)
    
    
status = cv2.imwrite('saved5.jpg', image)
print ("Image written to file-system : ",status)




 