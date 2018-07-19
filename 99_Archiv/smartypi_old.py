#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, time, sys
#import threading
import minimalmodbus
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


######################################
##### Modbus Communication Setup #####
######################################

# Setup modbus communication
#minimalmodbus.BAUDRATE = 115200
#minimalmodbus.BYTESIZE = 8
#minimalmodbus.PARITY   = 'N'
#minimalmodbus.STOPBITS = 1
#minimalmodbus.TIMEOUT  = 0.10

# PVmeter = Photovoltaicsmeasuremeter, Hmeter = Housemeasuremeter, Lmeter = Loadingmeasuremeter
# Measurment of powergeneration from the photovoltaics
#PVmeter = minimalmodbus.Instrument('/dev/ttyS0', 1, mode='rtu')
#meter.debug = False

# Measurement of powerusage of the household
#Hmeter = minimalmodbus.Instrument('/dev/ttyS0', 2, mode='rtu')
#meter.debug = False

# Measurment of loaded power / total powerconsumption during charging process
#Lmeter = minimalmodbus.Instrument('/dev/ttyS0', 3, mode='rtu')
#meter.debug = False

# CC = Chargecontroler = Arduino
#cc = minimalmodbus.Instrument('/dev/ttyS0', 16, mode='rtu')
#cc.debug = False


####################################
##### Mqtt Communication Setup #####
####################################

# The callbackresponse from the server.
Connected = False
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
        Connected = True
        client.subscribe("Chargingstation1")
    else:
        print("Connection failed")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
        

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print(str(msg.payload))

# Disconnect message
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# Publish callback
def on_publish(client, userdate, mid):
    print(mid)
  
  
#########################
##### smartypart :P #####
#########################

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect("128.127.67.86", 1883, 60)


# Send/publish single messages and disconnect "maybe easy way for pushing messages to the broker"
#First, publish not in a single connection, but I has to tweak-out if this usfull/doesn'T interrupt any other threads
client.loop_start()
try:
    while Connected !=True:
            #Die if-Bedingung wird später für die verschiedenen states benötigt "Start, Stop,Status,CDR)
            #if
        client.publish("AUDICPO","Start_Charging")
        time.sleep(1)
        
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()


