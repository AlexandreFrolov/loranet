#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import serial
import time
import sys
from time import sleep

print("It's UART test")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

M0 = 22
M1 = 27
CFG_CMD = [b'\xC1\xC1\xC1',
		   b'\xC3\xC3\xC3']


GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)

#GPIO.output(M0,GPIO.LOW)
#GPIO.output(M1,GPIO.LOW)

GPIO.output(M0,GPIO.HIGH)
GPIO.output(M1,GPIO.HIGH)

time.sleep(1)

#ser = serial.Serial("/dev/ttyS0",9600)
ser = serial.Serial("/dev/serial0", 9600)
ser.flushInput()

try :
	if ser.isOpen() :
            print("It's setting RELAY mode")
            ser.write("This is a GET CONFIG cmd:\r\n".encode())
            ser.write(CFG_CMD[0])
            ser.write("Received.\r\n".encode())

except :
	if ser.isOpen() :
		ser.close()
	GPIO.cleanup()


while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data
    ser.write(received_data)                #transmit data serially

