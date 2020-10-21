<h1>Mask detection on rpi</h1>
This module can be used to run Face Mask Detection in realtime on PiCamera.
<br>
For mask detection, first face detecion model is run, here caffe model is used for face detection. It returns the localization of the face if detected. 
<br>
Further, for classifying the cropped face image, a binary classifier is used. Transferred learning is used here to get a good acuuracy without much dataset and training time.
<br>
We have tried both inceptionV3 and mobilenetV2 architecure neural models, to find the best fit for this purpose. Further both the models are converted to tflite format to be light and portable and more importantly to run effeciently on the RPi.
<br>
OpenCV is used to process images and RPi screen is used as a display. Images captured with PiCamera through a video stream is processed and the result is dipayed in real-time.
<br>
Temperature and oximeter reading is also a part of the module.
