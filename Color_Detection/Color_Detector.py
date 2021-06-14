#importing required libraries

import numpy as np
import pandas as pd
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import easygui

#loading the dataset as a dataframe

index=['color' , 'color_name' , 'hex' , 'R' , 'G' , 'B']
color_data=pd.read_csv('colors.csv' , names=index , header=None)
#print(color_data.head())

img_path=""

#developing GUI using tkinter module
top=tk.Tk()
top.geometry('300x200')
top.title("Color Detection")
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

#function to select image
def upload():
    global img_path
    img_path=easygui.fileopenbox()
    img_path=img_path.replace('\\' , '/')
    top.destroy()

upload=Button(top,text="Select Your Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()

#reading image
img=cv2.imread(img_path)

#globlal variables
clicked=False
r=g=b=xpos=ypos=0

#functiion to find the matching color
def matchColor(R , G , B):
    minimum=10000
    for i in range(len(color_data)):
        d = abs(R- int(color_data.loc[i,"R"])) + abs(G- int(color_data.loc[i,"G"]))+ abs(B- int(color_data.loc[i,"B"]))
        if d<minimum:
            minimum=d
            color_matched=color_data.loc[i,'color_name']
    return color_matched

#function to find Position of click and its R,G,B values
def draw_function(event , x, y , flags , param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked=True
        xpos=x
        yposs=y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#defining mouse event
cv2.namedWindow("image")
cv2.setMouseCallback('image' , draw_function)

#main loop
while(1):
    cv2.imshow('image' , img)
    if(clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = matchColor(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break

#closes all the windows
cv2.destroyAllWindows()
