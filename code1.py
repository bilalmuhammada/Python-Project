import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(660,440)

cam= cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0
#font=cv2.InitFont(cv2.FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
font=cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, img=cam.read()
    img=cv2.resize(img,(800,620))

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    ##for i in range(len(conts)):
      #  x,y,w,h=cv2.boundingRect(conts[i])
       # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        #cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
        #cv2.putText(img, str(i+1),(x,y+h),font,(0,255,255))
    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
        mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=x1+w1//2
        cy1=y1+h1//2
        cx2=x2+w2//2
        cy2=y2+h2//2
        cx=(cx1+cx2)//2
        cy=(cy1+cy2)//2
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
       # mouse.position=(cx*sx/camx,cy*sy/camy)
        mouseLoc=(sx-(cx*sx//camx), cy*sy//camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
                pass
        #while mouse.position!=(cx*sx/camx,cy*sy/camy):

           
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        
        #if(pinchFlag==0):
           # pinchFlag=1
          #  mouse.press(Button.left)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx=x+w//2
        cy=y+h//2
        cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
        mouseLoc=(sx-(cx*sx//camx), cy*sy//camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
      #  while mouse.position!=(sx-(cx*sx/camx),cy*sy/camy):
         
            
        #mouse.press(Button.left)
    #cv2.imshow("maskClose",maskClose)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitKey(5)