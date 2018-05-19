from __future__ import print_function
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT) #dummy
import smbus
import time
import sys
import os
from twython import Twython
from random import choice
from subprocess import check_output
import paho.mqtt.publish as publish
import psutil
import Adafruit_DHT


bus = smbus.SMBus(1)
address = 0x04



replies = ['You shall not pass #Mohne',
           'One does not simply drive autonomously #Mohne',
           'Thats one small step for a drone, one giant leap for mankind #Mohne',
           'My humans think they can control me muahahaha #Mohne',
           'The human race may be the only intelligent beings in the galaxy - Stephen Hawking. Yeah....about that...'
        ]
consumer_key = 'VJmX2Ip8bK9A7dO8ON4SxzcJJ'
consumer_secret = 'gBC9TXEqhmzM37PGQKV8rpuqTm0tKlavKTNrV0gtrBR5t0LG4I'
access_token = '992389516777357313-7IsnQuFKB58hTl8JWXQwxpZK0J9pA1U'
access_token_secret = 'N87JxbTxX8oykSHW4UkXeBaMoXHjNkCOWERjGZZGaeTbB'


#mqtt
channelID = "475181"
#channelID2 = "484459"

apiKey = "XIBQHRG404SHA7HM"
#apiKey2 = "SNIK71JU8SE29XL2"
useUnsecuredTCP = True
useUnsecuredWebsockets = False
useSSLWebsockets = False
#sleeptime = 50 #noch testen

DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 5 #Pin anpassen





mqttHost = "mqtt.thingspeak.com"


from pynput import keyboard

def writeNumber(value):
    bus.write_byte(address, value)

    return -1

def readNumber():
        nummer = bus.read_byte(address)
        return nummer
  

def on_key_press(key):

        global tx_prev
        global rx_prev
        global tx_speed
        global rx_speed



        tx_prev = 0;
        rx_prev = 0;
        tx_speed = 0;
        rx_speed = 0;

        if key == keyboard.Key.right:
            
            writeNumber(int(2))
                      
        if key == keyboard.Key.up:
            
            writeNumber(int(1))
         
        if key == keyboard.Key.down:
            
            writeNumber(int(4))
          
        if key == keyboard.Key.left:
            
            writeNumber(int(3))
     
        if key == keyboard.Key.esc:
            
            print("Hasta la vista")
            sys.exit("Mohne sagt Ciao")
            
        if key == keyboard.Key.space:
            #takephoto = "raspistill -o /home/pi/picture.jpg"
            #os.system(takephoto)
            photo = open('/home/pi/picture.jpg', 'rb')
            twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
            image = twitter.upload_media(media=photo)
            twitter.update_status(status=(choice(replies)), media_ids=[image['media_id']])

        if key == keyboard.Key.tab:

            
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
            topic = "channels/" + channelID + "/publish/" + apiKey
            #topic2 = "channels/" + channelID2 + "/publish/" + apiKey2

            cpu_temp = check_output(["vcgencmd","measure_temp"])
            cputemp1 = cpu_temp [5:]
            cputemp = cputemp1 [:4]
            
            ramPercent = psutil.virtual_memory().percent
########
            #import time
            def get_bytes(t, iface='wlan0'):
                with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
                    data = f.read();
                return int(data)
            
            
            
#############
            tx = get_bytes('tx')
            rx = get_bytes('rx')
            print(tx)
            print(rx)
            print(tx_prev)
            print(rx_prev)
            if tx_prev > 0:
                tx_speed = tx - tx_prev
                print('TX: ', tx_speed, 'bps')
                #tx_prev = tx
            if rx_prev > 0:
                rx_speed = rx - rx_prev
                
                print('RX: ', rx_speed, 'bps')
          
            if tx_prev == 0:
                tx_speed = tx - tx_prev
               # tx_prev = tx
                print("Test 1")
            
            time.sleep(1)
            tx_prev = tx
            rx_prev = rx
            print (" CPU =",cputemp,"RAM =",ramPercent)
            print("hier")
            print(tx)
            print(rx)

            #Luftfeuchte, Temparatur = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
            #time.sleep(sleeptime)
            
            tPayload = "&field1=" + str(cputemp) + "&field2=" + str(ramPercent) + "&field5=" + str(tx_speed) + "&field6=" + str(rx_speed) #+ "&field3=" +str(Luftfeuchte) + "&field4=" + str(Temperatur)
            #tPayload2 = "&field1=" + str(cputemp)
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            #publish.single(topic2, payload=tPayload2, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            

            
        else:
           writeNumber(int(5))
           
               
            
def on_key_release(key):
    #motor aus
    GPIO.output(21, GPIO.LOW)
   


with keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release) as listener:
    listener.join()
    
    
GPIO.cleanup()


