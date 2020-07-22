import cv2
from threading import Thread

	
class Display(Thread):
	
	def __init__(self):
		Thread.__init__(self)
	
	def run(self,frame,ms=1): # This function launch the thread
		cv2.imshow("SAFE Biosecurity Solutions", frame)
		cv2.waitKey(ms)
