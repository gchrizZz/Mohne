# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

###   Start of user configuration   ###   

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "475172"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "15YA7O06S4034J0Q"

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

# Die Pause von zwei Sekunden zwischen den Messungen wird hier eingestellt
sleeptime = 5
 
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
 
# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
GPIO_Pin = 5

#Start traffic config
import time
def get_bytes(t, iface='wlan0'):
    with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)
tx_prev = 0;
rx_prev = 0;
tx_speed =0;
rx_speed =0;

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

# Run a loop which calculates the system performance every
#   20 seconds and published that to a ThingSpeak channel
#   using MQTT.
while(True):
    
    # get the system performance data
    cpuPercent = psutil.cpu_percent(interval=5)
    ramPercent = psutil.virtual_memory().percent
    print (" CPU =",cpuPercent,"   RAM =",ramPercent)
    #transmitted traffic
    tx = get_bytes('tx')
    #received traffic
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
    
    # Messung wird gestartet und das Ergebnis in die entsprechenden Variablen geschrieben
    Luftfeuchte, Temperatur = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
    #print('Temperatur  | rel. Luftfeuchtigkeit'.format(Temperatur, Luftfeuchte))
    time.sleep(sleeptime)
    
    # build the payload string
    tPayload = "field2=" + str(cpuPercent) + "&field3=" + str(ramPercent) + "field1=" + str(Temperatur) + "&field4=" + str(Luftfeuchte) + "&field5=" + str(tx_speed) + "&field6=" + str(rx_speed)

    # attempt to publish this data to the topic 
    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        GPIO.cleanup()
        break

    except:
        print ("There was an error while publishing the data.")
