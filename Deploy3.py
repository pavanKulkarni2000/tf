#import Temperature
#import max30102
#import hrcalc
import time
import os
import sys
import shutil
import draw
import cv2
import numpy as np
import detection
from SafeThreads import Display
from draw import *

tempLow=95; tempHigh=99;
oxygenLow=95; 

if __name__ == '__main__':
  cv2.destroyAllWindows()
  cv2.namedWindow("SAFE Biosecurity Solutions", cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty("SAFE Biosecurity Solutions",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
  
  Display().run(wait_screen())
  
  while True:
    if 'entry.txt' not in os.listdir("/home/pi/tf/target"):
      break
    else:
      time.sleep(0.5)
  
  #check face mask
  faceDetector=detection.Detector()
  frame,mask=faceDetector.start(frames=10)
  
  if not mask:
    Display().run(no_mask_screen1())
    time.sleep(4)
    faceDetector=detection.Detector()
    frame,mask=faceDetector.start(frames=10)
    if not mask:
      Display().run(no_mask_screen2())
      sys.exit("NO MASK")
    else:
      Display().run(temp_screen())
  else:
    Display().run(temp_screen())
    
  #check temperature
  '''
  temp_sensor = Temperature.MLX90614()
  tempVal=temp_sensor.get_avg_temp()'''
  tempVal=97.50
  if tempVal>tempHigh or tempVal<tempLow:
    Display().run(no_temp_screen1(tempVal,frame),5)
    time.sleep(4)
    '''
    temp_sensor = Temperature.MLX90614()
    tempVal=temp_sensor.get_avg_temp()'''
    tempVal=97.50
    if tempVal>tempHigh or tempVal<tempLow:
      Display().run(no_temp_screen2())
      sys.exit("TEMPERATURE")
    else:
      Display().run(oxy_screen())
  else:
    Display().run(oxy_screen())
  
    
  #check oxygen
  '''
  while True:
    max_obj = max30102.MAX30102()
    red_data, ir_data = max_obj.read_sequential()
    time.sleep(1)
    hr, hrc, spo2, spo2c = hrcalc.calc_hr_and_spo2(ir_data[:100], red_data[:100])
    if True:
      break
  '''
  spo2=99
  if spo2<oxyLow:
    Display().run(no_oxy_screen1(spo2,frame),5)
    time.sleep(4)
    '''
    while True:
      max_obj = max30102.MAX30102()
      red_data, ir_data = max_obj.read_sequential()
      time.sleep(1)
      hr, hrc, spo2, spo2c = hrcalc.calc_hr_and_spo2(ir_data[:100], red_data[:100])
      if True:
        break
    '''
    spo2=99
    if spo2<oxyLow:
      Display().run(no_oxy_screen2())
      sys.exit("OXYGEN")
  
  faceDetector = detection.Detector()
  frame,mask = faceDetector.start(tempVal,spo2,frames=10)
  if mask:
    f=open("target/entry.txt",'+w')
    f.close()
  else:
    Display().run(no_mask_screen2())
  cv2.destroyAllWindows()
  
	
