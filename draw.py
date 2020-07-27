import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAME_W,FRAME_H=(960,1640)
boxw=FRAME_W//4
boxh=boxw
ins_s0=1
ins_s1=1.4
ins_s2=1.6
ins_s3=2.5
ins_s4=3.5


def put_title(frame):
       framec=frame.copy()
       cv2.rectangle(frame,(0,0),(FRAME_W,100),(50,50,50),-1)
       alpha = 0.3
       frame = cv2.addWeighted(framec, alpha, frame, 1 - alpha, 0)
       frame = cv2.putText(frame, 'S.A.F.E. Biosecurity Solutions', (160,60), 
                            cv2.FONT_HERSHEY_COMPLEX, 1.4, (255,255,255), 2, cv2.LINE_AA) 
       return frame
       
def create_frame(val=0):
       scrn=np.full((FRAME_H,FRAME_W,3), val, dtype=np.uint8)
       scrn=put_title(scrn)
       return scrn
       
def start_screen(scrn=create_frame()):
       text1="WELCOME TO"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s3,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2="S.A.F.E. BOOTH"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s4,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -70),cv2.FONT_HERSHEY_COMPLEX, ins_s3, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +100),cv2.FONT_HERSHEY_COMPLEX, ins_s4, (255,255,255), 4, cv2.LINE_AA) 
       return scrn

def wait_screen(scrn=create_frame()):
       text1="The Booth is currently occupied,"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2="please await your turn."
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -20),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +40),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       return scrn
       
def no_face_screen(scrn=create_frame()):
       text1="Face not in range..."
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 3, cv2.LINE_AA) 
       return scrn

def no_mask_screen1(scrn=create_frame()):
       text1="PLEASE WEAR YOUR MASK TO GAIN ENTRY"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H-boxh-boxh//2),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 3, cv2.LINE_AA) 
       return scrn

def no_mask_screen2(scrn=create_frame()):
       text1="Sorry. No access granted,"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2="since you are not wearing a mask!"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -60),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 3, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +10),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 3, cv2.LINE_AA) 
       return scrn

def temp_screen(scrn=create_frame()):
       text1="Please place your wrist "
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2="near the Thermopile Sensor"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       text3="Measure your Body Temperature"
       (w,h),b=cv2.getTextSize(text3,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d3=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -60),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +10),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text3, (d3,FRAME_H//2 +100),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       return scrn

def no_temp_screen1(temp=None,scrn=create_frame()):
       scrn=edit_frame(scrn,True,temp,False,None,False)
       text1="Temperature beyond permissible limits."
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2="Please try again by placing your wrist"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       text3="closer to the Thermopile sensor."
       (w,h),b=cv2.getTextSize(text3,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d3=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H-boxh-boxh//2 -20),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H-boxh-boxh//2 +40),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text3, (d3,FRAME_H-boxh-boxh//2 +100),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 2, cv2.LINE_AA) 
       return scrn

def no_temp_screen2(scrn=create_frame()):
       text1="Sorry. No access granted since your temperature is"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2=" beyond acceptable limits!"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s0,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -20),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +40),cv2.FONT_HERSHEY_COMPLEX, ins_s0, (255,255,255), 2, cv2.LINE_AA) 
       return scrn

def oxy_screen(scrn=create_frame()):
       text1="Please place your finger "
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2=" in the Pulse Oximeter slot"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       text3="Measure your Body Oxygen Levels"
       (w,h),b=cv2.getTextSize(text3,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d3=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -60),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +10),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text3, (d3,FRAME_H//2 +100),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       return scrn

def no_oxy_screen1(temp=None,oxy=None,scrn=create_frame()):
       scrn=edit_frame(scrn,True,temp,True,oxy,False)
       text1="Oxygen below permissible limits."
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2=" Please try again by placing your finger"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       text3="on the Pulse Oximeter sensor."
       (w,h),b=cv2.getTextSize(text3,cv2.FONT_HERSHEY_COMPLEX,ins_s1,cv2.LINE_AA)
       d3=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -60),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +10),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text3, (d3,FRAME_H//2 +100),cv2.FONT_HERSHEY_COMPLEX, ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       return scrn

def no_oxy_screen2(scrn=create_frame()):
       text1="Sorry. No access granted"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       text2=" since your Oxygen levels are"
       (w,h),b=cv2.getTextSize(text2,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d2=(FRAME_W - w)//2
       text3="below acceptable limits!"
       (w,h),b=cv2.getTextSize(text3,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d3=(FRAME_W - w)//2
       scrn= cv2.putText(scrn,text1, (d1,FRAME_H//2 -60),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text2, (d2,FRAME_H//2 +10),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       scrn= cv2.putText(scrn,text3, (d3,FRAME_H//2 +90),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (255,255,255), 2, cv2.LINE_AA) 
       return scrn
       
def put_oxygen(frame,oxyVal,oxyBool):
       oxyVal =round(oxyVal,2)
       
       frame = cv2.putText(frame, 'OXYGEN', (3*boxw-20,FRAME_H-boxh), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       
       frame = cv2.putText(frame, str(oxyVal), (3*boxw+50,FRAME_H-boxh+80), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s2,  (0,255,0) if oxyBool else (0,0,255), 3, cv2.LINE_AA) 
       return frame 

def put_temperature(frame,tempVal,tempBool):
       tempVal =round(tempVal,2)
       
       frame = cv2.putText(frame, 'TEMPERATURE', (boxw+30,FRAME_H-boxh), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       
       frame = cv2.putText(frame, str(tempVal), (boxw+150,FRAME_H-boxh+80), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s2, (0,255,0) if tempBool else (0,0,255), 3, cv2.LINE_AA)  
       return frame 

def put_mask(frame,mask):
              
       frame = cv2.putText(frame, 'MASK', (50,FRAME_H-boxh), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s1, (255,255,255), 2, cv2.LINE_AA) 
       
       frame = cv2.putText(frame, 'YES' if mask else 'NO MASK', (50,FRAME_H-boxh+80), cv2.FONT_HERSHEY_COMPLEX,  
                               ins_s2, (0,255,0) if mask else (0,0,255), 3, cv2.LINE_AA)   
       return frame
       
def entry_screen(frame):
       #frame=edit_frame(frame,mask,tempVal,True,oxyVal,True)
       text1="You may now enter the booth"
       (w,h),b=cv2.getTextSize(text1,cv2.FONT_HERSHEY_COMPLEX,ins_s2,cv2.LINE_AA)
       d1=(FRAME_W - w)//2
       frame= cv2.putText(frame,text1, (d1,FRAME_H-boxh-boxh//2 -20),cv2.FONT_HERSHEY_COMPLEX, ins_s2, (0,255,0), 4, cv2.LINE_AA)  
       return frame
       
       
       
def edit_frame(frame,mask,tempVal=None,tempBool=False,oxyVal=None,oxyBool=False):
       

       frame=put_title(frame)
         
         
       framec=frame.copy()
       cv2.rectangle(frame,(0,FRAME_H-boxh-150),(FRAME_W,FRAME_H),(50,50,50),-1)
       alpha = 0.3
       frame = cv2.addWeighted(framec, alpha, frame, 1 - alpha, 0)     
       frame = put_mask(frame,mask)
     
       if tempVal is not None:
              frame=put_temperature(frame,tempVal,tempBool)
              
              if oxyVal is not None:
                     frame=put_oxygen(frame,oxyVal,oxyBool)
       
       return frame
