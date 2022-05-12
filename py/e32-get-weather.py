#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import serial
import time
import sys
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

M0 = 22
M1 = 27

GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)

GPIO.output(M0,GPIO.LOW)
GPIO.output(M1,GPIO.LOW)

#GPIO.output(M0,GPIO.HIGH)
#GPIO.output(M1,GPIO.HIGH)
time.sleep(1)

#ser = serial.Serial("/dev/ttyS0",9600, timeout=1)
ser = serial.Serial("/dev/serial0", 9600, timeout=1)
ser.flushInput()

try :
    if ser.isOpen() :
        ser.write('getWeather \n'.encode())

except :
    if ser.isOpen() :
        ser.close()
	GPIO.cleanup()

#received_data = ser.read()
received_data = ser.readline()

sleep(0.03)
data_left = ser.inWaiting()             #check for remaining byte
received_data += ser.read(data_left)
print (received_data.rstrip("\n"))                   #print received data
