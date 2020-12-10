# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:01:19 2020

@author: Kshitija Surange
"""


import cv2
from PIL import Image
import pytesseract
from pytesseract import Output
import re
import os
from scipy.ndimage import rotate
import scipy
import math
import numpy as np
import face_recognition

class Aadhaar_Card():
    #Constructor
    def __init__(self,config = {'orient' : True,'skew' : True,'crop': True,'contrast' : True,'psm': [3,4,6],'mask_color': (0, 165, 255), 'brut_psm': [6]}):
        self.config = config
    
    def extract(self, path):  #("path of input image")
        self.image_path = path
        self.read_image_cv()
        if self.config['orient']:
            self.cv_img = self.rotate(self.cv_img)

        if self.config['skew']:
            print("skewness correction not available")
        
        if self.config['crop']:
            print("Smart Crop not available")
        
        if self.config['contrast']:
            self.cv_img  = self.contrast_image(self.cv_img)
            #self.pil_img  = self.contrast_image(self.pil_img )
            print("correcting contrast")
            
        aadhaars = set()
        for i in range(len(self.config['psm'])):
            t = self.text_extractor(self.cv_img,self.config['psm'][i])
            anum = self.is_aadhaar_card(t)
            uid = self.find_uid(t)


            if anum != "Not Found" and len(uid) == 0:
                if len(anum) - anum.count(' ') == 12:
                   aadhaars.add(anum.replace(" ", ""))
            if anum == "Not Found" and len(uid) != 0:

                aadhaars.add(uid[0].replace(" ", ""))
            if anum != "Not Found" and len(uid) != 0:
                if len(anum) - anum.count(' ') == 12:
                   aadhaars.add(anum.replace(" ", ""))
                #print(uid[0].strip())
                aadhaars.add(uid[0].replace(" ", ""))

        return list(aadhaars)
    
    def read_image_cv(self):
        self.cv_img = cv2.imread(str(self.image_path), cv2.IMREAD_COLOR)
    
    def rotate_only(self, img, angle_in_degrees):
        self.img = img
        self.angle_in_degrees = angle_in_degrees
        rotated = scipy.ndimage.rotate(self.img, self.angle_in_degrees)
        return rotated
    
    def is_image_upside_down(self, img):
        self.img = img
        face_locations = face_recognition.face_locations(self.img)
        encodings = face_recognition.face_encodings(self.img, face_locations)
        image_is_upside_down = (len(encodings) == 0)
        return image_is_upside_down
    
    # Corrects orientation of image using tesseract OSD if rotation Angle is < 100.
    def rotate(self,img):
        #def orientation_correction(img): #, save_image = False):
        # GrayScale Conversion for the Canny Algorithm 
        self.img = img
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) 
        #self.display(img_gray)
        # Canny Algorithm for edge detection was developed by John F. Canny not Kennedy!! :)
        img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
        #self.display(img_edges)
        # Using Houghlines to detect lines
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
        img_copy = self.img.copy()
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(img_copy,(x1,y1),(x2,y2),(0,255,0),2)
        #cv2.imshow('hough',img_copy)
        #cv2.waitKey(0)
        
        angles = []
        for x1, y1, x2, y2 in lines[0]:
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)
        
        # Getting the median angle
        median_angle = np.median(angles)
        # Rotating the image with this median angle
        img_rotated = self.rotate_only(self.img, median_angle)
        #self.display(img_rotated)
        
        if self.is_image_upside_down(img_rotated):
            print("rotate to 180 degree")
            angle = -180
            img_rotated_final = self.rotate_only(img_rotated, angle)
            #self.save_image(img_rotated_final)
            #self.display(img_rotated_final)
            if self.is_image_upside_down(img_rotated_final):
                print("Kindly check the uploaded image, face encodings still not found!")
                return img_rotated
            else:
                print("image is now straight")
                return img_rotated_final
        else:
            #self.display(img_rotated)
            print("image is straight")
            return img_rotated

        
    # Turns images BnW using pixels, didn't have much success with this and skipped in final production 
    def contrast_image(self, img):
        self.img = img
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #self.display(thresh)
        return thresh
    
    # Extracts Texts from images
    def text_extractor(self, img, psm):
        config  = ('-l eng --oem 3 --psm '+ str(psm))
        t = pytesseract.image_to_string(img, lang='eng', config = config)
        return t

    def find_uid(self,text2):
        # Searching for UID
        uid = set()
        try:
            newlist = []
            for xx in text2.split('\n'):
                newlist.append(xx)
            newlist = list(filter(lambda x: len(x) > 12, newlist))
            for no in newlist:
                #print(no)
                if re.match("^[0-9 ]+$", no):
                    uid.add(no)

        except Exception:
            pass
        return list(uid)
    
    #Function to validate if an image contains text showing its an aadhaar card
    def is_aadhaar_card(self, text):
               res=text.split()
               aadhaar_number=''
               for word in res:
                  if len(word) == 4 and word.isdigit():
                      aadhaar_number=aadhaar_number  + word + ' '
               if len(aadhaar_number)>=14:
                   return aadhaar_number
                   
               else:

                    return "Not Found"
     
#from Aadhar import Aadhaar_Card
config = {'orient' : True,   #corrects orientation of image default -> True
          'skew' : True,     #corrects skewness of image default -> True
          'crop': True,      #crops document out of image default -> True
          'contrast' : True, #Bnw for Better OCR default -> True
          'psm': [3,4,6],    #Google Tesseract psm modes default -> 3,4,6 
          'mask_color': (0, 165, 255),  #Masking color BGR Format
          'brut_psm': [6]    #Keep only one for brut mask (6) is good to start
          }

obj = Aadhaar_Card(config)
aadhaar_list = obj.extract("C:/Users/admin/Desktop/aadhaar card intern/img1.jpeg") #supported types (png, jpeg, jpg)
    


