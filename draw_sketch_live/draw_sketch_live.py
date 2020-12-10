# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:33:55 2020

@author: admin
"""

import cv2
 
# generate sketch image
def sketch(image):
    # Convert color image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     
    # make blure image --GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]])
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
     
    # Extract edges - Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]])
    canny_edges = cv2.Canny(img_gray_blur, 60, 90)
     
    #return blure image
    return canny_edges
 
#start video carmera
cap = cv2.VideoCapture(0)
 
while True:
    #read images fro the camera
    responce, frame = cap.read()
     
    if responce == False:
        break
     
    #show the stech image
    cv2.imshow('Live Sketch Drawing', sketch(frame))
     
    # wait for 1ms for kye 'q' no responce then show next image
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
         
# Release camera and close all windows
cap.release()
cv2.destroyAllWindows()     