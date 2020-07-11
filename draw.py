import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

       
def edit_frame(frame,mask,oxygen=96,temp=97.25):
	if mask:
		mcolor=(0,255,0)
		cont=right
	else:
		mcolor=(0,0,255)
		cont=wrong
		
	framec=frame.copy()
	cv2.rectangle(frame,(768,4),(1020,252),(0,255,0),4)
	cv2.rectangle(frame,(768,260),(1020,508),(0,255,0),4)
	cv2.rectangle(frame,(768,516),(1020,764),mcolor,4)
	cv2.rectangle(framec,(768,4),(1020,252),(0,255,0),-1)
	cv2.rectangle(framec,(768,260),(1020,508),(0,255,0),-1)
	cv2.rectangle(framec,(768,516),(1020,764),mcolor,-1)
	alpha = 0.2
	frame = cv2.addWeighted(framec, alpha, frame, 1 - alpha, 0)
	
	frame = cv2.putText(frame, 'Oxygen', (768+50,0+50), cv2.FONT_HERSHEY_SIMPLEX,  
				   1, (100,255,50), 2, cv2.LINE_AA) 
	frame = cv2.putText(frame, str(oxygen), (768+50,256-50), cv2.FONT_HERSHEY_SIMPLEX,  
				   4, (0,255,0), 8, cv2.LINE_AA) 
	frame = cv2.putText(frame, 'Temperature', (768+10,256+50), cv2.FONT_HERSHEY_SIMPLEX,  
				   1, (100,255,50), 2, cv2.LINE_AA) 
	frame = cv2.putText(frame, str(temp), (768+20,512-50), cv2.FONT_HERSHEY_SIMPLEX,  
				   2, (0,255,0), 8, cv2.LINE_AA) 
	
	frame = cv2.putText(frame, 'Mask', (768+100,512+50), cv2.FONT_HERSHEY_SIMPLEX,  
				   1, mcolor, 1, cv2.LINE_AA) 
	
	cont[0]+=[[768+32,512+64]]
	
	frame = cv2.fillPoly(frame, cont, mcolor)
	
	return frame


right=[np.array([[[100,  19]],

       [[ 99,  20]],

       [[ 91,  27]],

       [[ 79,  39]],

       [[ 76,  44]],

       [[ 73,  47]],

       [[ 69,  54]],

       [[ 66,  57]],

       [[ 65,  60]],

       [[ 63,  62]],

       [[ 62,  65]],
       
       [[ 58,  72]],

       [[ 57,  73]],

       [[ 56,  76]],

       [[ 55,  77]],

       [[ 54,  80]],

       [[ 51,  85]],

       [[ 50,  84]],

       [[ 49,  79]],

       [[ 48,  78]],

       [[ 47,  74]],

       [[ 46,  73]],

       [[ 45,  70]],

       [[ 43,  68]],

       [[ 38,  66]],

       [[ 37,  67]],

       [[ 36,  67]],

       [[ 33,  70]],

       [[ 34,  70]],

       [[ 39,  75]],

       [[ 39,  76]],

       [[ 40,  77]],

       [[ 40,  78]],

       [[ 41,  79]],

       [[ 41,  81]],

       [[ 42,  82]],
       
       [[ 45,  90]],

       [[ 45,  92]],

       [[ 46,  93]],

       [[ 47,  99]],

       [[ 48, 100]],

       [[ 49, 102]],

       [[ 51, 100]],

       [[ 52, 100]],

       [[ 56,  93]],

       [[ 57,  92]],

       [[ 57,  89]],

       [[ 58,  88]],

       [[ 58,  87]],

       [[ 60,  82]],

       [[ 61,  81]],

       [[ 64,  73]],

       [[ 65,  72]],

       [[ 66,  69]],

       [[ 67,  68]],

       [[ 73,  58]],

       [[ 74,  55]],

       [[ 76,  53]],
       
       [[ 80,  46]],

       [[ 82,  43]],

       [[ 85,  40]],

       [[ 89,  35]],

       [[ 89,  34]],

       [[101,  20]]], dtype=np.int32)]
       
wrong=[np.array([[[ 30,   0]],

       [[ 10,  20]],

       [[ 32,  74]],

       [[ 27,  83]],

       [[  1, 126]],

       [[  0, 127]],
        
       [[ 44,  96]],
        
       [[ 99, 110]],

       [[127,  98]],

       [[ 67,  70]],

       [[ 93,  25]],

       [[ 63,  28]],

       [[ 60,  31]],

       [[ 31,   0]]], dtype=np.int32)]



