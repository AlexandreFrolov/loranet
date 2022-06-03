#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import serial
import time
import sys
from time import sleep
import json

NODE_ADDR_CHAN = [b'\x00\x0B\x0F',
                  b'\x00\x0C\x0F',
                  b'\x00\x0D\x0F']

def gpio_init ():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    M0 = 22
    M1 = 27
    GPIO.setup(M0,GPIO.OUT)
    GPIO.setup(M1,GPIO.OUT)
    GPIO.output(M0,GPIO.LOW)
    GPIO.output(M1,GPIO.LOW)
    time.sleep(1)
    ser = serial.Serial("/dev/serial0", 9600, timeout=1)
    ser.flushInput()
    return ser

def send_cmd(node):
    try :
        if ser.isOpen() :
            ser.write(NODE_ADDR_CHAN[node])
            ser.write('getRData \n'.encode())
    except :
        if ser.isOpen() :
            ser.close()
            GPIO.cleanup()

    while ser.inWaiting() == 0:
        sleep(0.03)

    data_left = ser.inWaiting() 
    received_data = ser.readline()
    sleep(0.03)
    received_data += ser.read(data_left)
    rec = received_data.decode("utf-8").strip()
    node_data = rec.split(';')
    return node_data

def format_node_data(node, node_data):
    NODE_1_2_ITEMS = ['Температура',
                  'Давление',
                  'Влажность',
                  'Точка росы']
    NODE_3_ITEMS = ['Температура CPU',
                  'Интенсивность освещения']
    node_dict={}
    i=0
    for val in node_data:
        val = str(val)
        if(node == 0 or node == 1 or node == 2):
            node_dict[NODE_1_2_ITEMS[i]]= val
        else:

            node_dict[NODE_3_ITEMS[i]]= val
        i = i+1
    return node_dict

def get_nodes_data():
    nodes_dict={}
    node = 2
    node_data = send_cmd(node)
    nodes_dict[node] = format_node_data(node, node_data)
    return nodes_dict

def save_nodes_data_to_file(nodes_dict):
    jsonString = json.dumps(nodes_dict, indent=2, ensure_ascii=False)
    print(jsonString)
    with open('hosts_data.json', 'w') as f:
        json.dump(nodes_dict, f, indent=2, ensure_ascii=False)


ser = gpio_init()
nodes_dict = get_nodes_data()
save_nodes_data_to_file(nodes_dict)
