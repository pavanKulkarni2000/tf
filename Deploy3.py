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
from SafeThreads import *
from draw import *

tempLow=95; tempHigh=99;
oxyLow=95; 

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
  mask=faceDetector.start(frames=6)
  time.sleep(1)
  
  
  if not mask:
    with picamera.PiCamera() as camera:
      with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (FRAME_W,FRAME_H)
        camera.capture(stream, format='bgr')
        image = stream.array
    Display().run(no_mask_screen1(image))
    time.sleep(4)
    mask=faceDetector.start(frames=10)
    if not mask:
      Display().run(no_mask_screen2(),4)
      time.sleep(4)
      sys.exit("NO MASK")
    
  Display().run(temp_screen(frame),3)
  time.sleep(3)
    
  #check temperature
  '''
  temp_sensor = Temperature.MLX90614()
  tempVal=temp_sensor.get_avg_temp()'''
  tempVal=97.50
  if tempVal>tempHigh or tempVal<tempLow:
    with picamera.PiCamera() as camera:
      with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (FRAME_W,FRAME_H)
        camera.capture(stream, format='bgr')
        image = stream.array
    Display().run(tempVal,no_temp_screen1(image),5)
    time.sleep(3)
    '''
    temp_sensor = Temperature.MLX90614()
    tempVal=temp_sensor.get_avg_temp()'''
    tempVal=97.50
    if tempVal>tempHigh or tempVal<tempLow:
      frame1=put_temperature(tempVal,frame.copy())
      Display().run(no_temp_screen2(frame1),3)
      time.sleep(3)
      sys.exit("TEMPERATURE")
    
  Display().run(oxy_screen())
    
  
    
  #check oxygen
  '''
  while True:
    Display().run(tempVal,no_temp_screen1(image))
    max_obj = max30102.MAX30102()
    red_data, ir_data = max_obj.read_sequential()
    time.sleep(1)
    hr, hrc, spo2, spo2c = hrcalc.calc_hr_and_spo2(ir_data[:100], red_data[:100])
    if True:
      break
  '''
  spo2=99
  if spo2<oxyLow:
    with picamera.PiCamera() as camera:
      with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (FRAME_W,FRAME_H)
        camera.capture(stream, format='bgr')
        image = stream.array
    Display().run(tempVal,spo2,no_oxy_screen1(spo2,frame),3)
    time.sleep(3)
    '''
    while True:
      Display().run(tempVal,spo2,no_oxy_screen1(spo2,frame))
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
  
  mask = faceDetector.start(tempVal,spo2,frames=10)
  if mask:
    f=open("target/entry.txt",'+w')
    f.close()
  else:
    Display().run(no_mask_screen2(),2)
    time.sleep(2)
  cv2.destroyAllWindows()
  
	
