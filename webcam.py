import cv2
import time
import pandas 
from colorama import init
from termcolor import colored
import pandas as pd
from datetime import datetime
import sys
from time import sleep
import logging as log
import datetime as dt


cascPath =r"C:\Users\Windows 10\Desktop\Motion Dectector\haarcascade_fullbody.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
first_frame=None

status_list=[None,None]

times=[]

df=pandas.DataFrame(columns=["Start","End"])
weblogs=log.basicConfig(filename='webcam.log',level=log.INFO)
video=cv2.VideoCapture(0)

anterior=0
while True:
    if not video.isOpened():
        print("Unable to load Camera ")
        sleep(0.1)
        pass

    check, frame = video.read()

    status = 0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )



    if first_frame is None:
        status_list.append(0)

        first_frame = gray
        continue


    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    contours, hierarchy=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # if image is greater than 10000 pixels

    for counter in contours:

        if cv2.contourArea(counter) < 10000:
            continue

        status = 1

        (x, y, w, h)=cv2.boundingRect(counter)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)
    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())

    elif status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    if anterior != len(faces):

        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta frame", delta_frame)
    cv2.imshow("Threshold",thresh_frame)
    cv2.imshow("Color Frame",frame)


    key = cv2.waitKey(1)
    print(gray)

    if key==ord('q'):
        
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)


df.to_csv(r'C:\Users\Windows 10\Desktop\Motion Dectector\Times.csv', sep='\t', encoding='utf-8',index=False)

video.release()

cv2.destroyAllWindows

