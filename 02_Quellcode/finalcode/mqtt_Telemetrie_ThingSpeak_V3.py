#!/usr/bin/python
#-*- coding: utf-8 -*-

# ThingSpeak Update Using MQTT

from __future__ import print_function
from subprocess import check_output
import paho.mqtt.publish as publish
import psutil
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
 

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "475181"
#channelID2 = "484459"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "XIBQHRG404SHA7HM"
#apiKey2 = "SNIK71JU8SE29XL2"

#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = True

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False
# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = False

# Hier wird die Pause zwischen den Messungen eingestellt

sleeptime = 50

# Hier die Sensoren mit den entsprechenden GPIOs konfigurieren

DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 5

# Hier wird der data traffic konfiguriert(auslesen)
import time
def get_bytes(t, iface='wlan0'):
    with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)
tx_prev = 0;
rx_prev = 0;
tx_speed = 0;
rx_speed = 0;

###   End of user configuration   ###

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey
#topic2 = "channels/" + channelID2 + "/publish/" + apiKey2

# Run a loop which calculates the system performance every
#   10 seconds and published that to a ThingSpeak channel
#   using MQTT.

while(True):
    # get the system performance data
    # CPU Temperatur
    cpu_temp = check_output(["vcgencmd","measure_temp"])
    cputemp1 = (cpu_temp [5:])
    cputemp = cputemp1 [:4]
    

    # RAM Auslastung in %
    ramPercent = psutil.virtual_memory().percent

    # Luftfeuchtigkeit & Temperatur(ambience)
    #Luftfeuchte, Temperatur = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)

    # übertragene Daten
    tx = get_bytes('tx')

    # empfangene Daten
    rx = get_bytes('rx')
    if tx_prev > 0:
        tx_speed = tx - tx_prev
        print('TX: ', tx_speed, 'bps')
    if rx_prev > 0:
        rx_speed = rx - rx_prev
        print('RX: ', rx_speed, 'bps')
    time.sleep(1)
    tx_prev = tx
    rx_prev = rx
    
    print (" CPU =",cputemp.decode("utf-8"),"RAM =",ramPercent)
    print (" LF =",Luftfeuchte," TEMP =",Temperatur)
    
    # build the payload string
    tPayload = "&field1=" + str(cputemp.decode("utf-8")) + "&field2=" + str(ramPercent) + "&field5=" + str(tx_speed) + "&field6=" + str(rx_speed) + "&field3=" +str(Luftfeuchte) + "&field4=" + str(Temperatur)
    #tPayload2 = "&field1=" + str(cputemp)
    # attempt to publish this data to the topic 
    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
        #publish.single(topic2, payload=tPayload2, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
        time.sleep(20)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")
