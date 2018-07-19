import os, time, sys
#import threading
import minimalmodbus
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


######################################
##### Modbus Communication Setup #####
######################################

# Setup modbus communication
minimalmodbus.BAUDRATE = 115200
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY   = 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT  = 0.10

# PVmeter = Photovoltaicsmeasuremeter, Hmeter = Housemeasuremeter, Lmeter = Loadingmeasuremeter
# Measurment of powergeneration from the photovoltaics
PVmeter = minimalmodbus.Instrument('/dev/ttyS0', 1, mode='rtu')
PVmeter.debug = False

# Measurement of powerusage of the household
Hmeter = minimalmodbus.Instrument('/dev/ttyS0', 2, mode='rtu')
Hmeter.debug = False

# Measurment of loaded power / total powerconsumption during charging process
Lmeter = minimalmodbus.Instrument('/dev/ttyS0', 3, mode='rtu')
Lmeter.debug = False

# CC = Chargecontroler = Arduino
cc = minimalmodbus.Instrument('/dev/ttyS0', 16, mode='rtu')
cc.debug = False


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
    print(msg.topic+" "+str(msg.payload))

# Disconnect message
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# Publish callback
def on_publish(client, userdate, mid):
    print(mid)
  
  
##################################
##### smartypart :P with UCs #####
##################################

# Setup mqtt connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect("128.127.67.86", 1883, 60)

# Calculation of available amount of power
class AvailablePower():
    def calculateAvailablePower():
            activeImportPV = PVmeter.read_long(0x5b14,2)/100
            activeImportH = Hmeter.read_long(0x5b14,2)/100
            voltageL1 = Hmeter.read_long(0x5b00,3,False)/10
            voltageL2 = Hmeter.read_long(0x5b02,3,False)/10
            voltageL3 = Hmeter.read_long(0x5b04,3,False)/10
            
            availablepower = (activeImportPV-activeImportH)/((voltageL1+voltageL2+voltageL3)/3)
            print(availablepower)
            return availablepower
        
###############
##### UC1 #####
###############
        
# Global register variables

# Hier sollte ich noch ein Array für die Variable Mode einpflegen und evtl.
# sämtliche modbusvariablen aufführen

Available_Power=AvailablePower()

while Available_Power.calculateAvailablePower >= 6:
    #print("Geht")
    cpstatus = cc.read_register(19,0)
    try:
        while cpstatus > 12:
            
            cc.write_register(0, 1)
            
            pvcurrent = availablepower*1000
            print(pvcurrent)
            cc.write_register(2,pvcurrent)
        
            client.loop_start()
            client.publish("AUDICPO","Statusuebertragung: Es wird PV geladen")
            time.sleep(1)
            
    except KeyboardInterrupt:
        
        client.loop_stop()
        client.disconnect()
        
    else:
        print("Es steckt kein Kabel")
        client.loop_stop()
else:
    print ("Es kommt nicht genug Saft aus der PV Anlage")
    cc.write_register(0, 0)

###############
##### UC2 #####
###############
    
i#f Available_Power.calculateAvailablePower < 6:
    #print("platzhalter")
#else:
    #print("platzhalter")

# Send/publish single messages and disconnect "maybe easy way for pushing messages to the broker"
#First, publish not in a single connection, but I has to tweak-out if this usfull/doesn'T interrupt any other threads
#client.loop_start()
#try:
#    while Connected !=True:
            #Die if-Bedingung wird später für die verschiedenen states benötigt "Start, Stop,Status,CDR)
            #if
#        client.publish("AUDICPO","Start_Charging")
        #time.sleep(1)
        
#except KeyboardInterrupt:
 
#    client.loop_stop()
#    client.disconnect()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()


