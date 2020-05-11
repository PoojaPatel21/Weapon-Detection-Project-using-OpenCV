# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:38:48 2020

@author: Pooja
"""

import smtplib 

from email.mime.multipart import MIMEMultipart 

from email.mime.text import MIMEText 

from email.mime.base import MIMEBase 

from email import encoders 

def sendmail(i):

    fromaddr = "weapondetectionsystem@gmail.com"
    
    toaddr = "pooja.patel@cumminscollege.in"
    
    msg = MIMEMultipart() 
     
    msg['From'] = fromaddr 
    
    msg['To'] = toaddr 
    
    msg['Subject'] = "URGENT WEAPON DETECTED"
    
    body = "Knife detected in the attached image"
    
    msg.attach(MIMEText(body, 'plain')) 
    
    filename = "knifedetected"+str(i)+".jpg"
    
    attachment = open(r"C:\Users\Pooja\Desktop\joc\ip\knifedetected"+str(i)+".jpg", "rb")  #here we have to specify the exact file location where image is being stored which will depend on the system in use SO CHANGE THIS PLS ILY
    
    p = MIMEBase('application', 'octet-stream') 
    
    p.set_payload((attachment).read()) 
    
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition',"attachment; filename= " + filename ) 
    
    msg.attach(p)  
    
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    
    s.starttls() 
    
    s.login(fromaddr, 'gaushapoo') 
    
    text = msg.as_string() 
    
    s.sendmail(fromaddr, toaddr, text) 
    
    s.quit() 
    
    
    
''' end of code to send mail '''    





''' main code to detect weapon '''

from detecto import core, visualize

model=core.Model.load('knife_model.pth',['knife'])


import cv2
import win32api

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


if (cap.isOpened()== False):
  print("Error opening video stream or file")

i=0
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
      cv2.imshow('Video', frame)
      predictions = model.predict(frame)
      labels, boxes, scores = predictions
      if len(scores)>0 and max(scores)>0.9:
        visualize.show_labeled_image(frame,boxes[0], labels[0]) 
        if i==0:
            win32api.MessageBox(0, 'KNIFE DETECTED. SAVING IMAGE.', 'ALERT', 0x00001000)
        x1,y1,x2,y2 = boxes[0]
        img=cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0, 255, 0),3)
        cv2.imshow('detected',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('knifedetected'+str(i)+'.jpg',frame)
        sendmail(i)
        i=i+1
    
    # Press Q on keyboard to  exit
      ch = cv2.waitKey(1)
      if ch == 27 or ch == ord('q') or ch == ord('Q'):
          break
  else:
    print('Not working')
cap.release()
cv2.destroyAllWindows() 
