import time
import cv2
import imutils
import sys
import numpy as np
from SafeThreads import Display
from PIL import Image
# import tensorflow as tf # TF2
import tflite_runtime.interpreter as tflite
from imutils.video.pivideostream import PiVideoStream
from draw import *


class LiteDetector:
	def __init__(self):
		self.interpreter = tflite.Interpreter(model_path="lite/IncV3.tflite")
		self.interpreter.allocate_tensors()
		self.input_details = self.interpreter.get_input_details()
		self.output_details = self.interpreter.get_output_details()
		# check the type of the input tenso
		self.floating_model = self.input_details[0]['dtype'] == np.float32
		# NxHxWxC, H:1, W:2
		self.height = self.input_details[0]['shape'][1]
		self.width = self.input_details[0]['shape'][2]
		
	def get_height(self):
		return self.height
		
	def get_width(self):
		return self.width
		
	def get_interpreter(self):
		return self.interpreter
	
	def is_floating_model(self):
		return self.floating_model
		
	def get_input_details(self):
		return self.input_details
		
	def get_output_details(self):
		return self.output_details
		
	def set_tensor(self,input_data):
		self.interpreter.set_tensor(self.input_details[0]['index'], [input_data])
	
	def get_results(self,input_data):
		input_data=cv2.resize(input_data,(self.get_width(), self.get_height()))
		if self.is_floating_model():
			input_data = (np.float32(input_data) - 127.5 )  / 127.5
		self.interpreter.set_tensor(self.input_details[0]['index'], [input_data])
		self.interpreter.invoke()
		
		output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
		print(output_data)
		return np.squeeze(output_data)
	



class Detector:
	
	def load_labels(self,filename):
		with open(filename, 'r') as f:
			return [line.strip() for line in f.readlines()]

	def detect_and_predict_mask(self,frame, faceNet):
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
		faceNet.setInput(blob)
		detections = faceNet.forward()
		faces = []
		locs = []
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]

			if confidence > 0.5:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
				locs.append((startX, startY, endX, endY))
				break

		return locs
	
	def __init__(self,caffe_model_file="face_detector/res10_300x300_ssd_iter_140000.caffemodel",caffe_prototxt_file="face_detector/deploy.prototxt"):
		self.lite=LiteDetector()
		#face detector
		self.faceNet=cv2.dnn.readNet(caffe_prototxt_file, caffe_model_file)
		
	def start(self,tempVal=None,tempBool=False,spo2=None,spo2Bool=False,frames=30):
		print("[INFO] starting video stream...")
		vs = PiVideoStream((FRAME_W,FRAME_H), 10).start()
		time.sleep(2.0)
		
		
		N=0;
		z=0;yes_mask=0;no_mask=0;no_face=0;
		while True:
			frame = vs.read()
			start_time = time.time()
			locs = self.detect_and_predict_mask(frame,self.faceNet)
			if len(locs) is 0:
				frame=put_title(frame)
				no_face+=1
				if no_face >=frames//2:
					if N > 2*frames:
						vs.stop()
						cv2.destroyAllWindows()
						sys.exit("No face recognized")
					Display().run(no_face_screen(frame),2)
					N+=z+1;z=0;no_face=0;
					time.sleep(1)
					continue
			else:
				for box in locs:
					(startX, startY, endX, endY)=box
					input_data=frame[startY:startY+endY, startX:startX+endX,:]
					results =self.lite.get_results(input_data)
					
					mask=results[0] > results[1]
					if mask:
						yes_mask+=1
						label ="Mask"
						color = (0, 255, 0)
						res=results[0]
					else:
						no_mask+=1
						label ="No Mask"
						color = (0, 0, 255)
						res=results[1]
					label = "{}: {:.2f}%".format(label, res * 100)
					print(label)
					cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
					cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
					frame=edit_frame(frame,mask,tempVal,tempBool,spo2,spo2Bool)
			stop_time = time.time()
			Display().run(frame)
			print(str((stop_time-start_time)*1000)+"ms")
			z+=1
			if yes_mask>frames//2 or no_mask>frames//2:
				vs.stop()
				return yes_mask>frames//2
			if z>=frames:
				if yes_mask>no_mask and yes_mask>frames//3:
					vs.stop()
					return True
				elif no_mask>yes_mask and no_mask>frames//3:
					vs.stop()
					return False
					


			
