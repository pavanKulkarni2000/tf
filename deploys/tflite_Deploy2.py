"""label_image for tflite."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import time

import numpy as np
from PIL import Image
from picamera import PiCamera
# import tensorflow as tf # TF2
import tflite_runtime.interpreter as tflite
import cv2


def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


def detect_and_predict_mask(frame, faceNet):
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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-i',
      '--image',
      default='4321.jpg',
      help='image to be classified')
  parser.add_argument(
      '-m',
      '--model_file',
      default='MobV2.tflite',
      help='.tflite model to be executed')
  parser.add_argument(
      '-l',
      '--label_file',
      default='labels.txt',
      help='name of file containing labels')
  parser.add_argument(
      '--input_mean',
      default=127.5, type=float,
      help='input_mean')
  parser.add_argument(
      '--input_std',
      default=127.5, type=float,
      help='input standard deviation')
  parser.add_argument(
      '--num_threads', default=None, type=int, help='number of threads')
  args = parser.parse_args()

  interpreter = tflite.Interpreter(
      model_path=args.model_file)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]
  with PiCamera() as cam:
    cam.capture('capture.jpg')
  # img = Image.open('capture.jpg').resize((width, height))

  start_time = time.time()
  faceNet=cv2.dnn.readNet("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")
  frame = cv2.imread('capture.jpg')
  # print(frame)
  locs = detect_and_predict_mask(frame, faceNet)
  # print(locs)
  for box in locs:
    (startX, startY, endX, endY)=box
    input_data=frame[startY:startY+endY, startX:startX+endX,:]
    input_data=cv2.resize(input_data,(width, height))
    if floating_model:
      input_data = (np.float32(input_data) - args.input_mean) / args.input_std

    interpreter.set_tensor(input_details[0]['index'], [input_data])
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)
  
    label = "Mask" if results[0] > results[1] else "No Mask"
    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
    label = "{}: {:.2f}%".format(label, max(results[0], results[1]) * 100)
    print(label)
    cv2.putText(frame, label, (startX, startY - 10),
      cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    
  stop_time = time.time()
  cv2.imwrite("result.jpg",frame)

  print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))


