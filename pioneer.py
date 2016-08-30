import RPi.GPIO as GPIO
from time import sleep
import datetime as dt

import picamera

GPIO.setmode(GPIO.BOARD)
#Setup LED pins
#Ready LED
GPIO.setup(22, GPIO.OUT)
#Countdown 3 LED
GPIO.setup(16, GPIO.OUT)
#Countdown 2 LED
GPIO.setup(15, GPIO.OUT)
#Countdown 1 LED
GPIO.setup(32, GPIO.OUT)
#RECord LED
GPIO.setup(33, GPIO.OUT)
#finisH LED
GPIO.setup(37, GPIO.OUT)

#Camera is ready, begin countdown
GPIO.output(37, False)
GPIO.output(22, True)
sleep(2)
GPIO.output(16, True)
sleep(2)
GPIO.output(16, False)
GPIO.output(15, True)
sleep(2)
GPIO.output(15, False)
GPIO.output(32, True)
sleep(2)
GPIO.output(32, False)
GPIO.output(22, False)

#Begin recording video
GPIO.output(33, True)

#Records 60 seconds of video at 90 fps; change wait_recording
#for length, in seconds, for video
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 90
    camera.exposure_mode = 'antishake'
    filename = dt.datetime.now().strftime('%d-%m-%Y-%H:%M:%S.h264')
    camera.annotate_text = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    camera.start_recording(filename,format='h264')
    start = dt.datetime.now()
    while (dt.datetime.now() - start).seconds < 60:
            camera.annotate_text = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            camera.wait_recording(0.2)
    camera.stop_recording()
    
#Finish
GPIO.output(33, False)
GPIO.output(37, True)
sleep(10)
GPIO.output(37, False)

GPIO.cleanup()
