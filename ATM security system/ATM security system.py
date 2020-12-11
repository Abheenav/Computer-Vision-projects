import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
cap = cv2.VideoCapture(0)


while True:
    ret, image = cap.read()
    ds_factor = 0.5
    image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30))
    print("Found {0} faces!".format(len(faces)))
    no_of_face = len(faces)
    if no_of_face > 1 or no_of_face == 0:
        print('one person is allowed to do transaction')
    if no_of_face ==1:
        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ey, ey+eh), (0,255,0), 2)
            
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                
            
            
            nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in nose_rects:
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 3)
        m = len(smiles)
        e = len(eyes)
        n = len(nose_rects)
        if e and n:
            print ('start doing transaction')
        else:
            print('alert message, door close, unconcious gas')
            break
status = cv2.imwrite('saved5.jpg', image)
print ("Image written to file-system : ",status)


